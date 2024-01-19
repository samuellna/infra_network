from common import Socket
from os.path import basename
import os.path

# inicializar cliente
client = Socket(port=1337, server=True)

DIRECTORY_CLIENT = "files_client"

# inicializar pasta cliente
if not os.path.exists(DIRECTORY_CLIENT):
    os.makedirs(DIRECTORY_CLIENT)
    

while True:
    
    client.print_menu()
    comando = input("Opcao: ")

    match comando:
        case "0":
            break
        
        case "1":
            filename = input("\tNome do arquivo: ")
            try:
                # Envio do arquivo
                with open(filename, "rb") as f:
                    client.sendMessageFile(port=5000, msg=f.read(), filename= 's_' + basename(filename), )

                # receber de volta
                header, _ = client.receive()
                client.receiveFile(header, path=DIRECTORY_CLIENT)
            except IOError:
                print("Nome de arquivo inválido!")
                
        case "2":
            mensagem = input("\nDigite sua mensagem: ")
            # enviar mensagem com o header mensagem
            client.sendMessageFile(mensagem.encode())
        
        case "3":
            client.sendMessageFile(port=5000, extra="3")
        
        case "4":
            os.system("cls")

client.sock.close()
