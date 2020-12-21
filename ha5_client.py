import socket
import sys
import os
import tqdm

SEPARATOR = "<SEPARATOR>"
BUF_SIZE = 4096 #Each step buffer size

filename = sys.argv[3]
filesize = os.path.getsize(filename)

def cmd():
    c = len(sys.argv)
    if c != 4:
        print("Error: Not enought parameters \nha3_server.py ip port")
    else:
        #check the existence of given file
        if os.path.exists(sys.argv[3]):
            try:
                ip = sys.argv[1]
                port = int(sys.argv[2])
                main(ip, port)
            except ValueError:
                print("ValueError. Numbers only")
        else:
            print("File not found")

def main(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create the socket
    try:
        s.connect((ip, port))
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
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

if __name__ == "__main__":
    cmd()