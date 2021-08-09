from socket import AF_INET, SOCK_STREAM, socket
import os
from datetime import datetime
from json import dumps
from threading import Thread
import argparse
from bin.fragments import body_script
from bin.tools.generate_control import generate_atomic_map
from bin.tools.generate_control import generate_control
from bin.tools.get_content import request
from bin.tools.showdetailsbrief import showdetailsbrief


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
        server = socket(AF_INET, SOCK_STREAM)
        server.bind((self.control['ip'], self.control['port']))
        print(f'[INFO] Listen on: {self.control["ip"]}/{self.control["port"]}')
        server.listen(5)
        
        while True:
            client_socket, addr = server.accept()
            print(f'[INFO] Client addres: {addr[0]}/{addr[1]}')
            
            client_handler = Thread(target=self.client_handler, args=(client_socket, ))
            client_handler.start()
        
    
    def create_agent(self):
        print('create agent')
        with open(f'{self.control["path"]}/client.py', 'w') as file:
            script = body_script.replace("'IP_SERVER'", f"'{self.control['ip']}'").replace("'PORT_SERVER'", f"{self.control['port']}")
            file.write(script)
        
    def client_handler(self, client_socket):
        print('------- To break send stop to sdtin --------')
        while True:
            atomic = input('[INFO] Atomic techinique: ')
            if not atomic or 'stop' in atomic:
                break
            try:
                control = generate_atomic_map(atomic)
                print(control)
                
            except:
                print('[ERROR] Exception, ERROR!')
                break
    
            action = control['action']
            if action == 'showdetailsbrief':
                control['content'] = request(control)
                brief = showdetailsbrief(control)
                print('----- Showdetailsbrief -----\n')
                for x in brief:
                    print(x)
                print()
                
                
            elif action == 'showdetails':
                control['content'] = request(control)
                print('--- Showdetails ---')
                control['action'] = 'showdetails'
                print(control['content'])
            
            if not 'show' in control['action']:
                try:
                    client_socket.send(dumps(control).encode())
                    buffer = client_socket.recv(1028).decode().split('\n')
                    print(f'[INFO] We receive: ')
                    for x in buffer:
                        print(x)
                except:
                    print(f'[ERROR] Client {addr} is off.')
                    break
            
            print('-'*50)


if __name__ == '__main__':
    first_execution = True
    if first_execution:
        print(f'[Info] Checking if pyyaml module exist')
        validation = os.popen('pip3 show pyyaml').read()
        if not validation:
            print(f'[*] Instaling pyyaml module')
            os.system('pip install pyyaml')
            print(f'[Info] Successful instaling pyyaml module')
        else:
            print(f'[Info] pyyaml module already exists')
            
        with open(os.path.basename(__file__), 'r') as file:
            content = file.read()
            content = content.replace('first_execution = False', 'first_execution = True')
        
        with open(os.path.basename(__file__), 'w') as file:
            file.write(content)
    import yaml
    
    
    args = argparse.ArgumentParser()
    args.add_argument('-l', '--listen', dest='listen', help='listen mode', default=True, nargs='?', const=True)
    args.add_argument('-ip', '--ip', dest='ip', default='0.0.0.0', type=str, help='Server ip')
    args.add_argument('-c', '--create', dest='create', help='Creat an agente', default=False, nargs='?', const=True)
    args.add_argument('-p', '--port', dest='port', default=45000, type=int, help='Port that the server will be listening')
    args.add_argument('-ph', '--path', dest='path', default=os.getcwd(), help='Path to creat a client')
    parse = args.parse_args()
    start = server()
    start.main()


