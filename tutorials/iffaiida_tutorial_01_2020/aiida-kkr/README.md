# AiiDA-KKR tutorial

## Preparation

1. If you are new to python and/or AiiDA you may want to look at the [python crash course notebook](../aiida-fleur/0_Python_crash-course_optional_.ipynb) 
and the [introduction to AiiDA notebook](../aiida-fleur/1_AiiDA_data_types_and_verdi_commands.ipynb) before starting this tutorial.

2. Follow the [notes on the setup for iffaiida](setup_for_iffaiida.md) to import the iffslurm computer and the preinstalled KKR codes.
The following codes and computers should then be installed:

```
$ verdi code list
# List of configured codes:
# (use 'verdi code show CODEID' to see the details)
* pk 156 - kkrhost_3.5_intel@iffslurm
* pk 157 - voronoi_3.5_AMD@iffslurm
* pk 158 - kkrhost_3.5_AMD@iffslurm
* pk 159 - voronoi_3.5_intel@iffslurm
* pk 160 - kkrimp_3.5_intel@iffslurm
* pk 161 - kkrimp_3.5_AMD@iffslurm

$ verdi computer list
Info: List of configured computers
Info: Use 'verdi computer show COMPUTERNAME' to display more detailed information
/opt/aiida-core/aiida/orm/computers.py:738: AiidaDeprecationWarning: this property is deprecated, use the `label` property instead
  warnings.warn('this property is deprecated, use the `label` property instead', AiidaDeprecationWarning)  # pylint: disable=no-member
* iffslurm
* localhost
```

3. Make sure to copy the tutorial to your working directory:

```
cp -r /opt/judft_tutorials/tutorials/iffaiida_tutorial_01_2020/ ~/Home/JupyterHub/AiiDA-Day-Jan21
```

The aiida-kkr tutorial can then be found in the `AiiDA-Day-Jan21/aiida-kkr/` directory.

4. Import tutorial datasets:

```
$ verdi import data/*.aiida
```

## Overview of the tutorial

The main part of the tutorial consists of 3 notebooks:
* [AiiDA-KKR_tutorial_basic_calculations.ipynb](AiiDA-KKR_tutorial_basic_calculations.ipynb)
* [AiiDA-KKR_tutorial_workflows_I.ipynb](AiiDA-KKR_tutorial_workflows_I.ipynb)
* [AiiDA-KKR_tutorial_workflows_II.ipynb](AiiDA-KKR_tutorial_workflows_II.ipynb)

Additionally AiiDA-KKR has a command line interface which you find in the `CLI_tutorial` directory.
