import socket

class Server:
    def __init__(self, maxplayers, port):
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(maxplayers)
        self.conn, self.addr = self.sock.accept()

    def send_data(self, data):
        data_bytes = bytearray(str(data), 'utf8')
        self.conn.send(data_bytes)

    def get_data(self):
        data = self.conn.recv(1024)
        return data

    def close_server(self):
        self.sock.close()

class Client:
    def __init__(self, ip, port):
        self.sock = socket.socket()
        self.sock.connect((str(ip), port))

    def send_data(self, data):
        data_bytes = bytearray(str(data), 'utf8')
        self.sock.send(data_bytes)

    def get_data(self):
        data = self.sock.recv(1024)
        return data
