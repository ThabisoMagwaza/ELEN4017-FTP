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
            elif command == "error":
                response = "500 Syntax error, command unrecognized"
                self.connectionSocket.send(response.encode())
                continue

            # respond with specified funcion response
            response = switcher(command, argument)

            self.connectionSocket.send(response.encode())

        self.connectionSocket.close()

# server protocol interpreter. Extracts (command, message) from recieved message


def serverPI(message):
    if " " in message:
        command, argument = message.split(' ')
        return command, argument
    elif message == "QUIT":
        return message, " "
    elif message == "NOOP":
        return message, " "
    else:
        return "error", " "
        # functions to handle implemented commands\


def USER(argument):
    return ' call USER: ' + argument


def PORT(argument):
    return ' call PORT: ' + argument


def TYPE(argument):
    return ' call TYPE: ' + argument


def MODE(argument):
    return ' call MODE: ' + argument


def RETR(argument):
    return ' call RETR: ' + argument


def STOR(argument):
    return ' call STOR: ' + argument


def NOOP(argument):
    return "OK"

# function to select function base on command


def switcher(command, argument):
    switch = {
        "USER": USER(argument),
        "PORT": PORT(argument),
        "TYPE": TYPE(argument),
        "MODE": MODE(argument),
        "RETR": RETR(argument),
        "STOR": STOR(argument),
        "NOOP": NOOP(argument)
    }
    func = switch.get(command, "502 Command not implemented")
    return func


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
