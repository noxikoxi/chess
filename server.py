import socket


class Server:
    def __init__(self):
        self.ip = "192.168.100.12"
        self.port = 5555
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        try:
            self.socket.bind((self.ip, self.port))
        except socket.error as e:
            print(str(e))

        self.socket.listen(1)
        print(f'Server started on : {self.ip}:{self.port}')

    def wait_for_client(self):
        # Akceptowanie połączenia od klienta
        print(f'Waiting for client to connect...')
        self.client_socket, self.client_address = self.socket.accept()
        print(f"Connected with: {self.client_address}")

    def sendData(self, data):
        # Obsługa komunikacji z klientem
        self.client_socket.send(data.encode())

    def waitForData(self):
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            else:
                print(f'Otrzymałem dane od klienta')
                return data

    def __del__(self):
        self.socket.close()
        self.client_socket.close()
