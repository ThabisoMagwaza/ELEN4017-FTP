from socket import *
import threading

functionsImplimented = ["USER", "QUIT", "PORT",
                        "TYPE",  "MODE", "RETR", "STOR", "NOOP"]


# Thread to serve a client


class ClientThread(threading.Thread):
    def __init__(self, address, connectionSocket):
        threading.Thread.__init__(self)
        self.address = address
        self.connectionSocket = connectionSocket
        self.Username = ""

    def run(self):
        print("connected to %s port %d" % (self.address[0], self.address[1]))
        while True:
            message = self.connectionSocket.recv(1024)
            message = message.decode()
            # interpret message
            command, argument = self.serverPI(message)
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
            response = self.switcher(command, argument)

            self.connectionSocket.send(response.encode())

        self.connectionSocket.close()

    # server protocol interpreter. Extracts (command, message) from recieved message

    def serverPI(self, message):
        if " " in message:
            command, argument = message.split(' ')
            return command, argument
        else:
            if message in functionsImplimented:
                return message, " "
            else:
                return "error", " "
            # functions to handle implemented commands\

    def USER(self, argument):
        self.Username = argument
        return ' call USER: ' + argument

    def PORT(self, argument):
        return ' call PORT: ' + argument

    def TYPE(self, argument):
        return ' call TYPE: ' + argument

    def MODE(self, argument):
        return ' call MODE: ' + argument

    def RETR(self, argument):
        return ' call RETR: ' + argument

    def STOR(self, argument):
        return ' call STOR: ' + argument

    def NOOP(self, argument):
        return "OK"

    # function to select function base on command

    def switcher(self, command, argument):
        switch = {
            "USER": self.USER(argument),
            "PORT": self.PORT(argument),
            "TYPE": self.TYPE(argument),
            "MODE": self.MODE(argument),
            "RETR": self.RETR(argument),
            "STOR": self.STOR(argument),
            "NOOP": self.NOOP(argument)
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
