import socket
import threading
from datetime import datetime
import os
 
# hash to save client cache
client_cache = {}
max_clients = 3
current_clients = 0
client_lock = threading.Lock()
cache_lock = threading.Lock()

FILE_DIRECTORY = "files"

def handle_client(client_socket, client_id_name):
    global current_clients
    client_accepted = False  
    try:
        client_name = client_id_name + client_socket.recv(1024).decode('utf-8')
        
        #logic to determine if max clients have been reached
        with client_lock:
            if current_clients >= max_clients:
                print(f"Max clients reached. Rejecting {client_name}")
                client_socket.send("Busy".encode())
                return
            else:
                current_clients += 1
                client_accepted = True
        
        
        print("Client count: ", current_clients)
        print(f"Client connected as {client_name}")

        #add start time to client cache when they join
        connection_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #add client to hash
        with cache_lock:
            client_cache[client_name] = {"start_time": connection_start, "end_time": None}
        
        #send client welcome so client can continue while loop
        client_socket.send("Welcome".encode())

        while True:
            
            message = client_socket.recv(1024).decode()
            if message.lower() == "exit":
                print(f"{client_name} has disconnected.")

                #add endtime to client cache when they disconnect
                with cache_lock:
                    client_cache[client_name]['end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                files = os.listdir(FILE_DIRECTORY)
                file_list = "\n".join(files)

                if not files:
                    file_list = "No files in the directory"
                
                client_socket.send(file_list.encode())

            elif message.lower().startswith("get "):
                #get file name
                filename = message[4:]
                filepath = os.path.join(FILE_DIRECTORY, filename)

                if os.path.exists(filepath):
                    with open(filepath, "rb") as file:
                        contents = file.read(1024)
                        while contents:
                            #send file
                            client_socket.send(contents)
                            contents = file.read(1024)
                    #send EOF flag to client so it knows to stop loop and file is done
                    client_socket.send("EOF".encode())
                else:
                    client_socket.send("File not found".encode)
                    
            else:
                response = message + " ACK"
                client_socket.send(response.encode())
    except Exception as e:
        print(f"An error occurred with {client_name}: {e}")
    finally:
            client_socket.close()
            if client_accepted:
                with client_lock:
                    current_clients -= 1
                with cache_lock:
                        client_cache[client_name]['end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Current Clients: ", current_clients)
        

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 55300))
    server_socket.listen(3)
    print("Server is listening...")

    client_id = 1
    while True:
        client_socket, addr = server_socket.accept()
        client_name_id = f"Client {client_id}: "
        print(f"Connection from {addr} as {client_name_id}")
        client_id += 1

            #create a new thread for multiple clients
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_name_id))
        client_thread.start() 

if __name__ == '__main__':
    server()


