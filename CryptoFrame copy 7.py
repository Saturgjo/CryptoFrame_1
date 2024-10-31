#import metadata ( dokonce nejsou jednoduše dohledatelné)

import os
import subprocess

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
    except subprocess.CalledProcessError:
        print('Failed to add metadata to video file.')

def hide_message_in_file(cover_file, secret_message, output_file, password):
    """
    Hide a secret message inside a video file using Steghide.

    Args:
        cover_file (str): Path to the cover file (video or image).
        secret_message (str): Secret message to be hidden.
        output_file (str): Output file after embedding the secret.
        password (str): Password for embedding the secret.
    """
    # Create a temporary secret text file
    secret_file = 'temp_secret.txt'
    with open(secret_file, 'w') as file:
        file.write(secret_message)

    command = [
        'steghide', 'embed', '-cf', cover_file, '-ef', secret_file, '-p', password, '-sf', output_file
    ]

    try:
        subprocess.run(command, check=True)
        print(f'Secret message hidden successfully in {output_file}')
    except subprocess.CalledProcessError:
        print('Failed to hide the secret message.')
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
    secret_message = f'UserName: {user_name}, UserID: {user_id}'
    password = 'secure_password'
    hide_message_in_file(output_video, secret_message, output_video, password)

# Example usage
if __name__ == "__main__":
    # Assuming this is run when a user downloads a video
    # input_video_file = r"trash\inport_example_MP3_2MG.mp3"
    input_video_file = "trash\input.mp4"

    output_video_file = r"D:\www\output.mp4"
    user_name = 'PTTTT'
    user_id = '007'
    automate_embedding(input_video_file, output_video_file, user_name, user_id)
