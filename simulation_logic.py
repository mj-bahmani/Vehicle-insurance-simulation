"""Simulation of a Vehicle Insurance Organization

Input Distributions and Event Types:
--------------------

1- Arrival:
    - System 1:
        - Mean = 5 (time = 132000)
        - Warm-up time = 12000
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
- Expert center: Three workers
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

- System 1: 132000 time units
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



class mainSystem:
    def __init__(self, env, system,time, frameLength):
        self.env = env  # this is the environment parameters such as rate of service and ....
        self.system = system  # this is the system parameters such as number of servers and ....
        self.statutil = statisticalUtils.statistics()  # this is the class for calculating the statistics
        self.time = time  # this is the time of simulation
        self.frameLength = frameLength  # this is the length of each frame
        self.warmup = None
        self.rep_number = None

    def starting_state(self, env):
        """ this is a function to evaluate the initial state of FEL in simulation"""
        # initialize all state variables
        state = States() # this is the class for state variables

        future_event_list = list() # this is the future event list

        r = random.random()
        # being alone with probability 0.3
        is_alone = 1 if r < env.being_alone_probability else 0
        # add the first event

        for i in range(self.time//self.frameLength-2): # this is the number of frames
            future_event_list.append({'Event Type': 'Frame_END', 'Event Time': (i+1)*self.frameLength}) # this is an event

        future_event_list.append({'Event Type': 'A','alone': is_alone, 'id': 0, 'Event Time': 0})  # This is an Event
        future_event_list.append({'Event Type': 'END', 'Event Time': self.time}) # this is an event
        return state, future_event_list

    def simulation(self,outputExcel=False,excelsaver=None):
        """ This is the main function of simulation that handles the modifications that each event notice
        applies on the state valriables
        """

        self.warmup.clear_vars()
        envparam = self.env # this to handle the parameters such as rate of service and ....
        state, future_event_list = self.starting_state(envparam) # this is the initial state of the system
        clock = 0
        handler = handleOutput(self.system) # handling out puts such as statistics and ....
        running = True
        id = 1
        last_id_inside = 0 # this is the id of the last customer that is inside the system
        system = self.system # this is parameters of the system such as num worker in each center
        i = 1
        sorted_fel = sorted(future_event_list, key=lambda x: x['Event Time']) # this is the sorted future event list
        while running:
            current_event = sorted_fel[0]  # Find imminent event
            a = current_event['id'] if 'id' in current_event.keys() else '' # this is the id of the customer
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
                if current_event['alone'] == 1: # this is for handeling the case that the customer is alone
                    handler.alone_cars.append(current_event['id']) # this is for handeling the case that the customer is alone
                if clock < self.time: # when the simulation hasnt end yet
                    if current_event['alone'] == 0:
                        if state.Length_Service_Photographer == system.num_photography_workers:
                            if state.Length_Queue_Photography == system.max_photography_queue_size:
                                # handler.update_outside_surface(clock,state)
                                handler.arivingOQ[current_event['id']] = clock # add the id of customer if he enters the outside queue

                                state.Length_Queue_OutSide += 1 # update the length of outside queue
                                state.waiting_Queue_OutSide.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                    'alone': 0 }) # add the customer to the outside queue

                            else:
                                state.Length_Queue_Photography += 1 # update the length of photography queue
                                handler.arivingPhQ[current_event['id']] = clock # add the id of customer if he enters the photography queue
                                state.waiting_Queue_Photography.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                    'alone': 0, })


                        else:
                            state.Length_Service_Photographer += 1 # update the length of photography service

                            future_event_list.append({'Event Type': 'DP', 'id' : current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Photography_service)})
                    else: # if it was alone do the
                        if state.Length_Queue_Photography == system.max_photography_queue_size: # if the queue is full
                            handler.arivingOQ[current_event['id']] = clock
                            state.Length_Queue_OutSide += 1 # update the length of outside queue
                            state.waiting_Queue_OutSide.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                    'alone': 1, }) # add the customer to the outside queue
                            future_event_list.append({'Event Type': 'PA', 'id':current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Single_car_waiting)})

                        else:
                            handler.update_waiting_parking(state)
                            state.Length_Waiting_Parking += 1 # update the length of parking queue
                            state.waiting_Waiting_Parking.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                    'alone': 1, }) # add the customer to the parking queue
                            state.alone_cars_in_parking_id.append(current_event['id']) # add the id of the customer to the list of alone cars in parking
                            future_event_list.append({'Event Type': 'PA','id':current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Single_car_waiting)})
                    r = random.random()
                    is_alone = 1 if r < envparam.being_alone_probability else 0
                    future_event_list.append({'Event Type': 'A','alone': is_alone, 'id': id, 'Event Time': clock + self.sample_exponential(1/envparam.arrival_mean)}) # add the next arrival event to the future event list

                    handler.arrive_time[current_event['id']] = clock # add the id of customer if he enters the system
                    id += 1
                    #update cumulative statistics
                else:

                    #update the missing customers
                    pass
            elif Event_Type == 'DP':
                # this is for handling the departure of the photography
                if state.Length_Queue_Photography == system.max_photography_queue_size: # if the queue was full get one of then and them and first check the parking then the outside and do that

                    state.Length_Queue_Photography -= 1 # update the length of photography queue
                    customer = state.waiting_Queue_Photography.pop(0)
                    handler.departPhQ[customer['id']] = clock
                    # update the statistics using the id of them
                    handler.update_sum_max_PhQ(handler.departPhQ[customer['id']]-handler.arivingPhQ[customer['id']])
                    if state.Length_Queue_Parking == 0:# if the queue was full get one of then and them and first check the parking then the outside and do that

                        future_event_list.append({'Event Type': 'OIN', 'Event Time': clock })

                    else:# if the queue was full get one of then and them and first check the parking then the outside and do that
                        state.Length_Queue_Photography += 1 # update the length of photography queue

                        customer = state.waiting_Queue_Parking.pop(0) # get the first customer in the parking queue
                        handler.arivingPhQ[customer['id']] = clock # add the id of customer if he enters the photography queue
                        state.waiting_Queue_Photography.append({'id': customer['id'], 'alone': 0 }) # add the customer to the photography queue

                        state.Length_Queue_Parking -= 1 # update the length of parking queue


                    future_event_list.append({'Event Type': 'DP','id': customer['id'] ,'Event Time': clock + self.sample_exponential(1/envparam.Photography_service)})


                elif state.Length_Queue_Photography == 0:# if the queue was empty set one of them idle

                    state.Length_Service_Photographer -= 1 # update the length of photography service

                else:
                    state.Length_Queue_Photography -= 1 # update the length of photography queue
                    customer = state.waiting_Queue_Photography.pop(0) # get the first customer in the photography queue
                    handler.departPhQ[customer['id']] = clock # add the id of customer if he enters the photography queue
                    handler.update_sum_max_PhQ(handler.departPhQ[customer['id']]-handler.arivingPhQ[customer['id']]) # update the statistics using the id of them

                    future_event_list.append({'Event Type': 'DP','id': customer['id']  ,'Event Time': clock + self.sample_exponential(1/envparam.Photography_service)})



                if state.Length_Service_Expert1 == system.num_filing_completing_workers:
                    state.Length_Queue_Filing += 1 # update the length of filing queue
                    state.waiting_Queue_Filing.append({'id': current_event['id']}) # add the customer to the filing queue

                else:
                    state.Length_Service_Expert1 += 1 # update the length of filing service
                    future_event_list.append({'Event Type': 'DF','id':current_event['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Filling_the_case_min,envparam.Filling_the_case_max,envparam.Filling_the_case_mode)})
            elif Event_Type == 'DF':
                # this is for departure of filing the case
                if state.Length_Queue_Complete_the_case == 0: # if we had departure fisrt check the complete queue
                    # then if it was empty check the filing queue due to the priority
                    if state.Length_Queue_Filing == 0:
                        state.Length_Service_Expert1 -= 1 # update the length of filing service

                    else:# if we had departure fisrt check the complete queue
                    # then if it was empty check the filing queue due to the priority

                        state.Length_Queue_Filing -= 1 # update the length of filing queue
                        customer = state.waiting_Queue_Filing.pop(0) # get the first customer in the filing queue
                        future_event_list.append({'Event Type': 'DF','id': customer['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Filling_the_case_min,envparam.Filling_the_case_max,envparam.Filling_the_case_mode)}) # add the next departure event to the future event list
                    pass
                else:# if we had departure fisrt check the complete queue
                    # then if it was empty check the filing queue due to the priority

                    state.Length_Queue_Complete_the_case -= 1
                    customer = state.waiting_Queue_Complete_the_case.pop(0) # get the first customer in the complete queue
                    future_event_list.append({'Event Type': 'DC','id': customer['id'] ,'Event Time': clock + self.sample_triangular(
                        envparam.Case_completion_min,envparam.Case_completion_max,envparam.Case_completion_mode)})

                if state.Length_Service_Expert2 == system.num_expert_workers: # if the expert part had idle worker let the pair in else move it to queue and add its id to compute the statistics
                    state.Length_Queue_Expert += 1
                    if current_event['id'] in handler.arivingEL.keys():
                        handler.arivingEL2[current_event['id']] = clock
                    else:# if the expert part had idle worker let the pair in else move it to queue and add its id to compute the statistics
                        handler.arivingEL[current_event['id']] = clock
                    r = random.random()
                    complaint = 1 if r < envparam.submiting_complaint_probability else 0# set the value if it wants to submit complaint
                    state.waiting_Queue_Expert.append({'id':current_event['id'],'complaint':complaint})

                else:
                    state.Length_Service_Expert2 += 1
                    r = random.random()
                    complaint = 1 if r < envparam.submiting_complaint_probability else 0# set the value if it wants to submit complaint
                    future_event_list.append(
                        {'Event Type': 'DE', 'complaint': complaint, 'id': current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Expert_service)})

            elif Event_Type == 'DC':# this is for departure of completing the case
                if current_event['id'] >  last_id_inside:# this is for finding the last person who was inside the system
                    last_id_inside = current_event['id']
                handler.depart_time[current_event['id']] = clock
                # updating the sum of remaing time each person has this is actually shows each person epend how much time in the system
                handler.update_sum_remaining_time(handler.depart_time[current_event['id']] - handler.arrive_time[current_event['id']])

                if state.Length_Queue_Complete_the_case == 0:# if no one was in the queue of completing check the filing queue
                    # due to the priority and if so set one worke to idle
                    if state.Length_Queue_Filing == 0:
                        state.Length_Service_Expert1 -= 1 # update the length of filing service

                    else:

                        state.Length_Queue_Filing -= 1 # update the length of filing queue
                        customer = state.waiting_Queue_Filing.pop(0) # get the first customer in the filing queue
                        future_event_list.append(
                            {'Event Type': 'DF', 'id': customer['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Filling_the_case_min,envparam.Filling_the_case_max,envparam.Filling_the_case_mode)})
                    pass
                else:
                    state.Length_Queue_Complete_the_case -= 1 # update the length of completing queue
                    customer = state.waiting_Queue_Complete_the_case.pop(0) # get the first customer in the completing queue
                    future_event_list.append(
                        {'Event Type': 'DC', 'id': customer['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Case_completion_min,envparam.Case_completion_max,envparam.Case_completion_mode)})

                pass
            elif Event_Type == 'DE':
                # this evnnt handling is for departure of expert
                if state.Length_Queue_Expert == 0: # if no one were in the queue set one of them to idle
                    state.Length_Service_Expert2 -= 1 # update the length of expert service

                else:# else get from the queue
                    state.Length_Queue_Expert -= 1

                    customer = state.waiting_Queue_Expert.pop(0) # get the first customer in the expert queue
                    # update the ids departed the queue to be used
                    if customer['id'] in handler.departEL.keys():

                        handler.departEL2[customer['id']] = clock
                        handler.update_sum_max_EL(handler.departEL2[customer['id']]-handler.arivingEL2[customer['id']])
                    else:
                        #this part is for the sake of that the a customer can be in the queue of expert center more than one time some we are handleing that with another
                        # dictionary to halp make the statistics be correct
                        handler.departEL[customer['id']] = clock
                        handler.update_sum_max_EL(handler.departEL[customer['id']]-handler.arivingEL[customer['id']]) # update the sum of max EL

                    future_event_list.append({'Event Type': 'DE','id': customer['id'], 'complaint': customer['complaint'], 'Event Time': clock + self.sample_exponential(1/envparam.Expert_service)})

                if current_event['complaint'] == 0:# if the customer wants to submit complaint and the worker wasnt busy send it
                    # in else sent it to the queu and update the dictionary of ariving time
                    if state.Length_Service_Expert1 == system.num_filing_completing_workers:
                        state.Length_Queue_Complete_the_case += 1
                        state.waiting_Queue_Complete_the_case.append({'id':current_event['id']}) # update the length of completing queue


                    else:
                        state.Length_Service_Expert1 += 1 # update the length of completing service
                        future_event_list.append({'Event Type': 'DC','id':current_event['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Case_completion_min,envparam.Case_completion_max,envparam.Case_completion_mode)}) # update the length of completing queue



                else:# else get the back to the previous part and do the same if the worker was busy ...
                    if state.Length_Service_Expert3 == system.num_submiting_complaint_workers:
                        handler.arivingSCL[current_event['id']] = clock # update the dictionary of ariving time
                        state.Length_Queue_Submitting_Complaint += 1 # update the length of submitting queue
                        state.waiting_Queue_Submitting_Complaint.append({'id': current_event['id']}) # update the length of submitting queue
                    else:
                        state.Length_Service_Expert3 += 1
                        future_event_list.append({'Event Type': 'DSC', 'id': current_event['id'],
                                                  'Event Time': clock + self.sample_exponential(1 / envparam.Complaint_service)})


                pass
            elif Event_Type == 'DSC':
                # to handle the submiting complement part
                if current_event['id'] in handler.alone_cars: # if the customer was alone in the system update the statistics
                    handler.alone_submited_complaint += 1
                state.noSubmitComplaint += 1 # update the number of submitted complaint
                if state.Length_Queue_Submitting_Complaint == 0:
                    state.Length_Service_Expert3 -= 1 # update the length of submitting service
                    pass
                else:

                    state.Length_Queue_Submitting_Complaint -= 1 # update the length of submitting queue
                    customer = state.waiting_Queue_Submitting_Complaint.pop(0)  # get the first customer in the submitting queue
                    handler.departSCL[customer['id']] = clock # update the dictionary of ariving time
                    # this is for updating the SCl max and mean time in queue
                    handler.update_sum_max_SCL(handler.departSCL[customer['id']]-handler.arivingSCL[customer['id']])
                    future_event_list.append({'Event Type': 'DSC', 'id': customer['id'],'Event Time': clock + self.sample_exponential(1/envparam.Complaint_service)})
                    pass

                if state.Length_Service_Expert2 == system.num_expert_workers:
                    # if the worker were full add to the queue and add id tho compute statistics
                    state.Length_Queue_Expert += 1 # update the length of expert queue
                    if current_event['id'] in handler.arivingEL.keys():
                        handler.arivingEL2[current_event['id']] = clock # update the dictionary of ariving time
                    else:
                        handler.arivingEL[current_event['id']] = clock # update the dictionary of ariving time
                    state.waiting_Queue_Expert.append({'id':current_event['id'],'complaint': 0})
                    pass
                else:# if the worker were idle set it busy
                    state.Length_Service_Expert2 += 1 # update the length of expert service
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
                            state.waiting_Waiting_Parking.remove(car) # remove it from the waiting parking list
                            state.Length_Waiting_Parking -= 1
                            break

                    if state.Length_Service_Photographer == system.num_photography_workers:
                        # if photographers werent idle let them in the queue
                        if state.Length_Queue_Photography == system.max_photography_queue_size:


                            state.Length_Queue_Parking += 1
                            # add the id to find the statistics
                            state.waiting_Queue_Parking.append({'id':current_event['id']})

                        else:# if there was a idle photographer let the pair in
                            handler.arivingPhQ[current_event['id']] = clock
                            state.Length_Queue_Photography += 1 # update the length of photography queue

                            state.waiting_Queue_Photography.append({'id':current_event['id']})

                    else:
                        state.Length_Service_Photographer += 1 # update the length of photography service
                        future_event_list.append({'Event Type': 'DP','id': current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Photography_service)})

            elif Event_Type == 'OIN':# entering a car from outside queue to inside
                if clock < self.time:
                    if state.Length_Queue_OutSide > 0:

                        customer = state.waiting_Queue_OutSide.pop(0) # get the first customer in the outside queue
                        handler.departOQ[customer['id']] = clock# when it leaves the outside queue we get the id and save it
                        state.Length_Queue_OutSide -= 1
                        handler.update_sum_max_OQ(handler.departOQ[customer['id']]-handler.arivingOQ[customer['id']])

                        if customer['alone'] == 0  :# if it wasnt alone move it to queue of inside
                            state.Length_Queue_Photography += 1
                            handler.arivingPhQ[customer['id']] = clock # update the dictionary of ariving time
                            state.waiting_Queue_Photography.append({'id':customer['id']})

                        else:# if it was alone move it to waiting cars
                            handler.update_waiting_parking(state)
                            state.Length_Waiting_Parking += 1 # update the length of waiting parking
                            state.waiting_Waiting_Parking.append({'id':customer['id'],'alone':1})


                            state.alone_cars_in_parking_id.append(customer['id']) # add it to the list of alone cars in parking

                            future_event_list.append({'Event Type': 'OIN','Event Time': clock })

                    else:
                        pass
                else:
                    # make the outside queue empty after hour 6
                    for pair in state.waiting_Queue_OutSide:
                        handler.departOQ[pair['id']] = self.time

                    state.Length_Queue_OutSide = 0 # update the length of outside queue

                    state.waiting_Queue_OutSide.clear()

            elif Event_Type == "END":

                running = False
            elif Event_Type == 'Frame_END':
                handler.update_photography_surface(clock, state) # update the photography surface
                handler.update_outside_surface(clock, state) # update the outside surface
                handler.update_submiting_surface(clock, state) # update the submiting surface
                handler.update_expert_surface(clock, state)
                handler.update_filing_surface(clock, state)
                handler.update_complete_surface(clock, state)
                self.warmup.warmup_Phq[self.rep_number].append((handler.SPhL-self.warmup.previous_Phq)/self.frameLength) # update the warmup list of photography queue
                self.warmup.previous_Phq = handler.SPhL

                self.warmup.warmup_Oq[self.rep_number].append(
                    (handler.SOL - self.warmup.previous_Oq) / self.frameLength) # update the warmup list of outside queue
                self.warmup.previous_Oq = handler.SOL

                self.warmup.warmup_fq[self.rep_number].append(
                    (handler.SFL - self.warmup.previous_fq) / self.frameLength) # update the warmup list of filing queue
                self.warmup.previous_fq = handler.SFL

                self.warmup.warmup_cq[self.rep_number].append(
                    (handler.SCL - self.warmup.previous_cq) / self.frameLength) # update the warmup list of complete queue
                self.warmup.previous_cq = handler.SCL

                self.warmup.warmup_eq[self.rep_number].append(
                    (handler.SEL - self.warmup.previous_eq) / self.frameLength) # update the warmup list of expert queue
                self.warmup.previous_eq = handler.SEL

                self.warmup.warmup_scq[self.rep_number].append(
                    (handler.SSCL - self.warmup.previous_scq) / self.frameLength) # update the warmup list of submiting complaint queue
                self.warmup.previous_scq = handler.SSCL


            # removes from the queue and go to next step
            future_event_list.remove(current_event)
            sorted_fel = sorted(future_event_list, key=lambda x: x['Event Time'])
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
        #return to get the out puts
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
        threshold = (mod - min)/(max - min)
        if r < threshold:
            return math.sqrt(r*(max-min)*(mod-min)) + min
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
        self.warmup.res_2_numpy()
        self.warmup.cal_mean()
        self.warmup.draw_chart(7)


env1 = environmentDistribution.EnvironmentDist(5 ,5, 6, 7, 6, 8, 9,9, 0.1 ) # make an environment object for sys1
env2 = environmentDistribution.EnvironmentDist(3.2,6,8,10,3,3.5,4,8,0) # make an environment object for sys2
sys1 = System.System(3,3) # make a system object for sys1
sys2 = System.System(4,3) # make a system object for sys2

simul1 = mainSystem(env1,sys1,21600, 30)
simul1.run_simul(50)

simul2 = mainSystem(env2,sys2,21600, 30)
simul2.run_simul(50)