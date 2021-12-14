import socket
import threading
import time


class StopThread(StopIteration): pass


threading.SystemExit = SystemExit, StopThread


class Server(threading.Thread):
    def __init__(self, maxplayers, port, map, x, y, delegate_data):
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(maxplayers)

        self.max_data = 2048

        self.conn, self.addr = self.sock.accept()

        data_bytes = bytearray(str(map), 'utf8')
        self.conn.send(data_bytes)

        coords = [1540, 1440, 2]
        data_bytes = bytearray(str(coords), 'utf8')
        # print(data_bytes)
        self.conn.send(data_bytes)
        self.data = [x, y, 2]

        self.delegate_data = delegate_data

        self.__flag = threading.Event()  # The flag used to pause the thread
        self.__flag.set()  # Set to True
        self.__running = threading.Event()  # Used to stop the thread identification
        self.__running.set()  # Set running to True

        threading.Thread.__init__(self)

    def send_data(self, data):
        # print("i send data")
        data_bytes = bytearray(str(data), 'utf8')
        self.conn.send(data_bytes)

    def get_data(self):
        data = self.conn.recv(self.max_data)
        data = eval(data)
        print(data)
        return data

    def close_server(self):
        self.sock.close()

    # everlasting loop def, that just rerenders everything
    def run(self):
        time.sleep(0.5)
        while self.__running.isSet():
            self.__flag.wait()
            time.sleep(0.1)
            x, y, hp = self.delegate_data()
            coords = (x, y, hp)
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


class Client(threading.Thread):
    def __init__(self, ip, port, delegate_data):
        self.sock = socket.socket()
        self.sock.connect((str(ip), port))
        self.max_data = 2048

        self.str_map = self.sock.recv(self.max_data)
        self.map = eval(self.str_map)

        self.start_x, self.start_y, self.start_hp = eval(self.sock.recv(self.max_data))
        #print(self.start_x, self.start_y)
        self.delegate_data = delegate_data

        self.__flag = threading.Event()  # The flag used to pause the thread
        self.__flag.set()  # Set to True
        self.__running = threading.Event()  # Used to stop the thread identification
        self.__running.set()  # Set running to True

        self.data = [1440, 1440, 2]

        threading.Thread.__init__(self)

    def send_data(self, data):
        data_bytes = bytearray(str(data), 'utf8')
        self.sock.send(data_bytes)

    def get_data(self):
        data = eval(self.sock.recv(self.max_data))
        print(data)
        return data

    # everlasting loop def, that just rerenders everything
    def run(self):
        import time

        time.sleep(1)
        #print("ok")

        while self.__running.isSet():
            self.__flag.wait()
            time.sleep(0.1)
            x, y, hp = self.delegate_data()
            coords = (x, y, hp)
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
