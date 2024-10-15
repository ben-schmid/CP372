import socket
import threading
from datetime import datetime
import os

client_cache = {}
max_clients = 3

def handle_client(client_socket, client_name):
    client_cache[client_name] = {"start_time": datetime.now(), "end_time": None}
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.lower() == "exit":
                print(f"{client_name} has disconnected.")
                client_cache[client_name]['end_time'] = datetime.now()
                client_socket.close()
                break
           # elif message.lower() == "status":
                #logic for status
           # elif message.low() == "list":
                #logic for list directory
            else:
                reponse = message + " ACK"
                client_socket.send(reponse.encode())
        except:
            break

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(3)
    print("Server is listening...")

    client_id = 1
    while True:
        if len(client_cache) < max_clients:
            client_socket, addr = server_socket.accept()
            client_name = f"Client  {client_id}"
            print(f"Connection from {addr} as {client_name}")
            client_id += 1

            #create a new thread for multiple clients 
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_name))
            client_thread.start() 

        else:
            print("Max client reached.")

if __name__ == '__main__':
    server()


