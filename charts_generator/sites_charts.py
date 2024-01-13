import matplotlib.pyplot as plt
import json
import pathlib

path = pathlib.Path(__file__).parent.parent / 'data_results'
saving_path = pathlib.Path(__file__).parent.parent / 'charts_data'

def collecting_data_from_file(path):

    algorithms = ['fifo.json', 'lfu.json', 'lru.json', 'opt.json']
    data = []

    for name in algorithms:

        f = open(path / name, 'r')
        data.append(json.load(f))

    return data


def creating_charts(metrix_data: list, save_file_path, algorithm_names: list):


    for index, algorithm in enumerate(metrix_data):

        colors = ['lightgreen', 'lightcoral']

        fig, axs = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(algorithm_names[index], fontsize=30)
        
        bars = axs[0].bar(['Page Hits', 'Page Faults'], [algorithm['page_hits'], algorithm['page_faults']], color=colors)
        axs[0].set_title('Page Hits / Faults')
        axs[0].spines['top'].set_visible(False)
        axs[0].spines['right'].set_visible(False)
        axs[0].spines['left'].set_visible(False)
        axs[0].set_yticks([])
        axs[0].set_ylabel('')

        for bar in bars:
            height = bar.get_height()
            axs[0].annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords='offset points',
                        ha='center', va='bottom')

        axs[1].pie([algorithm['%_hits'], algorithm['%_faults']], labels=['% Hits', '% Faults'],
                colors=['lightgreen', 'lightcoral'], autopct='%1.1f%%', startangle=140)
        axs[1].set_title('Page Hits / Faults %')

        axs[1].axis('equal')

        plt.tight_layout()
        fig.savefig(save_file_path / f'{algorithm_names[index]}.png', dpi=300)


metrix_data = collecting_data_from_file(path)
algorithms = ['First in First out', 'Least Frequently Used', 'Least Recently Used', 'Optimal Page Replacement']
creating_charts(metrix_data, saving_path, algorithms)