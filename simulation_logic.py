"""Simulation of a Vehicle Insurance Organization

Input Distributions and Event Types:
--------------------

1- Arrival:
    - System 1:
        - Mean = 5 (time = 148500)
        - Warm-up time = 13500
    - System 2:
        - Mean = 3.2 (time = 165000)
        - Warm-up time = 15000

2- Partner Arrival:
    - Exponential distribution with mean = 30 minutes

3- Photography Service:
    - Modeled with an Exponential distribution
    - Lambda = 1/6

4- Single Car Waiting:
    - Follows an Exponential distribution
    - Lambda = 1/30

5- Filling the Case:
    - System 1:
        - Service time follows a Triangular distribution with parameters (min=5, mode=6, max=7)
    - System 2:
        - Service time follows a Triangular distribution with parameters (min=6, mode=8, max=10)

6- Expert Service:
    - System 1:
        - Modeled with an Exponential distribution
        - Lambda = 1/9
    - System 2:
        - Modeled with an Exponential distribution
        - Lambda = 1/8

7- Case Completion:
    - System 1:
        - Service time follows a Triangular distribution with parameters (min=6, mode=8, max=9)
    - System 2:
        - Service time follows a Triangular distribution with parameters (min=3, mode=3.5, max=4)

8- Complaint Service:
    - Modeled with an Exponential distribution
    - System 1:
        - Lambda = 1/15
    - System 2:
        - Lambda = 0

Additional Parameters:
--------------------

1- Probability that a car arrives alone: 0 (for both systems)
2- Probability that a customer makes a complaint:
    - System 1: 0.1
    - System 2: 0

Staffing:
--------------------

System 1:
- Filling and Completing the Case center: Three workers
- Expert center: Two workers
- Photography center: Two photographers
- Complaint Submission center: One staff member

System 2:
- Filling and Completing the Case center: Four workers
- Expert center: Three workers
- Photography center: Two photographers
- Complaint Submission center: One staff member

Queuing Discipline:
--------------------

Majority of queues in this simulation follow a FIFO (First In, First Out) discipline. However, in the case of Filling and Completing the Case, Completing the Case queue receives higher priority over Filling the Case queue.

Outputs:
--------------------

- Efficiency of workers involved in the Photography, Expert, Complaint Submission, Filling, and Completion of the Case services for both systems.
- Average queue length for the Photography queue, Outside queue, Expert queue, and Complaint Submission queue for both systems.
- Maximum queue length for the Photography queue, Outside queue, Expert queue, and Complaint Submission queue for both systems.
- Average time spent in the Photography queue, Outside queue, Expert queue, and Complaint Submission queue for both systems.
- Probabilities that the Waiting Parking and Filling queue are empty for both systems.
- The percentage of customers who arrived alone and submitted a complaint (no customers arrive alone for both systems).
- Mean time of remaining in the system for both systems.
- Maximum queue length of the Expert queue for comparison between the two systems.

Goal:
--------------------

The goal of this simulation is to compare the two systems based on the waiting time of each queue,
including the average waiting time in the Photography queue, Expert queue, Filling and Completing the Case queue,
Complaint Submission queue, and Outside queue. By analyzing and comparing these waiting times, we can evaluate the performance and
efficiency of both systems and identify potential areas for improvement.

Simulation Run Time:
--------------------

- System 1: 148500 time units
- System 2: 165000 time units

Interactions in this simulation occur based on the occurrence of these events and the additional parameters.

Outputs:
--------------------

Detailed analysis of the operations of the insurance organization for both systems.

The simulation initializes in an empty state.

Author: Reza Alvandi, MohammadJavad Bahmani
Date:
"""


import pandas as pd
import random
import math
import System
import environmentDistribution
import excelOutput
import statisticalUtils
import warmUp
from States import States
from handleOutputs import handleOutput
from openpyxl.workbook import Workbook



