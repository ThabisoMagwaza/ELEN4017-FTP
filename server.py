from socket import *
import threading

# Thread to serve a client


class ClientThread(threading.Thread):
    def __init__(self, address, connectionSocket):
        threading.Thread.__init__(self)
        self.address = address
        self.connectionSocket = connectionSocket

    def run(self):
        print("connected to %s port %d" % (self.address[0], self.address[1]))
        while True:
            message = self.connectionSocket.recv(1024)
            message = message.decode()
            # interpret message
            command, argument = serverPI(message)
            print("Command: %s, Argument: %s" % (command, argument))
            if command == 'QUIT':
                print("closing connection to %s port %d" %
                      (self.address[0], self.address[1]))
                break
            response = command + " : " + argument
            # self.connectionSocket.send(response.encode())

        self.connectionSocket.close()

# server protocol interpreter. Extracts (command, message) from recieved message


def serverPI(message):
    if message == "QUIT":
        return message, " "
    else:
        command, argument = message.split(' ')
        return command, argument


serverPort = 6000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))

while True:
    serverSocket.listen(4)
    print("ready to receive new connection")
    connectionSocket, addr = serverSocket.accept()
    newTread = ClientThread(addr, connectionSocket)
    newTread.start()

serverSocket.close()
