##################################################################
# Atomic-python-team by: wesley587(https://github.com/wesley587) #
##################################################################


import subprocess
import os
import time
import re
import argparse
import multiprocessing
import platform

first_execution = True
system = platform.platform().lower()

if first_execution:

    os.system('pip install pyyaml')
    os.system('pip install requests')

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
arguments.add_argument('-action', '-ACTION', '-Action', action='store', dest='action', required=False, help='''Actions:
getprereqs (Install all prereqs of a test)
showdetails (Show details of a technique)
showdetailsbrief (Show the avaliable tests)
clenup (Execute the clenup command)
''')
arguments.add_argument('-except_time', '-Except_Time', '-EXCEPT_TIME', action='store', dest='except_time', required=False, default=120,
                help='This parameter is used to define the max time that the program wait until generate a exception')

parse = arguments.parse_args()

if re.match(r'T\d+(.\d+|)$', parse.uuid.upper()):
    
    class atomic:
        def __init__(self):
            self.uuid = parse.uuid
            self.testnumber = parse.testnumber
            self.action = parse.action
            self.content = {}
            self.except_time = parse.except_time

        def main(self):
            self.requests()
            if self.testnumber:
                print(f'Running...\n[*]{yaml.safe_load(self.content)["attack_technique"]} {yaml.safe_load(self.content)["atomic_tests"][int(self.testnumber) -1]["name"]}\n')
            else:
                print(f'Running...\n[*]{yaml.safe_load(self.content)["attack_technique"]}\n')

            if self.testnumber and not self.action or self.action == 'cleanup':
                initial_time = time.time()
                mult = multiprocessing.Process(target=self.execute)
                mult.start()

                while True:
                    if int(time.time() - initial_time) >= self.except_time:
                        mult.terminate()
                    if not mult.is_alive():
                        break
                    time.sleep(1)
            elif self.action:
                self.parsing()

        def requests(self):
            resp = requests.get(
                f'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/{self.uuid}/{self.uuid}.yaml')

            if resp.status_code == 200:
                self.content = resp.content.decode('utf-8')

            else:
                print('Technique not found, try again....')
                exit()

        def execute(self):
            content = yaml.safe_load(self.content)

            if not self.action:
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
            if self.action.lower() == 'getprereqs':
                self.getprereqs()

            elif self.action.lower() == 'showdetails':
                print(self.content)

            elif self.action.lower() == 'showdetailsbrief':
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
else:
    print('Technique not found, try again....')

