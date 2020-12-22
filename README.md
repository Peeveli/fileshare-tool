# fileshare-tool
Simple fileshare tool to share files between client and host by socket.
Requires python 3.5 or never

## SERVER Usage
1. Before running the first time

pip install tqdm

2. Usage
python3.7 server.py "source_ip" "source_port" "folder"

<ul>
  <li>Folder can be an existing or otherwise it will create it. Can be also a full path</li>
  <li>Every file server receives will need a unique name, otherwise it will write on top of the existing file (will add a optional filename for the future)</li>
</ul>

## CLIENT Usage
1. Before running the first time

pip install tqdm

2. Usage
python3.7 client.py "destination_ip" "destination_port" "command" "file -optional"

<ul>
  <li>file has to exist. Can be also a full path</li>
  <li>file is mandatory only for "get" and "send" commands</li>
  <li>Every file client receives will need a unique name, otherwise it will write on top of the existing file (will add a optional filename for the future)</li>
</ul>
3. Commands:
<ul>
  <li>list = Lists files from currently assigned folder by the running server</li>
  <li>get  = Transfer the wanted file from the server</li>
  <li>send = Send a specified file to the server folder</li>
  <li>stop = Terminate a running server (for buggy situations I quess?)</li>
</ul>
