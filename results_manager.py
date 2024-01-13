import json
import pathlib
import numpy as np


class ResultsManager():

    def __init__(self, process_list: list, algorithm_name: str):

        self.algorithm_name = algorithm_name
        self.file_path =pathlib.Path(__file__).parent / "data_results" / f'{self.algorithm_name}.json'
        self.data = process_list
        self.getting_avarages()
        self.saving_results()


    def getting_avarages(self):
        
        median_data = {
            'turnaround_time_m': [],
            'response_time_m': [],
            'waiting_time_m': []
        }

        std_data = {
            'turnaround_time_std': [],
            'response_time_std': [],
            'waiting_time_std': []
        }

        avg_data = {
            'avarage_turnaround_time': [],
            'avarage_response_time': [],
            'avarage_waiting_time' : []
        }
        
        self.metrix_dict = {
            'turnaround_time_m': 0,
            'response_time_m': 0,
            'waiting_time_m': 0,
            'turnaround_time_std': 0,
            'response_time_std': 0,
            'waiting_time_std': 0,
            'avarage_turnaround_time': 0,
            'avarage_response_time': 0,
            'avarage_waiting_time' : 0
        }
        
        for process in self.data:

            median_data['turnaround_time_m'].append(process['turnaround_time'])
            std_data['turnaround_time_std'].append(process['turnaround_time'])
            avg_data['avarage_turnaround_time'].append(process['turnaround_time'])

            median_data['response_time_m'].append(process['response_time'])
            std_data['response_time_std'].append(process['response_time'])
            avg_data['avarage_response_time'].append(process['response_time'])

            median_data['waiting_time_m'].append(process['waiting_time'])
            std_data['waiting_time_std'].append(process['waiting_time'])
            avg_data['avarage_waiting_time'].append(process['waiting_time'])

        self.metrix_dict['turnaround_time_m'] = np.median(median_data['response_time_m'])
        self.metrix_dict['response_time_m'] = np.median(median_data['response_time_m'])
        self.metrix_dict['waiting_time_m'] = np.median(median_data['waiting_time_m'])

        self.metrix_dict['turnaround_time_std'] = np.std(std_data['turnaround_time_std'])
        self.metrix_dict['response_time_std'] = np.std(std_data['response_time_std'])
        self.metrix_dict['waiting_time_std'] = np.std(std_data['waiting_time_std'])

        self.metrix_dict['avarage_turnaround_time'] = np.average(avg_data['avarage_turnaround_time'])
        self.metrix_dict['avarage_response_time'] = np.average(avg_data['avarage_response_time'])
        self.metrix_dict['avarage_waiting_time'] = np.average(avg_data['avarage_waiting_time'])


    def saving_results(self):

        try:

            file = open(self.file_path, 'w')
            json.dump(self.metrix_dict, file, indent=4)

        except:
            print("A problem occured while saving, check for path correctness...")


    def reading_results(self):

        try:

            file = open(self.file_path, 'r')
            results = json.load(file)

        except:

            print("A problem occured while reading file, check for path correctness...")

        return results
    

class PageResultsManager():


    def __init__(self, algorithm_name: str, page_hits: int, page_faults: int, page_amount: int):

        self.algorithm_name = algorithm_name
        self.file_path = pathlib.Path(__file__).parent / "data_results" / f'{self.algorithm_name}.json'
        self.page_faults = page_faults 
        self.page_hits = page_hits
        self.page_amount = page_amount
        self.calculate_metrix()
        self.saving_results()


    def calculate_metrix(self):

        self.metrix = {
            'page_hits': self.page_hits,
            'page_faults': self.page_faults,
            '%_hits': round((self.page_hits / self.page_amount) * 100, 2),
            '%_faults': round((self.page_faults / self.page_amount) * 100, 2)
        }


    def saving_results(self):

        try:

            file = open(self.file_path, 'w')
            json.dump(self.metrix, file)

        except:
            print("A problem occured while saving, check for path correctness...")


    def reading_results(self):

        try:

            file = open(self.file_path, 'r')
            results = json.load(file)

        except:

            print("A problem occured while reading file, check for path correctness...")

        return results
