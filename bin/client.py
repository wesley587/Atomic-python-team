import subprocess
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

ip = '0.0.0.0'
port = 20000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))
buffer = client_socket.recv(1028).decode()
print(buffer)

parser = buffer.replace('-', '.-').split('.')



class atomic:
    def __init__(self):
        self.control = self.generate_control(buffer)
        print(self.control)
        self.except_time = self.control['except_time']
    
    def generate_control(self, buffer):
        args = {'date': datetime.now().strftime('%d-%m-%Y -%H-%M-%S'),'except_time': 120}
        for x in parser:
            if '-tn' in x:
                x = x.replace('-tn', 'testnumber')
                print(x)
                args['action'] = 'execute'
            else:
                x = self.check_command_name(x)
            if x:
                if len(x.split()) > 1:
                    x = x.split() 
                    args[x[0]] = x[1]
                else:
                    args['action'] = x
        return args
    
    def check_command_name(self, arg):
        commands = {'uuid': ['-t', '--testnumber', '-T'],
                'testnuber': ['-tn', '--testnumber'],
                'except_time': ['-ex', '--except_time'],
                'cleanup': ['-c', '--cleanup'],
                'showdetailsbrief': ['-sdb', '--showdetailsbrief'],
                'showdetails': ['-sd', '--showdetails'],
                'getprereqs': ['-gp', '--getprereqs']}
        for k, v in commands.items():
            for c in v:
                if c in arg:
                    return arg.replace(c, k)
    
    def validate_args(self, parse):
        a = parse.showdetailsbrief
        b = parse.showdetails
        c = parse.cleanup
        d = parse.testnumber
        e = parse.getprereqs
        if a and b or a and c or a and d or a and e or b and c or b and d or b and e or c and e:
            print(f'[Error] INVALID ARGS')
            exit(1)
        
    
    def cache(self):
        data = dumps(self.control)
        with open(f'cache/{self.control["date"]}.json', 'w') as file:
            print(f'[*] Salving cache')
            file.write(data)
            print(f'[Info] Cache salved')

    
    def generate_dict(self, parse):
        values_dict = dict()
        values_dict['action'] = self.mode(parse)
        values_dict['uuid'] = args['-t']
        values_dict['testnumber'] = parse.testnumber
        values_dict['date'] = datetime.now().strftime('%d-%m-%y %H-%M-%S')
        return values_dict
        
    def mode(self, parse):
        for k, v in parse.items():
            if parse.cleanup:
                return 'cleanup'
            elif parse.showdetails:
                return 'showdetails'
            elif parse.showdetailsbrief:
                return 'showdetailsbrief'
            elif parse.getprereqs:
                return 'getprereqs'
            elif parse.testnumber:
                return 'execute'
        else:
            print('[Error] ERROR, PASS AN ARGUMENT')
            exit(0)

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
            exit(0)

    def execute(self):
        content = yaml.safe_load(self.control['content'])

        if self.control['action'] == 'execute':
            command = content['atomic_tests'][int(self.control["testnumber"]) - 1]['executor']['command'].split('\n')

        else:
            command = content['atomic_tests'][int(self.control["testnumber"]) - 1]['executor']['cleanup_command'].split('\n')

        shell = content['atomic_tests'][int(self.control["testnumber"]) - 1]['executor']['name']
        print(f'[Info] Runining on: {shell}')
        print(f'\n          ---------- OUTPUT ----------\n')

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


        [print(x.decode('windows-1252')) for x in output]


    def parsing(self):
        if self.control['action'].lower() == 'getprereqs':
            self.getprereqs()

        elif self.control['action'].lower() == 'showdetails':
            print(f'\n     ---------- DETAILS ----------\n')
            print(self.control['content'])

        elif self.control['action'].lower() == 'showdetailsbrief':
            print(f'\n     ---------- DETAILS BRIEF ----------\n')
            self.showdetailsbrief()

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

    def showdetailsbrief(self):
        yaml_contet = yaml.safe_load(self.control['content'])['atomic_tests']
        [print(f'[{c + 1}] {yaml_contet[c]["name"]}') for c in range(0, len(yaml_contet)) if
            system.split('-')[0] in yaml_contet[c]['supported_platforms']]
        print('')
if __name__ == '__main__':
    start = atomic()
    start.main()
