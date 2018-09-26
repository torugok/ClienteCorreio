from socket import*
from ssl import*
from base64 import*

def decodeMsg(msg,is64):
    msg = msg.decode('utf-8')
    if(is64):
        msg = b64decode(msg).decode('utf-8')
    return msg

servidor = 'smtp.gmail.com'
address = gethostbyname(servidor)

porta = 465 #sevidor ssl do gmail
sock = socket(AF_INET, SOCK_STREAM)
sslSock = wrap_socket(sock) #envelopa o socket como um socket SSL
sslSock.connect((servidor,porta))
print('Meu ip: '+gethostbyname(gethostname()) +'\n')
print('Servidor smtp: '+address+'\n')

message = decodeMsg(sslSock.recv(1024),False)
print(message)


sslSock.send('HELO smtp.gmail.com\r\n'.encode())
message = decodeMsg(sslSock.recv(1024),False)
print(message)

sslSock.send('AUTH LOGIN\r\n'.encode())
message = decodeMsg(sslSock.recv(1024),False)
print(message)

#usuario
print( decodeMsg(b64decode(message[4:]),False) )
username = input("")
sslSock.send((b64encode(username.encode()))+'\r\n'.encode())
message = decodeMsg(sslSock.recv(1024),False)
print(message)

#senha
if(message[:3] == '334'):
    print(  decodeMsg(b64decode(message[4:]),False) )
    password = input("")
    sslSock.send((b64encode(password.encode()))+'\r\n'.encode())
    message = decodeMsg(sslSock.recv(1024),False)
    print(message)

#MANDAR O EMAIL DE FATO
sslSock.send('MAIL FROM: <torugok@gmail.com>\r\n'.encode())
message = decodeMsg(sslSock.recv(1024),False)
print(message)

sslSock.send('RCPT To: <torugok@gmail.com>\r\n'.encode())
message = decodeMsg(sslSock.recv(1024),False)
print(message)


sslSock.send('DATA\r\n'.encode())
message = decodeMsg(sslSock.recv(1024),False)
print(message)

#mandando mensagem
sslSock.send('Eu sei mandar emails pelo python sou genio...\r\n'.encode())
sslSock.send('.\r\n'.encode()) #encerrando a mensagem
message = decodeMsg(sslSock.recv(1024),False)
print(message)

#adeus
sslSock.send('QUIT\r\n'.encode())
message = decodeMsg(sslSock.recv(1024),False)
print(message)



sslSock.close()
