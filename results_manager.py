import json
import pathlib
class ResultsManager():

    def __init__(self, process_list: list, algorithm_name: str):

        self.algorithm_name = algorithm_name
        self.file_path =pathlib.Path(__file__).parent / "data_results" / f'{self.algorithm_name}.json'
        self.data = process_list
        self.getting_avarages()
        self.saving_results()

    def getting_avarages(self):

        self.avarage_results = []
        avarage_turnaround_time = 0
        avarage_waiting_time = 0
        avarage_response_time = 0

        for process in self.data:

            avarage_turnaround_time += process['turnaround_time']
            avarage_response_time += process['response_time']
            avarage_waiting_time += process['waiting_time']

        self.avarage_results.append(round(avarage_turnaround_time/len(self.data), 2))
        self.avarage_results.append(round(avarage_waiting_time/len(self.data), 2))
        self.avarage_results.append(round(avarage_response_time/len(self.data), 2))
        

    def saving_results(self):

        try:

            file = open(self.file_path, 'w')
            json.dump(self.avarage_results, file)

        except:
            print("A problem occured while saving, check for path correctness...")


    def reading_results(self):

        try:

            file = open(self.file_path, 'r')
            results = json.load(file)

        except:

            print("A problem occured while reading file, check for path correctness...")

        return results