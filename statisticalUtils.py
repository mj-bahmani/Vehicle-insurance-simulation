import numpy as np
import scipy.stats as stats
class statistics:
    def __init__(self):
        self.remain_system = []
        self.APhL = []  # photo
        self.AOL = []  # outside
        self.ASCL = []  # submiting complaint
        self.AEL = []  # expert
        self.PEFQT = []  # filing empty time
        self.PEQPT = []  # waiting parking

        self.MPhL = []  # photo
        self.MOL = []  # outside
        self.MSCL = []  # submiting complaint
        self.MEL = []  # expert

        self.maxTimePhQ = []
        self.maxTimeOQ = []
        self.maxSCL = []
        self.maxEl = []

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
                         'PEQPT': [],
                         'APhCenter': [],
                         'AFilingCenter': [],
                         'AExpertCenter': [],
                         'AComplaintCenter': [],
                         'maxTimePhQ': [],
                         'maxTimeOQ': [],
                         'maxSCL': [],
                         'maxEl': [],
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
        self.remain_system.append(data[0])
        self.APhL.append(data[1])
        self.AOL.append(data[2])
        self.ASCL.append(data[3])
        self.AEL.append(data[4])
        self.PEFQT.append(data[5])
        self.PEQPT.append(data[6])
        self.APhCenter.append(data[7])
        self.AFilingCenter.append(data[8])
        self.AExpertCenter.append(data[9])
        self.AComplaintCenter.append(data[10])
        self.maxTimePhQ.append(data[11])
        self.maxTimeOQ.append(data[12])
        self.maxSCL.append(data[13])
        self.maxEl.append(data[14])
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
        data_dict = {
            'remain_system': np.array(self.remain_system),
            'APhL': np.array(self.APhL),
            'AOL': np.array(self.AOL),
            'ASCL': np.array(self.ASCL),
            'AEL': np.array(self.AEL),
            'PEFQT': np.array(self.PEFQT),
            'PEQPT': np.array(self.PEQPT),
            'APhCenter': np.array(self.APhCenter),
            'AFilingCenter': np.array(self.AFilingCenter),
            'AExpertCenter': np.array(self.AExpertCenter),
            'AComplaintCenter': np.array(self.AComplaintCenter),
            'maxTimePhQ': np.array(self.maxTimePhQ),
            'maxTimeOQ': np.array(self.maxTimeOQ),
            'maxSCL': np.array(self.maxSCL),
            'maxEl': np.array(self.maxEl),
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

        }
        mean_dict = {}

        for var_name, var_data in data_dict.items():
            mean = np.mean(var_data)
            mean_dict[var_name] = mean
        return mean_dict

    def add_for_confidence_interval(self,mean_dict):


        # Iterate over items in mean_dict
        for key, value in mean_dict.items():

            # Add each item to processed_data
            # (Replace 'process_value(value)' with your actual data processing)
            self.processdata[key].append(mean_dict[key])
    def compute_confidence_interval(self):
        for key, values in self.processdata.items():
            if values:  # If the list is not empty
                mean = np.mean(values)
                sem = stats.sem(values)
                ci = stats.t.interval(0.95, len(values) - 1, loc=mean, scale=sem)

                print(f"For {key}: Mean = {mean}, 95% Confidence Interval = {ci}")