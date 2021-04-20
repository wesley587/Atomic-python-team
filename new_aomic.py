import re
import argparse
import requests

arguments = argparse.ArgumentParser()
arguments.add_argument('-t', action='store', dest='uuid', help='', required=True)
arguments.add_argument('-testnumber', action='store', dest='testnumber', required=False)
arguments.add_argument('-getprereqs', action='store', dest='getprereqs', required=False)
parse = arguments.parse_args()

if re.match(r'T\d*$|T\d*.\d*$', parse.uuid):
    class atomic:
        def __init__(self):
            self.uuid = parse.uuid
            self.testnumber = parse.testnumber
            self.getprereqs = parse.getprereqs
            self.content = ''

        def main(self):
            self.requests()

        def requests(self):
            resp = requests.get(f'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/{self.uuid}/{self.uuid}.yaml')
            if resp.status_code == 200:
                self.content = resp.content.decode('utf-8')
            else:
                print('Not found...')
    start = atomic()
    start.main()
else:
    print('Technique not found, try again')
