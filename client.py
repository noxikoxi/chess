import socket


class Client:
    def __init__(self):
        self.serverIp = "192.168.100.12"
        self.serverPort = 5555
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isConnected = False

    def connect_with_server(self):
        self.socket.connect((self.serverIp, self.serverPort))
        print(f'Connected with server: {self.serverIp}:{self.serverPort}')
        self.isConnected = True

    def sendData(self, data):
        # Obsługa komunikacji z klientem
        self.socket.send(data.encode())

    def waitForData(self):
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            else:
                print(f'Otrzymałem dane od servera')
                return data

    def __del__(self):
        self.socket.close()
