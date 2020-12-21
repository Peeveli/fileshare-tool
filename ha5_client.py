import socket
import sys
import os
import tqdm

SEPARATOR = "<SEPARATOR>"
BUF_SIZE = 4096 #Each step buffer size

def cmd():
    c = len(sys.argv)
    if c <= 3:
        print("Error: Not enought parameters \n'list/send/get/stop' 'ip' 'port' 'file'")
    else:
        try:
            global command
            global ip
            global port
            global path
            command = sys.argv[1]
            ip = sys.argv[2]
            port = int(sys.argv[3])
            path = sys.argv[4]
            getFunc(command)
        except IndexError:
            if command != "send":
                getFunc(command)
            else:
                print("ValueError. No file specified")
        except ValueError:
            print("ValueError. Port has to be numbers")

def getFunc(i):
    switcher={
        "list":getList,
        "send":sendFile,
        "get":getFile,
        "stop":stopServer,
    }
    func=switcher.get(i,lambda :"Invalid")
    return func()


def stopServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create the socket
    try:
        s.connect((ip, port))
        s.send(command.encode())
    except socket.error:
            print("Cannot send data, something wrong with socket, address or port")
            print(str(s.recv(1024), "utf-8"))
    s.close()

def getFile():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create the socket
    try:
        s.connect((ip, port))
        s.send(command.encode())
    except socket.error:
            print("Cannot send data, something wrong with socket, address or port")
            print(str(s.recv(1024), "utf-8"))
    s.close()

def getList():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create the socket
    try:
        #send the command for listing the files back to client
        s.connect((ip, port))
        s.send(command.encode())
        #receive the list
        data = s.recv(BUF_SIZE)
    except:
        print("Cannot send data, something wrong with socket, address or port")
        print(str(s.recv(1024), "utf-8"))
    
    #print the list
    print("Server files: "+ data.decode())

def sendFile():
    #check if file exists
    if os.path.exists(path):
        global filesize
        filesize = os.path.getsize(path)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create the socket
        try:
            s.connect((ip, port))
            s.send(f"{command}{SEPARATOR}{path}{SEPARATOR}{filesize}".encode())
            progress = tqdm.tqdm(range(filesize), f"Sending {path}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(path, "rb") as f:
                for _ in progress:
                    #read the bytes from file
                    bytes_read = f.read(BUF_SIZE)
                    if not bytes_read:
                        #file transmit done, shutdown informs server not to receive anymore
                        s.shutdown(socket.SHUT_WR)
                        break
                    s.sendall(bytes_read)
                    #progress bar update
                    progress.update(len(bytes_read))

        except socket.error:
            print("Cannot send data, something wrong with socket, address or port")
            print(str(s.recv(1024), "utf-8"))
        s.close()
    else:
        print("File not found")

if __name__ == "__main__":
    cmd()