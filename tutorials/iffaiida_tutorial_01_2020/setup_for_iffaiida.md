# iffaiida tutorial setup from a fresh container:

The main task you should do is to use the iffdata command install and configure
some common aiida-nodes into the database. This will ensure that your work can 
be better linked to other peoples effort and relieve you from the burden to install
all computers and settings yourself.

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
$ iffdata list
```

The basic database with nodes everyone should use is the iff_base database which you should install now:

```
$ iffdata import base_iff
```
This command will install some computers and codes we prepared for you. You will be asked to confirm some questions during the installation.

After the import finished, you can query the AiiDA database to see your recent imports.
```
$ verdi code list
$ verdi computer list -a
```
You can also test the installation of computers again.
```
$ verdi computer test iffslurm
```

# Fleur specific installation
If all tests are green you are ready to launch workflows and calculations from the command line with aiida-fleur command to iffslurm.
If bash/tab completion of aiida-fleur is not enabled yet execute:
```
$ eval "$(_AIIDA_FLEUR_COMPLETE=source aiida-fleur)"
```

you can check what structures you already have, or provide structures from other input sources, like cif, poscar, xsf, ... files
```
$ verdi data structure list
```

check if the following commands can be executed.
```shell
$ aiida-fleur -h
$ aiida-fleur launch -h
```
