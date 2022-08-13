"""code used to generate sample audio files using Google's Text to Speech API"""

import os
import typing
from typing import Type
from preprocess import Preprocessor

class DataGenerator:

    def __init__(self,audio_directory=None, transcript_directory=None):
        self.audio_directory = audio_directory
        self.transcript_directory = transcript_directory

    def generate_segments(self, text_file, preprocessor: Type[Preprocessor] = None, n=1000, word_length=4):
        """creates segments of text from text file
        text_file: filenam
        n: number of segments to generate
        word_length: number of words in each segment
        """
        arr = []
        with open(text_file, 'r') as f:
            lines = f.readlines()
        
        if preprocessor: lines = preprocessor.process(lines)    # run preprocessing pipeline if provided
        arr = lines[0].split(" ")

        segments = [arr[i:i+word_length] for i in range(0, word_length*n, word_length)]
        for i in range(0, word_length*n, word_length):
            if i >= len(arr):
                return segments
            new_segment = " ".join(arr[i:i+word_length])
            
            segments.append(new_segment)
        return segments


    def generate_data(self, text, filename):
        """creates a .wav file and asssociated transcript"""
        """Synthesizes speech from the input string of text or ssml.
        Make sure to be working in a virtual environment.

        Note: ssml must be well-formed according to:
            https://www.w3.org/TR/speech-synthesis/
        """
        from google.cloud import texttospeech

        # Instantiates a clien
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16, 
            sample_rate_hertz=16000,
            speaking_rate = 0.6)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # save wav file in audio directory
        # The response's audio_content is binary.
        audio_file_path = os.path.join(self.audio_directory, filename+".wav")
        with open(audio_file_path, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print(f'Audio content written to file {audio_file_path}')
        
        
        # save transcript in directory
        transcript_file_path = os.path.join(self.transcript_directory, filename+".txt")
        with open(transcript_file_path, "w") as out:
            out.write(text)