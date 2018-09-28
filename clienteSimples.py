from socket import*
from ssl import*
from base64 import*
from datetime import*

class SmtpDialog:

    def __init__(self,servidor,porta):
        self.servidorName = servidor
        self.servidorPorta = porta
        self.ipServidor = gethostbyname(self.servidorName)

        #Protocolos - AF_INET = IPv4 ; SOCK_STREAM = TCP
        sock = socket(AF_INET, SOCK_STREAM)

        #Envelopa o socket como um socket SSL
        self.sslSocket = wrap_socket(sock)

        #Conecta com o servidor
        self.sslSocket.connect((self.ipServidor, self.servidorPorta))

        print('Meu ip: ' + gethostbyname(gethostname()) )
        print('Servidor SMTP: ' + self.ipServidor + '\n')

        print("Conexão estabelecida.")
        #primeira mensagem do servidor
        self.receive()


    def helo(self):
        self.send("HELO "+self.servidorName)
        self.receive()

    #http://www.samlogic.net/articles/smtp-commands-reference-auth.htm
    #Extensão para autenticação: https://tools.ietf.org/html/rfc4954
    def auth_login(self):
        self.send('AUTH LOGIN')
        message = self.receive()

        # usuario
        print(self.decode_msg(b64decode(message[4:])))
        username = input("")

        self.send(b64encode(username.encode()), True)
        message = self.receive()

        # senha
        if (message[:3] == '334'):
            print(self.decode_msg(b64decode(message[4:])))
            password = input("")

            self.send(b64encode(password.encode()), True)
            self.receive()

    def enviar_email(self):
        de = input("De: ")
        self.send("MAIL FROM: <"+de+">")
        self.receive()

        para = input("Para: ")
        self.send("RCPT TO: <"+para+">")
        self.receive()

        self.send("DATA")
        self.receive()

        #self.send("Date: "+datetime.datetime.day+" "+datetime.datetime.)

        self.send("From: " + de)
        assunto = input("Assunto: \n")
        self.send("Subject: " + assunto)
        self.send("To: " + para)


        terminou = False
        while(not terminou):
            mensagem = input("Digite sua mensagem: \n")
            self.send(mensagem)

            finaliza = input("Finalizar? <y/n> \n")
            if finaliza == 'y':
                terminou = True
                break

        self.send(".")

        self.receive()


    def finaliza(self):
        self.send("QUIT")
        self.receive()
        self.sslSocket.close()

    def decode_msg(self,msg):
        return msg.decode('utf-8')

    def receive(self):
        mensagem = self.decode_msg(self.sslSocket.recv(1024))
        print("Servidor: " + mensagem)
        if(mensagem[:3] == '535'):
            print("Usuário ou senha inválidos!\nEncerrando conexão...")
            self.finaliza()
            quit()
        return mensagem

    def send(self, mensagem,  b64=False):
        if b64 == False:
            print("Cliente: " + mensagem)
            mensagem = mensagem.encode()
        else:
            print("Cliente: " + mensagem.decode())

        self.sslSocket.send(mensagem + '\r\n'.encode())

#google
#smtp.gmail.com
#465

#unifesspa
#smtp.unifesspa.edu.br
#465

print("Bem vindo ao utilitário de envio de email em Python. By: Victor/Allef/Julielson")
servidor = input("Servidor SMTP: ")
porta = input("Porta SSL: ")

smtp = SmtpDialog(servidor, int(porta))


smtp.helo()
smtp.auth_login()

smtp.enviar_email()

smtp.finaliza()
