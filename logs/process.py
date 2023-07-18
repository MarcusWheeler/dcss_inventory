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
    
    def set_up_lists(self):
        with open(self.logs_path + 'terminated_logs.txt','r') as f:
            lines = f.readlines()
            for entry in lines:
                if "Final Reward" in entry:
                    #print(entry.split(":")[1].split(" ")[2].split("\n")[0])
                    self.list_rewards.append(float(entry.split(":")[1].split(" ")[2].split("\n")[0]))
                if "Final AC" in entry:
                    #print(entry.split(":")[1].split(" ")[2].split("\n")[0])
                    self.list_ac.append(int(entry.split(":")[1].split(" ")[2].split("\n")[0]))
                if "Final EV" in entry:
                    #print(entry.split(":")[1].split(" ")[2].split("\n")[0])
                    self.list_ev.append(int(entry.split(":")[1].split(" ")[2].split("\n")[0]))
                if "Final SH" in entry:
                    #print(entry.split(":")[1].split(" ")[2].split("\n")[0])
                    self.list_sh.append(int(entry.split(":")[1].split(" ")[2].split("\n")[0]))
                if "Final ENC" in entry:
                    #print(entry.split(":")[1].split(" ")[2].split("\n")[0])
                    self.list_enc.append(int(entry.split(":")[1].split(" ")[2].split("\n")[0]))
                if "Final ATT" in entry:
                    #print(entry.split(":")[1].split(" ")[2].split("\n")[0])
                    self.list_att.append(int(entry.split(":")[1].split(" ")[2].split("\n")[0]))
                if "Final ATTSP" in entry:
                    #print(entry.split(":")[1].split(" ")[2].split("\n")[0])
                    self.list_attsp.append(int(entry.split(":")[1].split(" ")[2].split("\n")[0]))

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
        fig1, ax1 = plt.subplots()
        self.plot_list(fig1, ax1, self.list_rewards, "Rewards", self.logs_path + "rewards.png")

        fig2, ax2 = plt.subplots()
        self.plot_list(fig2, ax2, self.list_ac, "AC", self.logs_path + "ac.png")

        fig3, ax3 = plt.subplots()
        self.plot_list(fig3, ax3, self.list_ev, "EV", self.logs_path + "ev.png")

        fig4, ax4 = plt.subplots()
        self.plot_list(fig4, ax4, self.list_sh, "SH", self.logs_path + "sh.png")

        fig5, ax5 = plt.subplots()
        self.plot_list(fig5, ax5, self.list_enc, "ENC", self.logs_path + "enc.png")

        fig6, ax6 = plt.subplots()
        self.plot_list(fig6, ax6, self.list_att, "ATT", self.logs_path + "att.png")

        fig7, ax7 = plt.subplots()
        self.plot_list(fig7, ax7, self.list_attsp, "ATTSP", self.logs_path + "attsp.png")
        