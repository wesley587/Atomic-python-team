import requests
import yaml
import os
import re
import subprocess


class atomic_read_team:
    def __init__(self):
        self.url_base = 'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/'
        self.helper = '''
        -ShowDetails
        -GetPrereqs
        -CheckPreregs
        -testNumber
        -ShowDetailsBrief
        '''
        self.param = ['-ShowDetails', '-GetPrereqs', '-CheckPreregs', '-testNumber']
        self.yaml_decode = ''
        self.active_param = False
        self.technique = ''

    def input(self):
        while True:
            while True:
                teq = input('technique Number: ').upper().split(' ')
                if re.match('T\d*$|T\d*.\d*$', teq[0]) or teq[0] == '-HELP':
                    if len(teq) == 1:
                        teq.append(input('oq deseja fazer? '))
                    break
                else:
                    print('check again....')
            if teq[0] == '-HELP':
                print(self.helper)
            else:
                content = self.requests(teq[0])
                if not content:
                    print('url error')
                else:
                    if len(teq) > 1:
                        self.parsing(teq[1:])
            self.__init__()

    def requests(self, teq):
        base = f'{self.url_base}{teq}/{teq}.yaml'
        resp = requests.get(base)
        if resp.status_code == 200:
            content = resp.content
            decode_content = content.decode('utf-8')
            self.yaml_decode = decode_content
            return True
        else:
            return False

    def parsing(self, param):
        for x in param:
            print(x)
            if x.lower() == '-showdetails':
                print(self.yaml_decode)
            elif x.lower() == '-showdetailsbrief':
                tests = yaml.safe_load(self.yaml_decode)['atomic_tests']
                count = 0
                for l in tests:
                    count += 1
                    if "windows" in str(l):
                        a, b = str(l).find('name'), str(l).find('auto_generated_guid')
                        print(f'[{count}] ' + str(l)[a:b].replace("\'", "").replace(",", ""))

            elif x.lower() == '-testnumber' or x.lower() == '-getprereqs' or x.lower() == '-checkpreregs':
                self.active_param = x.lower()
            elif self.active_param == '-testnumber':
                self.test(x)
            elif self.active_param == '-getprereqs':
                content = self.base(x)
                try:
                    dependencies = content['dependencies']
                    try:
                        shell = content['dependency_executor_name']
                    except:
                        shell = 'command_prompt'
                    for d in dependencies:
                        cond = False
                        for k, v in d.items():
                            print(k, v)
                            if '#' in str(v):
                                req = re.findall('\#{\w*}', v)
                                param = self.base(x, req)
                                for zip_req, zip_param in zip(req, param):
                                    v = v.replace(zip_req, zip_param)
                            if k == 'prereq_command':
                                if 'command_prompt' in shell:
                                    cond = subprocess.check_output([v.replace('exit 0', "$true").replace('exit 1', 'failed')])
                                else:
                                    cond = subprocess.check_output(['powershell', v.replace('exit 0', '$true').replace('exit 1', "$false")])
                            if k == 'get_prereq_command' and cond == 'False':
                                if shell == 'command_prompt':
                                    os.system(v)
                                else:
                                    subprocess.call(['powershell', v])
                            else:
                                print('depencies intled')

                except:
                    print('There are no prerequisites')


    def base(self, num, find=''):
        content = yaml.safe_load(self.yaml_decode)['atomic_tests'][int(num)-1]
        param = list()
        supported_platforms = content['supported_platforms']
        if "windows" in str(supported_platforms):
            if find != '':
                for f in find:
                    f = f.replace('#', '').replace('{', '').replace('}', '')
                    if f in content['input_arguments'].keys():
                        for k, v in content['input_arguments'].items():
                            if k == f:
                                for k2, v2 in v.items():
                                    if k2 == 'default':
                                        if 'PathToAtomicsFolder' in v2:
                                            print('j jnjnjanxj')
                                            v2.replace('PathToAtomicsFolder', 'C:\\AtomicRedTeam\atomics')
                                        param.append(v2)
        if find == '':
            return content
        else:
            return param


    def test(self, num):
        content = self.base(num)
        shell = content['executor']['name']
        command = content['executor']['command'].split('\n')
        for x in command:
            if '#' in x:
                req = re.findall('\#{\w*}', x)
                param = self.base(num, req)
                for zip_req, zip_param in zip(req, param):
                    x = x.replace(zip_req, zip_param)
            print(x)
            if shell == 'command_prompt':
                try:
                    os.system(x)
                except:
                    print('ERROS IN COMMAND')
            else:
                try:
                    output = subprocess.check_output(['powershell.exe', x], stdin=subprocess.PIPE)
                    print(output)
                except subprocess.CalledProcessError:
                    print('ERROR IN COMMAND')


if __name__ == '__main__':
    start = atomic_read_team()
    start.input()

