
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
        self.EQPT = 0  #waiting parking

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

        self.maxTimePhQ = -1
        self.maxTimeOQ = -1
        self.maxSCL = -1
        self.maxEl = -1

        self.SPhCenter = 0
        self.SFilingCenter = 0
        self.SExpertCenter = 0
        self.SComplaintCenter = 0

        column_names = ["Time", "Event","id", 'Length_Service_Photographer', 'Length_Service_Expert1',
                        'Length_Service_Expert2',
                        'Length_Service_Expert3', 'Length_Queue_Parking', 'Length_Queue_OutSide',
                        'Length_Queue_Photography',
                        'Length_Queue_Filing', 'Length_Queue_Complete_the_case', 'Length_Queue_Expert',
                        'Length_Queue_Submitting_Complaint', 'Length_Waiting_Parking','SPHL','SOL','SSCL','SEL','EFQT','EQPT',
                        'MPhL','MOL','MSCL','MEL','SPhCenter','SFilingCenter','SExpertCenter','SComplaintCenter','future event list']

        self.df = pd.DataFrame(columns=column_names)
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
        if state.Length_Queue_Parking == 0:
            self.EQPT += (clock - self.clockQueueParking)
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

    def add_row_df(self, data):
        self.df.loc[self.df.shape[0]] = data
    def save_df(self):
        self.df.to_csv("output.csv", index=False)
    def print_outputs(self,clock,last_id,id,state):
        remainingtime = []
        for k in self.arrive_time.keys():
            if k  in self.depart_time:
                remainingtime.append(self.depart_time[k]-self.arrive_time[k])
        s = 0
        for i in remainingtime:
            s += i



        time_in_PhQ = []
        time_in_OQ = []
        time_in_SCL = []
        time_in_El = []



        max_phQ = 0
        max_OQ = 0
        max_SCL = 0
        max_El = 0

        for k in self.arivingPhQ.keys():
            time_in_PhQ.append(self.departPhQ[k] - self.arivingPhQ[k])
            if self.departPhQ[k] - self.arivingPhQ[k]> max_phQ:
                max_phQ = self.departPhQ[k] - self.arivingPhQ[k]

        for k in self.arivingOQ.keys():
            a = self.departOQ[k] - self.arivingOQ[k]
            time_in_OQ.append(a)
            if a > max_OQ :
                max_OQ = a

        for k in self.arivingSCL.keys():
            time_in_SCL.append(self.departSCL[k] - self.arivingSCL[k])
            if self.departSCL[k] - self.arivingSCL[k]> max_SCL:
                max_SCL = self.departSCL[k] - self.arivingSCL[k]

        for k in self.arivingEL.keys():

            time_in_El.append(self.departEL[k] - self.arivingEL[k])
            if self.departEL[k] - self.arivingEL[k]> max_El:
                max_El = self.departEL[k] - self.arivingEL[k]

        for k in self.arivingEL2.keys():

            time_in_El.append(self.departEL2[k] - self.arivingEL2[k])
            if self.departEL2[k] - self.arivingEL2[k] > max_El:
                max_El = self.departEL2[k] - self.arivingEL2[k]


        sum_phQ = 0
        sum_OQ = 0
        sum_SCL = 0
        sum_El = 0


        for i in time_in_PhQ:
            sum_phQ += i
        for i in time_in_OQ:
            sum_OQ += i
        for i in time_in_SCL:
            sum_SCL += i
        for i in time_in_El:
            sum_El += i





        return [s/len(remainingtime),self.SPhL/clock,self.SOL / 600,self.SSCL / clock,\
            self.SEL / clock,self.EFQT / clock,self.EQPT / clock,self.SPhCenter/(self.system.num_photography_workers*clock),\
            self.SFilingCenter/(self.system.num_filing_completing_workers*clock),self.SExpertCenter/(self.system.num_expert_workers*clock),self.SComplaintCenter/(self.system.num_submiting_complaint_workers*clock),\
            max_phQ,max_OQ,max_SCL,max_El,sum_phQ/(last_id + 1),sum_OQ/(id+1),\
            sum_SCL/(state.noSubmitComplaint),self.MPhL,self.MOL,self.MSCL,self.MEL,sum_El/(last_id+1),self.MWPL,self.alone_submited_complaint/(last_id+1)]
































