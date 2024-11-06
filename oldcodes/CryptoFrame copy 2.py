# working metadata shipherer

import os
import subprocess
import tempfile

def add_metadata_video(input_file, output_file, metadata):
    """
    Add metadata to a video file using ffmpeg.

    Args:
        input_file (str): Path to the input video file.
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
        print(f'Failed to add metadata to video file. Error: {e}')

def hide_message_in_file(cover_file, secret_message, output_file, password):
    """
    Hide a secret message inside a file using Steghide.

    Args:
        cover_file (str): Path to the cover file (image or audio).
        secret_message (str): Secret message to be hidden.
        output_file (str): Output file after embedding the secret.
        password (str): Password for embedding the secret.
    """
    if not cover_file.lower().endswith(('.bmp', '.jpg', '.wav', '.au', '.mp3', '.wma')):
        print('Steghide only supports BMP, JPG, WAV, and AU formats. Please provide a compatible file.')
        return
        print('Steghide only supports BMP, JPG, WAV, AU, and MP3 formats. Please provide a compatible file.')
        return

    # Create a temporary secret text file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
        temp_file.write(secret_message)
        secret_file = temp_file.name

    command = [
        'steghide', 'embed', '-cf', cover_file, '-ef', secret_file, '-p', password
    ]

    try:
        subprocess.run(command, check=True)
        print(f'Secret message hidden successfully in {cover_file}')
    except subprocess.CalledProcessError as e:
        print(f'Failed to hide the secret message. Error: {e}')
    finally:
        # Clean up temporary secret file
        if os.path.exists(secret_file):
            os.remove(secret_file)

def automate_embedding(input_video, output_video, user_name, user_id):
    """
    Automate the embedding of user-specific data into video files.

    Args:
        input_video (str): Path to the input video file.
        output_video (str): Path to the output file.
        user_name (str): User's name to be added.
        user_id (str): User's ID to be added.
    """
    # Add metadata
    metadata = {
        'user_name': user_name,
        'user_id': user_id,
        'comment': f'Downloaded by {user_name} (ID: {user_id})'
    }
    add_metadata_video(input_video, output_video, metadata)

    # Hide secret information in the video file
    if output_video.lower().endswith(('.bmp', '.jpg', '.wav', '.au', '.mp3', '.wma')):
        secret_message = f'UserName: {user_name}, UserID: {user_id}'
        password = 'nqm159kkk'
        hide_message_in_file(output_video, secret_message, output_video, password)
    else:
        print('The specified output file format is not supported for hiding messages with Steghide.')

# Example usage
if __name__ == "__main__":
    # Assuming this is run when a user downloads a video
    # input_video_file = r"D:\www\input.flv"
    input_video_file = "trash\inport_example_MP3_2MG.mp3"
    # input_video_file = "trash\input.mp4"
    # input_video_file = "D:\www\inportt.wma"
    output_video_file = r"D:\www\output.mp3"
    user_name = 'PTred'
    user_id = '007'
    automate_embedding(input_video_file, output_video_file, user_name, user_id)
