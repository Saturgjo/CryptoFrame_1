# working metadata shipherer
# mp3 soubory zvládá 

import os
import subprocess
import tempfile
import shutil

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
    # Step 1: Add metadata to the input file
    metadata_output = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(input_file)[-1]).name
    metadata = {
        'user_name': user_name,
        'user_id': user_id,
        'comment': f'Downloaded by {user_name} (ID: {user_id})'
    }
    add_metadata_video(input_file, metadata_output, metadata)

    # Step 2: Convert to WAV for Steghide compatibility
    wav_output = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
    convert_to_wav(metadata_output, wav_output)

    # Step 3: Embed the secret text file into the WAV file
    password = 'nqm159kkk'
    hide_message_from_file(wav_output, secret_txt_file, password)

    # Step 4: Move the final output file to the desired location
    if not final_output_path:
        final_output_path = os.path.join(os.path.dirname(input_file), 'output_with_metadata_hidden.wav')
    else:
        output_dir = os.path.dirname(final_output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f'Created directory: {output_dir}')

    try:
        shutil.move(wav_output, final_output_path)
        print(f'File successfully moved to: {final_output_path}')
    except IOError as e:
        print(f'Failed to move the file to the specified output path. Error: {e}')
    print(f'Final file with metadata and hidden message is located at: {final_output_path}')

# Example usage
if __name__ == "__main__":
    # Assuming this is run when a user downloads a video or audio
    input_video_file = "trash\inport_example_MP3_2MG.mp3"
    user_name = 'PTred'
    user_id = '010'
    secret_txt_file = r"trash\message.txt"  # Text file to embed
    final_output_path = input('Enter the final destination path for the output file (leave empty for default): ')
    automate_embedding(input_video_file, user_name, user_id, secret_txt_file, final_output_path)