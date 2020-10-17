import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
# The above code is just for reference, will be deleted upon completion


class Server:

    def __init__(self, host, port):
        """
        Initializes the server object
        Creates an address tuple from the given host and port
        :param host: The IP of the server, will be received form the GUI
        :param port: The port that the socket will be connecting on, will be received from GUI
        """
        self.HOST = host  # the host IP
        self.PORT = port  # the host port
        self.address = (self.HOST, self.PORT)  # a tuple used by the socket object
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # the server socket object
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # allows the server and client to reconnect
        self.client = None  # just a placeholder for now, becomes the client when a successfully connected
        self.c_address = None  # just a placeholder for now, becomes the client when a successfully connected

    def initialize_connection(self):
        """
        Binds the server socket to the address
        Attempts to connect to the client
        Once connected self.client refers to the client socket
        self.c_address is the address of the client
        :return: nothing
        """
        self.server.bind(self.address)  # binds the server object to the HOST and PORT
        self.server.listen(5)  # waits for a connection from the client
        self.client, self.c_address = self.server.accept()  # when a successful connection is made


    def end_connection(self):
        """
        cleans up the sockets when we are done with them, leaving them open can cause problems
        :return: nothing
        """

        self.server.close()
        self.client.close()
