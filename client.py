import socket
import sys
import os
import tqdm

SEPARATOR = "<SEPARATOR>"
BUF_SIZE = 4096 #Each step buffer size

def cmd():
    c = len(sys.argv)
    if c <= 3:
        print("Error: Not enought parameters \n ip port 'list/send/get/stop' file(optional)")
    else:
        try:
            global command
            global ip
            global port
            global path
            command = sys.argv[3]
            ip = sys.argv[1]
            port = int(sys.argv[2])
            path = sys.argv[4]
            getFunc(command)
        except IndexError:
            if command == "send" or command == "get":   #file path must be assigned with these commands
                print("ValueError. No file specified")  #at this point nothing is sent to server
            else:
                getFunc(command)                        #continues to execute
        except ValueError:
            print("ValueError. Port has to be numbers")

def getFunc(i):
    switcher={      #collection for functions
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
        s.send(f"{command}{SEPARATOR}{path}".encode())  #send the info of wanted file

        receive = s.recv(BUF_SIZE).decode()     #receive the file info
        arguments = receive.split(SEPARATOR)    #parse info to array
        filename = arguments[0]
        filesize = arguments[1]
        filename = os.path.basename(filename)
        filesize = int(filesize)

        if (filename != "-"): #check for error prefix '-'
            #receive the actual file in 'BUF_SIZE' chunks
            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "wb") as f:
                for _ in progress:
                    bytes_read = s.recv(BUF_SIZE)
                    f.write(bytes_read)
                    progress.update(len(bytes_read))
                f.close()
        else:
            print("File does not exist. Nothing received")
    except:
        print("Cannot send data, something wrong with socket, address or port")
        print(str(s.recv(1024), "utf-8"))

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
    print("Server files:\n"+ data.decode())

def sendFile():
    #check if file exists
    if os.path.exists(path):
        filesize = os.path.getsize(path)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create the socket
        try:
            s.connect((ip, port))
            s.send(f"{command}{SEPARATOR}{path}{SEPARATOR}{filesize}".encode())
            progress = tqdm.tqdm(range(filesize), f"Sending {path}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(path, "rb") as f:
                for _ in progress:
                    bytes_read = f.read(BUF_SIZE)  #read the bytes from file
                    if not bytes_read:
                        s.shutdown(socket.SHUT_WR) #file transmit done, shutdown informs server not to receive anymore
                        break
                    s.sendall(bytes_read)
                    progress.update(len(bytes_read)) #progress bar update

        except socket.error:
            print("Cannot send data, something wrong with socket, address or port")
            print(str(s.recv(1024), "utf-8"))
        s.close()
    else:
        print("File not found")

if __name__ == "__main__":
    cmd()
