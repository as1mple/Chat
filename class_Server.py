import socket
import time

from tools import set_port, add_mysql


class Server:
    HOST: str
    PORT: str
    SOCKET: socket
    USERS = list()
    QUIT = False

    def connect(self) -> None:
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = set_port()
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.SOCKET.bind((self.HOST, self.PORT))

    def listten(self) -> None:
        print("[ Server Started ]")

        while not self.QUIT:
            try:
                data, addr = self.SOCKET.recvfrom(1024)
                timing = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
                if addr not in self.USERS:
                    self.USERS.append(addr)
                    ip, id = addr
                    add_mysql("SERVER", ip, id, data.decode(), timing)

                print("[" + addr[0] + "]=[" + str(addr[1]) + "]=[" + timing + "]/", end="")
                print(data.decode())
                for client in self.USERS:
                    if addr != client:
                        self.SOCKET.sendto(data, client)
            except Exception as e:
                print(e, "\n[ Server Stopped ]")
                self.QUIT = True

        self.SOCKET.close()
