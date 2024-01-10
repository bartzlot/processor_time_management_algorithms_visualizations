#PSWA (Priority Scheduling with Aging)
import matplotlib as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import subplots
from matplotlib.ticker import MultipleLocator

processes_list = []

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
            "start_time": 0
        }

        processes_list.append(process)

    time_quantum = int(data[3][0])
    rr_time_quantum = int(data[4][0])

    return time_quantum, rr_time_quantum

time_quantum, rr_time_quantum = collecting_data_from_file("data.txt")


def generate_results(processes_list: list):
    
    avarage_results = []
    avarage_turnaround_time = 0
    avarage_waiting_time = 0
    avarage_response_time = 0

    for process in processes_list:

        avarage_turnaround_time += process['turnaround_time']
        avarage_response_time += process['response_time']
        avarage_waiting_time += process['waiting_time']

    avarage_results.append(round(avarage_turnaround_time/len(processes_list), 2))
    avarage_results.append(round(avarage_waiting_time/len(processes_list), 2))
    avarage_results.append(round(avarage_response_time/len(processes_list), 2))
    
    return avarage_results


class PSWAisualizer:


    def __init__(self, master, data: list):
        
        self.master = master
        self.pswa_data = sorted(data, key=lambda x: (x['priority_lvl']))
        self.process_queue = []
        self.completed_processes = []
        self.current_time_unit = 0
        self.current_process_index = 0
        self.process_time_counter = []
        self.priority_lvl_counter = []


        self.whole_time = 0

        for p in self.pswa_data: self.whole_time += p['burst_time']
        for bt in data: self.process_time_counter.append(bt['burst_time'])
        for prlvl in data: self.priority_lvl_counter.append(prlvl['priority_lvl'])
        self.fig, self.ax = subplots(figsize=(50,20))
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side="left")
        self.ax.set_xlim(0, self.whole_time)
        self.ax.set_ylim(0, len(self.pswa_data))

        self.ax.hlines(list(range(1,len(self.pswa_data))), 0, self.whole_time, colors='green', linestyles='dotted')
        self.ax.xaxis.set_major_locator(MultipleLocator((self.whole_time // 25) + 1))
        self.ax.yaxis.set_major_locator(MultipleLocator(1))
        self.initialize_counters()
        self.canvas.draw()
        self.update_chart()


    def update_chart(self):

        if self.current_time_unit <= self.whole_time:

            self.pswa_data = sorted(self.pswa_data, key=lambda x: (x['priority_lvl'], x['burst_time']))

            for process in self.pswa_data:

                if process['burst_time'] == 0: continue

                if process['start_time'] == 0:

                    process['start_time'] = self.current_time_unit
                    process['response_time'] = process['start_time'] - process['arrival_time']

                    if process['response_time'] < 0:
                        process ['response_time'] = 0

                process['burst_time'] = process['burst_time'] - 1
                self.ax.broken_barh([(self.current_time_unit, 1)], (process['id'] - 1, 1), 
                            facecolors=(0.5, 0.5, 0.5), edgecolor='yellow', linewidth=1)
                
                self.process_time_counter[process['id']-1] = self.process_time_counter[process['id']-1] -1
                self.draw_x_line(process['id'])
                self.update_counters(process['id'])
                self.current_process_index = process['id']

                break

            for process in self.pswa_data:

                if process['start_time'] != 0 and process['burst_time'] > 0:
                    process['waiting_time'] = self.current_time_unit - process['arrival_time'] - (process['burst_time'] - 1)
                    process['turnaround_time'] = self.current_time_unit - process['arrival_time']
            if self.current_time_unit % time_quantum == 0 and self.current_time_unit != 0:
                
                self.processes_aging(self.current_process_index)            
            
            self.current_time_unit += 1

            self.canvas.draw()

            self.master.after(50, self.update_chart)
            
        else:
            pass


    def initialize_counters(self):

        self.counter_texts = {}

        for process in self.pswa_data:

            process_id = process['id']
            self.counter_texts[process_id] = self.ax.text(0, process_id - 0.5, 
                                                        f"P{process_id}: {self.process_time_counter[process_id - 1]} - priorytet: {self.priority_lvl_counter[process_id-1]} ", 
                                                        ha='center', va='center', color="blue", fontweight='bold', fontsize=10)
            

    def update_counters(self, process_id):
        
        self.counter_texts[process_id].remove()
        self.counter_texts[process_id] = self.ax.text(0, process_id - 0.5, 
                                                        f"P{process_id}: {self.process_time_counter[process_id - 1]} - priorytet: {self.priority_lvl_counter[process_id-1]} ", 
                                                        ha='center', va='center', color="blue", fontweight='bold', fontsize=10)
        

    def processes_aging(self, current_process_id):

        for process in self.pswa_data:

            if process['priority_lvl'] != current_process_id and process['priority_lvl'] > 0:

                process['priority_lvl'] = process['priority_lvl'] - 1
                self.priority_lvl_counter[process['id']-1] = self.priority_lvl_counter[process['id']-1] - 1
            self.update_counters(process['id'])



    def draw_x_line(self, process_id):

        if self.current_process_index != process_id and self.current_process_index != 0:

            self.ax.axvline(x=self.current_time_unit, color='purple', linestyle='solid')


root = tk.Tk()
# root.attributes('-fullscreen', True)
app = PSWAisualizer(root, processes_list)
root.mainloop()

avarage_results = generate_results(processes_list)
print(avarage_results)

