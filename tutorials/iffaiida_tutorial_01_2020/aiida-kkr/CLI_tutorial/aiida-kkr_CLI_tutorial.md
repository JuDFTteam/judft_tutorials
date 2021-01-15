# **AiiDA-KKR command line interface**


The AiiDA-KKR plugin comes with a command line interface that exposes some of it's functionalities.

So far the following commands are available:
* `aiida-kkr data parameter import` - tool to import calculation parameters from an `inputcard`
* `aiida-kkr data structure import` - tool to import structure (and calculation parameters from an `inputcard`)
* `aiida-kkr launch voro` - interface to voronoi calculation
* `aiida-kkr launch kkr` - interface to KKRhost calculation
* `aiida-kkr launch scf` - interface to KKRhost self-consistency workflow
* `aiida-kkr launch dos` - interface to DOS workflow
* `aiida-kkr launch bs` - interface to bandstructure workflow
* `aiida-kkr launch kkrimpscf` - interface to `kkr_imp_wc` impurity embedding workflow
* `aiida-kkr plot` - interface to `plot_kkr` tool
> __Note:__\
> use the `-h` argument to show a help for these commands and command groups.

In the following we will go through some of the CLI tools to demonstrate the usage. In this example we will import data from a sample `inputcard` and run a full scf calculation with the KKRhost code through aiida.

## **Importing data**

We start with importing the setup of a possible calculation. We will use the `aiida-kkr data structure import` tool to convert this inputcard:
```
# this is an example file of an inputcard that is used to read in the structure and paramters from a file

NSPIN= 1
LMAX= 2

ALATBASIS= 6.822  # in a_Bohr

BRAVAIS
0.0 0.5 0.5
0.5 0.0 0.5
0.5 0.5 0.0

NAEZ= 1

<RBASIS>      <ZATOM>
0.0 0.0 0.0     29

RCLUSTZ= 2.3

EMIN    EMAX    TEMPR  NPOL  NPT1  NPT2  NPT3
-0.4    1.0     500.0   6     4     18    4


RMAX=  7
GMAX= 65
```
into AiiDA nodes (namely `StructureData` and `Dict` nodes):

```shell
$ aiida-kkr data structure import CLI_tutorial/inputcard.txt --kkrpara 
Success: stored kkr params Dict node <1965>
Success: parsed and stored StructureData <1966> with formula Cu
```

We are going to reuse the structure and parameter nodes we imported. Thus we save them as environment variables:

```shell
$ export PK_PARA=1965
$ export PK_STRUC=1966
```

## **Running calculations**

We will use our imported data to run a simple calculation where we first run voronoi and then a KKRhost calculation. In these examples we will use the following codes:
```shell
$ verdi code list
# List of configured codes:
# (use 'verdi code show CODEID' to see the details)
* pk 210 - voronoi_intel@iffslurm
* pk 482 - kkrhost_develop_intel@iffslurm
* pk 1639 - kkrhost_develop_amd@iffslurm
```


### Voronoi calculation

We start by running the voronoi calulation (see `aiida-kkr voro launch -h` for a description of the inputs):
```shell
$ aiida-kkr launch voro \
  -s PK_STRUC \
  -p PK_PARA\
  -W 300 \
  -Q th1 \
  -v voronoi_intel@iffslurm \
  -d
Submitted VoronoiCalculation<2209> to the daemon
```
> __Note:__\
> Remember to change the pks of the structure and parameters to the output you got from the `aiida-kkr data structure import` command!

It might also be helpful to save the calculation's pk somewhere. For the following we will save it as an environment variable which we call `$PK_PARA`:
```shell
$ export PK_VORO=2209
```

After some time the calculation is finished. We can see this for instance with the `verdi node show` command (here we reuse our environment variable `PK_VORO`):

