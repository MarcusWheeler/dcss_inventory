import matplotlib.pyplot as plt
class Processor:
    def __init__(self, logs_path):
        self.logs_path = logs_path
        self.list_dict = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
        self.slot_dict = {0:"Reward", 1:"AC", 2:"EV", 3:"SH", 4:"ENC", 5:"ATT", 6:"ATTSP"}
        self.set_up_lists()
        
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
                        #print(entry.split(":")[1].split(" ")[2].split("\n")[0])
                        self.list_dict[key].append(float(entry.split(":")[1].split(" ")[2].split("\n")[0]))

    def plot_list(self,fig, ax, data, data_string, save_string):
        # Plot some data
        ax.plot(data, 'bo')
        
        if data_string in ["AC", "EV", "ENC", "Reward"]:
            ax.set_ylim(bottom=0, top=19*5)
        else:
            ax.set_ylim(bottom=0, top=20)
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
        