class mainSystem:
    """this class is for taking multiple systmes with different parameters and run them in simulation to compare them
    in wating time and other parameters"""

    def __init__(self, env, system,time, frameLength, warmup_time):
        """this is the main class of simulation that handles the main logic of simulation"""

        self.env = env # this is the environment parameters such as rate of service and ....
        self.system = system # this is the system parameters such as number of servers and ....
        self.statutil = statisticalUtils.statistics() # this is the class for calculating the statistics
        self.time = time # this is the time of simulation
        self.frameLength = frameLength # this is the length of each frame
        self.warmup = None
        self.rep_number = None
        self.warmup_Time = warmup_time # this is the warmup time of simulation


    def starting_state(self, env):
        """ this is a function to evaluate the initial state of FEL in simulation"""
        # initialize all state variables
        state = States() # this is the state of simulation

        future_event_list = list() # this is the future event list of simulation

        r = random.random()
        # being alone with probability 0.3
        is_alone = 1 if r < env.being_alone_probability else 0
        # add the first event

        # for i in range(self.time//self.frameLength-2):
        #     future_event_list.append({'Event Type': 'Frame_END', 'Event Time': (i+1)*self.frameLength})

        future_event_list.append({'Event Type': 'A','alone': is_alone, 'id': 0, 'Event Time': 0})  # This is an Event
        future_event_list.append({'Event Type': 'END', 'Event Time': self.time}) # This is an END Event
        return state, future_event_list

    def simulation(self,outputExcel=False,excelsaver=None):
        """ This is the main function of simulation that handles the modifications that each event notice
        applies on the state valriables
        """

        self.warmup.clear_vars() # this is for clearing the warmup variables
        envparam = self.env # this to handle the parameters such as rate of service and ....
        state, future_event_list = self.starting_state(envparam) # this is the initial state of simulation
        clock = 0
        handler = handleOutput(self.system, self.warmup_Time) #  this is the class for handling the outputs
        running = True
        id = 1
        last_id_inside = 0 # this is the id of the last car that is inside the system
        system = self.system # this is parameters of the system such as num worker in each center
        i = 1
        sorted_fel = sorted(future_event_list, key=lambda x: x['Event Time'] )
        while running:
            current_event = sorted_fel[0]  # Find imminent event
            a = current_event['id'] if 'id' in current_event.keys() else '' # this is for getting the id of the car

            Event_Type = current_event['Event Type'] # Find event type
            clock = current_event['Event Time']  # Advance time


            # these lines are for handeling and updating the cumulitive statistics
            handler.update_filing_empty(clock, state) # this is for updating the cumulitive statistics
            handler.update_queue_parking_empty(clock, state) # this is for updating the cumulitive statistics
            handler.update_photography_surface(clock, state) # this is for updating the cumulitive statistics
            handler.update_outside_surface(clock, state)
            handler.update_submiting_surface(clock, state)
            handler.update_expert_surface(clock, state)
            handler.update_Service_Photographer_surface(clock, state)
            handler.update_Expert1_surface(clock, state)
            handler.update_Expert2_surface(clock, state)
            handler.update_Expert3_surface(clock, state)
            handler.update_filing_surface(clock,state)
            handler.update_complete_surface(clock, state)


            if Event_Type == 'A': # this is for handeling arival event
                if current_event['alone'] == 1: # if the car arrives alone
                    handler.alone_cars.append(current_event['id']) # add the id of car to the list of alone cars
                if clock < self.time: # if the clock is less than the time of simulation
                    if current_event['alone'] == 0: # if the car arrives with a friend
                        if state.Length_Service_Photographer == system.num_photography_workers:
                            if state.Length_Queue_Photography == system.max_photography_queue_size: # if the queue of photography is full
                                # handler.update_outside_surface(clock,state)
                                handler.arivingOQ[current_event['id']] = clock # add the id of customer if he enters the outside queue

                                state.Length_Queue_OutSide += 1 # increase the length of outside queue
                                state.waiting_Queue_OutSide.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                    'alone': 0 }) # add the id of customer if he enters the outside queue

                            else:
                                state.Length_Queue_Photography += 1 # increase the length of photography queue
                                handler.arivingPhQ[current_event['id']] = clock
                                state.waiting_Queue_Photography.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                    'alone': 0, }) # add the id of customer if he enters the photography queue


                        else:
                            state.Length_Service_Photographer += 1 # increase the length of photography service
                            handler.update_sum_max_PhQ(0,clock)
                            future_event_list.append({'Event Type': 'DP', 'id' : current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Photography_service)})
                    else: # if it was alone do the
                        if state.Length_Queue_Photography == system.max_photography_queue_size:
                            handler.arivingOQ[current_event['id']] = clock # add the id of customer if he enters the outside queue
                            state.Length_Queue_OutSide += 1 # increase the length of outside queue
                            state.waiting_Queue_OutSide.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                    'alone': 1, }) # add the id of customer if he enters the outside queue
                            future_event_list.append({'Event Type': 'PA', 'id':current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Single_car_waiting)})

                        else:
                            handler.update_waiting_parking(state) # this is for updating the cumulitive statistics
                            state.Length_Waiting_Parking += 1 # increase the length of waiting parking
                            state.waiting_Waiting_Parking.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                    'alone': 1, }) # add the id of customer if he enters the waiting parking
                            state.alone_cars_in_parking_id.append(current_event['id']) # add the id of customer if he enters the waiting parking
                            future_event_list.append({'Event Type': 'PA','id':current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Single_car_waiting)})
                    r = random.random()
                    is_alone = 1 if r < envparam.being_alone_probability else 0
                    future_event_list.append({'Event Type': 'A','alone': is_alone, 'id': id, 'Event Time': clock + self.sample_exponential(1/envparam.arrival_mean)})

                    handler.arrive_time[current_event['id']] = clock # add the time that each customer entered the system
                    id += 1
                    #update cumulative statistics
                else:

                    #update the missing customers
                    pass
            elif Event_Type == 'DP':
                # this is for handling the departure of the photography
                if state.Length_Queue_Photography == system.max_photography_queue_size: # if the queue was full get one of then and them and first check the parking then the outside and do that

                    state.Length_Queue_Photography -= 1 # decrease the length of photography queue
                    customer = state.waiting_Queue_Photography.pop(0) # get the first customer in the queue
                    handler.departPhQ[customer['id']] = clock
                    # update the statistics using the id of them
                    handler.update_sum_max_PhQ(handler.departPhQ[customer['id']]-handler.arivingPhQ[customer['id']],handler.arivingPhQ[customer['id']])
                    if state.Length_Queue_Parking == 0:# if the queue was full get one of then and them and first check the parking then the outside and do that

                        future_event_list.append({'Event Type': 'OIN', 'Event Time': clock }) # add the id of customer if he enters from outside queue to inside

                    else:# if the queue was full get one of then and them and first check the parking then the outside and do that
                        state.Length_Queue_Photography += 1

                        customer = state.waiting_Queue_Parking.pop(0) # get the first customer in the queue
                        handler.arivingPhQ[customer['id']] = clock # add the time that customer enters the photogtraphy queue
                        state.waiting_Queue_Photography.append({'id': customer['id'], 'alone': 0 }) # add the id of customer if he enters the photography queue

                        state.Length_Queue_Parking -= 1


                    future_event_list.append({'Event Type': 'DP','id': customer['id'] ,'Event Time': clock + self.sample_exponential(1/envparam.Photography_service)})


                elif state.Length_Queue_Photography == 0:# if the queue was empty set one of them idle

                    state.Length_Service_Photographer -= 1 # decrease the length of photography service

                else:
                    state.Length_Queue_Photography -= 1 # decrease the length of photography queue
                    customer = state.waiting_Queue_Photography.pop(0) # get the first customer in the queue
                    handler.departPhQ[customer['id']] = clock
                    handler.update_sum_max_PhQ(handler.departPhQ[customer['id']]-handler.arivingPhQ[customer['id']],handler.arivingPhQ[customer['id']]) # update the statistics using the id of them

                    future_event_list.append({'Event Type': 'DP','id': customer['id']  ,'Event Time': clock + self.sample_exponential(1/envparam.Photography_service)})



                if state.Length_Service_Expert1 == system.num_filing_completing_workers:
                    state.Length_Queue_Filing += 1 # increase the length of filing queue
                    handler.ariving_FL[current_event['id']] = clock # add the time that customer enters the filing queue
                    state.waiting_Queue_Filing.append({'id': current_event['id']})

                else:
                    state.Length_Service_Expert1 += 1 # increase the length of filing service
                    handler.update_waiting_time_filing_case(0,clock)
                    future_event_list.append({'Event Type': 'DF','id':current_event['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Filling_the_case_min,envparam.Filling_the_case_max,envparam.Filling_the_case_mode)}) # add the id of customer if he enters the filing queue
            elif Event_Type == 'DF':
                # this is for departure of filing the case
                if state.Length_Queue_Complete_the_case == 0: # if we had departure fisrt check the complete queue
                    # then if it was empty check the filing queue due to the priority
                    if state.Length_Queue_Filing == 0:
                        state.Length_Service_Expert1 -= 1 # decrease the length of filing service

                    else:# if we had departure fisrt check the complete queue
                    # then if it was empty check the filing queue due to the priority

                        state.Length_Queue_Filing -= 1

                        customer = state.waiting_Queue_Filing.pop(0) # get the first customer in the queue
                        handler.depart_FL[customer['id']] = clock
                        handler.update_waiting_time_filing_case(handler.depart_FL[customer['id']]-handler.ariving_FL[customer['id']], handler.ariving_FL[customer['id']])
                        future_event_list.append({'Event Type': 'DF','id': customer['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Filling_the_case_min,envparam.Filling_the_case_max,envparam.Filling_the_case_mode)})
                    pass
                else:# if we had departure fisrt check the complete queue
                    # then if it was empty check the filing queue due to the priority

                    state.Length_Queue_Complete_the_case -= 1 # decrease the length of complete queue
                    customer = state.waiting_Queue_Complete_the_case.pop(0) # get the first customer in the queue
                    handler.depart_CL[customer['id']] = clock # add the time that customer enters the complete queue
                    handler.update_wating_time_complete_case(handler.depart_CL[customer['id']]-handler.ariving_CL[customer['id']], handler.ariving_CL[customer['id']])
                    future_event_list.append({'Event Type': 'DC','id': customer['id'] ,'Event Time': clock + self.sample_triangular(
                        envparam.Case_completion_min,envparam.Case_completion_max,envparam.Case_completion_mode)}) # add departure of complete tthe case event

                if state.Length_Service_Expert2 == system.num_expert_workers: # if the expert part had idle worker let the pair in else move it to queue and add its id to compute the statistics
                    state.Length_Queue_Expert += 1 # increase the length of expert queue
                    if current_event['id'] in handler.arivingEL.keys():
                        handler.arivingEL2[current_event['id']] = clock
                    else:# if the expert part had idle worker let the pair in else move it to queue and add its id to compute the statistics
                        handler.arivingEL[current_event['id']] = clock
                    r = random.random()
                    complaint = 1 if r < envparam.submiting_complaint_probability else 0# set the value if it wants to submit complaint
                    state.waiting_Queue_Expert.append({'id':current_event['id'],'complaint':complaint}) # add the id of customer if he enters the expert queue

                else:
                    state.Length_Service_Expert2 += 1 # increase the length of expert service
                    handler.update_sum_max_EL(0,clock)
                    r = random.random()
                    complaint = 1 if r < envparam.submiting_complaint_probability else 0# set the value if it wants to submit complaint
                    future_event_list.append(
                        {'Event Type': 'DE', 'complaint': complaint, 'id': current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Expert_service)})

            elif Event_Type == 'DC':# this is for departure of completing the case
                if current_event['id'] >  last_id_inside:# this is for finding the last person who was inside the system
                    last_id_inside = current_event['id']
                handler.depart_time[current_event['id']] = clock # add the time that customer departs the system
                # updating the sum of remaing time each person has this is actually shows each person epend how much time in the system
                handler.update_sum_remaining_time(handler.depart_time[current_event['id']] - handler.arrive_time[current_event['id']],handler.arrive_time[current_event['id']])

                if state.Length_Queue_Complete_the_case == 0:# if no one was in the queue of completing check the filing queue
                    # due to the priority and if so set one worke to idle
                    if state.Length_Queue_Filing == 0:
                        state.Length_Service_Expert1 -= 1 # decrease the length of filing service

                    else:

                        state.Length_Queue_Filing -= 1 # decrease the length of filing queue
                        customer = state.waiting_Queue_Filing.pop(0) # get the first customer in the queue
                        handler.depart_FL[customer['id']] = clock # add the time that customer departs the filing queue
                        handler.update_waiting_time_filing_case(
                            handler.depart_FL[customer['id']] - handler.ariving_FL[customer['id']],
                            handler.ariving_FL[customer['id']]) # update the waiting time of filing queue
                        future_event_list.append(
                            {'Event Type': 'DF', 'id': customer['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Filling_the_case_min,envparam.Filling_the_case_max,envparam.Filling_the_case_mode)}) # add the departure of filing event
                    pass
                else:
                    state.Length_Queue_Complete_the_case -= 1 # decrease the length of complete queue
                    customer = state.waiting_Queue_Complete_the_case.pop(0) # get the first customer in the queue
                    handler.depart_CL[customer['id']] = clock # add the time that customer departs the complete queue
                    handler.update_wating_time_complete_case(
                        handler.depart_CL[customer['id']] - handler.ariving_CL[customer['id']],
                        handler.ariving_CL[customer['id']])  #add the time that a customer enters the complete the case queue
                    future_event_list.append(
                        {'Event Type': 'DC', 'id': customer['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Case_completion_min,envparam.Case_completion_max,envparam.Case_completion_mode)}) # add the departure of complete the case event

                pass
            elif Event_Type == 'DE':
                # this evnnt handling is for departure of expert
                if state.Length_Queue_Expert == 0: # if no one were in the queue set one of them to idle
                    state.Length_Service_Expert2 -= 1

                else:# else get from the queue
                    state.Length_Queue_Expert -= 1

                    customer = state.waiting_Queue_Expert.pop(0)
                    # update the ids departed the queue to be used
                    if customer['id'] in handler.departEL.keys():

                        handler.departEL2[customer['id']] = clock # add the time that customer departs the expert queue
                        handler.update_sum_max_EL(handler.departEL2[customer['id']]-handler.arivingEL2[customer['id']], handler.arivingEL2[customer['id']])
                    else:
                        #this part is for the sake of that the a customer can be in the queue of expert center more than one time some we are handleing that with another
                        # dictionary to halp make the statistics be correct
                        handler.departEL[customer['id']] = clock # add the time that customer departs the expert queue
                        handler.update_sum_max_EL(handler.departEL[customer['id']]-handler.arivingEL[customer['id']],handler.arivingEL[customer['id']])

                    future_event_list.append({'Event Type': 'DE','id': customer['id'], 'complaint': customer['complaint'], 'Event Time': clock + self.sample_exponential(1/envparam.Expert_service)})

                if current_event['complaint'] == 0:# if the customer wants to submit complaint and the worker wasnt busy send it
                    # in else sent it to the queu and update the dictionary of ariving time
                    if state.Length_Service_Expert1 == system.num_filing_completing_workers:
                        state.Length_Queue_Complete_the_case += 1 # increase the length of complete queue
                        handler.ariving_CL[current_event['id']] = clock # add the time that customer enters the complete the case queue
                        state.waiting_Queue_Complete_the_case.append({'id':current_event['id']})


                    else:
                        state.Length_Service_Expert1 += 1 # increase the length of filing service

                        handler.update_wating_time_complete_case(0,clock)

                        future_event_list.append({'Event Type': 'DC','id':current_event['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Case_completion_min,envparam.Case_completion_max,envparam.Case_completion_mode)})



                else:# else get the back to the previous part and do the same if the worker was busy ...
                    if state.Length_Service_Expert3 == system.num_submiting_complaint_workers:
                        handler.arivingSCL[current_event['id']] = clock # add the time that customer enters the submiting complaint queue
                        state.Length_Queue_Submitting_Complaint += 1 # increase the length of submiting complaint queue
                        state.waiting_Queue_Submitting_Complaint.append({'id': current_event['id']})
                    else:
                        state.Length_Service_Expert3 += 1
                        future_event_list.append({'Event Type': 'DSC', 'id': current_event['id'],
                                                  'Event Time': clock + self.sample_exponential(1 / envparam.Complaint_service)})


                pass
            elif Event_Type == 'DSC':
                # to handle the submiting complement part
                if current_event['id'] in handler.alone_cars:
                    handler.alone_submited_complaint += 1
                state.noSubmitComplaint += 1 # increase the number of submiting complaint
                if state.Length_Queue_Submitting_Complaint == 0:
                    state.Length_Service_Expert3 -= 1 # decrease the length of submiting complaint service
                    pass
                else:

                    state.Length_Queue_Submitting_Complaint -= 1
                    customer = state.waiting_Queue_Submitting_Complaint.pop(0) # get the first customer in the queue
                    handler.departSCL[customer['id']] = clock
                    # this is for updating the SCl max and mean time in queue
                    handler.update_sum_max_SCL(handler.departSCL[customer['id']]-handler.arivingSCL[customer['id']])
                    future_event_list.append({'Event Type': 'DSC', 'id': customer['id'],'Event Time': clock + self.sample_exponential(1/envparam.Complaint_service)})
                    pass

                if state.Length_Service_Expert2 == system.num_expert_workers:
                    # if the worker were full add to the queue and add id tho compute statistics
                    state.Length_Queue_Expert += 1
                    if current_event['id'] in handler.arivingEL.keys():
                        handler.arivingEL2[current_event['id']] = clock # add the time that customer enters the expert queue
                    else:
                        handler.arivingEL[current_event['id']] = clock  # add the time that customer enters the expert queue
                    state.waiting_Queue_Expert.append({'id':current_event['id'],'complaint': 0})
                    pass
                else:# if the worker were idle set it busy
                    state.Length_Service_Expert2 += 1 # increase the length of expert service
                    handler.update_sum_max_EL(0,clock)
                    future_event_list.append({'Event Type': 'DE','complaint': 0,'id': current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Expert_service)})
                    pass

            elif Event_Type == 'PA':
                # if second car arrive try to find its corresponding car and join it
                if current_event['id'] not in state.alone_cars_in_parking_id: # if its pair wasnt in parking
                    for car in state.waiting_Queue_OutSide:# if its pair was in outside queue
                        if car['id'] == current_event['id']:
                            car['alone'] = 0
                            break


                else:# if its pair was inside

                    state.alone_cars_in_parking_id.remove(current_event['id']) # remove it from the list of alone cars in parking


                    for car in state.waiting_Waiting_Parking: # make its aloneness atribute to false
                        if car['id'] == current_event['id']:
                            handler.update_waiting_parking(state) # update the waiting parking list
                            state.waiting_Waiting_Parking.remove(car)
                            state.Length_Waiting_Parking -= 1 # decrease the length of waiting parking
                            break

                    if state.Length_Service_Photographer == system.num_photography_workers:
                        # if photographers werent idle let them in the queue
                        if state.Length_Queue_Photography == system.max_photography_queue_size:


                            state.Length_Queue_Parking += 1
                            # add the id to find the statistics
                            state.waiting_Queue_Parking.append({'id':current_event['id']})

                        else:# if there was a idle photographer let the pair in
                            handler.arivingPhQ[current_event['id']] = clock
                            state.Length_Queue_Photography += 1 # increase the length of photography queue

                            state.waiting_Queue_Photography.append({'id':current_event['id']})

                    else:
                        state.Length_Service_Photographer += 1
                        handler.update_sum_max_PhQ(0,clock)
                        future_event_list.append({'Event Type': 'DP','id': current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Photography_service)})

            elif Event_Type == 'OIN':# entering a car from outside queue to inside
                if clock < self.time:
                    if state.Length_Queue_OutSide > 0:

                        customer = state.waiting_Queue_OutSide.pop(0) # get the first customer in the queue
                        handler.departOQ[customer['id']] = clock# when it leaves the outside queue we get the id and save it
                        state.Length_Queue_OutSide -= 1
                        handler.update_sum_max_OQ(handler.departOQ[customer['id']]-handler.arivingOQ[customer['id']])

                        if customer['alone'] == 0  :# if it wasnt alone move it to queue of inside
                            state.Length_Queue_Photography += 1
                            handler.arivingPhQ[customer['id']] = clock # add the time that customer enters the photography queue
                            state.waiting_Queue_Photography.append({'id':customer['id']})

                        else:# if it was alone move it to waiting cars
                            handler.update_waiting_parking(state) # update the waiting parking list
                            state.Length_Waiting_Parking += 1
                            state.waiting_Waiting_Parking.append({'id':customer['id'],'alone':1}) # add the customer to waiting parking list


                            state.alone_cars_in_parking_id.append(customer['id']) # add the id to the list of alone cars in parking

                            future_event_list.append({'Event Type': 'OIN','Event Time': clock })

                    else:
                        pass
                else:
                    # make the outside queue empty after hour 6
                    for pair in state.waiting_Queue_OutSide:
                        handler.departOQ[pair['id']] = self.time

                    state.Length_Queue_OutSide = 0 # make the outside queue empty after time

                    state.waiting_Queue_OutSide.clear() # make the outside queue empty after time

            elif Event_Type == "END": # if the simulation ends
                # print(
                #     f'accumilitive for filing the case {handler.remain_filing_queue_waiting_time}  num of customers {handler.num_of_filing_queue_customer}')
                # print(
                #     f'accumilitive for completing the case {handler.remain_complete_the_case_queue_waiting_time}  num of customers {handler.num_of_complete_the_case_queue_customer}')

                self.warmup.mean_filing_the_case_waiting_time.append(handler.remain_filing_queue_waiting_time / handler.num_of_filing_queue_customer) # compute the mean of filing queue waiting time
                self.warmup.mean_complete_the_case_waiting_time.append(handler.remain_complete_the_case_queue_waiting_time / handler.num_of_complete_the_case_queue_customer) # compute the mean of complete the case queue waiting time
                self.warmup.mean_expert_waiting_time.append(handler.sum_Time_EL / handler.num_of_expert_queue_customer) # compute the mean of expert queue waiting time
                self.warmup.mean_photography_waiting_time.append(handler.sum_Time_phQ / handler.num_of_photography_queue_customer)  # compute the mean of photography queue waiting time
                self.warmup.mean_whole_system_remain_time.append(handler.remainSystem/ handler.num_of_remain_in_system_customer)
                self.warmup.max_expert_queue_length.append(handler.MEL) # compute the max of expert queue length
                self.warmup.max_photography_queue_length.append(handler.MPhL) # compute the max of photography queue length

                running = False
            elif Event_Type == 'Frame_END': # if the frame ends
                handler.update_photography_surface(clock, state) # update the photography surface
                handler.update_outside_surface(clock, state) # update the outside surface
                handler.update_submiting_surface(clock, state) # update the submiting surface
                handler.update_expert_surface(clock, state) # update the expert surface
                handler.update_filing_surface(clock, state) # update the filing surface
                handler.update_complete_surface(clock, state) # update the complete surface
                self.warmup.warmup_Phq[self.rep_number].append((handler.SPhL-self.warmup.previous_Phq)/self.frameLength) # compute the mean of photography queue length
                self.warmup.previous_Phq = handler.SPhL # update the previous photography queue length

                self.warmup.warmup_Oq[self.rep_number].append(
                    (handler.SOL - self.warmup.previous_Oq) / self.frameLength) # compute the mean of outside queue length
                self.warmup.previous_Oq = handler.SOL

                self.warmup.warmup_fq[self.rep_number].append(
                    (handler.SFL - self.warmup.previous_fq) / self.frameLength) # compute the mean of filing queue length
                self.warmup.previous_fq = handler.SFL

                self.warmup.warmup_cq[self.rep_number].append(
                    (handler.SCL - self.warmup.previous_cq) / self.frameLength) # compute the mean of complete the case queue length
                self.warmup.previous_cq = handler.SCL

                self.warmup.warmup_eq[self.rep_number].append(
                    (handler.SEL - self.warmup.previous_eq) / self.frameLength) # compute the mean of expert queue length
                self.warmup.previous_eq = handler.SEL

                self.warmup.warmup_scq[self.rep_number].append(
                    (handler.SSCL - self.warmup.previous_scq) / self.frameLength) # compute the mean of submiting complaint queue length
                self.warmup.previous_scq = handler.SSCL

            future_event_list.remove(current_event) # removes from the queue and go to next step
            sorted_fel = sorted(future_event_list, key=lambda x: x['Event Time']) # sort the future event list


            if outputExcel:# this is for outputing and excel file if it was selected
                excelsaver.add_row_df([i,current_event['Event Time'],  current_event['Event Type'],a,state.Length_Service_Photographer,state.Length_Service_Expert1,
                                    state.Length_Service_Expert2, state.Length_Service_Expert3,
                                    state.Length_Queue_Parking, state.Length_Queue_OutSide, state.Length_Queue_Photography, state.Length_Queue_Filing,
                                    state.Length_Queue_Complete_the_case, state.Length_Queue_Expert,
                                    state.Length_Queue_Submitting_Complaint, state.Length_Waiting_Parking,handler.SPhL, handler.SOL, handler.SSCL, handler.SEL,
                                    handler.EFQT, handler.EWPT, handler.MPhL ,handler.MOL, handler.MSCL, handler.MEL, handler.SPhCenter, handler.SFilingCenter
                                    , handler.SExpertCenter, handler.SComplaintCenter,handler.sum_Time_phQ,handler.sum_Time_OQ,handler.sum_Time_SCL,handler.sum_Time_EL,
                                       handler.max_Time_PhQ,handler.max_Time_OQ,handler.max_Time_SCL,handler.max_Time_EL, sorted_fel])


            i += 1



        #return to get the outputs
        return handler.print_outputs(clock,last_id_inside, id, state)

        print('done')
    def sample_exponential(self,lambda_val):
        """this is a function to sample from an exponential distribution with
        lambda: lambda_val using uniform value """
        # using the inverse method finds generate random variable
        r = random.random()
        return (-1/lambda_val)*math.log((1-r),math.e)

    def sample_triangular(self,min, max, mod):
        """this is a function to sample from a triangular distribution with
            mod, min and max using uniform distribution """

        r = random.random()
        threshold = (mod - min)/(max - min) # find the threshold
        if r < threshold: # if the random value is less than the threshold
            return math.sqrt(r*(max-min)*(mod-min)) + min # return the value
        else:
            return max - math.sqrt((1-r)*(max-min)*(max-mod))


    def run_simul(self,replication):
        """this is a function to run the simulation for a replication number of times
        and get the average of the outputs"""
        # make a list to save the outputs
        outputs = []
        self.warmup = warmUp.WarmUP(replication)
        for i in range(replication):
            # run the simulation
            self.rep_number = i
            self.simulation()
        self.warmup.res_2_numpy() # convert the results to numpy array
        self.warmup.cal_mean() # calculate the mean of the results
        self.warmup.draw_chart(7) # draw the chart

    def run_simul_for_mean(self, repeatTimes):
        """this is a function to run the simulation for a replication number of times and find the mean of the waiting times and return them"""
        self.warmup = warmUp.WarmUP(repeatTimes)
        for i in range(repeatTimes):
            self.simulation()
        a,b,c,d,e,f = self.warmup.mean_for_waiting_times()
        # print(f'the average waiting time for filing queue is {a} minutes')
        # print(f'the average waiting time for complete the case queue is {b} minutes')
        return a,b,c,d,e,f
    def get_final_res(self, replication, repeatTimes):
        """ after certain amount of replication and repeat times,
         this function will return the average waiting times for filing queue,
          complete the case queue, expert queue and photography queue"""
        filing_avg_times = [] # make a list to save the average waiting time for filing queue
        completing_avg_times = [] # make a list to save the average waiting time for complete the case queue
        expert_avg_times = [] # make a list to save the average waiting time for expert queue
        photography_avg_times = [] # make a list to save the average waiting time for photography queue
        whole_system_avg_times = [] # make a list to save the average waiting time for the whole system
        max_photography_queue_length = [] # make a list to save the maximum length of the expert queue
        for i in range(replication):
            a,b,c,d,e,f = self.run_simul_for_mean(repeatTimes)
            filing_avg_times.append(a) # append the average waiting time for filing queue
            completing_avg_times.append(b) # append the average waiting time for complete the case queue
            expert_avg_times.append(c)  # append the average waiting time for expert queue
            photography_avg_times.append(d) # append the average waiting time for photography queue
            whole_system_avg_times.append(e) # append the average waiting time for the whole system
            max_photography_queue_length.append(f) # append the maximum length of the expert queue
            print('done')


        return filing_avg_times,completing_avg_times,expert_avg_times,photography_avg_times,whole_system_avg_times,max_photography_queue_length



env1 = environmentDistribution.EnvironmentDist(5 ,5, 6, 7,
                                               6, 8, 9,9, 0.1 ) # create an environment for sys 1
env2 = environmentDistribution.EnvironmentDist(3.2,6,8,10,
                                               3,3.5,4,8,0) # create an environment for sys 2
sys1 = System.System(3,2) # create a system for sys 1
sys2 = System.System(4,3) # create a system for sys 2

# simul1 = mainSystem(env1,sys1,21600, 30)
# simul1.run_simul(20)

# simul2 = mainSystem(env2,sys2,21600, 30)
# simul2.run_simul(20)

simul1 = mainSystem(env1,sys1,148500, 30, 13500) # create a main system for sys 1
f1,c1,e1,ph1,r1,mph1 = simul1.get_final_res(20, 50 ) # get the final results for sys 1

simul2 = mainSystem(env2,sys2,165000, 30, 15000) # create a main system for sys 2
f2,c2,e2,ph2,r2,mph2 = simul2.get_final_res(20,50) # get the final results for sys 2





df1 = pd.DataFrame(map(list,zip(*[f1,f2])),columns =['sys1','sys2'] ) # make a dataframe for the average waiting time for filing queue
df2 = pd.DataFrame(map(list,zip(*[c1,c2])),columns =['sys1','sys2']) # make a dataframe for the average waiting time for complete the case queue
df3 = pd.DataFrame(map(list,zip(*[e1,e2])),columns =['sys1','sys2']) # make a dataframe for the average waiting time for expert queue
df4 = pd.DataFrame(map(list,zip(*[ph1,ph2])),columns = ['sys1','sys2']) # make a dataframe for the average waiting time for photography queue
df5 = pd.DataFrame(map(list,zip(*[r1,r2])),columns =['sys1','sys2']) # make a dataframe for the average waiting time for the whole system
df6 = pd.DataFrame(map(list,zip(*[mph1,mph2])),columns =['sys1','sys2']) # make a dataframe for the maximum length of the photography queue

with pd.ExcelWriter("output3.xlsx") as writer:
    # use to_excel function and specify the sheet_name and index
    # to store the dataframe in specified sheet

    df1.to_excel(writer,sheet_name="filing_avg_times", index=False ) # write the dataframe to excel file
    df2.to_excel(writer,sheet_name="completing_avg_times", index=False) # write the dataframe to excel file
    df3.to_excel(writer,sheet_name="expert_avg_times", index=False) # write the dataframe to excel file
    df4.to_excel(writer,sheet_name="photography_avg_times", index=False)
    df5.to_excel(writer,sheet_name="whole_system_avg_times", index=False)
    df6.to_excel(writer,sheet_name="max_photography_queue_length", index=False)
