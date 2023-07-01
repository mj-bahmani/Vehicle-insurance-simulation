

class handleOutput:
    def __init__(self):
        self.arrive_time = {}
        self.depart_time = {}
        self.remainSystem = 0

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

        self.arivingPhQ = {}
        self.departPhQ = {}
        self.arivingOQ = {}
        self.departOQ = {}
        self.arivingSCL = {}
        self.departSCL = {}
        self.arivingEL = {}
        self.departEL = {}

        self.maxTimePhQ = -1
        self.maxTimeOQ = -1
        self.maxSCL = -1
        self.maxEl = -1

        self.SPhCenter = 0
        self.SFilingCenter = 0
        self.SExpertCenter = 0
        self.SComplaintCenter = 0

        self.clockPhotography = 0
        self.clockOutside = 0
        self.clockSubmitting = 0
        self.clockExpert = 0
        self.clockFiling = 0
        self.clockWaiting = 0
        self.clockService_Photographer = 0
        self.clockExpert1 = 0
        self.clockExpert2 = 0
        self.clockExpert3 = 0
    def update_photography_surface(self,clock,state):
        self.SPhL += (clock - self.clockPhotography) * state.Length_Queue_Photography
        self.clockPhotography = clock
        if state.Length_Queue_Photography > self.MPhL:
            self.MPhL = state.Length_Queue_Photography

    def update_outside_surface(self,clock,state):
        self.SOL += (clock - self.clockOutside) * state.Length_Queue_OutSide
        self.clockOutside = clock
        if state.Length_Queue_OutSide > self.MPhL:
            self.MOL = state.Length_Queue_OutSide

    def update_submiting_surface(self,clock,state):
        self.SSCL += (clock - self.clockSubmitting) * state.Length_Queue_Submitting_Complaint
        self.clockSubmitting = clock
        if state.Length_Queue_Submitting_Complaint > self.MPhL:
            self.MSCL = state.Length_Queue_Submitting_Complaint
    def update_expert_surface(self,clock,state):
        self.SOL += (clock - self.clockExpert) * state.Length_Queue_Expert
        self.clockExpert = clock
        if state.Length_Queue_Expert > self.MPhL:
            self.MEL = state.Length_Queue_Expert

    def update_filing_empty(self,clock,state):
        if state.Length_Queue_Filing == 0:
            self.SOL += (clock - self.clockFiling)
        self.clockFiling = clock

    def update_waiting_empty(self,clock,state):
        if state.Length_Waiting_Parking == 0:
            self.SOL += (clock - self.clockWaiting)
        self.clockWaiting = clock

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














