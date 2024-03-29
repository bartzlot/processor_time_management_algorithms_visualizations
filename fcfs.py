#FCFS (First-Come, First-Served)
from results_manager import ResultsManager
import matplotlib as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import subplots
from matplotlib.ticker import MultipleLocator
import pathlib

data_file_path = pathlib.Path(__file__).parent / 'data_generators' / 'cpu_scheduling_data.txt'
processes_list = []
time_quantum = 0
rr_time_quantum = 0


def collecting_data_from_file(path: str):

    data = []
    with open(path) as f:

        for line in f:
            line = line.strip()
            data.append(line.split(' '))

    process_id = 0

    for i in range(len(data[0])):

        process_id += 1

        process = {
            "id" : process_id,
            "arrival_time" : int(data[0][i]),
            "burst_time" : int(data[1][i]),
            "priority_lvl" : int(data[2][i]),
            "turnaround_time": 0,
            "waiting_time": 0,
            "response_time": 0,
            "start_time": 0,
            "completion_time": 0
        }

        processes_list.append(process)

    time_quantum = int(data[3][0])
    rr_time_quantum = int(data[4][0])


collecting_data_from_file(data_file_path)

class FCFSVisualizer:


    def __init__(self, master, data: list):
        
        self.master = master
        self.fcfs_data = sorted(data, key=lambda x: (x['arrival_time'], x['burst_time']))
        self.process_queue = []
        self.completed_processes = []
        self.current_time_unit = 0
        self.current_process_index = 0
        self.row = 0
        self.process_time = 1

        self.whole_time = 0

        for p in self.fcfs_data: self.whole_time += p['burst_time']

        self.fig, self.ax = subplots(figsize=(50,20))
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side="left")
        self.ax.set_xlim(0, self.whole_time)
        self.ax.set_ylim(0, len(self.fcfs_data))

        self.ax.hlines(list(range(1,len(self.fcfs_data))), 0, self.whole_time, colors='green', linestyles='dotted')
        self.ax.xaxis.set_major_locator(MultipleLocator((self.whole_time // 25) + 1))
        self.ax.yaxis.set_major_locator(MultipleLocator(1))
        self.canvas.draw()
        


        self.update_chart()
    

    def update_chart(self):
        
        if self.current_process_index < len(self.fcfs_data):

            current_process = self.fcfs_data[self.current_process_index]

            if current_process['start_time'] == 0 and self.current_process_index != 0:
                current_process['start_time'] = self.current_time_unit
            
            elif self.current_process_index == 0:

                current_process['start_time'] = 0

            #setting current process burst time
            if self.current_process_index == 0:

                burst_time = current_process['burst_time']

            else:

                time_sum = 0
                #summing whole time from all processes
                for process in self.fcfs_data[:self.current_process_index+1]:

                    time_sum += process['burst_time']

                burst_time = time_sum

            if self.current_time_unit < burst_time:
                
                self.ax.broken_barh([(self.current_time_unit, 1)], (self.row, 1), 
                                    facecolors=(0.5, 0.5, 0.5), edgecolor='yellow', linewidth=1)
                counter = self.ax.text(0, self.row + 0.5, f"P{current_process['id']}: {self.process_time}", 
                    ha='center', va='center', color="blue", fontweight='bold', fontsize=10)

                self.canvas.draw()  

                self.current_time_unit += 1

            else:

                self.setting_end_chart(current_process)

                current_process['completion_time'] = self.current_time_unit
                current_process['turnaround_time'] = current_process['completion_time'] - current_process['arrival_time']
                current_process['waiting_time'] = current_process['turnaround_time'] - current_process['burst_time']

                if current_process['waiting_time'] < 0:
                    current_process['waiting_time'] = 0

                self.current_process_index += 1
                self.row += 1
                self.process_time = 0

            self.process_time += 1
            self.master.after(100, self.update_chart)
            
            counter.remove()
        else:
            
            pass


    def setting_end_chart(self, current_process: dict):

        self.ax.text(0, self.row + 0.5, f"P{current_process['id']}: {self.process_time-1}", 
            ha='center', va='center', color="blue", fontweight='bold', fontsize=10)
        self.ax.axvline(x=self.current_time_unit, color='purple', linestyle='solid')
        
root = tk.Tk()
# root.attributes('-fullscreen', True)
app = FCFSVisualizer(root, processes_list)
root.mainloop()
FCFSResults = ResultsManager(processes_list, 'fcfs')