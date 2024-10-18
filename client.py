import socket


SERVER_IP = '66.103.43.213'  # Server IP
SERVER_PORT = 55300      # Server  Port
def start_client():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect Socket to server Address
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connected to server.")
    except ConnectionRefusedError:
        print("Failed to connect to server.")
        return
    
    client_name = input("Enter your client name: ")
    client_socket.sendall(client_name.encode())
    
    # Main loop for sending and receiving messages
    try:
        while True:
            # Get message from user input
            message = input(f"{client_name}: ")
            
            # Send the message to the server
            client_socket.sendall(message.encode())
            
            # If the message is 'exit', close the connection
            if message.lower() == 'exit':
                print("Closing connection to server...")
                break
            
            # Receive response from the server
            response = client_socket.recv(1024).decode()
            print(f"Server: {response}")
            
            # Handle special command 'status' to fetch server cache
            if message.lower() == 'status':
                print("Fetching server status...")
            
            # Handle 'list' command to fetch file list from server
            elif message.lower() == 'list':
                print("Requesting file list from server...")
                # Server should respond with a list of files
            
            elif message.startswith("get "):
                filename = message.split(" ", 1)[1]
                print(f"Requesting file '{filename}' from server...")

    except KeyboardInterrupt:
        print("\nDisconnected from server.")

    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    start_client()