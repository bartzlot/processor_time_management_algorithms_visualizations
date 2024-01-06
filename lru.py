import matplotlib as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import subplots
from matplotlib.ticker import MultipleLocator


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

frame_quantity, sites = collecting_data_from_file("data2.txt")


class LRUVisualizer:


    def __init__(self, master, frame_quantity: int, sites: list):
        
        self.master = master
        self.sites_data = sites
        self.frame_amount = frame_quantity
        self.current_page = []
        self.current_time_unit = 0

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
                self.draw_chart()

            else:

                if len(self.current_page) < self.frame_amount:

                    self.current_page.append(self.sites_data[self.current_time_unit])
                    self.draw_chart()

                else:

                    # least_recent = self.sites_data[self.current_time_unit - self.frame_amount]
                    lr_index = self.finding_least_recent()
                    lr_index = self.current_page.index(self.sites_data[lr_index])
                    self.current_page[lr_index] = self.sites_data[self.current_time_unit]
                    self.draw_chart()

            self.canvas.draw()
            self.current_time_unit += 1
            self.master.after(1000, self.update_chart)

        else:
            pass


    def draw_chart(self):
        
        for i, page in enumerate(self.current_page):

            self.ax.broken_barh([(self.current_time_unit, 1)], (self.frame_amount - i - 1, 1), 
                                facecolors=(0.5, 0.5, 0.5), edgecolor='yellow', linewidth=1)            
            self.ax.text(self.current_time_unit + 0.5, self.frame_amount - i - 0.5, f"{page}", 
                    ha='center', va='center', color="orange", fontweight='bold', fontsize=10)
            self.ax.text(self.current_time_unit + 0.5, self.frame_amount,
                                               f"{self.sites_data[self.current_time_unit]}", 
                                                ha='center', va='center', color="purple", 
                                                fontweight='bold', fontsize=30)


    def finding_least_recent(self):

        least_used_index = []
        last_numbers = []

        for i in range(self.current_time_unit, -1, -1):

            if self.sites_data[i] in self.current_page and self.sites_data[i] not in last_numbers:

                last_numbers.append(self.sites_data[i])
                least_used_index.append(i)
            
            elif set(last_numbers) == set(self.current_page):
                break

        return min(least_used_index)



root = tk.Tk()
# root.attributes('-fullscreen', True)
app = LRUVisualizer(root, frame_quantity, sites)
root.mainloop()