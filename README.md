# Atomic python team


![python-4785225_1280](https://user-images.githubusercontent.com/72465364/115910383-26768e00-a443-11eb-9875-578fa5825de3.jpg)
![shield](https://img.shields.io/badge/python-3.8.5-orange)
![shield](https://img.shields.io/badge/platform-windows%20%7C%20linux-orange)



Atomic python team is a script that simulates the [***Atomic techniques***](https://github.com/redcanaryco/atomic-red-team/tree/master/atomics) using a shell to run,it is necessary to have the python intalled on your envovironment


## Usage
- Clone the repository or Copy and paste the [***main.py***](https://github.com/wesley587/Atomic_python_team/blob/main/main.py) in your enviroment

#### Cloning repo

```bash
https://github.com/wesley587/Atomic-python-team.git
```

### Commands table

| Command | Description | How to use |
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

The cache folder is used to store the details about the previous execution, it's used a json with the date on the moment to save this cache

### PathToAtomicsFolder

This folder is used to save additional scripts that the technique used



### examples 

#### See the available technique for your environment using T1082

``` bash
python main.py -t T1082 --showdetailsbrief
```

```bash
python main.py -t T1082 -sdb
```

#### Specify test number of techcinque T1082
```bash
python main.py -t T1082 --testnumber 10
```

```
python main.py -t T1082 -tn 10
```
#### Seeing the datails

```bash
python main.py -t T1220 --showdetails
```
```bash
python main.py -t T1220 -sd
```
#### Cleanp command

```bash
python main.p -t T1220 --cleanup --testnumber 1
```

```bash
python main.p -t T1220 -cn --testnumber 1
```
#### Changing the except_time
```bash
python main.py -t T1234 -TESTNUMBER 1 --except_time 100
```

```bash
python main.py -t T1234 -TESTNUMBER 1 -ex 100
```


## How to Contribute

1. Clone repo and create a new branch
2. Make changes and test
3. Submit Pull Request with a description of changes
