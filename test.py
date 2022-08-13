from datagen import DataGenerator


def main():
    dg  = DataGenerator(audio_directory="./data/audio", transcript_directory="./data/transcripts")
    sample_text = " She states that she has taken her prescribed medications tonight  She denies all other medical complaints  including  difficulty breathing  abdominal pain  nausea  vomiting  diarrhea  numbness  tingling  weakness  dizziness  blurry double vision  fever  cough  and rash  Medical history  medications  and allergies as noted  There are no other associated signs symptoms at this time"
    dg.generate_data(text=sample_text, filename="test3")









if __name__ == "__main__":
    main()