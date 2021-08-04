from socket import AF_INET, SOCK_STREAM, socket
from datetime import datetime
from json import dumps
from client_tools.generate_control import generate_control
from threading import Thread


def client_handler(client_socket):

    atomic = input('[INFO] Atomic techinique: ')
    try:
        control = dumps(generate_control(atomic)).encode()
    except:
        print('[ERROR] Exception, ERROR!')
    else:
        try:
            client_socket.send(control)
        except:
            print(f'[ERROR] Client {addr} is off.')
            return ''
        else:
            buffer = client_socket.recv(1028).decode().split('\n')
            print(f'[INFO] We receive: ', end='')
            print(buffer)
    return ''
    
ip = '0.0.0.0'
port = 45000
server = socket(AF_INET, SOCK_STREAM)
server.bind((ip, port))
server.listen(5)

print(f'[INFO] Lisening on: {ip}/{port}')
while True:
    client_socket, addr = server.accept()
    client_handler = Thread(target=client_handler, args=(client_socket, ))
    client_handler.start()
