
import pandas as pd

import System


class handleOutput:
    def __init__(self,sys):
        self.arrive_time = {}  # this is a dictionary that contains the time of arriving to system
        self.depart_time = {}  # this is a dictionary that contains the time of departing from system
        self.remainSystem = 0

        self.system = sys  # this is a class that contains the system variables
        self.SFL = 0
        self.SCL = 0
        self.SPhL = 0  # the surface under photography length based on time
        self.SOL = 0  # the surface under outside length based on time
        self.SSCL = 0  # the surface under submiting complaint length based on time
        self.SEL = 0  # the surface under expert length based on time
        self.EFQT = 0  # filing empty time surface
        self.EWPT = 0  # waiting parking empty time surface

        self.MPhL = 0  # max length of photograaphy
        self.MOL = 0  # max length of outside
        self.MSCL = 0  # max length of submiting complaint
        self.MEL = 0  # max length of expert
        self.MWPL = 0  # max length of waiting parking
        # these are the variables described in the first part
        self.arivingPhQ = {}  # this is the dictionary describing the time each customer entered the photography queue
        self.departPhQ = {}  # this is the dictionary describing the time each customer departed the photography queue
        self.arivingOQ = {}  # this is the dictionary describing the time each customer entered the outside queue
        self.departOQ = {}  # this is the dictionary describing the time each customer departed the outside queue
        self.arivingSCL = {}  # this is the dictionary describing the time each customer entered the submiting complaint queue
        self.departSCL = {}  # this is the dictionary describing the time each customer departed the submiting complaint queue
        self.arivingEL = {}  # this is the dictionary describing the time each customer entered the expert queue
        self.departEL = {}  # this is the dictionary describing the time each customer departed the expert queue

        self.arivingEL2 = {}  # this is the dictionary describing the time each customer entered the expert queue for some reason that a customer may come to this queue more than one time
        self.departEL2 = {}  # this is the dictionary describing the time each customer departed the expert queue for some reason that a customer may come to this queue more than one time

        self.SPhCenter = 0  # the surface under the number of busy workers in the photography center based on time
        self.SFilingCenter = 0  # the surface under the number of busy workers in the filing center based on time
        self.SExpertCenter = 0  # the surface under the number of busy workers in the expert center based on time
        self.SComplaintCenter = 0  # the surface under the number of busy workers in the complaint center based on time

        self.clockPhotography = 0  # this is used to calculate the surface it keeps the last time we compute the surface under the photography length
        self.clockOutside = 0  # this is used to calculate the surface it keeps the last time we compute the surface under the outside length
        self.clockfiling = 0  # this is used to calculate the surface it keeps the last time we compute the surface under the filing length
        self.clockcomplete = 0  # this is used to calculate the surface it keeps the last time we compute the surface under the complete length
        self.clockSubmitting = 0  # this is used to calculate the surface it keeps the last time we compute the surface under the submitting length
        self.clockExpert = 0  # this is used to calculate the surface it keeps the last time we compute the surface under the expert length
        self.clockFiling = 0  # this is used to calculate the surface it keeps the last time we compute the surface under the filing length
        self.clockQueueParking = 0  # this is used to calculate the surface it keeps the last time we compute the surface under the queue parking length

        self.clockService_Photographer = 0  # this is used to calculate the surface it keeps the last time we compute the surface under the number of busy workers in the photography center
        self.clockExpert1 = 0  # this is used to calculate the surface it keeps the last time we compute the surface under the number of busy workers in the complaint center
        self.clockExpert2 = 0  # this is used to calculate the surface it keeps the last time we compute the surface under the number of busy workers in the complaint center
        self.clockExpert3 = 0  # this is used to calculate the surface it keeps the last time we compute the surface under the number of busy workers in the complaint center

        self.alone_cars = []  # this is a list that contains the number of cars that came alone to the system
        self.alone_submited_complaint = 0  # this is a variable that contains the number of customers that came alone to the system and submited a complaint

        self.sum_Time_phQ = 0  # this is a variable that contains the sum of time that customers spent in the photography queue
        self.sum_Time_OQ = 0  # this is a variable that contains the sum of time that customers spent in the outside queue
        self.sum_Time_SCL = 0  # this is a variable that contains the sum of time that customers spent in the submiting complaint queue
        self.sum_Time_EL = 0  # this is a variable that contains the sum of time that customers spent in the expert queue

        self.max_Time_PhQ = 0  # this is a variable that contains the max of time that customers spent in the photography queue
        self.max_Time_OQ = 0  # this is a variable that contains the max of time that customers spent in the outside queue
        self.max_Time_SCL = 0  # this is a variable that contains the max of time that customers spent in the submiting complaint queue
        self.max_Time_EL = 0  # this is a variable that contains the max of time that customers spent in the expert queue


    def update_photography_surface(self,clock,state):
        """ this function is for getting the output self.MPhL  and  self.SPhL"""

        self.SPhL += (clock - self.clockPhotography) * state.Length_Queue_Photography # this is the surface under the number of customers in the photography queue
        self.clockPhotography = clock # this is the last time we compute the surface under the number of customers in the photography queue
        if state.Length_Queue_Photography > self.MPhL: # this is the maximum number of customers in the photography queue
            self.MPhL = state.Length_Queue_Photography # this is the maximum number of customers in the photography queue


    def update_outside_surface(self,clock,state):
        """ this function is for getting the output self.MOL  and self.SOL"""

        self.SOL += (clock - self.clockOutside) * state.Length_Queue_OutSide
        self.clockOutside = clock
        if state.Length_Queue_OutSide > self.MOL:
            self.MOL = state.Length_Queue_OutSide
    def update_filing_surface(self,clock,state):
        """ this function is for getting the output self.SFL  """

        self.SFL += (clock - self.clockfiling) * state.Length_Queue_Filing
        self.clockfiling = clock

    def update_complete_surface(self, clock, state):
        """ this function is for updating the output self.SCL  """

        self.SCL += (clock - self.clockcomplete) * state.Length_Queue_Complete_the_case
        self.clockcomplete = clock

    def update_submiting_surface(self,clock,state):
        """ this function is for getting the output self.MSCL and self.SSCL """

        self.SSCL += (clock - self.clockSubmitting) * state.Length_Queue_Submitting_Complaint
        self.clockSubmitting = clock
        if state.Length_Queue_Submitting_Complaint > self.MSCL:
            self.MSCL = state.Length_Queue_Submitting_Complaint
    def update_expert_surface(self,clock,state):
        """ this function is for getting the output self.SEL  and self.MEL"""

        self.SEL += (clock - self.clockExpert) * state.Length_Queue_Expert
        self.clockExpert = clock
        if state.Length_Queue_Expert > self.MEL:
            self.MEL = state.Length_Queue_Expert

    def update_filing_empty(self,clock,state):
        """ this function is for getting the output self.EFQT """

        if state.Length_Queue_Filing == 0:
            self.EFQT += (clock - self.clockFiling)
        self.clockFiling = clock

    def update_queue_parking_empty(self,clock,state):
        """ this function is for getting the output self.EWPT """

        if state.Length_Waiting_Parking == 0:
            self.EWPT += (clock - self.clockQueueParking)
        self.clockQueueParking = clock

    def update_Service_Photographer_surface(self,clock,state):
        """ this function is for getting the output self.SPhCenter """

        self.SPhCenter += (clock - self.clockService_Photographer) * state.Length_Service_Photographer
        self.clockService_Photographer = clock
    def update_Expert1_surface(self,clock,state):
        """ this function is for getting the output self.SFilingCenter """

        self.SFilingCenter += (clock - self.clockExpert1) * state.Length_Service_Expert1
        self.clockExpert1 = clock
    def update_Expert2_surface(self,clock,state):
        """ this function is for getting the output self.SExpertCenter """

        self.SExpertCenter += (clock - self.clockExpert2) * state.Length_Service_Expert2
        self.clockExpert2 = clock
    def update_Expert3_surface(self,clock,state):
        """ this function is for getting the output self.SComplaintCenter """

        self.SComplaintCenter += (clock - self.clockExpert3) * state.Length_Service_Expert3
        self.clockExpert3 = clock
    def update_waiting_parking(self,state):
        """ this function is for getting the output self.Length_Waiting_Parking and self.MWPL"""

        if state.Length_Waiting_Parking > self.MWPL:
            self.MWPL = state.Length_Waiting_Parking

    def update_sum_max_PhQ(self,time):
        """ this function is for getting the output self.sum_Time_phQ and self.max_Time_PhQ"""

        self.sum_Time_phQ += time
        if time > self.max_Time_PhQ:
            self.max_Time_PhQ = time
    def update_sum_max_OQ(self,time):
        """ this function is for getting the output self.sum_Time_OQ and self.max_Time_OQ"""

        self.sum_Time_OQ += time
        if time > self.max_Time_OQ:
            self.max_Time_OQ = time
    def update_sum_max_SCL(self, time):
        """ this function is for getting the output self.sum_Time_SCL and self.max_Time_SCL"""

        self.sum_Time_SCL += time
        if time > self.max_Time_SCL:
            self.max_Time_SCL = time
    def update_sum_max_EL(self,time):
        """ this function is for getting the output self.sum_Time_EL and self.max_Time_EL"""

        self.sum_Time_EL += time
        if time > self.max_Time_EL:
            self.max_Time_EL = time
    def update_sum_remaining_time(self,time):
        """ this function is for getting the output self.remainSystem"""
        self.remainSystem += time


    def print_outputs(self,clock,last_id,id,state):
        """ this function is for getting the output """
        remainingtime = []
        for k in self.arrive_time.keys():
            if k  in self.depart_time:
                remainingtime.append(self.depart_time[k]-self.arrive_time[k])
        s = 0
        for i in remainingtime:
            s += i

        temp =None
        try:
            temp = self.sum_Time_SCL/(state.noSubmitComplaint)
        except:
            pass

        return [s/len(remainingtime),self.SPhL/clock,self.SOL / clock,self.SSCL / clock,\
            self.SEL / clock,self.EFQT / clock,self.EWPT / clock,self.SPhCenter/(self.system.num_photography_workers*clock),\
            self.SFilingCenter/(self.system.num_filing_completing_workers*clock),self.SExpertCenter/(self.system.num_expert_workers*clock),self.SComplaintCenter/(self.system.num_submiting_complaint_workers*clock),\
            self.max_Time_PhQ,self.max_Time_OQ,self.max_Time_SCL,self.max_Time_EL,self.sum_Time_phQ/(last_id + 1),self.sum_Time_OQ/(id+1),\
            temp,self.MPhL,self.MOL,self.MSCL,self.MEL,self.sum_Time_EL/(last_id+1),self.MWPL,self.alone_submited_complaint/(last_id+1)]































