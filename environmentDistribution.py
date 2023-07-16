class EnvironmentDist:
    """
    A class that encapsulates the various service time distributions in the environment.
    """

    def __init__(self, arrival_mean,f_min, f_mod, f_max, c_min, c_mod, c_max,e, p_submit ):
        """
        Initializes parameters for various service time distributions in the environment.
        """

        self.being_alone_probability = 0
        self.submiting_complaint_probability = p_submit
        # Service time for the Photography service follows Exponential distribution with lambda=6
        self.Photography_service = 6

        # Time for Single car waiting follows Exponential distribution with lambda=30
        self.Single_car_waiting = 30
        self.arrival_mean = arrival_mean
        # Service time parameters for Filling the case follows Triangular distribution
        self.Filling_the_case_min = f_min
        self.Filling_the_case_mode = f_mod
        self.Filling_the_case_max = f_max

        # Service time for Expert service follows Exponential distribution with lambda=9
        self.Expert_service = e

        # Service time parameters for Case completion follows Triangular distribution
        self.Case_completion_min = c_min
        self.Case_completion_mode = c_mod
        self.Case_completion_max = c_max

        # Service time for Complaint service follows Exponential distribution with lambda=15
        self.Complaint_service = 15


