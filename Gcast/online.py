import socket
import threading
import time


class StopThread(StopIteration):
    pass


threading.SystemExit = SystemExit, StopThread


class Server(threading.Thread):
    def __init__(self, maxplayers, port, map, x, y, delegate_data):
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(maxplayers)

        self.max_data = 2048

        self.conn, self.addr = self.sock.accept()

        map = [[1, 5, 5, 5, 5, 5, 5, 5, 5, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 2, 0, 0, 2, 2, 0, 1], [1, 0, 2, 2, 0, 0, 2, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 3, 3, 0, 0, 0, 0, 3, 3, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 2, 2, 0, 0, 2, 2, 0, 1],
            [1, 0, 2, 2, 0, 0, 2, 2, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 4, 4, 4, 4, 4, 4, 4, 1]]

        map = tuple(tuple(i) for i in map)

        data_bytes = bytearray(str(map), 'utf8')
        self.conn.send(data_bytes)

        coords = "150!150!100!0!0!"

        self.send_data(coords)
        data_bytes = bytearray(str(coords), 'utf8')

        self.conn.send(data_bytes)
        time.sleep(1)

        self.data = [1440, 1440, 100, 0, 0]

        self.delegate_data = delegate_data

        self.__flag = threading.Event()  # The flag used to pause the thread
        self.__flag.set()  # Set to True
        self.__running = threading.Event()  # Used to stop the thread identification
        self.__running.set()  # Set running to True

        threading.Thread.__init__(self)

    def send_data(self, data):
        data_bytes = bytearray(str(data), 'utf8')
        self.conn.send(data_bytes)

    def get_data(self):
        try:
            data_raw = self.conn.recv(self.max_data)
            data_raw = data_raw.decode('utf8')
            data_splited = data_raw.split("!")
            x, y, hp, shoot, move = float(data_splited[0]), float(data_splited[1]), int(
                float(data_splited[2])), int(float(data_splited[3])), int(float(data_splited[4]))
            data = (x, y, hp, shoot, move)
            return data
        except:
            return (0, 0, 0, 0, 0)

    def close_server(self):
        self.sock.close()

    # everlasting loop def, that just rerenders everything
    def run(self):

        # time.sleep(1)
        while self.__running.isSet():
            self.__flag.wait()
            time.sleep(0.03)
            x, y, hp, shoot, move = self.delegate_data()
            coords = str(x) + "!" + str(y) + "!" + str(hp) + \
                "!" + str(shoot) + "!" + str(move) + "!"
            self.send_data(coords)
            self.data = self.get_data()
        self.close_server()

    # defs that are needed to control the thread: pause render,resume render,stop render process

    def pause(self):
        self.__flag.clear()  # Set to False to block the thread

    def resume(self):
        self.__flag.set()  # Set to True, let the thread stop blocking

    def stop(self):
        self.__flag.set()  # Resume the thread from the suspended state, if it is already suspended
        self.__running.clear()  # Set to False


class Client(threading.Thread):
    def __init__(self, ip, port, delegate_data):
        self.sock = socket.socket()
        self.sock.connect((str(ip), port))
        self.max_data = 2048

        self.str_map = self.sock.recv(self.max_data)
        self.map = eval(self.str_map)
        self.data = [1540, 1440, 100, 0, 0]
        self.start_x, self.start_x, hp, shoot, move = self.get_data()

        self.delegate_data = delegate_data

        self.__flag = threading.Event()  # The flag used to pause the thread
        self.__flag.set()  # Set to True
        self.__running = threading.Event()  # Used to stop the thread identification
        self.__running.set()  # Set running to True

        threading.Thread.__init__(self)

    def send_data(self, data):
        data_bytes = bytearray(str(data), 'utf8')
        self.sock.send(data_bytes)

    def get_data(self):
        data_raw = self.sock.recv(self.max_data)
        data_raw = data_raw.decode('utf8')
        data_splited = data_raw.split("!")
        x, y, hp, shoot, move = float(data_splited[0]), float(data_splited[1]), int(
            float(data_splited[2])), int(float(data_splited[3])), int(float(data_splited[4]))
        data = (x, y, hp, shoot, move)
        return data

    # everlasting loop def, that just rerenders everything
    def run(self):
        import time

        time.sleep(1)

        while self.__running.isSet():
            self.__flag.wait()
            time.sleep(0.03)
            x, y, hp, shoot, move = self.delegate_data()
            coords = str(x) + "!" + str(y) + "!" + str(hp) + \
                "!" + str(shoot) + "!" + str(move) + "!"
            self.send_data(coords)
            self.data = self.get_data()

    # defs that are needed to control the thread: pause render,resume render,stop render process
    def pause(self):
        self.__flag.clear()  # Set to False to block the thread

    def resume(self):
        self.__flag.set()  # Set to True, let the thread stop blocking

    def stop(self):
        self.__flag.set()  # Resume the thread from the suspended state, if it is already suspended
        self.__running.clear()  # Set to False