```shell
$ verdi node show $PK_VORO
Property     Value
-----------  ------------------------------------
type         VoronoiCalculation
state        Finished [0]
pk           2209
uuid         a98d6c12-dde4-4978-8e44-e16ba6f1df4a
label
description
ctime        2021-01-14 15:56:11.610267+00:00
mtime        2021-01-14 16:00:00.197688+00:00
computer     [3] iffslurm

Inputs        PK  Type
----------  ----  -------------
code         210  Code
parameters  1965  Dict
structure   1966  StructureData

Outputs              PK  Type
-----------------  ----  ----------
output_parameters  2216  Dict
remote_folder      2210  RemoteData
retrieved          2215  FolderData

Log messages
---------------------------------------------
There are 1 log messages for this calculation
Run 'verdi process report 2209' to see them
```

### KKRhost calculation

A KKRhost calculation requires a previous voronoi calculation to have the starting potential and shapefunction. We now continue the previous step with a KKRhost calculation using the `aiida-kkr launch kkr` tool: 
```shell
$ aiida-kkr launch kkr \
  -k kkrhost_develop_amd@iffslurm \
  -p $PK_PARA \
  --parent-folder 2210 \
  --with-mpi -M 32 \
  -W 3600 \
  -N 1 \
  -Q th1-2020-32 \
  -d
Submitted KkrCalculation<2218> to the daemon

$ export PK_KKR=2218
```

> __Note:__\
> Remember to change the pk of the `parent-folder` inputs to the output you got from the voronoi calculation.

And once that job finishes we can inspect its outcome or continue calculations from there.
In the process list we find information on our job:

```shell
$ verdi process list -a -p1 | grep $PK_KKR
2218  29s ago    KkrCalculation          ⏵ Waiting         Waiting for transport task: upload
```

after some time the jobs finishes (depending on the availability of the cluster):

```shell
$ verdi process list -a -p1 | grep $PK_KKR
2218  6m ago     KkrCalculation          ⏹ Finished [0]
```

and we can take a look at the output:

```shell
$ verdi calcjob outputcat $PK_KKR | tail -n20
 Exited MADELUNG3D
 ++++++++++++++++++++++++++++++++++++++++++++++++++++++
 +++            SCF ITERATIONS START                +++
 ++++++++++++++++++++++++++++++++++++++++++++++++++++++
started on 2021/ 1/14 at 17:11:26
               Ne        
          TOT 11.02337793
      ITERATION   1 charge neutrality in unit cell =     0.023378
                new E FERMI   0.4060321548  DOS(E_F) =     7.285464
      ITERATION   1 average rms-error : v+ + v- =  1.7741D-01
TOTAL ENERGY in ryd. :            -3304.85547462

            ++++++ NUMBER OF SCF STEPS EXHAUSTED ++++++
*******************************************************************************
Iteration finished on 2021/ 1/14 at 17:11:26
 -------------------MEMORY CONSUMPTION REPORT-----------------------
 166 allocations and 288 deallocations, remaining memory(B):-38278286
 Memory occupation peak: 8883 kB
 For the array: "RHO2NSNM" in routine "main2"
 -----------------END MEMORY CONSUMPTION REPORT---------------------
```

You can see that only a single iteration ran because we did not specify `NSTEPS` in our inputcard and the default value in the KKRhost code is to do a single iteration only.

> __Note:__\
> The following commands are helpful to see the input/output files of the calculation:
> 
> ```shell
> $ verdi calcjob -h
> Usage: verdi calcjob [OPTIONS] COMMAND [ARGS]...
>
>  Inspect and manage calcjobs.
>
>Options:
>  -h, --help  Show this message and exit.
>
>Commands:
>  cleanworkdir  Clean all content of all output remote folders of calcjobs.
>  gotocomputer  Open a shell in the remote folder on the calcjob.
>  inputcat      Show the contents of one of the calcjob input files.
>  inputls       Show the list of the generated calcjob input files.
>  outputcat     Show the contents of one of the calcjob retrieved outputs.
>  outputls      Show the list of the retrieved calcjob output files.
>  res           Print data from the result output Dict node of a calcjob.
> ```

## **Running workflows**

### Bandstructure

The command line interface of aiida-kkr also supports some workflows. We first want to use the bandstructure workflow. This takes as input a `remote_folder` of a previous (converged) calculation. For demonstration purposes we continue from our previous KKR calculation although it is not converged yet.

