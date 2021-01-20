# Common problems with the tutorial

# Setting up iffslurm

## When testing the computer connection:

### If you get an error like:
```
* Opening connection... 01/20/2021 06:57:03 PM <3696> paramiko.transport: [ERROR] Unknown exception: q must be exactly 160, 224, or 256 bits long
```
Then the prepared (automatic) keyfile setup has not worked for you.
You still need to configure the computer again per hand with a different key file.
You might need to change user name and the path to key file. For exmaple `/home/{your-username}/.ssh/id_rsa`
For this run:
```
$verdi computer configure ssh iffslurm

```
After this run and check if everything is fine now 
```
$verdi computer test iffslurm
```

### If you get an error like:
```
* Checking for spurious output... [Failed]: 
We detected some spurious output in the stdout when connecting to the computer, as shown between the bars
=====================================================================================================

< Here stands the output found >

=====================================================================================================
Please check that you don't have code producing output in your ~/.bash_profile, ~/.bashrc or similar.
If you don't want to remove the code, but just to disable it for non-interactive shells, see comments
in this troubleshooting section of the online documentation: https://bit.ly/2FCRDc5
```
This means you get some output from you .bashrc .profile .bash_profile files on iff slurm all the time when executing an ssh command to iffslurm
This might go well, but should be circumvented since aiida parses what the ssh commands return. It cannot 'understand the additional' information you print out everytime and it can also not now how this differs from scheduler responses.
Therefore, solution:
```
ssh iffslurm
```
Check on the source and comment out or delete the lines which cause these outputs to stdout, look for echos.


### If you see an error like
```
No permission to create file xyz
```
Your account is not in the iff group and does not have to right to create any files on the partition on iffslurm, which we use per default.
You have to write to one of the people of our IT to add you to the IFF group
By executing `groups` you can check to which groups your account belongs.


# Aiida-fleur tutorial

## Notebook 3

### Schema file not found error
This was related to a bug we had when creating new data from shared data, which is solved now.
Solution:
```
cd /opt/aiida-fleur/
git pull
```
