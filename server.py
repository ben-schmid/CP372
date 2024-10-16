import socket
import threading
from datetime import datetime
import os
 
# hash to save client cache
client_cache = {}
max_clients = 3
current_clients = 0

def handle_client(client_socket, client_name):
    global current_clients
    current_clients += 1
    #add start time to client cache when they join
    connection_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #add client to hash
    client_cache[client_name] = {"start_time": connection_start, "end_time": None}
    while True:
        
        message = client_socket.recv(1024).decode()
        if message.lower() == "exit":
            print(f"{client_name} has disconnected.")

            #add endtime to client cache when they disconnect
            client_cache[client_name]['end_time'] = datetime.now()
            client_socket.close()
            current_clients -= 1
            break
        elif message.lower() == "status":
            status_message = ""
            
            #loop to list the cache of all clients that have connected
            for client, times in client_cache.items():

                #extract times from hash
                start_time = times["start_time"]
                if times["end_time"] != None:
                    end_time = times["end_time"]
                else:
                    end_time = "Still Connected"
                status_message += f"{client} - Start: {start_time}, End: {end_time}\n"
            
            #If loop is not run, there are no clients that have connected
            if status_message == "":
                status_message = "No clients connected"
            
            #send status to clients
            client_socket.send(status_message.encode())
        elif message.lower() == "list":
            files = os.listdir("/Users/benschmid/vscode/CP372/files")
            file_list = "\n".join(files)

            if not files:
                file_list = "No files in the directory"
            
            client_socket.send(file_list.encode())

        elif message.lower().startswith("get "):
            filename = message[4:]
            filepath = os.path.join("/Users/benschmid/vscode/CP372/files", filename)

            if os.path.exists(filepath):
                with open(filepath, "rb") as file:
                    contents = file.read(1024)
                    while contents:
                        client_socket.send(contents)
                        contents = file.read(1024)
                
                client_socket.send("EOF".encode())
            else:
                client_socket.send("File not found".encode)
        

            
        else:
            reponse = message + " ACK"
            client_socket.send(reponse.encode())
        

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(3)
    print("Server is listening...")

    client_id = 1
    while True:
        if current_clients <=3:
            client_socket, addr = server_socket.accept()
            client_name = f"Client  {client_id}"
            print(f"Connection from {addr} as {client_name}")
            client_id += 1

            #create a new thread for multiple clients 
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_name))
            client_thread.start() 

        else:
            print("Max clients reached.")

if __name__ == '__main__':
    server()


