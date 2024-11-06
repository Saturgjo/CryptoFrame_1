import os
import subprocess
import shutil

def extract_metadata(input_file):
    """
    Extract metadata from an audio or video file using ffmpeg.

    Args:
        input_file (str): Path to the input audio or video file.
    """
    command = [
        'ffmpeg', '-i', input_file, '-f', 'ffmetadata', '-'
    ]

    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print('Extracted Metadata:')
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f'Failed to extract metadata from {input_file}. Error: {e}')

def extract_hidden_message(cover_file, password, output_dir):
    """
    Extract a hidden message from a cover file using Steghide.

    Args:
        cover_file (str): Path to the cover file (image or audio).
        password (str): Password for extracting the hidden secret.
        output_dir (str): Directory where the extracted file should be saved.
    """
    if not cover_file.lower().endswith(('.bmp', '.jpg', '.wav', '.au')):
        print('Steghide only supports BMP, JPG, WAV, and AU formats. Please provide a compatible file.')
        return

    command = [
        'steghide', 'extract', '-sf', cover_file, '-p', password
    ]

    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f'Secret message successfully extracted from {cover_file}')
        # Check and move the extracted file to output_dir
        for file in os.listdir('.'): 
            if file.endswith('.txt'):
                extracted_file_path = os.path.join('.', file)
                output_path = os.path.join(output_dir, file)
                shutil.move(extracted_file_path, output_path)
                print(f'Secret file successfully moved to: {output_path}')
                break
    except subprocess.CalledProcessError as e:
        print(f'Failed to extract the secret message. Error: {e}')

def automate_extraction(input_file, password, output_dir):
    """
    Automate the extraction of metadata and hidden messages or files from an audio or video file.

    Args:
        input_file (str): Path to the input audio or video file.
        password (str): Password for extracting the hidden message or file.
        output_dir (str): Directory where the extracted file should be saved.
    """
    # Extract metadata
    print("\nExtracting metadata from file:")
    extract_metadata(input_file)

    # Extract hidden message
    print("\nExtracting hidden message from file:")
    extract_hidden_message(input_file, password, output_dir)

# Example usage
if __name__ == "__main__":
    # Assuming this is run when a user wants to extract information
    input_video_file = r"D:\www\extracted\tmph1zlfavp.wav"
    password = 'nqm159kkk'
    output_dir = r"D:\www\extracted"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    automate_extraction(input_video_file, password, output_dir)
