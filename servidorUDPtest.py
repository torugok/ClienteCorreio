from socket import*

porta = 5055

servSocket = socket(AF_INET,SOCK_DGRAM)

servSocket.bind(('',porta))

print("O servidor está rodando, VAIRODANDO ")

while 1:
    message,clientAddress = servSocket.recvfrom(2048)

    message = message.decode().upper()
    servSocket.sendto(message.encode(),clientAddress)