```shell
$ aiida-kkr launch bs -k kkrhost_develop_amd@iffslurm -P <PARENT-REMOTE-PK> -opt 38f06f41 -d
```
    
> __Note:__\
> The `opt` input to the bandstructure workflow is the first part of an option Dict node's uuid that is used to identify the node. The iffslurm input from `base_iff` comes with ready-to-use default option nodes that are used in workflows. They define the `queue_name` and default resources for the different architechtures (i.e. node types) of iffslurm.
>
> Predefined option nodes:
>
> |label  |  uuid  | description|
> | --- | --- | --- |
> | `options_iffslurm_oscar_serial`   | `836e5316-d000-498a-aac8-6f86d561ffe9` | `oscar` partition (single core on intel node) without MPI |
> | `options_iffslurm_oscar` | `3b6c327e-d894-48ef-9f82-b45570149779` | `oscar` partition (12 core intel node) with MPI |
> | `options_slurm_amd32_serial`   | `51d94945-6f65-46ac-9a87-5e5391192ca8` | `th1-2020-32` partition (single core on AMD node) without MPI |
> | `options_slurm_amd32`   | `38f06f41-1547-4b34-ae2d-bf9a8ae0c95e` | `th1-2020-32` partition (32 core AMD node) with MPI |
> | `options_slurm_amd64`   | `83fef094-2e88-4543-94c5-20ac85de2688` | `th1-2020-32` partition (64 core AMD node) with MPI |

    
We can use the `aiida-kkr plot` tool to visualize the bandstructure (here we add the additional keyword argument `silent=True` to suppress further output to the stdout and `filename=my-plot-name.png` to write a png file called `my-plot.png`):
    
```shell
$ aiida-kkr plot -o silent=True -o filename=my-plot.png 669
{'silent': True, 'filename': 'my-plot.png'}
cannot open tk gui, fall back to static image
saved static plot to  my-plot.png
```

### self consistency

We now want to use the scf workflow of the KKRhost code. In the previous step we already got the calculation parameters and a structure node which will be inputs to our calculation.

To find out how to use the scf workflow we have a look at the help of the command line tool: `aiida-kkr launch scf -h`.

In addition to the nodes we used above we need to specify options for the computer (`queue_name` etc.) which come already prepared. The following `Dict` node can be used to run calculations on the `th1` queue:
```shell
$ verdi node show 49cf1dc1
Property     Value
-----------  -----------------------------------------------------------------------------
type         Dict
pk           1654
uuid         49cf1dc1-06d0-4dd8-a93d-db7eed4b793a
label        options_iffslurm_th1
description  default options for the th1 nodes on iffslurm (12 core intel nodes) using mpi
ctime        2021-01-13 12:44:28.792883+00:00
mtime        2021-01-13 12:44:28.800423+00:00

$ verdi data dict show 49cf1dc1
{
    "max_wallclock_seconds": 3600,
    "queue_name": "th1",
    "resources": {
        "num_machines": 1,
        "tot_num_mpiprocs": 12
    },
    "withmpi": true
}
```

#### Submission of the workflow

We have now collected all the nodes (we will reuse the same nodes as in the calculations part above) we need to submit a self consistency calculation:
```shell
$ aiida-kkr launch scf -s 1966 -p 1965 -k kkrhost_develop_intel@iffslurm -v voronoi_intel@iffslurm -opt 49cf1dc1 -d
Submitted kkr_scf_wc<2056> to the daemon
```
> __Note:__\
> In this example we have used the pk of the structure and parameters, a label for the codes and the short version of the uuid for the options node.
> 
> If we had chosed to omit the -d flag the workflow would run in the foreground.

### Checking the progress / output of the workflow

We can use the `verdi process`  and `verdi calcjob` commands of the AiiDA CLI to check on the process of out job.

