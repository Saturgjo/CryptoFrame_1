# working metadata shipherer

import os
import subprocess
import tempfile
import shutil
from datetime import datetime

def add_metadata_video(input_file, output_file, metadata):
    """
    Add metadata to a video or audio file using ffmpeg.

    Args:
        input_file (str): Path to the input video or audio file.
        output_file (str): Path to the output file.
        metadata (dict): Metadata to be added, in key-value format.
    """
    metadata_params = []
    for key, value in metadata.items():
        metadata_params += ['-metadata', f'{key}={value}']

    command = [
        'ffmpeg', '-i', input_file, *metadata_params, '-codec', 'copy', output_file
    ]

    try:
        subprocess.run(command, check=True)
        print(f'Metadata added successfully to {output_file}')
    except subprocess.CalledProcessError as e:
        print(f'Failed to add metadata to file. Error: {e}')

def convert_to_wav(input_file, output_file):
    """
    Convert an audio or video file to WAV format using ffmpeg.

    Args:
        input_file (str): Path to the input audio or video file.
        output_file (str): Path to the output WAV file.
    """
    command = [
        'ffmpeg', '-i', input_file, output_file
    ]

    try:
        subprocess.run(command, check=True)
        print(f'Converted {input_file} to WAV format at {output_file}')
    except subprocess.CalledProcessError as e:
        print(f'Failed to convert {input_file} to WAV. Error: {e}')

    # Verify if the output WAV file was successfully created
    if not os.path.exists(output_file):
        raise FileNotFoundError(f'WAV file not created at {output_file}')

def hide_message_from_file(cover_file, secret_file, password):
    """
    Hide a secret file inside a cover file using Steghide.

    Args:
        cover_file (str): Path to the cover file (image or audio).
        secret_file (str): Path to the secret text file to be hidden.
        password (str): Password for embedding the secret.
    """
    if not cover_file.lower().endswith(('.bmp', '.jpg', '.wav', '.au')):
        print('Steghide only supports BMP, JPG, WAV, and AU formats. Please provide a compatible file.')
        return

    command = [
        'steghide', 'embed', '-cf', cover_file, '-ef', secret_file, '-p', password
    ]

    try:
        subprocess.run(command, check=True)
        print(f'Secret file {secret_file} hidden successfully in {cover_file}')
    except subprocess.CalledProcessError as e:
        print(f'Failed to hide the secret file. Error: {e}')

def automate_embedding(input_file, user_name, user_id, secret_txt_file, final_output_path):
    """
    Automate the embedding of user-specific data into audio or video files.

    Args:
        input_file (str): Path to the input audio or video file.
        user_name (str): User's name to be added.
        user_id (str): User's ID to be added.
        secret_txt_file (str): Path to a text file to be embedded.
        final_output_path (str): Path to the final output file.
    """
    try:
        # Step 1: Add metadata to the input file
        metadata_output = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(input_file)[-1]).name
        metadata = {
            'user_name': user_name,
            'user_id': user_id,
            'comment': f'Downloaded by {user_name} (ID: {user_id}) {user_created}' ,
            'creation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        add_metadata_video(input_file, metadata_output, metadata)

        # Step 2: Determine if the file is audio or video
        if input_file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
            # Video file: move directly to the final output path
            if not final_output_path:
                final_output_path = os.path.join(os.path.dirname(input_file), f'Download_{datetime.now().strftime("%Y%m%d_%H%M%S")}.mkv')
            else:
                final_output_path = os.path.join(final_output_path, f'Download_{datetime.now().strftime("%Y%m%d_%H%M%S")}.mkv')
            shutil.copy(metadata_output, final_output_path)
            print(f'File successfully moved to: {final_output_path}')
            print(f'File successfully moved to: {final_output_path}')
        elif input_file.lower().endswith(('.mp3', '.wav', '.au')):
            # Audio file: convert to WAV for Steghide compatibility
            current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            wav_output = os.path.join(os.path.dirname(input_file), f'Download_{current_time}.wav')
            convert_to_wav(metadata_output, wav_output)

            # Step 3: Embed the secret text file into the WAV file
            password = 'nqm159kkk'
            hide_message_from_file(wav_output, secret_txt_file, password)

            # Step 4: Move the final output file to the desired location
            final_output_path = final_output_path or os.path.join(os.path.dirname(input_file), 'output_with_metadata_hidden.wav')
            try:
                shutil.move(wav_output, final_output_path)
                print(f'File successfully moved to: {final_output_path}')
            except IOError as e:
                print(f'Failed to move the file to the specified output path. Error: {e}')
                # As a fallback, try copying the file
                try:
                    shutil.copy(wav_output, final_output_path)
                    print(f'File successfully copied to: {final_output_path}')
                except IOError as e:
                    print(f'Failed to copy the file to the specified output path. Error: {e}')

        print(f'Final file with metadata and hidden message is located at: {final_output_path}')

    except Exception as e:
        print(f'An error occurred during the embedding process: {e}')

# Example usage
if __name__ == "__main__":
    # Assuming this is run when a user downloads a video or audio
    # input_video_file = "trash\inport_example_MP3_2MG.mp3"
    input_video_file = "trash\inputt.mp4"
    user_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_name = 'PTred'
    user_id = '69'
    secret_txt_file = r"trash\message.txt"  # Text file to embed
    final_output_path = input('Enter the final destination path for the output file (leave empty for default): ')
    final_output_path = final_output_path or 'D:\www\extracted'
    automate_embedding(input_video_file, user_name, user_id, secret_txt_file, final_output_path)
