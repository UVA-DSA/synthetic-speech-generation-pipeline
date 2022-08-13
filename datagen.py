"""code used to generate sample audio files using Google's Text to Speech API"""

import os
from typing import Type
from preprocess import Preprocessor
from google.cloud import texttospeech
import random


class DataGenerator:

    def __init__(self,audio_directory=None, transcript_directory=None):
        self.audio_directory = audio_directory
        self.transcript_directory = transcript_directory
        self.client = texttospeech.TextToSpeechClient()
        self.voices = []
        
        # storer all en-US WaveNet voices in array (used later in random sampling)
        for voice in self.client.list_voices().voices:
            if "en-US-Wavenet" in voice.name:
                self.voices.append(voice)
                

    def generate_segments(self, text: str, preprocessor: Type[Preprocessor] = None, n:int=1000, word_length:int=4):
        """creates segments of text from text file
        text_file: filenam
        n: number of segments to generate
        word_length: number of words in each segment
        """
        if preprocessor: 
            arr = preprocessor.process(text)    # run preprocessing pipeline if provided
        else:
            arr = text.split(" ")

        segments = [arr[i:i+word_length] for i in range(0, word_length*n, word_length)]
        segments = [" ".join(segment) for segment in segments]

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

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        # voice_test = texttospeech.VoiceSelectionParams(name="en-US-Wavenet-E")
        # voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        # print(self.voices)
        random_voice = random.choice(self.voices)
        voice = texttospeech.VoiceSelectionParams(
            language_code= random_voice.language_codes[0],
            name = random_voice.name,
            ssml_gender= random_voice.ssml_gender
        )


        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16, 
            sample_rate_hertz=16000,
            speaking_rate = random.uniform(0.7, 1))

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # save wav file in audio directory
        # The response's audio_content is binary.
        audio_file_path = os.path.join(self.audio_directory, filename+".wav")
        with open(audio_file_path, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            # print(f'Audio content written to file {audio_file_path}')
        
        
        # save transcript in directory
        transcript_file_path = os.path.join(self.transcript_directory, filename+".txt")
        with open(transcript_file_path, "w") as out:
            out.write(text)