""" Simulation of a Vehicle Insurance Organization

Input Distributions and Event Types:
    1- Arrival: Depends on weather and time, modeled with an Exponential distribution
    2- Partner Arrival: Exponential distribution with mean = 30 minutes
    3- Photography Service: Modeled with an Exponential distribution (lambda=1/6)
    4- Single Car Waiting: Follows an Exponential distribution (lambda=1/30)
    5- Filling the Case: Service time follows a Triangular distribution (min=5, mode=6, max=7)
    6- Expert Service: Modeled with an Exponential distribution (lambda=1/9)
    7- Case Completion: Service time follows a Triangular distribution (min=6, mode=8, max=9)
    8- Complaint Service: Modeled with an Exponential distribution (lambda=1/15)

Additional Parameters:
    1- Probability that a car arrives alone: 0.3
    2- Probability that a customer makes a complaint: 0.1

Staffing:
    1- Filling and Completing the Case center: Three workers
    2- Expert center: Two experts
    3- Photography center: Two photographers
    4- Complaint Submission center: One staff member

Queuing Discipline:
    Majority of queues in this simulation follow a FIFO (First In, First Out) discipline. However,
    in the case of Filling and Completing the Case, Completing the Case queue receives higher priority over Filling the Case queue.

Outputs:
    1- Efficiency of workers involved in the Photography, Expert, Complaint Submission, Filling, and Completion of the Case services.
    2- Average queue length for the Photography queue, Outside queue, Expert queue, and Complaint Submission queue.
    3- Maximum queue length for the Photography queue, Outside queue, Expert queue, and Complaint Submission queue.
    4- Average time spent in the Photography queue, Outside queue, Expert queue, and Complaint Submission queue.
    5- Probabilities that the Waiting Parking and Filling queue are empty.
    6- The percentage of customers who arrived alone and submitted a complaint.
    7- Mean time of remaining in the system.
Interactions in this simulation occur based on the occurrence of these events and the additional parameters.

Outputs:
    Detailed analysis of the operations of the insurance organization

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
    def __init__(self, env, system,time, frameLength, warmup_time):
        self.env = env
        self.system = system
        self.statutil = statisticalUtils.statistics()
        self.time = time
        self.frameLength = frameLength
        self.warmup = None
        self.rep_number = None
        self.warmup_Time = warmup_time


    def starting_state(self, env):
        """ this is a function to evaluate the initial state of FEL in simulation"""
        # initialize all state variables
        state = States()

        future_event_list = list()

        r = random.random()
        # being alone with probability 0.3
        is_alone = 1 if r < env.being_alone_probability else 0
        # add the first event

        # for i in range(self.time//self.frameLength-2):
        #     future_event_list.append({'Event Type': 'Frame_END', 'Event Time': (i+1)*self.frameLength})

        future_event_list.append({'Event Type': 'A','alone': is_alone, 'id': 0, 'Event Time': 0})  # This is an Event
        future_event_list.append({'Event Type': 'END', 'Event Time': self.time})
        return state, future_event_list

    def simulation(self,outputExcel=False,excelsaver=None):
        """ This is the main function of simulation that handles the modifications that each event notice
        applies on the state valriables
        """

        self.warmup.clear_vars()
        envparam = self.env # this to handle the parameters such as rate of service and ....
        state, future_event_list = self.starting_state(envparam)
        clock = 0
        handler = handleOutput(self.system, self.warmup_Time) # handling out puts
        running = True
        id = 1
        last_id_inside = 0
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
            handler.update_queue_parking_empty(clock, state)
            handler.update_photography_surface(clock, state)
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
                    handler.alone_cars.append(current_event['id'])
                if clock < self.time:
                    if current_event['alone'] == 0:
                        if state.Length_Service_Photographer == system.num_photography_workers:
                            if state.Length_Queue_Photography == system.max_photography_queue_size:
                                # handler.update_outside_surface(clock,state)
                                handler.arivingOQ[current_event['id']] = clock # add the id of customer if he enters the outside queue

                                state.Length_Queue_OutSide += 1
                                state.waiting_Queue_OutSide.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                    'alone': 0 })

                            else:
                                state.Length_Queue_Photography += 1
                                handler.arivingPhQ[current_event['id']] = clock
                                state.waiting_Queue_Photography.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                    'alone': 0, })


                        else:
                            state.Length_Service_Photographer += 1

                            future_event_list.append({'Event Type': 'DP', 'id' : current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Photography_service)})
                    else: # if it was alone do the
                        if state.Length_Queue_Photography == system.max_photography_queue_size:
                            handler.arivingOQ[current_event['id']] = clock
                            state.Length_Queue_OutSide += 1
                            state.waiting_Queue_OutSide.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                    'alone': 1, })
                            future_event_list.append({'Event Type': 'PA', 'id':current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Single_car_waiting)})

                        else:
                            handler.update_waiting_parking(state)
                            state.Length_Waiting_Parking += 1
                            state.waiting_Waiting_Parking.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                    'alone': 1, })
                            state.alone_cars_in_parking_id.append(current_event['id'])
                            future_event_list.append({'Event Type': 'PA','id':current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Single_car_waiting)})
                    r = random.random()
                    is_alone = 1 if r < envparam.being_alone_probability else 0
                    future_event_list.append({'Event Type': 'A','alone': is_alone, 'id': id, 'Event Time': clock + self.sample_exponential(1/envparam.arrival_mean)})

                    handler.arrive_time[current_event['id']] = clock
                    id += 1
                    #update cumulative statistics
                else:

                    #update the missing customers
                    pass
            elif Event_Type == 'DP':
                # this is for handling the departure of the photography
                if state.Length_Queue_Photography == system.max_photography_queue_size: # if the queue was full get one of then and them and first check the parking then the outside and do that

                    state.Length_Queue_Photography -= 1
                    customer = state.waiting_Queue_Photography.pop(0)
                    handler.departPhQ[customer['id']] = clock
                    # update the statistics using the id of them
                    handler.update_sum_max_PhQ(handler.departPhQ[customer['id']]-handler.arivingPhQ[customer['id']],handler.arivingPhQ[customer['id']])
                    if state.Length_Queue_Parking == 0:# if the queue was full get one of then and them and first check the parking then the outside and do that

                        future_event_list.append({'Event Type': 'OIN', 'Event Time': clock })

                    else:# if the queue was full get one of then and them and first check the parking then the outside and do that
                        state.Length_Queue_Photography += 1

                        customer = state.waiting_Queue_Parking.pop(0)
                        handler.arivingPhQ[customer['id']] = clock
                        state.waiting_Queue_Photography.append({'id': customer['id'], 'alone': 0 })

                        state.Length_Queue_Parking -= 1


                    future_event_list.append({'Event Type': 'DP','id': customer['id'] ,'Event Time': clock + self.sample_exponential(1/envparam.Photography_service)})


                elif state.Length_Queue_Photography == 0:# if the queue was empty set one of them idle

                    state.Length_Service_Photographer -= 1

                else:
                    state.Length_Queue_Photography -= 1
                    customer = state.waiting_Queue_Photography.pop(0)
                    handler.departPhQ[customer['id']] = clock
                    handler.update_sum_max_PhQ(handler.departPhQ[customer['id']]-handler.arivingPhQ[customer['id']],handler.arivingPhQ[customer['id']])

                    future_event_list.append({'Event Type': 'DP','id': customer['id']  ,'Event Time': clock + self.sample_exponential(1/envparam.Photography_service)})



                if state.Length_Service_Expert1 == system.num_filing_completing_workers:
                    state.Length_Queue_Filing += 1
                    handler.ariving_FL[current_event['id']] = clock
                    state.waiting_Queue_Filing.append({'id': current_event['id']})

                else:
                    state.Length_Service_Expert1 += 1
                    future_event_list.append({'Event Type': 'DF','id':current_event['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Filling_the_case_min,envparam.Filling_the_case_max,envparam.Filling_the_case_mode)})
            elif Event_Type == 'DF':
                # this is for departure of filing the case
                if state.Length_Queue_Complete_the_case == 0: # if we had departure fisrt check the complete queue
                    # then if it was empty check the filing queue due to the priority
                    if state.Length_Queue_Filing == 0:
                        state.Length_Service_Expert1 -= 1

                    else:# if we had departure fisrt check the complete queue
                    # then if it was empty check the filing queue due to the priority

                        state.Length_Queue_Filing -= 1

                        customer = state.waiting_Queue_Filing.pop(0)
                        handler.depart_FL[customer['id']] = clock
                        handler.update_waiting_time_filing_case(handler.depart_FL[customer['id']]-handler.ariving_FL[customer['id']], handler.ariving_FL[customer['id']])
                        future_event_list.append({'Event Type': 'DF','id': customer['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Filling_the_case_min,envparam.Filling_the_case_max,envparam.Filling_the_case_mode)})
                    pass
                else:# if we had departure fisrt check the complete queue
                    # then if it was empty check the filing queue due to the priority

                    state.Length_Queue_Complete_the_case -= 1
                    customer = state.waiting_Queue_Complete_the_case.pop(0)
                    handler.depart_CL[customer['id']] = clock
                    handler.update_wating_time_complete_case(handler.depart_CL[customer['id']]-handler.ariving_CL[customer['id']], handler.ariving_CL[customer['id']])
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
                handler.update_sum_remaining_time(handler.depart_time[current_event['id']] - handler.arrive_time[current_event['id']],handler.arrive_time[current_event['id']])

                if state.Length_Queue_Complete_the_case == 0:# if no one was in the queue of completing check the filing queue
                    # due to the priority and if so set one worke to idle
                    if state.Length_Queue_Filing == 0:
                        state.Length_Service_Expert1 -= 1

                    else:

                        state.Length_Queue_Filing -= 1
                        customer = state.waiting_Queue_Filing.pop(0)
                        handler.depart_FL[customer['id']] = clock
                        handler.update_waiting_time_filing_case(
                            handler.depart_FL[customer['id']] - handler.ariving_FL[customer['id']],
                            handler.ariving_FL[customer['id']])
                        future_event_list.append(
                            {'Event Type': 'DF', 'id': customer['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Filling_the_case_min,envparam.Filling_the_case_max,envparam.Filling_the_case_mode)})
                    pass
                else:
                    state.Length_Queue_Complete_the_case -= 1
                    customer = state.waiting_Queue_Complete_the_case.pop(0)
                    handler.depart_CL[customer['id']] = clock
                    handler.update_wating_time_complete_case(
                        handler.depart_CL[customer['id']] - handler.ariving_CL[customer['id']],
                        handler.ariving_CL[customer['id']])
                    future_event_list.append(
                        {'Event Type': 'DC', 'id': customer['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Case_completion_min,envparam.Case_completion_max,envparam.Case_completion_mode)})

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

                        handler.departEL2[customer['id']] = clock
                        handler.update_sum_max_EL(handler.departEL2[customer['id']]-handler.arivingEL2[customer['id']], handler.arivingEL2[customer['id']])
                    else:
                        #this part is for the sake of that the a customer can be in the queue of expert center more than one time some we are handleing that with another
                        # dictionary to halp make the statistics be correct
                        handler.departEL[customer['id']] = clock
                        handler.update_sum_max_EL(handler.departEL[customer['id']]-handler.arivingEL[customer['id']],handler.arivingEL[customer['id']])

                    future_event_list.append({'Event Type': 'DE','id': customer['id'], 'complaint': customer['complaint'], 'Event Time': clock + self.sample_exponential(1/envparam.Expert_service)})

                if current_event['complaint'] == 0:# if the customer wants to submit complaint and the worker wasnt busy send it
                    # in else sent it to the queu and update the dictionary of ariving time
                    if state.Length_Service_Expert1 == system.num_filing_completing_workers:
                        state.Length_Queue_Complete_the_case += 1
                        handler.ariving_CL[current_event['id']] = clock
                        state.waiting_Queue_Complete_the_case.append({'id':current_event['id']})


                    else:
                        state.Length_Service_Expert1 += 1
                        future_event_list.append({'Event Type': 'DC','id':current_event['id'], 'Event Time': clock + self.sample_triangular(
                        envparam.Case_completion_min,envparam.Case_completion_max,envparam.Case_completion_mode)})



                else:# else get the back to the previous part and do the same if the worker was busy ...
                    if state.Length_Service_Expert3 == system.num_submiting_complaint_workers:
                        handler.arivingSCL[current_event['id']] = clock
                        state.Length_Queue_Submitting_Complaint += 1
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
                state.noSubmitComplaint += 1
                if state.Length_Queue_Submitting_Complaint == 0:
                    state.Length_Service_Expert3 -= 1
                    pass
                else:

                    state.Length_Queue_Submitting_Complaint -= 1
                    customer = state.waiting_Queue_Submitting_Complaint.pop(0)
                    handler.departSCL[customer['id']] = clock
                    # this is for updating the SCl max and mean time in queue
                    handler.update_sum_max_SCL(handler.departSCL[customer['id']]-handler.arivingSCL[customer['id']])
                    future_event_list.append({'Event Type': 'DSC', 'id': customer['id'],'Event Time': clock + self.sample_exponential(1/envparam.Complaint_service)})
                    pass

                if state.Length_Service_Expert2 == system.num_expert_workers:
                    # if the worker were full add to the queue and add id tho compute statistics
                    state.Length_Queue_Expert += 1
                    if current_event['id'] in handler.arivingEL.keys():
                        handler.arivingEL2[current_event['id']] = clock
                    else:
                        handler.arivingEL[current_event['id']] = clock
                    state.waiting_Queue_Expert.append({'id':current_event['id'],'complaint': 0})
                    pass
                else:# if the worker were idle set it busy
                    state.Length_Service_Expert2 += 1
                    future_event_list.append({'Event Type': 'DE','complaint': 0,'id': current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Expert_service)})
                    pass

            elif Event_Type == 'PA':
                # if second car arrive try to find its corresponding car and join it
                if current_event['id'] not in state.alone_cars_in_parking_id:
                    for car in state.waiting_Queue_OutSide:# if its pair was in outside queue
                        if car['id'] == current_event['id']:
                            car['alone'] = 0
                            break


                else:# if its pair was inside

                    state.alone_cars_in_parking_id.remove(current_event['id'])


                    for car in state.waiting_Waiting_Parking: # make its aloneness atribute to false
                        if car['id'] == current_event['id']:
                            handler.update_waiting_parking(state)
                            state.waiting_Waiting_Parking.remove(car)
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
                            state.Length_Queue_Photography += 1

                            state.waiting_Queue_Photography.append({'id':current_event['id']})

                    else:
                        state.Length_Service_Photographer += 1
                        future_event_list.append({'Event Type': 'DP','id': current_event['id'], 'Event Time': clock + self.sample_exponential(1/envparam.Photography_service)})

            elif Event_Type == 'OIN':# entering a car from outside queue to inside
                if clock < self.time:
                    if state.Length_Queue_OutSide > 0:

                        customer = state.waiting_Queue_OutSide.pop(0)
                        handler.departOQ[customer['id']] = clock# when it leaves the outside queue we get the id and save it
                        state.Length_Queue_OutSide -= 1
                        handler.update_sum_max_OQ(handler.departOQ[customer['id']]-handler.arivingOQ[customer['id']])

                        if customer['alone'] == 0  :# if it wasnt alone move it to queue of inside
                            state.Length_Queue_Photography += 1
                            handler.arivingPhQ[customer['id']] = clock
                            state.waiting_Queue_Photography.append({'id':customer['id']})

                        else:# if it was alone move it to waiting cars
                            handler.update_waiting_parking(state)
                            state.Length_Waiting_Parking += 1
                            state.waiting_Waiting_Parking.append({'id':customer['id'],'alone':1})


                            state.alone_cars_in_parking_id.append(customer['id'])

                            future_event_list.append({'Event Type': 'OIN','Event Time': clock })

                    else:
                        pass
                else:
                    # make the outside queue empty after hour 6
                    for pair in state.waiting_Queue_OutSide:
                        handler.departOQ[pair['id']] = self.time

                    state.Length_Queue_OutSide = 0

                    state.waiting_Queue_OutSide.clear()

            elif Event_Type == "END":
                self.warmup.mean_filing_the_case_waiting_time.append(handler.remain_filing_queue_waiting_time / handler.num_of_filing_queue_customer)
                self.warmup.mean_complete_the_case_waiting_time.append(handler.remain_complete_the_case_queue_waiting_time / handler.num_of_complete_the_case_queue_customer)
                self.warmup.mean_expert_waiting_time.append(handler.sum_Time_EL / handler.num_of_expert_queue_customer)
                self.warmup.mean_photography_waiting_time.append(handler.sum_Time_phQ / handler.num_of_photography_queue_customer)
                self.warmup.mean_whole_system_remain_time.append(handler.remainSystem/ handler.num_of_remain_in_system_customer)
                self.warmup.max_expert_queue_length.append(handler.MEL)
                running = False
            elif Event_Type == 'Frame_END':
                handler.update_photography_surface(clock, state)
                handler.update_outside_surface(clock, state)
                handler.update_submiting_surface(clock, state)
                handler.update_expert_surface(clock, state)
                handler.update_filing_surface(clock, state)
                handler.update_complete_surface(clock, state)
                self.warmup.warmup_Phq[self.rep_number].append((handler.SPhL-self.warmup.previous_Phq)/self.frameLength)
                self.warmup.previous_Phq = handler.SPhL

                self.warmup.warmup_Oq[self.rep_number].append(
                    (handler.SOL - self.warmup.previous_Oq) / self.frameLength)
                self.warmup.previous_Oq = handler.SOL

                self.warmup.warmup_fq[self.rep_number].append(
                    (handler.SFL - self.warmup.previous_fq) / self.frameLength)
                self.warmup.previous_fq = handler.SFL

                self.warmup.warmup_cq[self.rep_number].append(
                    (handler.SCL - self.warmup.previous_cq) / self.frameLength)
                self.warmup.previous_cq = handler.SCL

                self.warmup.warmup_eq[self.rep_number].append(
                    (handler.SEL - self.warmup.previous_eq) / self.frameLength)
                self.warmup.previous_eq = handler.SEL

                self.warmup.warmup_scq[self.rep_number].append(
                    (handler.SSCL - self.warmup.previous_scq) / self.frameLength)
                self.warmup.previous_scq = handler.SSCL



            sorted_fel = sorted(future_event_list, key=lambda x: x['Event Time'])
            future_event_list.remove(current_event) # removes from the queue and go to next step

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

    def run_simul_for_mean(self, repeatTimes):
        self.warmup = warmUp.WarmUP(repeatTimes)
        for i in range(repeatTimes):
            self.simulation()
        a,b,c,d,e,f = self.warmup.mean_for_waiting_times()
        # print(f'the average waiting time for filing queue is {a} minutes')
        # print(f'the average waiting time for complete the case queue is {b} minutes')
        return a,b,c,d,e,f
    def get_final_res(self, replication, repeatTimes):

        filing_avg_times = []
        completing_avg_times = []
        expert_avg_times = []
        photography_avg_times = []
        whole_system_avg_times = []
        max_expert_queue_length = []
        for i in range(replication):
            a,b,c,d,e,f = self.run_simul_for_mean(repeatTimes)
            filing_avg_times.append(a)
            completing_avg_times.append(b)
            expert_avg_times.append(c)
            photography_avg_times.append(d)
            whole_system_avg_times.append(e)
            max_expert_queue_length.append(f)


        return filing_avg_times,completing_avg_times,expert_avg_times,photography_avg_times,whole_system_avg_times,max_expert_queue_length



env1 = environmentDistribution.EnvironmentDist(5 ,5, 6, 7, 6, 8, 9,9, 0.1 )
env2 = environmentDistribution.EnvironmentDist(3.2,6,8,10,3,3.5,4,8,0)
sys1 = System.System(3,3)
sys2 = System.System(4,3)

# simul1 = mainSystem(env1,sys1,21600, 30)
# simul1.run_simul(20)

# simul2 = mainSystem(env2,sys2,21600, 30)
# simul2.run_simul(20)

simul1 = mainSystem(env1,sys1,132000, 30, 12000)
f1,c1,e1,ph1,r1,me1 = simul1.get_final_res(20, 50 )

simul2 = mainSystem(env2,sys2,165000, 30, 15000)
f2,c2,e2,ph2,r2,me2 = simul2.get_final_res(20,50)





df1 = pd.DataFrame(map(list,zip(*[f1,f2])),columns =['sys1','sys2'] )
df2 = pd.DataFrame(map(list,zip(*[c1,c2])),columns =['sys1','sys2'])
df3 = pd.DataFrame(map(list,zip(*[e1,e2])),columns =['sys1','sys2'])
df4 = pd.DataFrame(map(list,zip(*[ph1,ph2])),columns = ['sys1','sys2'])
df5 = pd.DataFrame(map(list,zip(*[r1,r2])),columns =['sys1','sys2'])
df6 = pd.DataFrame(map(list,zip(*[me1,me2])),columns =['sys1','sys2'])

with pd.ExcelWriter("output3.xlsx") as writer:
    # use to_excel function and specify the sheet_name and index
    # to store the dataframe in specified sheet

    df1.to_excel(writer,sheet_name="filing_avg_times", index=False )
    df2.to_excel(writer,sheet_name="completing_avg_times", index=False)
    df3.to_excel(writer,sheet_name="expert_avg_times", index=False)
    df4.to_excel(writer,sheet_name="photography_avg_times", index=False)
    df5.to_excel(writer,sheet_name="whole_system_avg_times", index=False)
    df6.to_excel(writer,sheet_name="max_expert_queue_length", index=False)
