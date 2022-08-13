from datagen import DataGenerator
from preprocess import EMSPreprocessor, Preprocessor
import pandas as pd
import wave
import contextlib
import os
from tqdm import tqdm

DESIRED_LENGTH = 25 * 60    # (number of minutes * 60 seconds)
# DESIRED_LENGTH = 30    # (number of minutes * 60 seconds)

TRANSCRIPT_DIRECTORY = "./data/transcripts"
AUDIO_DIRECTORY = "./data/audio"

def main():
    import pandas as pd

    ems_preprocessor = EMSPreprocessor()
    datagen = DataGenerator(AUDIO_DIRECTORY, TRANSCRIPT_DIRECTORY)

    df = pd.read_excel("RAA Data 2020.xlsx")
    combined_medic_notes = " ".join(map(str, df.loc[:, "Medic Notes"]))

    combined_medic_notes = combined_medic_notes[0:200000]
    segments = datagen.generate_segments(combined_medic_notes, ems_preprocessor, n=3000, word_length=7)

    current_length = 0
    segment_index = 0

    pbar = tqdm(total=DESIRED_LENGTH)
    while current_length < DESIRED_LENGTH and segment_index < len(segments):
        
        if segment_index%5 == 0:
            print("current segment index: ", segment_index)

        curr_segment = segments[segment_index]
        name = f"synth_data_2020_{segment_index}"
        datagen.generate_data(curr_segment, name)
        length_of_file = calculate_wav_length(os.path.join(AUDIO_DIRECTORY, name+".wav"))
        current_length += length_of_file
        pbar.update(length_of_file)
        segment_index += 1
    pbar.close()
    

def calculate_wav_length(fname):
    """calculates length of wav file"""
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)


# def calculate_current_length(directory):
#     "calculates total length of generated .wav files in specified directory"
#     total_length = 0
#     files = os.listdir(directory)
#     for fname in files:
#         if fname.endswith(".wav"):
#             full_path = os.path.join(directory, fname)

#     return total_length



if __name__ == "__main__":
    main()