To see all the steps that were already done by the workflow we can do
```shell
$ verdi process status 2056
kkr_scf_wc<2056> Waiting [2:while_(condition)(1:run_kkr)]
    ├── update_params_wf<2059> Finished [0]
    ├── kkr_startpot_wc<2062> Finished [0] [3:error_handler]
    │   ├── update_params_wf<2064> Finished [0]
    │   ├── VoronoiCalculation<2066> Finished [0]
    │   └── create_out_dict_node<2104> Finished [0]
    ├── update_params_wf<2107> Finished [0]
    └── KkrCalculation<2110> Waiting
```

We can also check how the input file of the KKRhost calculation looks like:
```shell
$ verdi calcjob inputcat 2110
ALATBASIS=        4.823882461255
BRAVAIS
       0.000000000000        0.707106781187        0.707106781187
       0.707106781187        0.000000000000        0.707106781187
       0.707106781187        0.707106781187        0.000000000000
NAEZ= 1
CARTESIAN= True

<RBASIS>
       0.000000000000        0.000000000000        0.000000000000

KSHAPE= 2
<SHAPE>
1

NSPIN= 1
<ZATOM>
      29.000000000000

LINIPOL= False
HFIELD=        0.000000000000
LMAX= 2
BZDIVIDE= 10 10 10

EMIN=       -0.400000000000
EMAX=        1.000000000000
TEMPR=     1000.000000000000
NPT1= 3
NPT2= 11
NPT3= 3
NPOL= 7
RCLUSTZ=        2.300000000000
INS= 1
RMAX=        7.000000000000
GMAX=       65.000000000000

NSTEPS= 50
IMIX= 0
STRMIX=        0.030000000000
BRYMIX=        0.050000000000
QBOUND= 8.000000e-03
```

Once the job finishes we can take a look at the output file:
```shell
$ verdi calcjob outputcat 2110
iffcluster0702: Using Ethernet for MPI communication.
iffcluster0702: Using Ethernet for MPI communication.
iffcluster0702: Using Ethernet for MPI communication.
iffcluster0702: Using Ethernet for MPI communication.
iffcluster0702: Using Ethernet for MPI communication.
iffcluster0702: Using Ethernet for MPI communication.
iffcluster0702: Using Ethernet for MPI communication.
iffcluster0702: Using Ethernet for MPI communication.
iffcluster0702: Using Ethernet for MPI communication.
iffcluster0702: Using Ethernet for MPI communication.
iffcluster0702: Using Ethernet for MPI communication.
iffcluster0702: Using Ethernet for MPI communication.
 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 !!! Most output written to output.myrank.txt files !!!
 !!! please check these files as well               !!!
 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
     Screened Korringa-Kohn-Rostoker Electronic Structure Code
                      for Bulk and Interfaces
                    Juelich-Munich 2001 - 2018

  Code version: v3.1-1726-ga413250
  Compile options: intel mpi 
  serial number for files: JuKKR_v3.1-1726-ga413250_intel_20210114152654
 Number of MPI ranks used:   12

*******************************************************************************

 Calling MADELUNG3D
 Exited MADELUNG3D
 ++++++++++++++++++++++++++++++++++++++++++++++++++++++
 +++            SCF ITERATIONS START                +++
 ++++++++++++++++++++++++++++++++++++++++++++++++++++++
started on 2021/ 1/14 at 15:26:54
               Ne        
          TOT 10.93496053
      ITERATION   1 charge neutrality in unit cell =    -0.065039
                new E FERMI   0.4189881528  DOS(E_F) =     6.672663
      ITERATION   1 average rms-error : v+ + v- =  1.7828D-01
TOTAL ENERGY in ryd. :            -3304.84484362

Iteration finished on 2021/ 1/14 at 15:26:55
               Ne        
          TOT 10.92377173
      ITERATION   2 charge neutrality in unit cell =    -0.076228
                new E FERMI   0.4300932258  DOS(E_F) =     6.864275
      ITERATION   2 average rms-error : v+ + v- =  1.6730D-01
TOTAL ENERGY in ryd. :            -3304.85751782

Iteration finished on 2021/ 1/14 at 15:26:56
               Ne        
          TOT 10.92547777
      ITERATION   3 charge neutrality in unit cell =    -0.074522
                new E FERMI   0.4407752819  DOS(E_F) =     6.976394
      ITERATION   3 average rms-error : v+ + v- =  1.5735D-01
TOTAL ENERGY in ryd. :            -3304.86751224

...
```

