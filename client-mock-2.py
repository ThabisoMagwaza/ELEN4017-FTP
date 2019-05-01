from socket import *

serverName = gethostname()
serverPort = 6000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    command = input('Enter Command: ')
    clientSocket.send(command.encode())
    if command != 'QUIT':
        print('message sent')
        response = clientSocket.recv(1024)
        print(response.decode())
    else:
        break
clientSocket.close()
