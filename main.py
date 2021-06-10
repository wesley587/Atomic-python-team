import subprocess
import os
import time
import re
import argparse
import multiprocessing
from platform import platform
from colorama import Fore, Style
from datetime import datetime
from json import dumps

first_execution = True
system = platform().lower()

if first_execution:
    print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Checking if pyyaml module exist')
    validation = os.popen('pip3 show pyyaml').read()
    if not validation:
        print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Instaling pyyaml module')
        os.system('pip install pyyaml')
        print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Successful instaling pyyaml module')
    else:
        print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] pyyaml module already exists')

    print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Checking if requests module exist')
    validation = os.popen('pip3 show requests').read()
    if not validation:
        print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Instaling requests module')
        os.system('pip install requests')
        print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Successful instaling requests module')
    else:
        print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] requests module already exists')
    
    try:
        os.mkdir('cache')
        print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Cache folder created')
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

arguments = argparse.ArgumentParser()
arguments.add_argument('-t', '-T', action='store', dest='uuid', help='Technique number ', required=True)
arguments.add_argument('-tn', '-testnumber', '-TESTNUMBER' '-TestNumber', action='store', dest='testnumber', required=False,
                       help='Test number, to view the number of a test pass -action showdetailsbrief')
arguments.add_argument('-except_time', '-Except_Time', '-EXCEPT_TIME', action='store', dest='except_time', required=False, default=120,
                help='This parameter is used to define the max time that the program wait until generate a exception')
arguments.add_argument('--cleanup', '-c', dest='cleanup', const=True, nargs='?', help='It is used to activate the cleanup action of a testnumbe')
arguments.add_argument('-sdb', '--showdetailsbrief', dest='showdetailsbrief', const=True, nargs='?', help='See the available technique for your environment')
arguments.add_argument('-sd', '--showdetails', dest='showdetails', const=True, nargs='?', help='Show the details of a technique')
arguments.add_argument('-gp', '--getprereqs', dest='getprereqs', const=True, nargs='?', help='Case a technique save a file in your environment use this command to delete')

