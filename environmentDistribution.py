class EnvironmentDist:
    """
    A class that encapsulates the various service time distributions in the environment.
    """

    def __init__(self):
        """
        Initializes parameters for various service time distributions in the environment.
        """

        # Service time for the Photography service follows Exponential distribution with lambda=6
        self.Photography_service = 6

        # Time for Single car waiting follows Exponential distribution with lambda=30
        self.Single_car_waiting = 30

        # Service time parameters for Filling the case follows Triangular distribution
        self.Filling_the_case_min = 5
        self.Filling_the_case_mode = 6
        self.Filling_the_case_max = 7

        # Service time for Expert service follows Exponential distribution with lambda=9
        self.Expert_service = 9

        # Service time parameters for Case completion follows Triangular distribution
        self.Case_completion_min = 6
        self.Case_completion_mode = 8
        self.Case_completion_max = 9

        # Service time for Complaint service follows Exponential distribution with lambda=15
        self.Complaint_service = 15



