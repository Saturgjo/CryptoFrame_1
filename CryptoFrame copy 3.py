#working extractions

import os
import subprocess

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
        print('Failed to extract metadata from the video file.')

def extract_hidden_message(cover_file, password):
    """
    Extract a hidden message from a video file using Steghide.

    Args:
        cover_file (str): Path to the cover file (video or image).
        password (str): Password for extracting the hidden secret.
    """
    command = ['steghide', 'extract', '-sf', cover_file, '-p', password]

    try:
        subprocess.run(command, check=True)
        print(f'Secret message successfully extracted from {cover_file}')
    except subprocess.CalledProcessError:
        print('Failed to extract the secret message.')

def automate_extraction(input_video, password):
    """
    Automate the extraction of metadata and hidden messages from a video file.

    Args:
        input_video (str): Path to the input video file.
        password (str): Password to extract the hidden message.
    """
    # Extract metadata
    print("\nExtracting metadata from video file:")
    extract_metadata(input_video)

    # Extract hidden message
    print("\nExtracting hidden message from video file:")
    extract_hidden_message(input_video, password)

# Example usage
if __name__ == "__main__":
    # Assuming this is run when a user wants to extract metadata and hidden message from the video
    # input_video_file = 'D:\www\koš\personalized_output.mp4'
    # input_video_file = "D:\www\output.mp3"
    input_video_file = r"D:\www\extracted\tmp41kowlzt.wav"
    password = 'nqm159kkk'
    automate_extraction(input_video_file, password)
