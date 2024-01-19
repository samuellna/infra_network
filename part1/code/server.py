from common import Socket
from os.path import join as pathjoin
import os.path

server = Socket(port=5000, server=True)

DIRECTORY_SERVER = "files_server"

# inicializar pasta sever
if not os.path.exists(DIRECTORY_SERVER):
    os.makedirs(DIRECTORY_SERVER)

header, address = None, []

while True:
    if header is None:
        header, address = server.receive()

    else:
        # comando de debug para desligar o servidor remotamente
        if header[Socket.Header.EXTRA] == "3":
            break

        # ida do arquivo
        server.receiveFile(header, path=DIRECTORY_SERVER)
        
        # volta do arquivo
        with open(pathjoin(DIRECTORY_SERVER, header[Socket.Header.FILENAME]), "rb") as f:
            server.sendMessageFile(ip=address[0], port=address[1], msg=f.read(), filename='c_'+header[Socket.Header.FILENAME], )
        
        header = None


server.sock.close()
