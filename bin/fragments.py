body_script = r'''import subprocess
import os
import time
import re
import argparse
import multiprocessing
from platform import platform
from datetime import datetime
from json import dumps
import socket
import sys
import re
from json import loads


first_execution = False
system = platform().lower()

if first_execution:
    print(f'[Info] Checking if pyyaml module exist')
    validation = os.popen('pip3 show pyyaml').read()
    if not validation:
        print(f'[*] Instaling pyyaml module')
        os.system('pip install pyyaml')
        print(f'[Info] Successful instaling pyyaml module')
    else:
        print(f'[Info] pyyaml module already exists')

    print(f'[Info] Checking if requests module exist')
    validation = os.popen('pip3 show requests').read()
    if not validation:
        print(f'[*] Instaling requests module')
        os.system('pip install requests')
        print(f'[Info] Successful instaling requests module')
    else:
        print(f'[Info] requests module already exists')
    
    try:
        os.mkdir('cache')
        print(f'[Info] Cache folder created')
    except:
        pass
    try:
        os.mkdir('PathToAtomicsFolder')
    except:
        pass



    with open(os.path.basename(__file__), 'r') as f:
        _content = f.read()
        f.close()

    with open(os.path.basename(__file__), 'w') as f:
        _content = _content.replace('first_execution = True', 'first_execution = False')
        f.write(_content)
        f.close()

import requests
import yaml


class atomic:
    def __init__(self, buffer):
        self.control = loads(buffer)
        print(self.control)
        self.except_time = self.control['except_time']
     
    def cache(self):
        data = dumps(self.control)
        with open(f'cache/{self.control["date"]}.json', 'w') as file:
            print(f'[*] Salving cache')
            file.write(data)
            print(f'[Info] Cache salved')
        

    def main(self):
        self.requests()
        if self.control['action'] == 'execute':
            print(f'[*] Runing: {yaml.safe_load(self.control["content"])["attack_technique"]} {yaml.safe_load(self.control["content"])["atomic_tests"][int(self.control["testnumber"]) -1]["name"]}\n')
            initial_time = time.time()
            mult = multiprocessing.Process(target=self.execute)
            mult.start()

            while True:
                if int(time.time() - initial_time) >= self.except_time:
                    mult.terminate()
                if not mult.is_alive():
                    break
                time.sleep(1)
        elif self.control['action']:
            print(f'[Info] {self.control["uuid"]} {self.control["action"]}')
            self.parsing()
        self.cache()
        

    def requests(self):
        resp = requests.get(
            f'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/{self.control["uuid"].upper()}/{self.control["uuid"].upper()}.yaml')

        if resp.status_code == 200:
            print(f'[Info] {self.control["uuid"]} is valid')

            self.control['content'] = resp.content.decode('utf-8')

        else:
            print(f'[Info] {self.control["uuid"]} is invalid')
            print('[Error] Technique not found, try again....')
            client_socket.send('[Error] Technique not found, try again....').encode()
            exit(0)

    def execute(self):
        content = yaml.safe_load(self.control['content'])

        if self.control['action'] == 'execute':
            command = content['atomic_tests'][int(self.control["testnumber"]) - 1]['executor']['command'].split('\n')

        else:
            command = content['atomic_tests'][int(self.control["testnumber"]) - 1]['executor']['cleanup_command'].split('\n')

        shell = content['atomic_tests'][int(self.control["testnumber"]) - 1]['executor']['name']
        print(f'[Info] Runining on: {shell}')
        client_output = '\n          ---------- OUTPUT ----------\n'

        output = list()
        for x in command:
            if x:
                
                if not re.findall('#{\w*}', x):
                    if shell == 'powershell':
                        x = ('powershell.exe ' + x).split()
                        output.append(subprocess.check_output(x))
                    else:
                        print(x)
                        x = x.split()
                        output.append(subprocess.check_output(x, shell=True))
                else:
                    if shell == 'powershell':
                        x = ('powershell.exe ' + self.input_arguments(x)).split()
                        output.append(subprocess.check_output(x))
                    else:
                        x = self.input_arguments(x).split()
                        output.append(subprocess.check_output([self.input_arguments(x)], shell=True))

        [client_socket.send((client_output + x.decode('windows-1252')).encode()) for x in output]
        

    def parsing(self):
        if self.control['action'].lower() == 'getprereqs':
            self.getprereqs()
        else:
            client_socket.send(b'[ERROR] Exception, try again...')
            
    def getprereqs(self):
        print(f"[*] Instaling depedencies")
        content = yaml.safe_load(self.control['content'])
        dependencies = content['atomic_tests'][int(self.control["testnumber"]) - 1]['dependencies']
        
        try:
            shell = content['atomic_tests'][int(self.control["testnumber"]) - 1]['dependency_executor_name']
        
        except:
            shell = 'powershell'
        
        print(f'[Info] Runining on: {shell}')
        for dependencie in dependencies:
            print(f'[Info] Dependencie description: {dependencie["description"]}')

            prep_comm = dependencie['prereq_command']
            get_prep_comm = dependencie['get_prereq_command']
        
            if shell == 'powershell':
        
                try:
                    subprocess.check_output(['powershell.exe', prep_comm if not re.findall('#{\w*}',
                                                            prep_comm) else self.input_arguments(
                        prep_comm)], shell=True)
                    print(f'[Info] Successful in running prereq_command')

        
                except:
                    print(f'[Error] Fail in running prereq_command')
                    print(f'[Info] Trying run get_prereq_command')
                    [subprocess.check_output(
                        ['powershell.exe', x if not re.findall('#{\w*}', x) else self.input_arguments(x)],
                        shell=True) for x in get_prep_comm.split('\n')]
                    print(f'[Info] Success in running get_prereq_command')

            else:
                subprocess.check_output(
                    [prep_comm if not re.findall('#{\w*}', prep_comm) else self.input_arguments(prep_comm)],
                    shell=True)
                try:
                    subprocess.check_output([prep_comm if not re.findall('#{\w*}',
                                                            prep_comm) else self.input_arguments(
                        prep_comm)], shell=True)
                    print(f'[Info] Successful in running prereq_command')

        
                except:
                    print(f'[Error] Fail in running prereq_command')
                    print(f'[Info] Trying run get_prereq_command')
                    [subprocess.check_output(
                        [x if not re.findall('#{\w*}', x) else self.input_arguments(x)],
                        shell=True) for x in get_prep_comm.split('\n')]
                    print(f'[Info] Success in running get_prereq_command')


    def input_arguments(self, command):
        input_arguments = yaml.safe_load(self.control['content'])['atomic_tests'][int(self.control["testnumber"]) - 1]['input_arguments']
        parser = re.findall('#{\w*}', command)
        a = [input_arguments[x.replace('#{', '').replace('}', '')]['default'] for x in parser]

        for ex, de in zip(parser, a):
            command = command.replace(ex, de if not 'PathToAtomicsFolder' in de else self.PathToAtomicsFolder(de))
        return command

    def PathToAtomicsFolder(self, default):
        path = subprocess.check_output(['cd'], shell=True)
        path = path.decode('utf-8').replace('\r', '').replace('\n', '')
        path_file = default.replace('\\', '/')
        url = f'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics{default.replace("PathToAtomicsFolder", "")}'
        print(url)
        resp = requests.get(url)
        local_f = path_file.rfind('/')
        try:
            dirs = os.path.join(path, path_file[: local_f])
            os.makedirs(dirs)
            print(f'[Info] Folder created: {dirs}')
        except:
            pass
        print(f'[*] Creating file on: {path}{path_file}')
        with open(f'{path}{path_file}', 'w') as file:
            file.write(resp.content.decode('utf-8'))
        path_file = path_file.replace("/", "\\")
        return f'{path}{path_file}'


if __name__ == '__main__':
    ip = 'IP_SERVER'
    port = 'PORT_SERVER'

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    buffer = client_socket.recv(1028).decode()
    print(f'[INFO] We receiv: {buffer}')

    parser = buffer.replace('-', '.-').split('.')
    start = atomic(buffer)
    start.main()
'''