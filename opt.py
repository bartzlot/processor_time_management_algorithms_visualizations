#Optimal page replacement algorithm
import matplotlib as plt
from results_manager import PageResultsManager
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import subplots
from matplotlib.ticker import MultipleLocator
import pathlib

data_file_path = pathlib.Path(__file__).parent / 'data_generators' / 'page_replacement_data.txt'

def collecting_data_from_file(path: str):

    data = []
    with open(path) as f:

        for line in f:
            line = line.strip()
            data.append(line.split(' '))

    data[1][0] = int(data[1][0])

    for i in range(len(data[0])):

        data[0][i] = int(data[0][i])

    return data[1][0], data[0]

frame_quantity, sites = collecting_data_from_file(data_file_path)


class LRUVisualizer:


    def __init__(self, master, frame_quantity: int, sites: list):
        
        self.master = master
        self.sites_data = sites
        self.frame_amount = frame_quantity
        self.current_page = []
        self.current_time_unit = 0
        self.page_hits = 0
        self.page_faults = 0

        self.fig, self.ax = subplots(figsize=(50,20))
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side="left")
        self.ax.set_xlim(0, len(self.sites_data))
        self.ax.set_ylim(0, self.frame_amount)

        self.ax.xaxis.set_major_locator(MultipleLocator(1))
        self.ax.yaxis.set_major_locator(MultipleLocator(1))
        
        self.update_chart()
        self.canvas.draw()


    def update_chart(self):

        if self.current_time_unit < len(self.sites_data):

            if self.sites_data[self.current_time_unit] in self.current_page: 
                self.draw_chart("lightgreen")
                self.page_hits += 1

            else:

                if len(self.current_page) < self.frame_amount:

                    self.current_page.append(self.sites_data[self.current_time_unit])
                    self.draw_chart("red")

                else:

                    lr_index = self.finding_least_recent()
                    
                    self.current_page[lr_index] = self.sites_data[self.current_time_unit]
                    self.draw_chart("red")
                self.page_faults += 1

            self.canvas.draw()
            self.current_time_unit += 1
            self.master.after(1000, self.update_chart)

        else:
            pass


    def draw_chart(self, text_color: str):
        
        for i, page in enumerate(self.current_page):

            self.ax.broken_barh([(self.current_time_unit, 1)], (self.frame_amount - i - 1, 1), 
                                facecolors=(0.5, 0.5, 0.5), edgecolor='yellow', linewidth=1)            
            self.ax.text(self.current_time_unit + 0.5, self.frame_amount - i - 0.5, f"{page}", 
                    ha='center', va='center', color=text_color, fontweight='bold', fontsize=10)
            self.ax.text(self.current_time_unit + 0.5, self.frame_amount,
                                               f"{self.sites_data[self.current_time_unit]}", 
                                                ha='center', va='center', color="purple", 
                                                fontweight='bold', fontsize=30)


    def finding_least_recent(self):

        least_used_index = []
        near_numbers = []

        for i in range(self.current_time_unit, len(self.sites_data)):
            
            if self.sites_data[i] in self.current_page and self.sites_data[i] not in near_numbers:

                near_numbers.append(self.sites_data[i])
                least_used_index.append(i)
            
            elif set(near_numbers) == set(self.current_page):
                break
            
        if len(near_numbers) < self.frame_amount:

            for number in self.current_page:

                if number not in near_numbers:

                    return self.current_page.index(number)
        
        lr_index = max(least_used_index)
        lr_index = self.current_page.index(self.sites_data[lr_index])

        return lr_index


    def return_metrix(self):
        return self.page_hits, self.page_faults
    

root = tk.Tk()
# root.attributes('-fullscreen', True)
app = LRUVisualizer(root, frame_quantity, sites)
root.mainloop()
page_hits, page_faults = app.return_metrix()
OPTResults = PageResultsManager('opt', page_hits, page_faults, len(sites))