Or we look at the information that was parsed from the output files and is now stored as a `Dict` node in the database:
```shell
 $ verdi calcjob res 2110 | grep timings_group -A10
    "timings_group": {
        "Time in Iteration": 0.6411,
        "main0": 0.1406,
        "main1a  ": 0.3067,
        "main1a - tbref": 0.2799,
        "main1b  ": 0.178,
        "main1b - calctref13": 0.0001,
        "main1c  ": 0.0681,
        "main1c - serial part": 0.0013,
        "main2": 0.062
    },
```

As long as the working directory has not been deleted on the cluster we can also go to that working directory and investigate the files directly (this also works when the job has been transferred to the cluster, e.g. while it is still running): 
```shell
$ verdi calcjob gotocomputer 2110
Info: going to the remote work directory...
/etc/profile.d/lang.sh: line 19: warning: setlocale: LC_CTYPE: cannot change locale (C.UTF-8)
locale: Cannot set LC_CTYPE to default locale: No such file or directory
locale: Cannot set LC_ALL to default locale: No such file or directory

ruess@iffslurm:/local/th1/iff003/ruess/aiida_run/1f/b9/039b-7c02-4d98-9580-ff5487624903$ ls
_aiidasubmit.sh  inputcard                meminfo.txt  out_potential   output.0.txt  out_timing.000.txt  _scheduler-stderr.txt  shapefun
clusters         inputcard_generated.txt  out_kkr      output.000.txt  output.2.txt  potential           _scheduler-stdout.txt

ruess@iffslurm:/local/th1/iff003/ruess/aiida_run/1f/b9/039b-7c02-4d98-9580-ff5487624903$ exit
logout
Connection to iffslurm closed.
```

The `verdi process report` command gives us the output log of the process that would have been printed to the stdout if we did not put the `-d` flag while submission.
```shell
$ verdi process report 2056 | head -n 22
2021-01-14 14:19:57 [3382 | REPORT]: [2056|kkr_scf_wc|start]: INFO: started KKR convergence workflow version 0.10.4
2021-01-14 14:19:58 [3383 | REPORT]: [2056|kkr_scf_wc|start]: INFO: use the following parameter:

General settings
use mpi: True
max number of KKR runs: 5
Resources: {'num_machines': 1, 'tot_num_mpiprocs': 12}
Walltime (s): 3600
queue name: th1
scheduler command: 
description: Workflow for a KKR scf calculation starting either from a structure with automatic voronoi calculation or a valid RemoteData node of a previous calculation
label: kkr_scf_wc

Mixing parameter
Straight mixing factor: 0.03
Anderson mixing factor: 0.05
Nsteps scf cycle: 50
Convergence criterion: 1e-08
threshold_aggressive_mixing: 0.008
threshold_switch_high_accuracy: 0.001
convergence_setting_coarse: {'n1': 3, 'n2': 11, 'n3': 3, 'npol': 7, 'kmesh': [10, 10, 10], 'tempr': 1000.0}
convergence_setting_fine: {'n1': 7, 'n2': 29, 'n3': 7, 'npol': 5, 'kmesh': [30, 30, 30], 'tempr': 600.0}
```

