import socket


SERVER_IP = '66.103.43.213'  # Server IP
SERVER_PORT = 55300      # Server  Port
def start_client():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #set timeout
    client_socket.settimeout(20)
    # Connect Socket to server Address
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connected to server.")
    except ConnectionRefusedError:
        print("Failed to connect to server.")
        return
    
    client_name = input("Enter your client name: ")
    client_socket.sendall(client_name.encode())


    #check if servers max clients is reached
    initial_response = client_socket.recv(1024).decode()
    if initial_response == "Busy":
        print("Server is busy. Try again later.")
        client_socket.close()
        return
    #welcome is handshake between server and client
    elif initial_response == "Welcome":
        print("Connected to the server successfully.")
    else:
        print("Unexpected response from server.")
        client_socket.close()
        return
    
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
            
            #exctract file from server
            if message.lower().startswith("get "):
                #open file name
                with open(message[4:], "wb") as file:
                    while True:
                        # Receive data
                        chunk = client_socket.recv(1024)
                        if not chunk:
                            break
                        # Check if EOF is in the chunk
                        if b"EOF" in chunk:
                            # Write data up to EOF
                            eof_index = chunk.find(b"EOF")
                            file.write(chunk[:eof_index])
                            print("File received successfully.")
                            break
                        else:
                            file.write(chunk)
                continue

            else:
                response = client_socket.recv(1024).decode()
                print(f"Server: {response}")

    except KeyboardInterrupt:
        print("\nDisconnected from server.")

    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    start_client()