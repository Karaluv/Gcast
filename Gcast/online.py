import socket


class Server:
    def __init__(self, maxplayers, port, map, x, y):
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(maxplayers)

        self.conn, self.addr = self.sock.accept()

        data_bytes = bytearray(str(map), 'utf8')
        self.conn.send(data_bytes)

        data_bytes = bytearray(str(x), 'utf8')
        self.conn.send(data_bytes)

        data_bytes = bytearray(str(y), 'utf8')
        self.conn.send(data_bytes)

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

        self.map = self.sock.recv(1024)

        self.start_x = self.sock.recv(1024)

        self.start_y = self.sock.recv(1024)

    def send_data(self, data):
        data_bytes = bytearray(str(data), 'utf8')
        self.sock.send(data_bytes)

    def get_data(self):
        data = self.sock.recv(1024)
        return data
