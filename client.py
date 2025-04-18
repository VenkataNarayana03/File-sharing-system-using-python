import socket
import os

def start_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = input("Enter the server address: ").strip()
        client_socket.connect((host, 8080))
        print("Connected to the server.")

        # Authentication
        print(client_socket.recv(1024).decode(), end="")  # Username prompt
        username = input().strip()
        client_socket.send(username.encode())

        print(client_socket.recv(1024).decode(), end="")  # Password prompt
        password = input().strip()
        client_socket.send(password.encode())

        auth_response = client_socket.recv(1024).decode()
        print(auth_response)

        if "failed" in auth_response.lower():
            print("Authentication failed. Exiting.")
            client_socket.close()
            return

        while True:
            user_input = input("Enter command (upload/download/exit): ").strip().lower()
            client_socket.send(user_input.encode())

            if user_input == "exit":
                print("Closing connection...")
                break

            elif user_input == "upload":
                filename = input("Enter the filename to upload: ").strip()
                if not os.path.exists(filename):
                    print("File not found. Please check the filename and try again.")
                    continue

                client_socket.send(filename.encode())  
                server_response = client_socket.recv(1024).decode()
                if server_response != "OK":
                    print("Server rejected the file upload.")
                    continue

                with open(filename, 'rb') as f:
                    while chunk := f.read(4096):
                        client_socket.send(chunk)

                client_socket.send(b"<EOF>")  # End-of-file marker
                print(client_socket.recv(1024).decode())  # Success message

            elif user_input == "download":
                filename = input("Enter the filename to download: ").strip()
                client_socket.send(filename.encode())  

                response = client_socket.recv(1024).decode(errors="ignore")
                if response == "OK":
                    print(f"Downloading '{filename}'...\n")

                    # Create a new file with the specified name
                    with open(filename, 'wb') as f:
                        while True:
                            file_data = client_socket.recv(4096)
                            
                            # If we detect the EOF marker, remove it and stop writing
                            if file_data.endswith(b"<EOF>"):
                                f.write(file_data[:-5])  # Remove <EOF> marker before writing
                                break
                            
                            f.write(file_data)

                    print(f"✅ File '{filename}' saved successfully.")
                else:
                    print(f"❌ Error: {response}")

        client_socket.close()

    except ConnectionRefusedError:
        print("❌ Error: Unable to connect to the server. Please check the server address and try again.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()