import socket
import threading
import time

from tools import set_port_key


class Client:
    SHUTDOWN: bool = False
    JOIN: bool = False
    KEY: int
    HOST: str
    PORT: int
    SOCKET: socket
    ALIAS: str
    SERVER: tuple
    NAME_THREAD: str

    def listen(self) -> None:
        while not self.SHUTDOWN:
            if not self.JOIN:
                self.SOCKET.sendto(("[" + self.ALIAS + "] => join chat ").encode("utf-8"), self.SERVER)
                self.JOIN = True
            else:
                try:
                    message = input()
                    crypt = ""
                    for i in message:
                        crypt += chr(ord(i) ^ self.KEY)
                    message = crypt
                    if message != "":
                        self.SOCKET.sendto(("[" + self.ALIAS + "] :: " + message).encode("utf-8"), self.SERVER)
                    time.sleep(0.2)
                except:
                    self.SOCKET.sendto(("[" + self.ALIAS + "] <= left chat ").encode("utf-8"), self.SERVER)
                    self.SHUTDOWN = True

    def receving(self, name: str, sock: socket) -> None:
        while not self.SHUTDOWN:
            try:
                while True:
                    data, addr = sock.recvfrom(1024)
                    decrypt = ""
                    flag = False
                    for i in data.decode("utf-8"):
                        if i == ":":
                            flag = True
                            decrypt += i
                        elif not flag or i == " ":
                            decrypt += i
                        else:
                            decrypt += chr(ord(i) ^ self.KEY)
                    print(decrypt)
                    self.NAME_THREAD = name
                    time.sleep(0.2)
            except:
                pass

    def connect(self) -> None:
        self.PORT, self.KEY = set_port_key()
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.SERVER = ("127.0.1.1", self.PORT)
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.SOCKET.bind((self.HOST, False))
        self.SOCKET.setblocking(False)
        print('Setup Server...')
        time.sleep(1)
        self.ALIAS = input('Enter name: ')
        rT = threading.Thread(target=self.receving, args=("RecvThread", self.SOCKET))
        rT.start()
        self.listen()
        rT.join()
        self.SOCKET.close()