class atomic:
    def __init__(self):
        parse = arguments.parse_args()
        self.validate_args(parse)

        self.control = self.generate_dict(parse)
        self.except_time = parse.except_time
    
    def validate_args(self, parse):
        a = parse.showdetailsbrief
        b = parse.showdetails
        c = parse.cleanup
        d = parse.testnumber
        e = parse.getprereqs
        if a and b or a and c or a and d or a and e or b and c or b and d or b and e or c and e or e:
            print(f'[{Fore.RED + "+" + Style.RESET_ALL}] INVALID ARGS')
            exit(1)
        
    
    def cache(self):
        data = dumps(self.control)
        with open(f'cache/{self.control["date"]}.json', 'w') as file:
            print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Salving cache')
            file.write(data)
            print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Cache salved')

    
    def generate_dict(self, parse):
        values_dict = dict()
        values_dict['action'] = self.mode(parse)
        values_dict['uuid'] = parse.uuid
        values_dict['testnumber'] = parse.testnumber
        values_dict['date'] = datetime.now().strftime('%d-%m-%y %H:%M:%S')
        return values_dict
        
    def mode(self, parse):
        if parse.cleanup:
            return 'cleanup'
        elif parse.showdetails:
            return 'showdetails'
        elif parse.showdetailsbrief:
            return 'showdetailsbrief'
        elif parse.getprereqs:
            return 'getprereqs'
        elif parse.testnumber:
            return 'execult'
        else:
            print(Fore.RED + 'ERROR, PASS AN ARGUMENT', Style.RESET_ALL)
            exit(0)

    def main(self):
        self.requests()
        if self.control['action'] == 'execult':
            print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Runing: {yaml.safe_load(self.control["content"])["attack_technique"]} {yaml.safe_load(self.control["content"])["atomic_tests"][int(self.control["testnumber"]) -1]["name"]}\n')
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
            print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] {self.control["uuid"]} {self.control["action"]}')
            self.parsing()
        self.cache()

    def requests(self):
        resp = requests.get(
            f'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/{self.control["uuid"].upper()}/{self.control["uuid"].upper()}.yaml')

        if resp.status_code == 200:
            print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] {self.control["uuid"]} is valid')

            self.control['content'] = resp.content.decode('utf-8')

        else:
            print(f'[{Fore.RED + "+" + Style.RESET_ALL}] {self.control["uuid"]} is invalid')
            print(Fore.RED + 'Technique not found, try again....' + Style.RESET_ALL)
            exit(0)

    def execute(self):
        content = yaml.safe_load(self.control['content'])

        if self.control['action'] == 'execult':
            command = content['atomic_tests'][int(self.control["testnumber"]) - 1]['executor']['command'].split('\n')

        else:
            command = content['atomic_tests'][int(self.control["testnumber"]) - 1]['executor']['cleanup_command'].split('\n')

        shell = content['atomic_tests'][int(self.control["testnumber"]) - 1]['executor']['name']
        print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Runining on: {shell}')
        print(f'\n          ----------{Fore.BLUE + " OUTPUT " + Style.RESET_ALL}----------\n')
        output = [subprocess.check_output(['powershell.exe',
            x if not re.findall('#{\w*}', x) else self.input_arguments(
            x)], shell=True) if shell == 'powershell' else subprocess.check_output(
            [x if not re.findall('#{\w*}', x) else self.input_arguments(x)], shell=True) for x in
            command if
            x != '']

        [print(x.decode('windows-1252')) for x in output]


    def parsing(self):
        if self.control['action'].lower() == 'getprereqs':
            self.getprereqs()

        elif self.control['action'].lower() == 'showdetails':
            print(f'\n     ---------- {Fore.BLUE + "DETAILS" + Style.RESET_ALL} ----------\n')
            print(self.control['content'])

        elif self.control['action'].lower() == 'showdetailsbrief':
            print(f'\n     ---------- {Fore.BLUE + "DETAILS BRIEF" + Style.RESET_ALL} ----------\n')
            self.showdetailsbrief()

    def getprereqs(self):
        print(f"[{Fore.GREEN + '+' + Style.RESET_ALL}] Instaling depedencies")
        content = yaml.safe_load(self.control['content'])
        dependencies = content['atomic_tests'][int(self.control["testnumber"]) - 1]['dependencies']
        
        try:
            shell = content['atomic_tests'][int(self.control["testnumber"]) - 1]['dependency_executor_name']
        
        except:
            shell = 'powershell'
        
        print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Runining on: {shell}')
        for dependencie in dependencies:
            print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Dependencie description: {dependencie["description"]}')

            prep_comm = dependencie['prereq_command']
            get_prep_comm = dependencie['get_prereq_command']
        
            if shell == 'powershell':
        
                try:
                    subprocess.check_output(['powershell.exe', prep_comm if not re.findall('#{\w*}',
                                                            prep_comm) else self.input_arguments(
                        prep_comm)], shell=True)
                    print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Successful in running prereq_command')

        
                except:
                    print(f'[{Fore.RED + "+" + Style.RESET_ALL}] Fail in running prereq_command')
                    print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Trying run get_prereq_command')
                    [subprocess.check_output(
                        ['powershell.exe', x if not re.findall('#{\w*}', x) else self.input_arguments(x)],
                        shell=True) for x in get_prep_comm.split('\n')]
                    print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Success in running get_prereq_command')

            else:
                subprocess.check_output(
                    [prep_comm if not re.findall('#{\w*}', prep_comm) else self.input_arguments(prep_comm)],
                    shell=True)
                try:
                    subprocess.check_output([prep_comm if not re.findall('#{\w*}',
                                                            prep_comm) else self.input_arguments(
                        prep_comm)], shell=True)
                    print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Successful in running prereq_command')

        
                except:
                    print(f'[{Fore.RED + "+" + Style.RESET_ALL}] Fail in running prereq_command')
                    print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Trying run get_prereq_command')
                    [subprocess.check_output(
                        [x if not re.findall('#{\w*}', x) else self.input_arguments(x)],
                        shell=True) for x in get_prep_comm.split('\n')]
                    print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Success in running get_prereq_command')


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
        path_file = default.replace("PathToAtomicsFolder", "").replace('\\', '/')
        url = f'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/058b5c2423c4a6e9e226f4e5ffa1a6fd9bb1a90e/atomics{default}'
        resp = requests.get(url)
        local_f, local_i = path_file.rfind('/'), path_file.find('/')
        print(path_file[local_i + 1: local_f])

        try:
            dirs = os.path.join(path, path_file[local_i + 1: local_f])
            os.makedirs(dirs)
            print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Folder created: {dirs}')
        except:
            pass
        Print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] Creating file on: {path}{path_file}')
        with open(f'{path}{path_file}', 'w') as file:
            file.write(resp.content.decode('utf-8'))
        path_file = path_file.replace("/", "\\")
        return f'{path}{path_file}'

    def showdetailsbrief(self):
        yaml_contet = yaml.safe_load(self.control['content'])['atomic_tests']
        [print(f'[{Fore.BLUE + f"{c + 1}" + Style.RESET_ALL}] {yaml_contet[c]["name"]}') for c in range(0, len(yaml_contet)) if
            system.split('-')[0] in yaml_contet[c]['supported_platforms']]
        print('')
if __name__ == '__main__':
    start = atomic()
    start.main()
