"""code used to generate sample audio files using Google's Text to Speech API"""

from email.mime import audio
import os

class DataGenerator:

    def __init__(self,audio_directory, transcript_directory):
        self.audio_directory = audio_directory
        self.transcript_directory = transcript_directory

    def generate_data(self, text, filename):
        """creates a .wav file and asssociated transcript"""
        """Synthesizes speech from the input string of text or ssml.
        Make sure to be working in a virtual environment.

        Note: ssml must be well-formed according to:
            https://www.w3.org/TR/speech-synthesis/
        """
        from google.cloud import texttospeech

        # Instantiates a client
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


    def generate_segments(self,):
        """creates segments of text from text file"""
        pass