""" Simulation of a Vehicle Insurance Organization

Input Distributions and Event Types:
    1- Arrival: Depends on weather and time, modeled with an Exponential distribution
    2- Partner Arrival: Exponential distribution with mean = 30 minutes
    3- Photography Service: Modeled with an Exponential distribution (lambda=6)
    4- Single Car Waiting: Follows an Exponential distribution (lambda=30)
    5- Filling the Case: Service time follows a Triangular distribution (min=5, mode=6, max=7)
    6- Expert Service: Modeled with an Exponential distribution (lambda=9)
    7- Case Completion: Service time follows a Triangular distribution (min=6, mode=8, max=9)
    8- Complaint Service: Modeled with an Exponential distribution (lambda=15)

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
from States import States
from handleOutputs import handleOutput


def starting_state():
    """ this is a function to evaluate the initial state of FEL in simulation"""
    # initialize all state variables
    state = States() # this is for making an object of state to store the state variables

    future_event_list = list() # this is for making a list of future events

    r = random.random()
    # being alone with probability 0.3
    is_alone = 1 if r < 0.3 else 0
    # add the first event
    future_event_list.append({'Event Type': 'A','alone': is_alone, 'id': 0, 'Event Time': 0})  # add the first event to FEL

    return state, future_event_list

def simulation(outputExcel=True,excelsaver=None):
    """ This is the main function of simulation that handles the modifications that each event notice
    applies on the state valriables and FEL
    """
    dataset = pd.read_csv('datasets/Arrival Rate.csv') # this is the dataset of arrival rate
    envparam = environmentDistribution.EnvironmentDist() # this to handle the parameters such as rate of service and ....
    state, future_event_list = starting_state() # this is the initial state of the system
    r = random.random()
    weather_condition = 'rainy' if r < 0.31 else 'sunny' # this is the weather condition
    print(f'the weather condition is {weather_condition}')
    clock = 0
    handler = handleOutput() # handling out puts
    running = True
    id = 1
    last_id_inside = 0 # this is the id of last customer that is inside the system
    system = System.System() # this is parameters of the system such as num worker in each center
    i = 1
    sorted_fel = sorted(future_event_list, key=lambda x: x['Event Time']) # sort the FEL based on the time of events

    while running: # this is the main loop of simulation

        current_event = sorted_fel[0]  # Find imminent event

        a = current_event['id'] if 'id' in current_event.keys() else '' # this is the id of current event

        Event_Type = current_event['Event Type'] # this is the type of current event
        clock = current_event['Event Time']  # Advance time

        # these lines are for handeling and updating the cumulitive statistics
        handler.update_filing_empty(clock, state) # update the cumulitive statistics of filing empty
        handler.update_queue_parking_empty(clock, state)    # update the cumulitive statistics of parking empty
        handler.update_photography_surface(clock, state)
        handler.update_outside_surface(clock, state)
        handler.update_submiting_surface(clock, state)
        handler.update_expert_surface(clock, state)
        handler.update_Service_Photographer_surface(clock, state)
        handler.update_Expert1_surface(clock, state)
        handler.update_Expert2_surface(clock, state)
        handler.update_Expert3_surface(clock, state)



        if Event_Type == 'A': # this is for handeling arival event
            if current_event['alone'] == 1: # if the customer is alone
                handler.alone_cars.append(current_event['id'])
            if clock < 600: # if the time is less than 600
                if current_event['alone'] == 0: # if the customer is not alone
                    if state.Length_Service_Photographer == system.num_photography_workers: # if the number of busy photographer is equal to the number of photographer
                        if state.Length_Queue_Photography == system.max_photography_queue_size:
                            handler.arivingOQ[current_event['id']] = clock # add the id of customer if he enters the outside queue

                            state.Length_Queue_OutSide += 1 # increase the length of outside queue
                            state.waiting_Queue_OutSide.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                'alone': 0 }) # add the customer to the outside queue

                        else: # if the length of outside queue is less than the maximum length
                            state.Length_Queue_Photography += 1
                            handler.arivingPhQ[current_event['id']] = clock
                            state.waiting_Queue_Photography.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                'alone': 0, }) # add the customer to the photography queue


                    else: # if the number of busy photographer is less than the number of photographer
                        state.Length_Service_Photographer += 1

                        future_event_list.append({'Event Type': 'DP', 'id' : current_event['id'], 'Event Time': clock + sample_exponential(1/envparam.Photography_service)}) # add the departure event of photography to FEL
                else:  # if the customer is alone
                    if state.Length_Queue_Photography == system.max_photography_queue_size:
                        handler.arivingOQ[current_event['id']] = clock # add the id of customer if he enters the outside queue
                        state.Length_Queue_OutSide += 1
                        state.waiting_Queue_OutSide.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                'alone': 1, }) # add the customer to the outside queue
                        future_event_list.append({'Event Type': 'PA', 'id':current_event['id'], 'Event Time': clock + sample_exponential(1/envparam.Single_car_waiting)}) # add the departure event of parking to FEL

                    else: # if the length of outside queue is less than the maximum length
                        handler.update_waiting_parking(state)
                        state.Length_Waiting_Parking += 1 # increase the length of waiting parking
                        state.waiting_Waiting_Parking.append({'id': current_event['id'], 'Event Time': current_event['Event Time'],
                                                                'alone': 1, }) # add the customer to the waiting parking queue
                        state.alone_cars_in_parking_id.append(current_event['id']) # add the id of customer to the list of alone cars in parking
                        future_event_list.append({'Event Type': 'PA','id':current_event['id'], 'Event Time': clock + sample_exponential(1/envparam.Single_car_waiting)})
                r = random.random()
                is_alone = 1 if r < 0.3 else 0
                future_event_list.append({'Event Type': 'A','alone': is_alone, 'id': id, 'Event Time':
                    clock + sample_exponential(1/arrival_rate(weather_condition,clock,dataset))}) # add the next arival event to FEL

                handler.arrive_time[current_event['id']] = clock # add the time of arival of customer to the dictionary of arival time
                id += 1
                #update cumulative statistics
            else:

                #update the missing customers
                pass
        elif Event_Type == 'DP': # this is for handeling departure of photography
            # this is for handling the departure of the photography
            if state.Length_Queue_Photography == system.max_photography_queue_size: # if the queue was full get one of then and them and first check the parking then the outside and do that

                state.Length_Queue_Photography -= 1 # decrease the length of photography queue
                customer = state.waiting_Queue_Photography.pop(0) # get the first customer in the queue
                handler.departPhQ[customer['id']] = clock
                # update the statistics using the id of them
                handler.update_sum_max_PhQ(handler.departPhQ[customer['id']]-handler.arivingPhQ[customer['id']]) # update the sum and max of the time of customer in photography queue
                if state.Length_Queue_Parking == 0:# if the queue was full get one of then and them and first check the parking then the outside and do that

                    future_event_list.append({'Event Type': 'OIN', 'Event Time': clock }) # add the outside in event to FEL

                else:# if the queue was full get one of then and them and first check the parking then the outside and do that
                    state.Length_Queue_Photography += 1 # increase the length of photography queue

                    customer = state.waiting_Queue_Parking.pop(0) # get the first customer in the queue
                    handler.arivingPhQ[customer['id']] = clock # add the time of arival of customer to the dictionary of arival time
                    state.waiting_Queue_Photography.append({'id': customer['id'], 'alone': 0 })

                    state.Length_Queue_Parking -= 1 # decrease the length of parking queue


                future_event_list.append({'Event Type': 'DP','id': customer['id'] ,'Event Time': clock + sample_exponential(1/envparam.Photography_service)}) # add the departure event of photography to FEL


            elif state.Length_Queue_Photography == 0:# if the queue was empty set one of them idle

                state.Length_Service_Photographer -= 1

            else:   # if the queue was not empty get one of them and set him to busy
                state.Length_Queue_Photography -= 1 # decrease the length of photography queue
                customer = state.waiting_Queue_Photography.pop(0)   # get the first customer in the queue
                handler.departPhQ[customer['id']] = clock # add the time of departure of customer to the dictionary of departure time
                handler.update_sum_max_PhQ(handler.departPhQ[customer['id']]-handler.arivingPhQ[customer['id']]) # update the sum and max of the time of customer in photography queue

                future_event_list.append({'Event Type': 'DP','id': customer['id']  ,'Event Time': clock + sample_exponential(1/envparam.Photography_service)})



            if state.Length_Service_Expert1 == system.num_filing_completing_workers:
                state.Length_Queue_Filing += 1
                state.waiting_Queue_Filing.append({'id': current_event['id']})

            else:   # if the queue was not empty get one of them and set him to busy
                state.Length_Service_Expert1 += 1 # decrease the length of photography queue
                future_event_list.append({'Event Type': 'DF','id':current_event['id'], 'Event Time': clock + sample_triangular(
                    envparam.Filling_the_case_min,envparam.Filling_the_case_max,envparam.Filling_the_case_mode)}) # departure filing event
        elif Event_Type == 'DF':
            # this is for departure of filing the case
            if state.Length_Queue_Complete_the_case == 0: # if we had departure fisrt check the complete queue
                # then if it was empty check the filing queue due to the priority
                if state.Length_Queue_Filing == 0: # if we had departure fisrt check the complete queue
                    state.Length_Service_Expert1 -= 1

                else:# if we had departure fisrt check the complete queue
                # then if it was empty check the filing queue due to the priority

                    state.Length_Queue_Filing -= 1 # decrease the length of photography queue
                    customer = state.waiting_Queue_Filing.pop(0)  # get the first customer in the queue
                    future_event_list.append({'Event Type': 'DF','id': customer['id'], 'Event Time': clock + sample_triangular(
                    envparam.Filling_the_case_min,envparam.Filling_the_case_max,envparam.Filling_the_case_mode)}) # departure filing event
                pass
            else:# if we had departure fisrt check the complete queue
                # then if it was empty check the filing queue due to the priority

                state.Length_Queue_Complete_the_case -= 1
                customer = state.waiting_Queue_Complete_the_case.pop(0) # get the first customer in the queue
                future_event_list.append({'Event Type': 'DC','id': customer['id'] ,'Event Time': clock + sample_triangular(
                    envparam.Case_completion_min,envparam.Case_completion_max,envparam.Case_completion_mode)}) # departure complete event

            if state.Length_Service_Expert2 == system.num_expert_workers: # if the expert part had idle worker let the pair in else move it to queue and add its id to compute the statistics
                state.Length_Queue_Expert += 1
                if current_event['id'] in handler.arivingEL.keys():
                    handler.arivingEL2[current_event['id']] = clock # add the time of arival of customer to the dictionary of arival time
                else:# if the expert part had idle worker let the pair in else move it to queue and add its id to compute the statistics
                    handler.arivingEL[current_event['id']] = clock
                r = random.random()
                complaint = 1 if r < 0.1 else 0# set the value if it wants to submit complaint
                state.waiting_Queue_Expert.append({'id':current_event['id'],'complaint':complaint}) # add the customer to the queue

            else:
                state.Length_Service_Expert2 += 1 # decrease the length of photography queue
                r = random.random()
                complaint = 1 if r < 0.1 else 0# set the value if it wants to submit complaint
                future_event_list.append(
                    {'Event Type': 'DE', 'complaint': complaint, 'id': current_event['id'], 'Event Time': clock + sample_exponential(1/envparam.Expert_service)})

        elif Event_Type == 'DC':# this is for departure of completing the case
            if current_event['id'] >  last_id_inside:# this is for finding the last person who was inside the system
                last_id_inside = current_event['id']
            handler.depart_time[current_event['id']] = clock # add the time of departure of customer to the dictionary of departure time
            # updating the sum of remaing time each person has this is actually shows each person epend how much time in the system
            handler.update_sum_remaining_time(handler.depart_time[current_event['id']] - handler.arrive_time[current_event['id']])

            if state.Length_Queue_Complete_the_case == 0:# if no one was in the queue of completing check the filing queue
                # due to the priority and if so set one worke to idle
                if state.Length_Queue_Filing == 0: # if no one was in the queue of completing check the filing queue
                    state.Length_Service_Expert1 -= 1

                else:

                    state.Length_Queue_Filing -= 1 # decrease the length of Filing queue
                    customer = state.waiting_Queue_Filing.pop(0) # get the first customer in the queue
                    future_event_list.append(
                        {'Event Type': 'DF', 'id': customer['id'], 'Event Time': clock + sample_triangular(
                    envparam.Filling_the_case_min,envparam.Filling_the_case_max,envparam.Filling_the_case_mode)}) # departure filing event
                pass
            else:
                state.Length_Queue_Complete_the_case -= 1 # decrease the length of completing queue
                customer = state.waiting_Queue_Complete_the_case.pop(0)
                future_event_list.append(
                    {'Event Type': 'DC', 'id': customer['id'], 'Event Time': clock + sample_triangular(
                    envparam.Case_completion_min,envparam.Case_completion_max,envparam.Case_completion_mode)})

            if clock < 600:# if the hour passed 600 make a Is end event to check wether there is some one in the system or not
                pass
            else:
                if state.Length_Service_Expert1 == 0:# this actually checks that
                    future_event_list.append({'Event Type': 'ISEND', 'Event Time': clock}) # if there is no one in the system make a Is end event to check wether there is some one in the system or not
                    pass
                else:
                    pass
            pass
        elif Event_Type == 'DE':
            # this evnnt handling is for departure of expert
            if state.Length_Queue_Expert == 0: # if no one were in the queue set one of them to idle
                state.Length_Service_Expert2 -= 1   # decrease the length of expert queue

            else:# else get from the queue
                state.Length_Queue_Expert -= 1

                customer = state.waiting_Queue_Expert.pop(0) # get the first customer in the queue
                # update the ids departed the queue to be used
                if customer['id'] in handler.departEL.keys():

                    handler.departEL2[customer['id']] = clock
                    handler.update_sum_max_EL(handler.departEL2[customer['id']]-handler.arivingEL2[customer['id']])
                else:
                    #this part is for the sake of that the a customer can be in the queue of expert center more than one time some we are handleing that with another
                    # dictionary to halp make the statistics be correct
                    handler.departEL[customer['id']] = clock
                    handler.update_sum_max_EL(handler.departEL[customer['id']]-handler.arivingEL[customer['id']]) # update the sum of max EL

                future_event_list.append({'Event Type': 'DE','id': customer['id'], 'complaint': customer['complaint'], 'Event Time': clock + sample_exponential(1/envparam.Expert_service)})

            if current_event['complaint'] == 0:# if the customer wants to submit complaint and the worker wasnt busy send it
                # in else sent it to the queu and update the dictionary of ariving time
                if state.Length_Service_Expert1 == system.num_filing_completing_workers:
                    state.Length_Queue_Complete_the_case += 1 # increase the length of completing queue
                    state.waiting_Queue_Complete_the_case.append({'id':current_event['id']}) # add the customer to the queue


                else:
                    state.Length_Service_Expert1 += 1 # decrease the length of filing queue
                    future_event_list.append({'Event Type': 'DC','id':current_event['id'], 'Event Time': clock + sample_triangular(
                    envparam.Case_completion_min,envparam.Case_completion_max,envparam.Case_completion_mode)}) # departure complete event



            else:# else get the back to the previous part and do the same if the worker was busy ...
                if state.Length_Service_Expert3 == system.num_submiting_complaint_workers:
                    handler.arivingSCL[current_event['id']] = clock # update the dictionary of ariving time
                    state.Length_Queue_Submitting_Complaint += 1 # increase the length of submitting queue
                    state.waiting_Queue_Submitting_Complaint.append({'id': current_event['id']}) # add the customer to the queue
                else:
                    state.Length_Service_Expert3 += 1 # decrease the length of submitting queue
                    future_event_list.append({'Event Type': 'DSC', 'id': current_event['id'],
                                              'Event Time': clock + sample_exponential(1 / envparam.Complaint_service)}) # departure submiting event


            pass
        elif Event_Type == 'DSC':
            # to handle the submiting complement part
            if current_event['id'] in handler.alone_cars:
                handler.alone_submited_complaint += 1 # update the number of alone cars
            state.noSubmitComplaint += 1 # update the number of no submiting complaint
            if state.Length_Queue_Submitting_Complaint == 0:
                state.Length_Service_Expert3 -= 1
                pass
            else:

                state.Length_Queue_Submitting_Complaint -= 1 # decrease the length of submitting queue
                customer = state.waiting_Queue_Submitting_Complaint.pop(0) # get the first customer in the queue
                handler.departSCL[customer['id']] = clock
                # this is for updating the SCl max and mean time in queue
                handler.update_sum_max_SCL(handler.departSCL[customer['id']]-handler.arivingSCL[customer['id']])
                future_event_list.append({'Event Type': 'DSC', 'id': customer['id'],'Event Time': clock + sample_exponential(1/envparam.Complaint_service)})
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
                future_event_list.append({'Event Type': 'DE','complaint': 0,'id': current_event['id'], 'Event Time': clock + sample_exponential(1/envparam.Expert_service)})
                pass

        elif Event_Type == 'PA':
            # if second car arrive try to find its corresponding car and join it
            if current_event['id'] not in state.alone_cars_in_parking_id:
                for car in state.waiting_Queue_OutSide:# if its pair was in outside queue
                    if car['id'] == current_event['id']:
                        car['alone'] = 0
                        break


            else:# if its pair was inside

                state.alone_cars_in_parking_id.remove(current_event['id']) # remove it from the alone cars in parking


                for car in state.waiting_Waiting_Parking: # make its aloneness atribute to false
                    if car['id'] == current_event['id']:
                        handler.update_waiting_parking(state) # update the waiting parking max and mean time
                        state.waiting_Waiting_Parking.remove(car) # remove it from the waiting parking queue
                        state.Length_Waiting_Parking -= 1
                        break

                if state.Length_Service_Photographer == system.num_photography_workers:
                    # if photographers werent idle let them in the queue
                    if state.Length_Queue_Photography == system.max_photography_queue_size: # if the queue was full


                        state.Length_Queue_Parking += 1
                        # add the id to find the statistics
                        state.waiting_Queue_Parking.append({'id':current_event['id']})

                    else:# if there was a idle photographer let the pair in
                        handler.arivingPhQ[current_event['id']] = clock
                        state.Length_Queue_Photography += 1 # increase the length of photography queue

                        state.waiting_Queue_Photography.append({'id':current_event['id']})

                else:
                    state.Length_Service_Photographer += 1
                    future_event_list.append({'Event Type': 'DP','id': current_event['id'], 'Event Time': clock + sample_exponential(1/envparam.Photography_service)})

        elif Event_Type == 'OIN':# entering a car from outside queue to inside
            if clock < 600:
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
                        handler.update_waiting_parking(state) # update the waiting parking statistics
                        state.Length_Waiting_Parking += 1 # increase the length of waiting parking
                        state.waiting_Waiting_Parking.append({'id':customer['id'],'alone':1})


                        state.alone_cars_in_parking_id.append(customer['id']) # add it to the alone cars in parking

                        future_event_list.append({'Event Type': 'OIN','Event Time': clock })

                else:
                    pass
            else:
                # make the outside queue empty after hour 6
                for pair in state.waiting_Queue_OutSide:
                    handler.departOQ[pair['id']] = 600

                state.Length_Queue_OutSide = 0 # make the outside queue empty

                state.waiting_Queue_OutSide.clear() # clear the outside queue

        elif Event_Type == 'ISEND':# checks wether the the center is empty and simulation is done
            if state.Length_Waiting_Parking == 0:
                if state.Length_Service_Photographer == 0:
                    if state.Length_Service_Expert2 == 0: # if all the queues were empty and all the workers were idle stop the simulation
                        if state.Length_Service_Expert3 == 0:


                            running = False # if all the queues were empty and all the workers were idle stop the simulation
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
            pass

        # removes from the queue and go to next step
        future_event_list.remove(current_event) # remove the current event from the fel
        sorted_fel = sorted(future_event_list, key=lambda x: x['Event Time']) # sort the fel

        if outputExcel:  # this is for outputing and excel file if it was selected
            excelsaver.add_row_df(
                [i, current_event['Event Time'], current_event['Event Type'], a, state.Length_Service_Photographer,
                 state.Length_Service_Expert1,
                 state.Length_Service_Expert2, state.Length_Service_Expert3,
                 state.Length_Queue_Parking, state.Length_Queue_OutSide, state.Length_Queue_Photography,
                 state.Length_Queue_Filing,
                 state.Length_Queue_Complete_the_case, state.Length_Queue_Expert,
                 state.Length_Queue_Submitting_Complaint, state.Length_Waiting_Parking, handler.SPhL, handler.SOL,
                 handler.SSCL, handler.SEL,
                 handler.EFQT, handler.EWPT, handler.MPhL, handler.MOL, handler.MSCL, handler.MEL, handler.SPhCenter,
                 handler.SFilingCenter
                    , handler.SExpertCenter, handler.SComplaintCenter, handler.sum_Time_phQ, handler.sum_Time_OQ,
                 handler.sum_Time_SCL, handler.sum_Time_EL,
                 handler.max_Time_PhQ, handler.max_Time_OQ, handler.max_Time_SCL, handler.max_Time_EL, sorted_fel]) # add the row to the excel file

        i += 1

    #return to get the out puts
    return handler.print_outputs(clock,last_id_inside, id, state)

    print('done')
def sample_exponential(lambda_val):
    """this is a function to sample from an exponential distribution with
    lambda: lambda_val using uniform value """
    # using the inverse method finds generate random variable
    r = random.random()
    return (-1/lambda_val)*math.log((1-r),math.e)

def sample_triangular(min, max, mod):
    """this is a function to sample from a triangular distribution with
        mod, min and max using uniform distribution """

    r = random.random()
    threshold = (mod - min)/(max - min) # find the threshold
    if r < threshold:
        return math.sqrt(r*(max-min)*(mod-min)) + min # find the value using the inverse method
    else:
        return max - math.sqrt((1-r)*(max-min)*(max-mod)) # find the value using the inverse method

def arrival_rate(weather_condition, time, dataset):
    """ this is a function to find the arrival rate using weather condition and time of the
    day from the arrival rate data set"""

    hour = time/60 + 8 # convert the time to hour
    w = 0 if weather_condition == 'rainy' else 1 # find the weather condition
    times = [8, 10, 13, 15]
    group = -1
    #reads from the file and choose the distributiion
    for t in times:
        if hour >= t:
            group += 1
        else:
            break
    return dataset.iloc[w,group+1]

def convert_to_hour(time):
    #this function converts minutes to hour as the time of simulation
    return 8 + time/60





statutil = statisticalUtils.statistics() # create an object of statistical utils


def runsimul(noreplication):
    """ this function useed to run simulation for a value asigned to it as the number of replication """
    for i in range(noreplication): # run the simulation for the number of replication
        print(f'replication {i + 1}')
        l = simulation(False)
        statutil.add_static(l) # add the results to the statistical utils

        data = statutil.find_statistic() # find the statistics
    return data


getExcel = False # this is for getting the excel file

num = 20
noreplication = 1

if not getExcel:
    # this is for getting the resullts
    for j in range(num):
        print(f'num {j + 1}')
        data = runsimul(noreplication) # run the simulation
        statutil.add_for_confidence_interval(data) # add the results to the statistical utils
    statutil.compute_confidence_interval() # find the confidence interval
else:
    #this is for getting the excel
    excelSaver = excelOutput.ExcelOutput()
    for i in range(30):
        simulation(True,excelSaver) # run the simulation
        excelSaver.add_empty_row()
        excelSaver.add_empty_row() # add empty rows to the excel file
    excelSaver.save_df() # save the excel file