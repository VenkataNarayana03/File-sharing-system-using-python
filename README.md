# File Sharing System

An efficient file sharing system built with Python that allows users to upload, download, and manage files across a network.

## Features

### Secure Authentication
- Username and password protected access
- Encrypted credentials storage
- Session-based authentication

### File Management
- **List Files**: View all available files on the server
- **Upload Files**: Transfer files from client to server
- **Download Files**: Retrieve files from server to client
- **File Integrity**: Ensures complete file transfers with EOF markers

### Network Features
- Multi-client support using threading
- Real-time file transfers
- Error handling and connection management
- Cross-platform compatibility

### User Interface
- Simple command-line interface
- Interactive menu system
- Clear status messages and error reporting

## Getting Started

### Prerequisites
- Python 3.x
- Network connectivity between client and server

### Running the System
1. **Start the server**:
   ```bash or cmd
   python server/server.py
   ```

2. **Run the client**:
   ```bash or cmd
   python client/client.py
   ```
   - Enter the server's IP address when prompted
   - Use the provided credentials to authenticate

## Usage
1. **List Files**: View all available files on the server
2. **Upload**: Send files from your local machine to the server
3. **Download**: Retrieve files from the server to your local machine
4. **Exit**: Close the connection and exit the application

## Security Note
- Always ensure the server is running in a secure, trusted network
- Change default credentials before production use
