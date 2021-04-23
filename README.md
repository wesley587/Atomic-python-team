## Atomic python team

Atomic python is a python script that simulates the [***Atomic techniques***](https://github.com/redcanaryco/atomic-red-team/tree/master/atomics) using a shell to run,it is necessary to have the python intalled on your envovironment


### Usage
- Copy and paste or clone the [***file***](link) in your enviroment
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
| -t | Is used to specify the technique number | -t T1082 |
| -action | Use -action the specify some action | -action |

### ***Action parameters***
| command |descrpiton | how to use |
| --- | --- | --- |
| GetPrereqs| Case some technique has a prereqs use this command to dowload the prereqs| -action GetPrereqs |
| ShowDetails | Used to see the details | -action ShowDetails |
| ShowDetailsBrief | See the available technique for your enviroment| -action ShowDetailsBrief |
| Cleanup | Case a technique save a file in your environment use this command to delete | -action Cleanup|


### examples 

```
python main.py -t T1082 -action showdetailsbrief
----------------------------------------------------
python main.py -t T1234 -testnumber 123
----------------------------------------------------
python main.py -t T1220 -action showdetails
----------------------------------------------------
python main.p -t T1220 -action cleanup -testnumber 1
----------------------------------------------------
```
