# Atomic python team (BETA)


![python-4785225_1280](https://user-images.githubusercontent.com/72465364/115910383-26768e00-a443-11eb-9875-578fa5825de3.jpg)
![shield](https://img.shields.io/badge/python-3.8.5-orange)
![shield](https://img.shields.io/badge/platform-windows%20%7C%20linux-orange)



Atomic python team is a Python Programing that simulates the [***Atomic Red Team***](https://github.com/redcanaryco/atomic-red-team), runs remotely agents to use [**Atomic Techniques**](https://github.com/redcanaryco/atomic-red-team/tree/master/atomics), it's necessary to have the python installed on your environment.


## Server installation 

- Download the Atomic-python team;

- Open the port 55000 on your gateway or router. If you need to change this number go to [***main.py***](https://github.com/wesley587/Atomic_python_team/blob/main/main.py) and edit the file

## Client installation

- Use the [***main.py***](https://github.com/wesley587/Atomic_python_team/blob/main/main.py) -c to create a client, you'll need to run the script in the host target

## Usage 

1º The first step is rum the main.py and make the libs installations

#### commands table

| Commands | Description | Usage |
| --- | --- | --- | 
| -c, --creat | Used to creat an agent on host | python3 main.py -c | 
| -p, --port | Used to especify the port number | python3 main.py -p ***port num*** | 
| -ph, --path | Path to creat an agent | python3 main.py -ph ***/home/user*** |
| -l, --listen | Used to especify that the file is on listening mode | python3 main.py -l | 
| -ip, --ip | Server ip | python3 main.py -ip | 

You can use mult commands on the same time 

2º Creat an client, use the -c parameter to creat an agente on you environment

```
python3 main.py -c
```

3º Run the client

4º After that the client make conection with the server run the commands

#### Commands table

| Command | Description | Usage |
| --- | --- | --- |
| -h | It's used to see all parameters | -h, --help | 
| -t | It's used to specify the technique number | -t or -T T1082 |
| -tn, --testnumber | It's used to specify the test number | -testnumber |
| -except_time | Define the max time to run the file | -except_time 120 |
| --cleanup, -c | It's used to activate the cleanup action of a testnumber | -cleanup / -c |
| -sdb, --showdetailsbrief | See the available technique for your environment| -sdb, --showdetailsbrief |
| -sd, --showdetails | Show the details of a technique | -sd, --showdetails | 
| -gp, --getprereqs | Case a technique save a file in your environment use this command to delete | -gp, --getprereqs | 


### Cache folder

The cache folder is used to store the details about the previous execution, it's used a json with the date of the moment to save this cache

### PathToAtomicsFolder

This folder is used to save additional scripts that the technique used

### bin folder

The bin folder is used to store some tools 




## How to Contribute

1. Clone repo and create a new branch
2. Make changes and test
3. Submit Pull Request with a description of changes
