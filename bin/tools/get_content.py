def request(control):
    from requests import get
    resp = get(
            f'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/{control["uuid"].upper()}/{control["uuid"].upper()}.yaml')

    if resp.status_code == 200:
        print(f'[Info] {control["uuid"]} is valid')
        return resp.content.decode('utf-8')

    else:
        return f'[Info] {control["uuid"]} is invalid'
        