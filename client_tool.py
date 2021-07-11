import socket
import pickle


def trade_with_server(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    print(data)
    data = pickle.dumps(data)
    print(data)
    sock.send(data)
    data_new = sock.recv(32768)
    print(data_new)
    return pickle.loads(data_new)


def stop():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.send(pickle.dumps([{'name': 'stop'}]))
    data_new = list(sock.recv(16384))
    if (data_new == [255, 255, 255]):
        print("succesfully stopped")


ip = 'localhost'
port = 55000


def get():
    data = pickle.dumps([{'x': 26, 'y': 12, 'param': 32}, {'x': 22, 'y': 17, 'param': 11}])
    data_new = trade_with_server(data)
    return data_new
