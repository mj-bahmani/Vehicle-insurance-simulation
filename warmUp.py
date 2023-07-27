import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

class WarmUP:
    def __init__(self, num):
        """ this class is for calculating the statistics of the simulation and save them in a dictionary so we can use them later
         this is especially used for finding the warmup period and for obtainig that we use the following variables:"""
        self.warmup_Phq = [[] for i in range(num)] # this is used to store photography mean wating time in each simulation
        self.warmup_Oq = [[] for i in range(num)] # this is used to store outside mean wating time in each simulation
        self.warmup_fq = [[] for i in range(num)] # this is used to store filing mean wating time in each simulation
        self.warmup_eq = [[] for i in range(num)] # this is used to store expert mean wating time in each simulation
        self.warmup_cq = [[] for i in range(num)] # this is used to store complaint mean wating time in each simulation
        self.warmup_scq = [[] for i in range(num)] # this is used to store submiting complaint mean wating time in each repeat

        self.previous_Phq = 0
        self.previous_Oq = 0
        self.previous_fq = 0
        self.previous_cq = 0
        self.previous_scq = 0
        self.previous_eq = 0


        self.mean_complete_the_case_waiting_time = [] # this is used to store complete the case mean wating time in each replication
        self.mean_filing_the_case_waiting_time = [] # this is used to store filing the case mean wating time in each replication
        self.max_expert_queue_length = [] # this is used to store expert max queue length in each replication
        self.mean_expert_waiting_time = [] # this is used to store expert mean wating time in each replication
        self.mean_photography_waiting_time = [] # this is used to store photography mean wating time in each replication
        self.mean_whole_system_remain_time = [] # this is used to store whole system mean wating time in each replication


    def res_2_numpy(self):
        """ this function is used to convert the list of list to numpy array so we can use them in the next step"""
        self.warmup_Phq1 = np.array(self.warmup_Phq)
        self.warmup_Oq1 = np.array(self.warmup_Oq)
        self.warmup_fq1 = np.array(self.warmup_fq)
        self.warmup_eq1 = np.array(self.warmup_eq)
        self.warmup_cq1 = np.array(self.warmup_cq)
        self.warmup_scq1 = np.array(self.warmup_scq)

    def cal_mean(self):
        """ this function is used to calculate the mean of the each waiting time"""
        self.mean_Phq = np.mean(self.warmup_Phq1, axis=0)
        self.mean_Oq = np.mean(self.warmup_Oq1, axis=0)
        self.mean_fq = np.mean(self.warmup_fq1, axis=0)
        self.mean_eq = np.mean(self.warmup_eq1, axis=0)
        self.mean_cq = np.mean(self.warmup_cq1, axis=0)
        self.mean_scq = np.mean(self.warmup_scq1, axis=0)


    def smoother(self,kernel_size, array):
        """ this function is used to smooth the data using moving average"""
        n = array.shape[0]
        array1 = array.tolist()
        output_list = []
        for i in range(n):
            output_list.append(sum(array1[max(i - kernel_size // 2, 2 * i - n + 1, 0):min(i + kernel_size // 2 + 1, 2 * i + 1, n)]) / (
                    min(i + kernel_size // 2, 2 * i, n - 1) - max(i - kernel_size // 2, 2 * i - n + 1, 0) + 1))
        return output_list
    def draw_chart(self, kernel_size):
        """ this function is used to draw the chart of the mean of the waiting time"""
        plt.figure(figsize=(25, 7))
        x = np.arange(0, self.warmup_Phq1.shape[1])
        plt.plot(x, self.mean_Phq, label='mean Phq',linewidth=3.0, color='red')
        smoothed = self.smoother(kernel_size, self.mean_Phq) # find the moving average
        plt.plot(x, smoothed, label='mean Phq',linewidth=3.0, color='k',)
        plt.legend(['avg across replication', 'moving average'],fontsize = 15)
        plt.title('mean length of Photography queue',fontsize = 30)
        plt.xlabel("frame number",fontsize = 20)
        plt.ylabel("length of Photography queue ",fontsize = 20)
        plt.show()

        plt.figure(figsize=(25, 7))
        smoothed = self.smoother(kernel_size, self.mean_Oq) # find the moving average
        plt.plot(x, self.mean_Oq, label='mean Oq',linewidth=3.0, color='red')
        plt.plot(x, smoothed, label='mean Oq',linewidth=3.0,color='k')
        plt.legend(['avg across replication', 'moving average'],fontsize = 15)
        plt.title('mean length of Outside queue',fontsize = 30)
        plt.xlabel("frame number",fontsize = 20)
        plt.ylabel("length of Outside queue ",fontsize = 20)
        plt.show()

        plt.figure(figsize=(25, 7))
        smoothed = self.smoother(kernel_size, self.mean_fq) # find the moving average
        plt.plot(x, self.mean_fq, label='mean fq',linewidth=3.0,color='red')
        plt.plot(x, smoothed, label='mean fq',linewidth=3.0,color='k')
        print(self.mean_fq)
        print(smoothed)
        plt.legend(['avg across replication', 'moving average'],fontsize = 15)
        plt.title('mean length of filing the case queue',fontsize = 30)
        plt.xlabel("frame number",fontsize = 20)
        plt.ylabel("length of filing the case queue ",fontsize = 20)

        plt.show()


        plt.figure(figsize=(25, 7))
        smoothed = self.smoother(kernel_size, self.mean_eq) # find the moving average
        plt.plot(x, self.mean_eq, label='mean eq',linewidth=3,color='red')
        plt.plot(x, smoothed, label='mean eq',linewidth=3,color='k')
        # print(self.mean_eq)
        # print(smoothed)
        plt.legend(['avg across replication', 'moving average'],fontsize = 15)
        plt.title('mean length of Expert queue',fontsize = 30)
        plt.xlabel("frame number",fontsize = 20)
        plt.ylabel("length of Expert queue ",fontsize = 20)
        plt.show()

        plt.figure(figsize=(25, 7))
        smoothed = self.smoother(kernel_size, self.mean_cq) # find the moving average
        plt.plot(x, self.mean_cq, label='mean cq',linewidth=3.0,color='red')
        plt.plot(x, smoothed, label='mean cq',linewidth=3.0,color='k')
        plt.legend(['avg across replication', 'moving average'],fontsize = 15)
        plt.title('mean length of complete the case queue',fontsize = 30)
        plt.xlabel("frame number",fontsize = 20)
        plt.ylabel("length of complete the case queue ",fontsize = 20)
        plt.show()

        plt.figure(figsize=(25, 7))
        smoothed = self.smoother(kernel_size, self.mean_scq) # find the moving average
        plt.plot(x, self.mean_scq, label='mean scq',linewidth=3.0,color='red')
        plt.plot(x, smoothed, label='mean scq',linewidth=3.0 ,color='k')
        plt.legend(['avg across replication', 'moving average'],fontsize = 15)
        plt.title('mean length of submitting the complaint queue',fontsize = 30)
        plt.xlabel("frame number",fontsize = 20)
        plt.ylabel("length of submitting the complaint queue ",fontsize = 20)
        plt.show()




    def clear_vars(self):
        """ this function is used to clear the variables"""
        self.previous_cq = 0
        self.previous_scq = 0
        self.previous_eq = 0
        self.previous_fq = 0
        self.previous_Phq = 0
        self.previous_Oq = 0

    def mean_for_waiting_times(self):
        """ this function is used to calculate the mean of the waiting times"""



        return  (sum(self.mean_filing_the_case_waiting_time)/len(self.mean_filing_the_case_waiting_time),
                 sum(self.mean_complete_the_case_waiting_time)/len(self.mean_complete_the_case_waiting_time),
                 sum(self.mean_expert_waiting_time)/len(self.mean_expert_waiting_time),sum(self.mean_photography_waiting_time)/len(self.mean_photography_waiting_time),
                 sum(self.mean_whole_system_remain_time)/len(self.mean_whole_system_remain_time), sum(self.max_expert_queue_length)/len(self.max_expert_queue_length))
