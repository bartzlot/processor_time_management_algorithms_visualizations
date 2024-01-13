import matplotlib.pyplot as plt
import json
import pathlib

path = pathlib.Path(__file__).parent.parent / 'data_results'
saving_path = pathlib.Path(__file__).parent.parent / 'charts_data'

def collecting_data_from_file(path):

    algorithms = ['pswa.json', 'sjf.json', 'fcfs.json']
    data = []

    for name in algorithms:

        f = open(path / name, 'r')
        data.append(json.load(f))

    return data


def add_value_labels(ax, spacing=5):
    for rect in ax.patches:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2
        label = "{:.2f}".format(y_value)
        ax.annotate(label, (x_value, y_value), xytext=(0, spacing), 
                    textcoords="offset points", ha='center', va='bottom')


def creating_charts(metrix_data: list, save_file_path, algorithm_names: list):

    
    for index, algorithm in enumerate(metrix_data):

        labels = ['Średnia', 'Odchylenie Standardowe', 'Mediana']
        bar_width = 0.4 
        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))
        fig.subplots_adjust(wspace=5)
        fig.suptitle(algorithm_names[index], fontsize=30)


        axes[0].bar(labels, [algorithm['avarage_turnaround_time'], algorithm['turnaround_time_std'], 
                            algorithm['turnaround_time_m']], color=['#add8e6', '#ff6347', '#f4a460'], width=bar_width)
        axes[0].set_title('Turnaround Time')
        axes[0].set_yticks([])
        add_value_labels(axes[0])
        axes[0].grid(axis='y', alpha=0.75)
        axes[0].spines['top'].set_visible(False)
        axes[0].spines['right'].set_visible(False)
        axes[0].spines['left'].set_visible(False)


        axes[1].bar(labels, [algorithm['avarage_response_time'], algorithm['response_time_std'], 
                            algorithm['response_time_m']], color=['#add8e6', '#ff6347', '#f4a460'], width=bar_width)
        axes[1].set_title('Response Time')
        axes[1].set_yticks([])
        add_value_labels(axes[1])
        axes[1].grid(axis='y', alpha=0.75)
        axes[1].spines['top'].set_visible(False)
        axes[1].spines['right'].set_visible(False)
        axes[1].spines['left'].set_visible(False)


        axes[2].bar(labels, [algorithm['avarage_waiting_time'], algorithm['waiting_time_std'], 
                            algorithm['waiting_time_m']], color=['#add8e6', '#ff6347', '#f4a460'], width=bar_width)
        axes[2].set_title('Waiting Time')
        axes[2].set_yticks([])
        add_value_labels(axes[2])
        axes[2].grid(axis='y', alpha=0.75)
        axes[2].spines['top'].set_visible(False)
        axes[2].spines['right'].set_visible(False)
        axes[2].spines['left'].set_visible(False)

        plt.tight_layout()
        fig.savefig(save_file_path / f'{algorithm_names[index]}.png', dpi=300)

algorithms = ['Priority Schedule with Aging', 'Shortest Job First', 'First Come First Serve']
metrix_data = collecting_data_from_file(path)
creating_charts(metrix_data, saving_path, algorithms)

    


