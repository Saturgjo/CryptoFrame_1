# import os
# import subprocess
# import sys

# def add_metadata_audio(input_file, output_file, metadata):
#     """
#     Add metadata to an audio file using ffmpeg.

#     Args:
#         input_file (str): Path to the input audio file.
#         output_file (str): Path to the output file.
#         metadata (dict): Metadata to be added, in key-value format.
#     """
#     metadata_params = []
#     for key, value in metadata.items():
#         metadata_params += ['-metadata', f'{key}={value}']
    
#     command = [
#         'ffmpeg', '-i', input_file, *metadata_params, '-codec', 'copy', output_file
#     ]
    
#     try:
#         subprocess.run(command, check=True)
#         print(f'Metadata added successfully to {output_file}')
#     except subprocess.CalledProcessError:
#         print('Failed to add metadata to audio file.')

# def add_metadata_video(input_file, output_file, metadata):
#     """
#     Add metadata to a video file using ffmpeg.

#     Args:
#         input_file (str): Path to the input video file.
#         output_file (str): Path to the output file.
#         metadata (dict): Metadata to be added, in key-value format.
#     """
#     metadata_params = []
#     for key, value in metadata.items():
#         metadata_params += ['-metadata', f'{key}={value}']
    
#     command = [
#         'ffmpeg', '-i', input_file, *metadata_params, '-codec', 'copy', output_file
#     ]
    
#     try:
#         subprocess.run(command, check=True)
#         print(f'Metadata added successfully to {output_file}')
#     except subprocess.CalledProcessError:
#         print('Failed to add metadata to video file.')

# def hide_message_in_file(cover_file, secret_file, password):
#     """
#     Hide a secret message or file inside an audio file using Steghide.

#     Args:
#         cover_file (str): Path to the cover file (audio or image).
#         secret_file (str): Path to the secret file (text or other file).
#         password (str): Password for embedding the secret.
#     """
#     command = [
#         'steghide', 'embed', '-cf', cover_file, '-ef', secret_file, '-p', password
#     ]
    
#     try:
#         subprocess.run(command, check=True)
#         print(f'Secret file {secret_file} hidden inside {cover_file} successfully.')
#     except subprocess.CalledProcessError:
#         print('Failed to hide the secret message.')

# def main():
#     # # Example usage:
#     # # Adding metadata to an audio file
#     # input_audio_file = 'input.mp3'
#     # output_audio_file = 'output_with_metadata.mp3'
#     # audio_metadata = {
#     #     'title': 'My Custom Title',
#     #     'artist': 'My Artist Name',
#     #     'comment': 'This is a hidden message in the metadata'
#     # }
#     # add_metadata_audio(input_audio_file, output_audio_file, audio_metadata)

#     # Adding metadata to a video file
#     input_video_file = 'trash\input.mp4'
#     output_video_file = "D:\www\output.mkv"
#     video_metadata = {
#         'title': 'HUH',
#         'director': 'PT',
#         'comment': 'F this shit'
#     }
#     add_metadata_video(input_video_file, output_video_file, video_metadata)

#     # # Hiding a secret message in an audio file
#     # cover_file = 'cover_audio.mp3'
#     # secret_file = 'secret.txt'
#     # password = 'your_password'
#     # hide_message_in_file(cover_file, secret_file, password)

# if __name__ == "__main__":
#     main()
