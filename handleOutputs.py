
import pandas as pd

import System


class handleOutput:
    def __init__(self):
        self.arrive_time = {}
        self.depart_time = {}
        self.remainSystem = 0


        self.system = System.System()

        self.SPhL = 0  #photo
        self.SOL = 0  #outside
        self.SSCL = 0    #submiting complaint
        self.SEL = 0    #expert
        self.EFQT = 0   # filing empty time
        self.EWPT = 0  #waiting parking

        self.MPhL = 0  # photo
        self.MOL = 0  # outside
        self.MSCL = 0  # submiting complaint
        self.MEL = 0  # expert
        self.MWPL = 0  # waiting parking

        self.arivingPhQ = {}
        self.departPhQ = {}
        self.arivingOQ = {}
        self.departOQ = {}
        self.arivingSCL = {}
        self.departSCL = {}
        self.arivingEL = {}
        self.departEL = {}

        self.arivingEL2 = {}
        self.departEL2 = {}


        self.SPhCenter = 0
        self.SFilingCenter = 0
        self.SExpertCenter = 0
        self.SComplaintCenter = 0


        self.clockPhotography = 0
        self.clockOutside = 0
        self.clockSubmitting = 0
        self.clockExpert = 0
        self.clockFiling = 0
        self.clockQueueParking = 0

        self.clockService_Photographer = 0
        self.clockExpert1 = 0
        self.clockExpert2 = 0
        self.clockExpert3 = 0

        self.alone_cars = []
        self.alone_submited_complaint = 0

        self.sum_Time_phQ = 0
        self.sum_Time_OQ = 0
        self.sum_Time_SCL = 0
        self.sum_Time_EL = 0

        self.max_Time_PhQ = 0
        self.max_Time_OQ = 0
        self.max_Time_SCL = 0
        self.max_Time_EL = 0

    def update_photography_surface(self,clock,state):
        self.SPhL += (clock - self.clockPhotography) * state.Length_Queue_Photography
        self.clockPhotography = clock
        if state.Length_Queue_Photography > self.MPhL:
            self.MPhL = state.Length_Queue_Photography

    def update_outside_surface(self,clock,state):
        self.SOL += (clock - self.clockOutside) * state.Length_Queue_OutSide
        self.clockOutside = clock
        if state.Length_Queue_OutSide > self.MOL:
            self.MOL = state.Length_Queue_OutSide

    def update_submiting_surface(self,clock,state):
        self.SSCL += (clock - self.clockSubmitting) * state.Length_Queue_Submitting_Complaint
        self.clockSubmitting = clock
        if state.Length_Queue_Submitting_Complaint > self.MSCL:
            self.MSCL = state.Length_Queue_Submitting_Complaint
    def update_expert_surface(self,clock,state):
        self.SEL += (clock - self.clockExpert) * state.Length_Queue_Expert
        self.clockExpert = clock
        if state.Length_Queue_Expert > self.MEL:
            self.MEL = state.Length_Queue_Expert

    def update_filing_empty(self,clock,state):
        if state.Length_Queue_Filing == 0:
            self.EFQT += (clock - self.clockFiling)
        self.clockFiling = clock

    def update_queue_parking_empty(self,clock,state):
        if state.Length_Waiting_Parking == 0:
            self.EWPT += (clock - self.clockQueueParking)
        self.clockQueueParking = clock

    def update_Service_Photographer_surface(self,clock,state):
        self.SPhCenter += (clock - self.clockService_Photographer) * state.Length_Service_Photographer
        self.clockService_Photographer = clock
    def update_Expert1_surface(self,clock,state):
        self.SFilingCenter += (clock - self.clockExpert1) * state.Length_Service_Expert1
        self.clockExpert1 = clock
    def update_Expert2_surface(self,clock,state):
        self.SExpertCenter += (clock - self.clockExpert2) * state.Length_Service_Expert2
        self.clockExpert2 = clock
    def update_Expert3_surface(self,clock,state):
        self.SComplaintCenter += (clock - self.clockExpert3) * state.Length_Service_Expert3
        self.clockExpert3 = clock
    def update_waiting_parking(self,state):

        if state.Length_Waiting_Parking > self.MWPL:
            self.MWPL = state.Length_Waiting_Parking

    def update_sum_max_PhQ(self,time):
        self.sum_Time_phQ += time
        if time > self.max_Time_PhQ:
            self.max_Time_PhQ = time
    def update_sum_max_OQ(self,time):
        self.sum_Time_OQ += time
        if time > self.max_Time_OQ:
            self.max_Time_OQ = time
    def update_sum_max_SCL(self, time):
        self.sum_Time_SCL += time
        if time > self.max_Time_SCL:
            self.max_Time_SCL = time
    def update_sum_max_EL(self,time):
        self.sum_Time_EL += time
        if time > self.max_Time_EL:
            self.max_Time_EL = time
    def update_sum_remaining_time(self,time):
        self.remainSystem += time


    def print_outputs(self,clock,last_id,id,state):
        remainingtime = []
        for k in self.arrive_time.keys():
            if k  in self.depart_time:
                remainingtime.append(self.depart_time[k]-self.arrive_time[k])
        s = 0
        for i in remainingtime:
            s += i
        return [s/len(remainingtime),self.SPhL/clock,self.SOL / 600,self.SSCL / clock,\
            self.SEL / clock,self.EFQT / clock,self.EWPT / clock,self.SPhCenter/(self.system.num_photography_workers*clock),\
            self.SFilingCenter/(self.system.num_filing_completing_workers*clock),self.SExpertCenter/(self.system.num_expert_workers*clock),self.SComplaintCenter/(self.system.num_submiting_complaint_workers*clock),\
            self.max_Time_PhQ,self.max_Time_OQ,self.max_Time_SCL,self.max_Time_EL,self.sum_Time_phQ/(last_id + 1),self.sum_Time_OQ/(id+1),\
            self.sum_Time_SCL/(state.noSubmitComplaint),self.MPhL,self.MOL,self.MSCL,self.MEL,self.sum_Time_EL/(last_id+1),self.MWPL,self.alone_submited_complaint/(last_id+1)]
































