import socket
from enum import IntEnum
from os.path import join as pathjoin

'''
Funções comuns a serem usadas pelos sockets

'''

class Socket: 
    HEADER_START = "HELLO"

    # define as posições de cada um dos elementos do header de uma transferência
    class Header(IntEnum):
        START = 0
        FILENAME = 1
        DATA_LENGTH = 2
        EXTRA = 3

    def print_menu(self):
        print("Transmissor de arquivos e mensagens\n Digite:")
        print("- 1 para enviar arquivo")
        print("- 2 para enviar mensagem")
        print("- 3 para desligar o servidor")
        print("- 4 para limpar o terminal")
        print("- 0 sair do programa\n")
        
    def __init__(self, sock=None, host="localhost", port=5000, buffer_size=1024, server=False):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.sock = sock
        self.ip = (host, port)
        self.buffer_size = buffer_size

        if server:
            self.sock.bind(self.ip)
    
    def receiveUDP(self):
        return self.sock.recvfrom(self.buffer_size)
    
    def sendMessageFile(self, port, ip="localhost", msg=[], filename="", extra=""):
        # 1) calcular tamanho da mensagem em bytes
        LENGTH_MESSAGE = len(msg)
        bytes_sent = 0
        destination = (ip, port)

        # 2) definir header da mensagem
        header = [self.HEADER_START, filename, str(LENGTH_MESSAGE), extra]

        # 3) enviar header da mensagem
        print(f"Enviando um header de {len(header)} bytes")
        self.sock.sendto(",".join(header).encode(), destination)
        

        # 4) enviar mensagem parcelada em pacotes tamanho buffer_size
        print(f"Enviando um arquivo de {LENGTH_MESSAGE} bytes")
        while bytes_sent < LENGTH_MESSAGE: # enquanto a mensagem ainda não foi completamente enviada
            bytes_sent += self.sock.sendto(msg[bytes_sent:bytes_sent + self.buffer_size], destination)

        if bytes_sent > 0 and bytes_sent == LENGTH_MESSAGE: 
            print(f"Arquivo enviado com sucesso: {filename}")

    # Espera o recebimento de um header
    def receive(self):
        msg, address = self.receiveUDP()

        if msg.decode()[:len(self.HEADER_START)] == self.HEADER_START:
            header = msg.decode().split(",")
            print(f"Header recebido: {header}")
            return (header, address)
        
        return (None, address)
        
    # Recebe e salva um arquivo segundo as especificações de um header
    def receiveFile(self, header, path="output"):
        self.sock.settimeout(5)
        filename = pathjoin(path, header[Socket.Header.FILENAME])
        try:
            with open(filename, "wb") as newFile:
                sizeMessage = 0
                while True:
                    msg, _ = self.receiveUDP()
                    sizeMessage += len(msg)
                    newFile.write(msg)
                    
                    # parar quando tiver recebido todos os bytes especificados no header
                    if sizeMessage == int(header[Socket.Header.DATA_LENGTH]):
                        break
                print(f"Arquivo salvo: {filename}")
        except TimeoutError:
            print ("Erro no recebimento do arquivo")
        self.sock.settimeout(None)