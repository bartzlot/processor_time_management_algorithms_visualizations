import matplotlib as plt
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
            "priority_lvl" : int(data[2][i])
        }

        processes_list.append(process)

    time_quantum = int(data[3][0])
    rr_time_quantum = int(data[4][0])


collecting_data_from_file("data.txt")


class SJFVisualizer:


    def __init__(self, master, data: list):
        
        self.master = master
        self.sjf_data = sorted(data, key=lambda x: (x['arrival_time']))
        self.process_queue = []
        self.completed_processes = []
        self.current_time_unit = 0
        self.current_process_index = 0
        self.process_time_counter = []
        self.last_process_id = 0

        self.whole_time = 0

        for p in self.sjf_data: self.whole_time += p['burst_time']

        for bt in self.sjf_data: self.process_time_counter.append(bt['burst_time'])

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
            
            minimum_burst_time_process_id = 1
            minumim_burst_time = 0
            available_processes = self.finding_avaliable_processes()

            for j, index in enumerate(available_processes):
                
                if j == 0:

                    minumim_burst_time = self.sjf_data[index]['burst_time']
                
                if minumim_burst_time > self.sjf_data[index]['burst_time'] and self.sjf_data[index]['burst_time'] > 0 or len(available_processes) == 1:

                    minimum_burst_time_process_id = self.sjf_data[index]['id']
                    minumim_burst_time = self.sjf_data[index]['burst_time']

            
            self.sjf_data[minimum_burst_time_process_id - 1]['burst_time'] = self.sjf_data[minimum_burst_time_process_id - 1]['burst_time'] - 1

            self.ax.broken_barh([(self.current_time_unit, 1)], (minimum_burst_time_process_id - 1, 1), 
                                facecolors=(0.5, 0.5, 0.5), edgecolor='yellow', linewidth=1)
            
            self.process_time_counter[minimum_burst_time_process_id - 1] = self.process_time_counter[minimum_burst_time_process_id - 1] - 1

            self.update_counters(minimum_burst_time_process_id)
            self.draw_x_line(minimum_burst_time_process_id)
            self.canvas.draw()
            
            self.current_time_unit += 1
            self.last_process_id = minimum_burst_time_process_id

            self.master.after(200, self.update_chart)
            
        else:
            pass


    def initialize_counters(self):

        self.counter_texts = {}

        for process in self.sjf_data:

            process_id = process['id']
            self.counter_texts[process_id] = self.ax.text(0, process_id - 0.5, 
                                                        f"P{process_id}: {self.process_time_counter[process_id - 1]} ", 
                                                        ha='center', va='center', color="blue", fontweight='bold', fontsize=10)


    def update_counters(self, process_id):

        self.counter_texts[process_id].remove()
        self.counter_texts[process_id] = self.ax.text(0, process_id - 0.5, 
                                                        f"P{process_id}: {self.process_time_counter[process_id - 1]} ", 
                                                        ha='center', va='center', color="blue", fontweight='bold', fontsize=10)


    def draw_x_line(self, process_id):

        if self.last_process_id != process_id and self.last_process_id != 0:

            self.ax.axvline(x=self.current_time_unit, color='purple', linestyle='solid')


    def finding_avaliable_processes(self):

        available_processes = []

        for i in range(len(self.sjf_data)):

            if self.sjf_data[i]['arrival_time'] <= self.current_time_unit and self.sjf_data[i]['burst_time'] > 0:

                if i not in available_processes:
                    available_processes.append(i)

        return available_processes


root = tk.Tk()
# root.attributes('-fullscreen', True)
app = SJFVisualizer(root, processes_list)
root.mainloop()