When the calculation finishes we can see a summary in the output log:
```shell
$ verdi process report 2056 | tail -n 20
2021-01-14 14:43:56 [3677 | REPORT]: [2056|kkr_scf_wc|return_results]: Found last_params
2021-01-14 14:43:56 [3678 | REPORT]: [2056|kkr_scf_wc|return_results]: INFO: collect outputnode_dict
2021-01-14 14:43:56 [3679 | REPORT]: [2056|kkr_scf_wc|return_results]: STATUS: Done, the convergence criteria are reached.
INFO: The charge density of the KKR calculation pk= 2139 converged after 5 KKR runs and 5 iterations to 1.2961e-09 

2021-01-14 14:43:56 [3680 | REPORT]: [2056|kkr_scf_wc|return_results]: INFO: create results node
2021-01-14 14:43:56 [3681 | REPORT]: [2056|kkr_scf_wc|return_results]: INFO: overview of the result:

|------|---------|--------|------|--------|-------------------|-----------------|-----------------|-------------
| irun | success | isteps | imix | mixfac | accuracy settings |       rms       | abs(neutrality) | pk and uuid 
|      |         |        |      |        | qbound  | higher? | first  |  last  | first  |  last  |             
|------|---------|--------|------|--------|---------|---------|--------|--------|--------|--------|-------------
|     1|True     |      50|     0|3.00e-02|1.000e-03|False    |1.78e-01|2.98e-02|6.50e-02|7.84e-03| 2110 | 1fb9039b-7c02-4d98-9580-ff5487624903
|     2|True     |      44|     0|3.00e-02|1.000e-03|False    |2.89e-02|7.78e-03|7.59e-03|1.99e-03| 2115 | 7f305b6b-25b7-472f-b40b-7a31aeb9b3bd
|     3|True     |      43|     5|5.00e-02|1.000e-03|False    |7.69e-03|1.33e-09|1.07e-03|0.00e+00| 2123 | 77372de1-f82c-438e-b2d4-1501f2d88939
|     4|True     |      43|     5|5.00e-02|1.000e-08|True     |4.26e-03|1.30e-09|4.66e-02|0.00e+00| 2139 | 2d5b7a34-a3e4-4b4a-86cb-db9a6a6a2f54

2021-01-14 14:43:56 [3682 | REPORT]: [2056|kkr_scf_wc|return_results]: 
INFO: done with kkr_scf workflow!
```

And in the `process status` we can see which calculation have been done:
```shell
$ verdi process status 2056
kkr_scf_wc<2056> Finished [0] [5:return_results]
    ├── update_params_wf<2059> Finished [0]
    ├── kkr_startpot_wc<2062> Finished [0] [3:error_handler]
    │   ├── update_params_wf<2064> Finished [0]
    │   ├── VoronoiCalculation<2066> Finished [0]
    │   └── create_out_dict_node<2104> Finished [0]
    ├── update_params_wf<2107> Finished [0]
    ├── KkrCalculation<2110> Finished [0]
    ├── KkrCalculation<2115> Finished [0]
    ├── update_params_wf<2120> Finished [0]
    ├── KkrCalculation<2123> Finished [0]
    ├── update_params_wf<2136> Finished [0]
    ├── KkrCalculation<2139> Finished [0]
    └── create_scf_result_node<2152> Finished [0]
```

We can furthermore see the input and output nodes of our workflow:
```shell
$ verdi node show 2056
Property     Value
-----------  ------------------------------------
type         kkr_scf_wc
state        Finished [0]
pk           2056
uuid         7f9e3b38-2413-4786-9761-25ff12c0885c
label
description
ctime        2021-01-14 14:19:57.657771+00:00
mtime        2021-01-14 14:43:56.475952+00:00
computer     [3] iffslurm

Inputs             PK  Type
---------------  ----  -------------
calc_parameters  1965  Dict
kkr               482  Code
options          1654  Dict
structure        1966  StructureData
voronoi           210  Code
wf_parameters    2055  Dict

Outputs                               PK  Type
----------------------------------  ----  ----------
last_InputParameters                2137  Dict
last_RemoteData                     2140  RemoteData
last_calc_out                       2150  Dict
output_kkr_scf_wc_ParameterResults  2151  Dict
results_vorostart                   2105  Dict

Called      PK  Type
--------  ----  ----------------------
CALL      2059  update_params_wf
CALL      2062  kkr_startpot_wc
CALL      2107  update_params_wf
CALL      2110  KkrCalculation
CALL      2115  KkrCalculation
CALL      2120  update_params_wf
CALL      2123  KkrCalculation
CALL      2136  update_params_wf
CALL      2139  KkrCalculation
CALL      2152  create_scf_result_node

Log messages
-----------------------------------------------
There are 124 log messages for this calculation
Run 'verdi process report 2056' to see them
```