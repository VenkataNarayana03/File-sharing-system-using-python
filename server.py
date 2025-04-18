# Segment 1: Libraries
import socket
import threading
import os
import time

# Segment 2: Dummy Authentication Data
VALID_USERS = {
    "Dhaya": "Police",
    "user": "pass"
}

# Segment 3: Client Handler
def handle_client(client_socket, addr):
    print(f"[+] Connection from {addr}")

    # Segment 3.1: Authentication
    client_socket.send(b"Username: ")
    username = client_socket.recv(1024).decode().strip()

    client_socket.send(b"Password: ")
    password = client_socket.recv(1024).decode().strip()

    if VALID_USERS.get(username) != password:
        client_socket.send(b"Authentication failed.")
        client_socket.close()
        return

    client_socket.send(b"Authentication successful.\n")

    while True:
        try:
            command = client_socket.recv(1024).decode().strip()
            if not command:
                break

            # Segment 3.2: Exit Command
            if command == "exit":
                print(f"[-] {addr} disconnected.")
                break

            # Segment 3.3: File Upload
            elif command == "upload":
                filename = client_socket.recv(1024).decode().strip()
                if not filename:
                    client_socket.send(b"Invalid filename.")
                    continue

                client_socket.send(b"OK")
                with open(filename, "wb") as f:
                    while True:
                        data = client_socket.recv(4096)
                        if data.endswith(b"<EOF>"):
                            f.write(data[:-5])
                            break
                        f.write(data)

                client_socket.send(b"File uploaded and saved successfully.")

            # Segment 3.4: File Download
            elif command == "download":
                filename = client_socket.recv(1024).decode().strip()
                if not os.path.exists(filename):
                    client_socket.send(b"File not found.")
                    continue

                client_socket.send(b"OK")
                time.sleep(0.5)
                with open(filename, "rb") as f:
                    while chunk := f.read(4096):
                        client_socket.send(chunk)
                client_socket.send(b"<EOF>")

        # Segment 3.5: Error Handling
        except Exception as e:
            print(f"Error with client {addr}: {e}")
            break

    # Segment 3.6: Close Connection
    client_socket.close()

# Segment 4: Server Starter
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))
    server.listen(5)
    print("[*] Server listening on port 8080...\n")

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

# Segment 5: Entry Point
if __name__ == "__main__":
    start_server()