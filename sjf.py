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
        self.row = 0
        self.process_time = 1

        self.whole_time = 0

        for p in self.sjf_data: self.whole_time += p['burst_time']

        self.fig, self.ax = subplots(figsize=(50,20))
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side="left")
        self.ax.set_xlim(0, self.whole_time)
        self.ax.set_ylim(0, len(self.sjf_data))

        self.ax.hlines(list(range(1,len(self.sjf_data))), 0, self.whole_time, colors='green', linestyles='dotted')
        self.ax.xaxis.set_major_locator(MultipleLocator((self.whole_time // 25) + 1))
        self.ax.yaxis.set_major_locator(MultipleLocator(1))
        # self.canvas.draw()
        
        self.update_chart()

    def update_chart(self):

        if self.current_time_unit < self.whole_time:
            
            minimum_burst_time_process_id = 0
            minumim_burst_time = 0
            available_processes = []

            for i in range(len(self.sjf_data)):

                if self.sjf_data[i]['arrival_time'] <= self.current_time_unit:

                    if i not in available_processes:
                        available_processes.append(i)
            print(available_processes)
            for j, index in enumerate(available_processes):
                print(minumim_burst_time)
                if j == 0:

                    minumim_burst_time = self.sjf_data[index]['burst_time']
                
                if minumim_burst_time > self.sjf_data[index]['burst_time']:

                    minimum_burst_time_process_id = self.sjf_data[index]['id']
                    minumim_burst_time = self.sjf_data[index]['burst_time']

            print(minimum_burst_time_process_id)
            print(minumim_burst_time)


                    






            # self.master.after(500, self.update_chart)

        else:
            pass



root = tk.Tk()
# root.attributes('-fullscreen', True)
app = SJFVisualizer(root, processes_list)
root.mainloop()