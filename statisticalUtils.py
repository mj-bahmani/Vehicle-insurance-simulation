import numpy as np
import scipy.stats as stats
class statistics:
    def __init__(self):
        """ this class is for calculating the statistics of the simulation and save them in a dictionary so we can use them later
        in this class we use the following variables:

        """

        self.remain_system = []
        self.APhL = []  # photo
        self.AOL = []  # outside
        self.ASCL = []  # submiting complaint
        self.AEL = []  # expert
        self.PEFQT = []  # filing empty time
        self.PEWPT = []  # waiting parking

        self.MPhL = []  # photo
        self.MOL = []  # outside
        self.MSCL = []  # submiting complaint
        self.MEL = []  # expert

        self.maxTimePhQ = []
        self.maxTimeOQ = []
        self.maxTimeSCL = []
        self.maxTimeEL = []

        self.APhCenter = []
        self.AFilingCenter = []
        self.AExpertCenter = []
        self.AComplaintCenter = []
        self.mean_in_PHQ = []
        self.mean_in_outside = []
        self.mean_in_SCL = []
        self.mean_in_EL =[]
        self.MWPL = []
        self.PASC = []
        self.processdata = {
                         'remain_system': [],
                         'APhL': [],
                         'AOL': [],
                         'ASCL': [],
                         'AEL': [],
                         'PEFQT': [],
                         'PEWPT': [],
                         'APhCenter': [],
                         'AFilingCenter': [],
                         'AExpertCenter': [],
                         'AComplaintCenter': [],
                         'maxTimePhQ': [],
                         'maxTimeOQ': [],
                         'maxTimeSCL': [],
                         'maxTimeEL': [],
                         'mean_in_PHQ': [],
                         'mean_in_outside': [],
                         'mean_in_SCL': [],
                         'MPhL': [],
                         'MOL': [],
                         'MSCL': [],
                         'MEL': [],
                        'mean_in_EL':[],
                        'MWPL':[],
                        'PASC':[]
                        }
        pass
    def add_static(self,data):
        """ this function is for adding the data of the simulation to the dictionary to calculate the statistics of the simulation"""
        self.remain_system.append(data[0]) # remain system
        self.APhL.append(data[1]) # photo
        self.AOL.append(data[2])
        self.ASCL.append(data[3])
        self.AEL.append(data[4])
        self.PEFQT.append(data[5])
        self.PEWPT.append(data[6])
        self.APhCenter.append(data[7])
        self.AFilingCenter.append(data[8])
        self.AExpertCenter.append(data[9])
        self.AComplaintCenter.append(data[10])
        self.maxTimePhQ.append(data[11])
        self.maxTimeOQ.append(data[12])
        self.maxTimeSCL.append(data[13])
        self.maxTimeEL.append(data[14])
        self.mean_in_PHQ.append(data[15])
        self.mean_in_outside.append(data[16])
        self.mean_in_SCL.append(data[17])
        self.MPhL.append(data[18])
        self.MOL.append(data[19])
        self.MSCL.append(data[20])
        self.MEL.append(data[21])
        self.mean_in_EL.append(data[22])
        self.MWPL.append(data[23])
        self.PASC.append(data[24])



    def find_statistic(self):
        """ this function is for calculating the statistics of the simulation and save them in a dictionary so we can use them later"""
        data_dict = {
            'remain_system': np.array(self.remain_system),
            'APhL': np.array(self.APhL),
            'AOL': np.array(self.AOL),
            'ASCL': np.array(self.ASCL),
            'AEL': np.array(self.AEL),
            'PEFQT': np.array(self.PEFQT),
            'PEWPT': np.array(self.PEWPT),
            'APhCenter': np.array(self.APhCenter),
            'AFilingCenter': np.array(self.AFilingCenter),
            'AExpertCenter': np.array(self.AExpertCenter),
            'AComplaintCenter': np.array(self.AComplaintCenter),
            'maxTimePhQ': np.array(self.maxTimePhQ),
            'maxTimeOQ': np.array(self.maxTimeOQ),
            'maxTimeSCL': np.array(self.maxTimeSCL),
            'maxTimeEL': np.array(self.maxTimeEL),
            'mean_in_PHQ': np.array(self.mean_in_PHQ),
            'mean_in_outside': np.array(self.mean_in_outside),
            'mean_in_SCL': np.array(self.mean_in_SCL),
            'MPhL': np.array(self.MPhL),
            'MOL': np.array(self.MOL),
            'MSCL': np.array(self.MSCL),
            'MEL': np.array(self.MEL),
            'mean_in_EL': np.array(self.mean_in_EL),
            'MWPL': np.array(self.MWPL),
            'PASC': np.array(self.PASC)

        }   # Create dictionary of data
        mean_dict = {} # Create empty dictionary

        for var_name, var_data in data_dict.items(): # Loop over items in dictionary
            mean = np.mean(var_data) # Calculate mean
            mean_dict[var_name] = mean # Add to dictionary
        return mean_dict

    def add_for_confidence_interval(self,mean_dict):
        """ this function is for adding the data of the simulation to the dictionary to calculate the statistics of the simulation"""

        # Iterate over items in mean_dict
        for key, value in mean_dict.items():

            # Add each item to processed_data
            # (Replace 'process_value(value)' with your actual data processing)
            self.processdata[key].append(mean_dict[key])
    def compute_confidence_interval(self):
        """ this function is for calculating the confidence interval of the simulation and save them in a dictionary so we can use them later"""
        for key, values in self.processdata.items():
            if values:  # If the list is not empty
                mean = np.mean(values)
                sem = stats.sem(values)
                ci = stats.t.interval(0.95, len(values) - 1, loc=mean, scale=sem)

                print(f"For {key}: Mean = {mean}, 95% Confidence Interval = {ci}")