def generate_control(args):
    control = dict()
    if args.listen and not args.create:
        control['action'] = 'listen'
    elif args.create:
        control['action'] = 'create'
        control['path'] = args.path
    else:
        return '[ERROR] Exeption, Arguments invalids.'
    control['ip'] = args.ip
    control['port'] = args.port
    return control

def generate_atomic_map(buffer):
    from datetime import datetime
    args = {'date': datetime.now().strftime('%d-%m-%Y -%H-%M-%S'),'except_time': 120, 'action': 'execute'}
    for x in buffer.replace('-', '.-').split('.'):
        if x:
            x = check_command_name(x)
            if len(x.split()) > 1:
                x = x.split() 
                args[x[0]] = x[1]
            else:
                args['action'] = x
    return args

def check_command_name( arg):
    commands = {'uuid': ['-t', '--testnumber', '-T'],
            'testnumber': ['-tn', '--testnumber'],
            'except_time': ['-ex', '--except_time'],
            'cleanup': ['-c', '--cleanup'],
            'showdetailsbrief': ['-sdb', '--showdetailsbrief'],
            'showdetails': ['-sd', '--showdetails'],
            'getprereqs': ['-gp', '--getprereqs']}
    for k, v in commands.items():
        for c in v:
            if c == arg.split()[0]:
                return arg.replace(c, k)
            
