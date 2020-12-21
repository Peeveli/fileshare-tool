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
        #check if the given path exists
        if os.path.isdir(sys.argv[3]):
            #Start the sockserver
            try:
                ip = sys.argv[1]
                port = int(sys.argv[2])
                sockserv(ip, port)
            except ValueError:
                print("ValueError. Numbers only")
        else: print("Selected path not valid or does not exist")

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
            
                #receive the file info first
                receive = conn.recv(BUF_SIZE).decode()
                (filename, filesize) = receive.split(SEPARATOR)
                filename = os.path.basename(filename)
                filesize = int(filesize)

                #receive the actual file in 4096 byte chunks
                progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                with open(os.path.join(sys.argv[3], filename), "wb") as f:
                    for _ in progress:
                        bytes_read = conn.recv(BUF_SIZE)
                        f.write(bytes_read)
                        progress.update(len(bytes_read))
                f.close()

        except socket.error:
            print("Cannot bind port")
        
if __name__ == "__main__":
    cmd()