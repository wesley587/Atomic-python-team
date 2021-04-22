import re
import argparse
import requests
import yaml
import subprocess
import os

arguments = argparse.ArgumentParser()
arguments.add_argument('-t', action='store', dest='uuid', help='', required=True)
arguments.add_argument('-testnumber', action='store', dest='testnumber', required=False)
arguments.add_argument('-action', action='store', dest='action', required=False)

parse = arguments.parse_args()

if re.match(r'T\d*$|T\d*.\d*$', parse.uuid):
    class atomic:
        def __init__(self):
            self.uuid = parse.uuid
            self.testnumber = parse.testnumber
            self.action = parse.action
            self.content = ''

        def main(self):
            self.requests()
            if self.testnumber and not self.action:
                self.execute()
            elif self.action:
                self.parsing()

        def requests(self):
            resp = requests.get(f'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/{self.uuid}/{self.uuid}.yaml')
            if resp.status_code == 200:
                self.content = resp.content.decode('utf-8')
            else:
                print('Not found...')
                exit()

        def execute(self):
            content = yaml.safe_load(self.content)
            command = content['atomic_tests'][int(self.testnumber) -1]['executor']['command'].split('\n')
            shell = content['atomic_tests'][int(self.testnumber) -1]['executor']['name']
            [os.system(x) if shell == 'command_prompt' else subprocess.Popen(['powershell.exe', '-command', x]) for x in command if x != '']

        def parsing(self):
            if self.action.lower() == 'getprereqs':
                self.getprereqs()

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
                        subprocess.check_output(['powershell.exe', prep_comm if not re.findall('#{\w*}', prep_comm) else self.input_arguments(prep_comm)], shell=True)
                    except:
                        subprocess.check_output(['powershell.exe', get_prep_comm if not re.findall('#{\w*}', get_prep_comm) else self.input_arguments(get_prep_comm)], shell=True)
                else:
                    subprocess.check_output([prep_comm if not re.findall('#{\w*}', prep_comm) else self.input_arguments(prep_comm)], shell=True)

        def input_arguments(self, command):
            input_arguments = yaml.safe_load(self.content)['atomic_tests'][int(self.testnumber) - 1]['input_arguments']
            parser = re.findall('#{\w*}', command)
            a = [input_arguments[x.replace('#{', '').replace('}', '')]['default'] for x in parser]
            print(a)
            for ex, de in zip(parser, a):
                command = command.replace(ex, de)
            return command

        def if_contains(self, k, v):
            try:
                value = k[v]
                return value
            except:
                return ''


    start = atomic()
    start.main()
else:
    print('Technique not found, try again')


