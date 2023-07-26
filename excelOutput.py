import pandas as pd

class ExcelOutput:
    """
    A class to manage the creation and updating of an output CSV file for a simulation project.
    """

    def __init__(self):
        """
        Initializes a pandas DataFrame with the desired column names for the simulation output.
        """
        column_names = ['Step', "Time", "Event", "id", 'Length_Service_Photographer', 'Length_Service_Expert1',
                        'Length_Service_Expert2', 'Length_Service_Expert3', 'Length_Queue_Parking',
                        'Length_Queue_OutSide','Length_Queue_Photography', 'Length_Queue_Filing',
                        'Length_Queue_Complete_the_case', 'Length_Queue_Expert', 'Length_Queue_Submitting_Complaint',
                        'Length_Waiting_Parking', 'SPHL', 'SOL', 'SSCL', 'SEL', 'EFQT', 'EWPT', 'MPhL', 'MOL',
                        'MSCL', 'MEL', 'SPhCenter', 'SFilingCenter', 'SExpertCenter', 'SComplaintCenter','sum_Time_phQ',
                        'sum_Time_OQ', 'sum_Time_SCL', 'sum_Time_EL', 'max_Time_PhQ', 'max_Time_OQ',
                        'max_Time_SCL', 'max_Time_EL', 'future event list']

        self.df = pd.DataFrame(columns=column_names) # Create a new DataFrame with the given column names


    def add_row_df(self, data):
        """
        Adds a new row to the DataFrame using the given data.

        Parameters:
        data (list): A list of simulation output data to be added as a new row.
        """
        self.df.loc[self.df.shape[0]] = data # Add a new row to the DataFrame with the given data


    def save_df(self):
        """
        Saves the current DataFrame to a CSV file named 'output.csv'.
        """
        self.df.to_csv("output.csv", index=False) # Save the DataFrame to a CSV file

    def add_empty_row(self):
        """
        Adds an empty row at the end of the DataFrame.
        """
        self.df.loc[self.df.shape[0]] = [None] * len(self.df.columns) # Add a new empty row to the DataFrame