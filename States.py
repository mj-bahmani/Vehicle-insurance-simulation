class States:

    def __init__(self,Length_Service_Photographer=0, Length_Service_Expert1=0, Length_Service_Expert2=0,
                 Length_Service_Expert3=0, Length_Queue_Parking=0, Length_Queue_OutSide=0,
                 Length_Queue_Photography=0, Length_Queue_Filing=0, Length_Queue_Complete_the_case=0,
                 Length_Queue_Expert=0, Length_Queue_Submitting_Complaint=0, Length_Waiting_Parking=0 ):
        """"
        initializing all the state variables of the Queue systems such as the length of the queue and the length of the service

        """
        self.Length_Service_Photographer = Length_Service_Photographer # the length of the service of the photographer
        self.Length_Service_Expert1 = Length_Service_Expert1 # the length of the service of the filing and completing the case
        self.Length_Service_Expert2 = Length_Service_Expert2 # the length of the service of the expert
        self.Length_Service_Expert3 = Length_Service_Expert3 # the length of the service of the submitting the complaint
        self.Length_Queue_Parking = Length_Queue_Parking # the length of the queue of the parking
        self.Length_Queue_OutSide = Length_Queue_OutSide # the length of the queue of the outside
        self.Length_Queue_Photography = Length_Queue_Photography # the length of the queue of the photography
        self.Length_Queue_Filing = Length_Queue_Filing # the length of the queue of the filing
        self.Length_Queue_Complete_the_case = Length_Queue_Complete_the_case # the length of the queue of the completing the case
        self.Length_Queue_Expert = Length_Queue_Expert # the length of the queue of the expert
        self.Length_Queue_Submitting_Complaint = Length_Queue_Submitting_Complaint # the length of the queue of the submitting the complaint
        self.Length_Waiting_Parking = Length_Waiting_Parking # the length of the waiting queue of the parking
        self.alone_cars_in_parking_id = [] # the id of the cars that are alone in the parking
        self.noSubmitComplaint = 0 # the number of the cars that  submit the complaint



        self.waiting_Queue_Parking = [] # the waiting queue of the parking
        self.waiting_Queue_OutSide = [] # the waiting queue of the outside
        self.waiting_Queue_Photography = [] # the waiting queue of the photography
        self.waiting_Queue_Filing = [] # the waiting queue of the filing
        self.waiting_Queue_Complete_the_case = [] # the waiting queue of the completing the case
        self.waiting_Queue_Expert = [] # the waiting queue of the expert
        self.waiting_Queue_Submitting_Complaint = [] # the waiting queue of the submitting the complaint
        self.waiting_Waiting_Parking = [] # the waiting queue of the waiting parking
    def __str__(self):
        return f'Length_Service_Photographer : {self.Length_Service_Photographer}, Length_Service_Expert1: {self.Length_Service_Expert1},\n' \
               f'Length_Service_Expert2 : {self.Length_Service_Expert2}, Length_Service_Expert3 : {self.Length_Service_Expert2}, Length_Queue_Parking: {self.Length_Queue_Parking}' \
               f'Length_Queue_OutSide : {self.Length_Queue_OutSide}, Length_Queue_Photography : {self.Length_Queue_Photography}\n' \
               f'Length_Queue_Filing : {self.Length_Queue_Filing}, Length_Queue_Complete_the_case : {self.Length_Queue_Complete_the_case}' \
               f'Length_Queue_Expert : {self.Length_Queue_Expert}, Length_Queue_Submitting_Complaint: {self.Length_Queue_Submitting_Complaint}\n' \
               f'Length_Waiting_Parking : {self.Length_Waiting_Parking}, alone_cars_in_parking_id: {self.alone_cars_in_parking_id} '



