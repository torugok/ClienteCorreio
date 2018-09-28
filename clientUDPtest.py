from socket import*


servidor = 'localhost'
porta = 5055

clientSock = socket(AF_INET,SOCK_DGRAM)

mensagem = input("Digite algo: ")

clientSock.sendto(mensagem.encode(),(servidor,porta))
resposta, serverAddress = clientSock.recvfrom(2048)
print(resposta)
input("")