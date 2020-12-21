import socket
import sys
import os
import tqdm

BUF_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def cmd():
    #Check the amount of arguments given
    c = len(sys.argv)
    if c != 4:
        print("Error: Not enought parameters \nha3_server.py ip port")
    else:
        #set given arguments
        global path
        global ip
        global port
        path = sys.argv[3]
        ip = sys.argv[1]
        port = int(sys.argv[2])
        #create folder
        try:
            os.mkdir(path)
        except OSError:
            #folder already exist
            print("Failed to create folder, using existing one")
            listener()
        else:
            #folder created
            print(f"Created folder {path}")
            listener()

def listener():
    #Tries to start listener with given arquments
    try:
        sockserv(ip, port)
    except ValueError:
        print("ValueError. Numbers only")

def sockserv(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
    with sock as s:
        try: #bind port and ip
            s.bind((ip, port))
            while True:
                #allow maximium connections of 5
                s.listen(5)
                print("Listening socket... ")

                (conn, addr) = s.accept()
                print(f"{addr} is connected.")
                
                #check if command is sent correctly
                #everything ok
                                    
                #receive the file info first
                receive = conn.recv(BUF_SIZE).decode()
                arguments = receive.split(SEPARATOR)
                if arguments[0] == "send":
                    
                    #receive the file info first
                    filename = arguments[1]
                    filesize = arguments[2]
                    filename = os.path.basename(filename)
                    filesize = int(filesize)

                    #receive the actual file in 4096 byte chunks
                    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                    with open(os.path.join(path, filename), "wb") as f:
                        for _ in progress:
                            bytes_read = conn.recv(BUF_SIZE)
                            f.write(bytes_read)
                            progress.update(len(bytes_read))
                        f.close()
                
                elif arguments[0] == "list":
                    data = ""
                    files = os.listdir(path)
                    for x in files:
                        data = data+x+" "
                    print(data)
                    conn.send(data.encode())

                
                elif arguments[0] == "get":
                    print("GETTING FILE")
                
                elif arguments[0] == "stop":
                    print(f"SERVER TERMINATED BY {addr}")
                    break
        
        except socket.error:
            print("Cannot bind port")

if __name__ == "__main__":
    cmd()