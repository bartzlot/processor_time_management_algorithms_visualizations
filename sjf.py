import matplotlib as plt
from results_manager import ResultsManager
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import subplots
from matplotlib.ticker import MultipleLocator

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


collecting_data_from_file("data2.txt")


class SJFVisualizer:


    def __init__(self, master, data: list):
        
        self.master = master
        self.sjf_data = sorted(data, key=lambda x: x['arrival_time'])
        self.current_time_unit = 0
        self.process_time_counter = []
        self.last_process_id = 0
        self.burst_times = []
        self.whole_time = 0

        for p in self.sjf_data: self.whole_time += p['burst_time']

        for bt in self.sjf_data: 
            self.process_time_counter.append(bt['burst_time'])
            self.burst_times.append(bt['burst_time'])

        self.fig, self.ax = subplots(figsize=(50,20))
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side="left")
        self.ax.set_xlim(0, self.whole_time)
        self.ax.set_ylim(0, len(self.sjf_data))

        self.ax.hlines(list(range(1,len(self.sjf_data))), 0, self.whole_time, colors='green', linestyles='dotted')
        self.ax.xaxis.set_major_locator(MultipleLocator((self.whole_time // 25) + 1))
        self.ax.yaxis.set_major_locator(MultipleLocator(1))
        self.canvas.draw()
        self.initialize_counters()
        self.update_chart()


    def update_chart(self):
        
        if self.current_time_unit <= self.whole_time:

            minimum_burst_time_process_index = None
            minumim_burst_time = float('inf')
            available_processes = self.finding_avaliable_processes()

        for index in available_processes:

            process = self.sjf_data[index]

            if process['burst_time'] > 0 and process['burst_time'] < minumim_burst_time:
                
                minimum_burst_time_process_index = index
                minumim_burst_time = process['burst_time']
                

        if minimum_burst_time_process_index is not None:

            selected_process = self.sjf_data[minimum_burst_time_process_index]
            self.update_counters(minimum_burst_time_process_index)
            

            if selected_process['start_time'] == 0 and minimum_burst_time_process_index != 0:
                selected_process['start_time'] = self.current_time_unit
            
            elif self.current_time_unit == 0:

                selected_process['start_time'] = 0

            selected_process['burst_time'] -= 1
            self.ax.broken_barh([(self.current_time_unit, 1)], (minimum_burst_time_process_index, 1), 
                                facecolors=(0.5, 0.5, 0.5), edgecolor='yellow', linewidth=1)
            self.process_time_counter[minimum_burst_time_process_index] -= 1
            self.canvas.draw()

            if self.last_process_id != minimum_burst_time_process_index:
                self.last_process_id = minimum_burst_time_process_index
                self.draw_x_line()
                
            self.current_time_unit += 1

            if selected_process['burst_time'] == 0:
                selected_process['completion_time'] = self.current_time_unit
                selected_process['turnaround_time'] = selected_process['completion_time'] - selected_process['arrival_time']
                selected_process['waiting_time'] = selected_process['start_time'] - selected_process['arrival_time']
                selected_process['response_time'] = selected_process['completion_time'] - selected_process['arrival_time']

            self.master.after(1, self.update_chart)

        else:
            pass


    def initialize_counters(self):

        self.counter_texts = {}

        for process in self.sjf_data:

            process_id = process['id']
            self.counter_texts[process_id] = self.ax.text(0, process_id - 0.5, 
                                                        f"P{process_id}: {self.process_time_counter[process_id - 1]} ", 
                                                        ha='center', va='center', color="blue", fontweight='bold', fontsize=10)

    def update_counters(self, process_index):

        process_id = self.sjf_data[process_index]['id']
        self.counter_texts[process_id].remove()
        self.counter_texts[process_id] = self.ax.text(0, process_index + 0.5, 
                                                    f"P{process_id}: {self.process_time_counter[process_index]-1} ", 
                                                    ha='center', va='center', color="blue", fontweight='bold', fontsize=10)

    def draw_x_line(self):

        self.ax.axvline(x=self.current_time_unit, color='purple', linestyle='solid')


    def finding_avaliable_processes(self):

        available_processes = []

        for i in range(len(self.sjf_data)):

            if self.sjf_data[i]['arrival_time'] <= self.current_time_unit and self.sjf_data[i]['burst_time'] > 0:
 
                if i not in available_processes:
                    available_processes.append(i)

        return available_processes


    def count_metrix(self):
        print(self.burst_times)
        for process in enumerate(self.sjf_data):
            process['turnaround_time'] = process['completion_time'] - process['arrival_time']
            process['waiting_time'] = process['start_time'] - process['arrival_time']
            process['response_time'] = process['completion_time'] - process['arrival_time']

root = tk.Tk()
app = SJFVisualizer(root, processes_list)
root.mainloop()
print(processes_list)
SJFResults = ResultsManager(processes_list, 'sjf')