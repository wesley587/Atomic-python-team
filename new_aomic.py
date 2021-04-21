import re
import argparse
import requests
import yaml
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
                print('issmsmskm')

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
            [os.system(x) for x in command if x != '']

    start = atomic()
    start.main()
else:
    print('Technique not found, try again')

