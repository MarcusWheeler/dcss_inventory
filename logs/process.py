import matplotlib.pyplot as plt
class Processor:
    def __init__(self, logs_path):
    
        self.list_rewards = []
        self.list_ac = []
        self.list_ev = []
        self.list_sh = []
        self.list_enc = []
        self.list_att = []
        self.list_attsp = []
        self.logs_path = logs_path
        self.list_dict = {0:self.list_rewards, 1:self.list_ac, 2:self.list_ev, 3:self.list_sh, 4:self.list_enc, 5:self.list_att, 6:self.list_attsp}
        self.slot_dict = {0:"Rewards", 1:"AC", 2:"EV", 3:"SH", 4:"ENC", 5:"ATT", 6:"ATTSP"}
    
    def set_up_lists(self):
        with open(self.logs_path + 'terminated_logs.txt','r') as f:
            lines = f.readlines()
            for entry in lines:
                #Check our slot_dict to find out which one we're in
                for key in self.slot_dict:
                    #Add this to exclude the SK categories
                    
                    concatenated = "Final " + self.slot_dict[key]
                    #If you're in the entry, use the key on the list_dict to get the proper list
                    if concatenated in entry:
                        self.list_dict[key].append(float(entry.split(":")[1].split(" ")[2].split("\n")[0]))


    def plot_list(self,fig, ax, data, data_string, save_string):
        # Plot some data
        ax.plot(data, 'bo')

        # Set the title and labels
        ax.set_title(data_string)
        ax.set_xlabel("Trial")
        ax.set_ylabel(data_string)

        # Show the plot
        plt.savefig(save_string)
        

    def plot_all(self):    
        # Create a figure and axes
        for i in range(7):
            fig1, ax1 = plt.subplots()
            self.plot_list(fig1, ax1, self.list_dict[i], self.slot_dict[i], self.logs_path + self.slot_dict[i] + ".png")
        