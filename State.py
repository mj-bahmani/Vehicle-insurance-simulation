class state:

    def __init__(self,Length_Service_Photographer=0, Length_Service_Expert1=0, Length_Service_Expert2=0,
                 Length_Service_Expert3=0, Length_Queue_Parking=0, Length_Queue_OutSide=0,
                 Length_Queue_Photography=0, Length_Queue_Filing=0, Length_Queue_Complete_the_case=0,
                 Length_Queue_Expert=0, Length_Queue_Submitting_Complaint=0, Length_Waiting_Parking=0 ):
        """"
        initializing all the state variables of the Queue system

        """
        self.Length_Service_Photographer = Length_Service_Photographer
        self.Length_Service_Expert1 = Length_Service_Expert1
        self.Length_Service_Expert2 = Length_Service_Expert2
        self.Length_Service_Expert3 = Length_Service_Expert3
        self.Length_Queue_Parking = Length_Queue_Parking
        self.Length_Queue_OutSide = Length_Queue_OutSide
        self.Length_Queue_Photography = Length_Queue_Photography
        self.Length_Queue_Filing = Length_Queue_Filing
        self.Length_Queue_Complete_the_case = Length_Queue_Complete_the_case
        self.Length_Queue_Expert = Length_Queue_Expert
        self.Length_Queue_Submitting_Complaint = Length_Queue_Submitting_Complaint
        self.Length_Waiting_Parking = Length_Waiting_Parking
        self.alone_cars_in_parking_id = []


        self.waiting_Queue_Parking = []
        self.waiting_Queue_OutSide = []
        self.waiting_Queue_Photography = []
        self.waiting_Queue_Filing = []
        self.waiting_Queue_Complete_the_case = []
        self.waiting_Queue_Expert = []
        self.waiting_Queue_Submitting_Complaint = []
        self.waiting_Waiting_Parking = []



