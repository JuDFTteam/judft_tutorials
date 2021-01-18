# iffaiida tutorial setup from a fresh container:

##  install aiida_nodes if not already there
check if the `iffdata` command is there and working.
if not do:
```
git clone aiida_nodes
pip3 install -e aiida_nodes
# To enable bash completion, maybe at this to your profile
eval "$(_IFFDATA_COMPLETE=source iffdata)"
```

# Setup base database
list registered datasets
```
$ iffdata registry list
```
confirm aiida is running fine and no codes are yet installed

```
$ verdi status
$ verdi code list
```
install iff base database
```
$ iffdata import base_iff
```

now we have some codes and computers
```
$ verdi code list
$ verdi computer list -A
```

check if you can passwordless connect to iffslurm and logout from iffslurm again
```
ssh iffslurm
```
if you had to type a password, add the corresponding ssh key file to the ssh agent
check if agent runs and what keys he has
```
$ ssh-add -L
```
if agent is not running: 
```
$ eval `ssh-agent -s`
```
add your key file to the ssh agent and type in your password
```
$ ssh-add path_to_keyfile
```

Now you have to configure the iffslurm computer in aiida for your user
```
$ verdi computer configure ssh iffslurm
$ verdi computer test iffslurm
```
if all tests are green you are ready to launch workflows and calculations from the command line with aiida-fleur command to iffslurm.
If bash/tab completion of aiida-fleur is not enabled yet execute:
```
$ eval "$(_AIIDA_FLEUR_COMPLETE=source aiida-fleur)"
```

you can check what structures you already have, or provide structures from other input sources, like cif, poscar, xsf, ... files
```
$ verdi data structure list
```

check if the following commands can be executed.
```
$ aiida-fleur -h
$ aiida-fleur launch -h
```