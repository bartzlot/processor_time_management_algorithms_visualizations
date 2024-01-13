import numpy as np
import pathlib

def generate_random_data(max_duration=20, max_arrival=20, num_processes=50):

    arrival_times = np.random.randint(0, max_arrival + 1, num_processes)
    arrival_times[0] = 0  # Ensure at least one process has zero arrival time
    durations = np.random.randint(1, max_duration + 1, num_processes)
    priorities = np.random.randint(0, 11, num_processes)  # Priority range from 0 to 10

    return arrival_times, durations, priorities


def save_data_to_file(filename, arrival_times, durations, priorities, time_quantum_priority, time_quantum_rr):
 
    sorted_indices = np.argsort(arrival_times)
    sorted_arrival_times = arrival_times[sorted_indices]
    sorted_durations = durations[sorted_indices]
    sorted_priorities = priorities[sorted_indices]

    with open(filename, 'w') as file:
        file.write(' '.join(sorted_arrival_times.astype(str)) + '\n')
        file.write(' '.join(sorted_durations.astype(str)) + '\n')
        file.write(' '.join(sorted_priorities.astype(str)) + '\n')
        file.write(str(time_quantum_priority) + '\n')
        file.write(str(time_quantum_rr) + '\n')


if __name__ == "__main__":

    arrival_times, durations, priorities = generate_random_data()
    time_quantum_priority = 3
    time_quantum_rr = 5
    path = pathlib.Path(__file__).parent / 'cpu_scheduling_data.txt'
    save_data_to_file(path, arrival_times, durations, priorities, time_quantum_priority, time_quantum_rr)
