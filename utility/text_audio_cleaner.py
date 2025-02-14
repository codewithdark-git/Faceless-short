import re
import os
from pydub import AudioSegment

def clean_text(text):
    """
    Removes symbols and cleans the input text.
    """
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.strip()  # Remove leading/trailing whitespace
    return text

def process_audio(audio_path, output_path):
    """
    Cleans and normalizes the audio.
    """
    try:
        audio = AudioSegment.from_file(audio_path)
        # Simple normalization (you can add more sophisticated methods)
        normalized_audio = audio.normalize()
        normalized_audio.export(output_path, format="wav")
        return output_path
    except Exception as e:
        print(f"Error processing audio: {e}")
        return None

def convert_to_wav(input_file):
    """
    Convert any audio file to WAV format.
    """
    try:
        # Load the audio file
        audio = AudioSegment.from_file(input_file)
        
        # Define the output WAV file path
        output_wav = os.path.splitext(input_file)[0] + ".wav"
        
        # Export the audio to WAV format
        audio.export(output_wav, format="wav")
        
        return output_wav
    except Exception as e:
        print(f"Error converting to WAV: {e}")
        return None
