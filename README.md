## Atomic python team


![python-4785225_1280](https://user-images.githubusercontent.com/72465364/115910383-26768e00-a443-11eb-9875-578fa5825de3.jpg)
![shield](https://img.shields.io/badge/python-3.8.5-orange)
![shield](https://img.shields.io/badge/platform-windows%20%7C%20linux-orange)



Atomic python team is a script that simulates the [***Atomic techniques***](https://github.com/redcanaryco/atomic-red-team/tree/master/atomics) using a shell to run,it is necessary to have the python intalled on your envovironment


### Usage
- Clone the repository or Copy and paste the [***main.py***](https://github.com/wesley587/Atomic_python_team/blob/main/main.py) in your enviroment
- Run a shell
- Is necessary has the pthon language install 

### commands

To run a technique use this sintax
```
python main.py -t T1082 -TestNumber 10
```
Seen the tests using this syntax
```
python main.py -t T1082 -action ShowDetailsBrief
```
### ***Parameters***
| Command | Description | How to use |
| --- | --- | --- |
| -h | Is used to seen all parameters | -h, --help | 
| -t | Is used to specify the technique number | -t or -T T1082 |
| -action | Use -action the specify some action | -action |
| -except_time | Define the max time to run the file | -except_time 120 |

### ***Action parameters***
| command |descrpiton | how to use |
| --- | --- | --- |
| GetPrereqs| Case some technique has a prereqs use this command to dowload the prereqs| -action GetPrereqs |
| ShowDetails | Used to see the details | -action ShowDetails |
| ShowDetailsBrief | See the available technique for your enviroment| -action ShowDetailsBrief |
| Cleanup | Case a technique save a file in your environment use this command to delete | -action Cleanup|

### Cache folder

The cache foler is used to store file case the technique has a additional file to work


### examples 

```
python main.py -t T1082 -action showdetailsbrief
------------------------------------------------------
python main.py -t T1234 -testnumber 123
------------------------------------------------------
python main.py -t T1220 -action showdetails
------------------------------------------------------
python main.p -t T1220 -action cleanup -testnumber 1
------------------------------------------------------
python main.py -t T1234 -TESTNUMBER 1 -except_time 100
------------------------------------------------------
python main.py -t T12345 -h
```
