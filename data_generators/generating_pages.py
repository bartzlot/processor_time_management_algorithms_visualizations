import numpy as np
import pathlib

def generate_page_reference_data(max_page_number=10, sequence_length=50, max_frames=5):

    page_reference_sequence = np.random.randint(0, max_page_number, sequence_length)
    number_of_frames = np.random.randint(1, max_frames + 1)

    return page_reference_sequence, number_of_frames


def save_page_reference_data_to_file(filename, page_reference_sequence, number_of_frames):

    with open(filename, 'w') as file:
        file.write(' '.join(page_reference_sequence.astype(str)) + '\n')
        file.write(str(number_of_frames) + '\n')


if __name__ == "__main__":

    page_reference_sequence, number_of_frames = generate_page_reference_data()
    path = pathlib.Path(__file__).parent / 'page_replacement_data.txt'
    save_page_reference_data_to_file(path, page_reference_sequence, number_of_frames)
