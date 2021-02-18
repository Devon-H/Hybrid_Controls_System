import socket
import queue

# the HOST and PORT are just part of the test code at the bottom, ignore for purposes of Client class
HOST = '127.0.0.1'
PORT = 9999


class NoConnection(Exception):
    """
    A custom exception raised when attempting to utilize the client when no connection has been made
    """

    def __str__(self):
        return "NoConnection"


class ConnectionFailure(Exception):
    """
    A custom exception raised when the client fails to connect to a server
    """
    def __str__(self):
        return "ConnectionFailure"


class Client:

    def __init__(self, host, port):
        """
        Initializes the client object
        Creates an address tuple from the given host and port
        :param host: The IP of the client, IS HARD CODED, NEED TO CHANGE IF IP OF SERVER CHANGES
        :param port: The port that the socket will be connecting on. Hard coded to 9999
        """
        self.host = host  # The ip of the server that the client connects to
        self.port = port  # The port the client connects on
        self.address = (self.host, self.port)  # A tuple formed from the given host and ip, used for socket object
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Initializes the client socket
        self.feedback_queue = queue.Queue()  # A queue used to store the incoming instructions from the server

    def initialize_connection(self):
        """
        Connects the the server. The server must be running first in order to make this work
        """
        try:
            self.client.connect(self.address)   # connects the client to the server, server must be running first
        except WindowsError:  # this is the error generated by a invalid address or a timed out connection attempt
            raise ConnectionFailure

    def end_connection(self):
        """
        Cleans up the socket objects
        """
        self.client.close()  # cleans up the socket

    def send_states(self, data):
        """
        Send state to server, used when input is received from control software
        :param data: The state being sent
        :return: nothing
        """
        try:
            self.client.sendall((data+" ").encode())  # send off the data
        except WindowsError: # his will fail if there is no connection initialized
            raise NoConnection

    def receive_states(self):
        """
        Receive data from server and tokenize it, then add it to the instruction queue
        :return: nothing
        """
        try:
            data = self.client.recv(1024).decode()  # receives data which it decodes() into a string
            data = data.split()
            print(data)
            for i in range(0, int(len(data) / 2), 2):
                token = (data[i], data[i + 1])
                print(token)
                self.feedback_queue.put(token)
        except Exception as e:
            print(f'Client receive_states: {e}')
            raise NoConnection



if __name__ == '__main__':
    """
        this is just test code, good for troubleshooting
    """
    c = Client(HOST, PORT)
    c.initialize_connection()
    while True:

        c.receive_states()

        while c.feedback_queue.qsize() > 0:
            token = c.feedback_queue.get()
            d = token[0]
            b = token[1]
            if d == 'connected' and b == 'false':
                exit()
            print(f'{d} {b}')
        c.send_states(f'{d} {b}')
