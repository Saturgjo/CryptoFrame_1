#this code is for checking CryptoFrame.py četní také funguje 

import os
import subprocess
import sys

def extract_metadata(file_path):
    """
    Extract metadata from an audio or video file using ffmpeg.

    Args:
        file_path (str): Path to the file from which to extract metadata.
    """
    command = ['ffmpeg', '-i', file_path, '-f', 'ffmetadata', '-']
    
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print('Extracted Metadata:')
        print(result.stdout)
    except subprocess.CalledProcessError:
        print('Failed to extract metadata.')

def extract_hidden_message(cover_file, password):
    """
    Extract a hidden message or file from an audio file using Steghide.

    Args:
        cover_file (str): Path to the cover file (audio or image).
        password (str): Password for extracting the hidden secret.
    """
    command = ['steghide', 'extract', '-sf', cover_file, '-p', password]
    
    try:
        subprocess.run(command, check=True)
        print(f'Secret message successfully extracted from {cover_file}')
    except subprocess.CalledProcessError:
        print('Failed to extract the secret message.')

def main():
    # Example usage:
    # Extract metadata from files
    output_audio_file = 'D:\www\output_with_metadata.mp3'
    output_video_file = 'D:\www\output_with_metadata.mkv'
    # extract_metadata(output_audio_file)
    extract_metadata(output_video_file)

    # # Extract hidden message from audio file
    # cover_file = 'trash\inport_example_WAV_5MG.wav'
    # password = 'nqm159kkk'
    # extract_hidden_message(cover_file, password)

if __name__ == "__main__":
    main()
