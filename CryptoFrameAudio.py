import os
import zlib
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from base64 import b64encode, b64decode
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import wave
import numpy as np
from pydub import AudioSegment

SALT_SIZE = 16
NUM_ITERATIONS = 100000
KEY_SIZE = 32
IV_SIZE = 16
NUM_LAYERS = 7


def encrypt_message(message, public_key_path):
    with open(public_key_path, 'rb') as f:
        public_key = RSA.import_key(f.read())
    cipher_rsa = PKCS1_OAEP.new(public_key)

    session_key = get_random_bytes(16)
    salt = get_random_bytes(SALT_SIZE)
    key = PBKDF2(session_key, salt, dkLen=KEY_SIZE, count=NUM_ITERATIONS)

    data = zlib.compress(message.encode('utf-8'))

    for _ in range(NUM_LAYERS):
        iv = get_random_bytes(IV_SIZE)
        cipher_aes = AES.new(key, AES.MODE_CBC, iv)
        data = cipher_aes.encrypt(pad(data, AES.block_size))
        data = iv + data

    enc_session_key = cipher_rsa.encrypt(session_key)
    enc_session_key_b64 = b64encode(enc_session_key).decode('utf-8')
    salt_b64 = b64encode(salt).decode('utf-8')
    data_b64 = b64encode(data).decode('utf-8')
    return f"{enc_session_key_b64}:{salt_b64}:{data_b64}"


def decrypt_message(encrypted_message, private_key_path, passphrase):
    enc_session_key_b64, salt_b64, data_b64 = encrypted_message.split(':')
    with open(private_key_path, 'rb') as f:
        key_data = f.read()
        private_key = RSA.import_key(key_data, passphrase=passphrase)
    
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(b64decode(enc_session_key_b64))
    salt = b64decode(salt_b64)
    data = b64decode(data_b64)

    key = PBKDF2(session_key, salt, dkLen=KEY_SIZE, count=NUM_ITERATIONS)

    for _ in range(NUM_LAYERS):
        iv = data[:IV_SIZE]
        data = data[IV_SIZE:]
        cipher_aes = AES.new(key, AES.MODE_CBC, iv)
        data = unpad(cipher_aes.decrypt(data), AES.block_size)

    # Decompress the data after decrypting
    data = zlib.decompress(data)

    return data.decode('utf-8')


def hide_data_in_audio(input_audio_path, output_audio_path, message):
    audio = AudioSegment.from_file(input_audio_path)
    samples = np.array(audio.get_array_of_samples())

    # Convert message to bytes and compress
    message_bytes = zlib.compress(message.encode('utf-8'))
    message_bits = ''.join(format(byte, '08b') for byte in message_bytes)

    if len(message_bits) > len(samples):
        raise ValueError("Message is too large to hide in this audio file.")

    # Hide message bits in the least significant bit of each audio sample
    modified_samples = samples.copy()
    for i in range(len(message_bits)):
        modified_samples[i] = (modified_samples[i] & ~1) | int(message_bits[i])

    # Create a new audio segment with the modified samples
    modified_audio = audio._spawn(modified_samples.tobytes())
    modified_audio.export(output_audio_path, format="wav")


def unhide_data_from_audio(audio_path):
    audio = AudioSegment.from_file(audio_path)
    samples = np.array(audio.get_array_of_samples())

    # Extract the least significant bit of each sample
    message_bits = [str(sample & 1) for sample in samples]
    message_bytes = bytearray()
    for i in range(0, len(message_bits), 8):
        byte = message_bits[i:i+8]
        if len(byte) == 8:
            message_bytes.append(int(''.join(byte), 2))

    # Decompress the message
    try:
        message = zlib.decompress(message_bytes).decode('utf-8')
    except zlib.error:
        raise ValueError("Failed to decompress hidden message.")

    return message


def parse_arguments():
    parser = ArgumentParser(description="Hide or reveal text in audio files using steganography.",
                            epilog="Examples:\n"
                                   "  Hide a message: python CryptoFrame.py hide --input input.mp3 --output output.wav --message 'Privacy is a fundamental right' --public_key public.pem\n"
                                   "  Unhide a message: python CryptoFrame.py unhide --input output.wav --private_key private.pem --passphrase strong_password\n",
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('action', choices=['hide', 'unhide'], help="Action to perform: 'hide' or 'unhide'")
    parser.add_argument('input', help="Input audio file path.")
    parser.add_argument('--output', help="Output audio file path for 'hide' action.")
    parser.add_argument('--message', help="Text to hide or path to a text file containing the message.")
    parser.add_argument('--public_key', help="Path to the public key file for encryption.")
    parser.add_argument('--private_key', help="Path to the private key file for decryption.")
    parser.add_argument('--passphrase', nargs='?', default='', help="Passphrase for the private key.")
    args = parser.parse_args()

    if args.action == 'hide' and not args.output:
        parser.error("The --output argument is required for the 'hide' action.")

    if args.action == 'hide' and not args.message:
        parser.error("The --message argument is required for the 'hide' action.")

    if args.action == 'hide' and not args.public_key:
        parser.error("The --public_key argument is required for the 'hide' action.")

    if args.action == 'unhide' and args.private_key and not args.passphrase:
        args.passphrase = getpass.getpass(prompt="Enter private key passphrase: ")
        if not args.passphrase.strip():
            parser.error("Passphrase is required to unlock the private key")

    return args


def main():
    args = parse_arguments()

    if args.action == 'hide':
        message = args.message
        if os.path.isfile(message):
            with open(message, 'r', encoding='utf-8') as file:
                message = file.read()

        encrypted_message = encrypt_message(message, args.public_key)
        hide_data_in_audio(args.input, args.output, encrypted_message)

    elif args.action == 'unhide':
        encrypted_message = unhide_data_from_audio(args.input)
        decrypted_message = decrypt_message(encrypted_message, args.private_key, args.passphrase)
        print("Decrypted Message:", decrypted_message)


if __name__ == "__main__":
    main()
