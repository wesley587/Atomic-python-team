import subprocess
import os
import time
import re
import argparse
import multiprocessing
from platform import platform
from colorama import Fore, Style

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
arguments.add_argument('-testnumber', '-TESTNUMBER' '-TestNumber', action='store', dest='testnumber', required=False,
                       help='Test number, to view the number of a test pass -action showdetailsbrief')
arguments.add_argument('-except_time', '-Except_Time', '-EXCEPT_TIME', action='store', dest='except_time', required=False, default=120,
                help='This parameter is used to define the max time that the program wait until generate a exception')
arguments.add_argument('--cleanup', '-c', dest='cleanup', const=True, nargs='?')
arguments.add_argument('-sdb', '--showdetailsbrief', dest='showdetailsbrief', const=True, nargs='?')
arguments.add_argument('-sd', '--showdetails', dest='showdetails', const=True, nargs='?')
arguments.add_argument('-gp', '--getprereqs', dest='getprereqs', const=True, nargs='?')
parse = arguments.parse_args()

class atomic:
    def __init__(self):

        if not re.match(r'(T|t)\d+(.\d+|)$', parse.uuid.upper()):
            print(Fore.RED + f'NOT FOUND {parse.uuid} TECHNIQUE' + Style.RESET_ALL)
        self.control = self.generate_dict()
        self.testnumber = parse.testnumber
        self.content = {}
        self.except_time = parse.except_time
    
    def generate_dict(self):
        values_dict = dict()
        values_dict['action'] = self.mode()
        values_dict['uuid'] = parse.uuid
        if parse.testnumber:
            values_dict['testnumber'] = parse.testnumber
        return values_dict
        
        
    
    def mode(self):
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

    # Inicio
    def main(self):
        self.requests()
        if self.testnumber:
            print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}]{yaml.safe_load(self.content)["attack_technique"]} {yaml.safe_load(self.content)["atomic_tests"][int(self.testnumber) -1]["name"]}\n')
        else:
            print(f'[{Fore.GREEN + "+" + Style.RESET_ALL}] {yaml.safe_load(self.content)["attack_technique"]}\n')
        print(self.control)
        if self.control['action'] == 'execult':
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
            self.parsing()

    def requests(self):
        resp = requests.get(
            f'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/{self.control["uuid"]}/{self.control["uuid"]}.yaml')

        if resp.status_code == 200:
            self.content = resp.content.decode('utf-8')

        else:
            print('Technique not found, try again....')
            exit()

    def execute(self):
        content = yaml.safe_load(self.content)


        if self.control['action'] == 'execult':
            command = content['atomic_tests'][int(self.testnumber) - 1]['executor']['command'].split('\n')

        else:
            command = content['atomic_tests'][int(self.testnumber) - 1]['executor']['cleanup_command'].split('\n')

        shell = content['atomic_tests'][int(self.testnumber) - 1]['executor']['name']

        command_exit = [subprocess.check_output(['powershell.exe',
            x if not re.findall('#{\w*}', x) else self.input_arguments(
            x)], shell=True) if shell == 'powershell' else subprocess.check_output(
            [x if not re.findall('#{\w*}', x) else self.input_arguments(x)], shell=True) for x in
            command if
            x != '']

        [print(x.decode('windows-1252')) for x in command_exit]


    def parsing(self):
        if self.control['action'].lower() == 'getprereqs':
            self.getprereqs()

        elif self.control['action'].lower() == 'showdetails':
            print(self.content)

        elif self.control['action'].lower() == 'showdetailsbrief':
            self.showdetailsbrief()

    def getprereqs(self):
        content = yaml.safe_load(self.content)
        dependencies = content['atomic_tests'][int(self.testnumber) - 1]['dependencies']
        
        try:
            shell = content['atomic_tests'][int(self.testnumber) - 1]['dependency_executor_name']
        
        except:
            shell = 'powershell'
        
        for dependencie in dependencies:
            prep_comm = dependencie['prereq_command']
            get_prep_comm = dependencie['get_prereq_command']
        
            if shell == 'powershell':
        
                try:
                    subprocess.check_output(['powershell.exe', prep_comm if not re.findall('#{\w*}',
                                                            prep_comm) else self.input_arguments(
                        prep_comm)], shell=True)
        
                except:
                    [subprocess.check_output(
                        ['powershell.exe', x if not re.findall('#{\w*}', x) else self.input_arguments(x)],
                        shell=True) for x in get_prep_comm.split('\n')]
                    print(get_prep_comm)
            else:
                subprocess.check_output(
                    [prep_comm if not re.findall('#{\w*}', prep_comm) else self.input_arguments(prep_comm)],
                    shell=True)

    def input_arguments(self, command):
        input_arguments = yaml.safe_load(self.content)['atomic_tests'][int(self.testnumber) - 1]['input_arguments']
        parser = re.findall('#{\w*}', command)
        a = [input_arguments[x.replace('#{', '').replace('}', '')]['default'] for x in parser]

        for ex, de in zip(parser, a):
            command = command.replace(ex, de if not 'PathToAtomicsFolder' in de else self.PathToAtomicsFolder(de))
        return command

    def PathToAtomicsFolder(self, default):
        path = subprocess.check_output(['cd'], shell=True)
        path = path.decode('utf-8').replace('\r', '').replace('\n', '') + '/cache'
        path_file = default.replace("PathToAtomicsFolder", "").replace('\\', '/')
        url = f'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/058b5c2423c4a6e9e226f4e5ffa1a6fd9bb1a90e/atomics{default}'
        resp = requests.get(url)
        local_f, local_i = path_file.rfind('/'), path_file.find('/')
        print(path_file[local_i + 1: local_f])

        try:
            dirs = os.path.join(path, path_file[local_i + 1: local_f])
            print(dirs)
            os.makedirs(dirs)
        
        except:
            pass
        
        with open(f'{path}{path_file}', 'w') as file:
            file.write(resp.content.decode('utf-8'))
            file.close()
        path_file = path_file.replace("/", "\\")
        return f'{path}{path_file}'

    def showdetailsbrief(self):
        yaml_contet = yaml.safe_load(self.content)['atomic_tests']
        [print(f'[{c + 1}] {yaml_contet[c]["name"]}') for c in range(0, len(yaml_contet)) if
            system.split('-')[0] in yaml_contet[c]['supported_platforms']]

if __name__ == '__main__':
    start = atomic()
    start.main()


