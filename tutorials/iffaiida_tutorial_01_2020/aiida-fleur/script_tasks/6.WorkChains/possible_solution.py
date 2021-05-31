from aiida.orm import Dict, load_node
from aiida.engine import submit

# import the FleurinpgenCalculation
from aiida_fleur.calculation.fleur import FleurCalculation

# load Fleur Code
fleur_code = fleur_code(146)

fleurinp_Fe = load_node(xxx)
fleurinp_Co = load_node(xxx)
fleurinp_Ni = load_node(xxx)

fleurinp_data_list = [fleurinp_Fe, fleurinp_Co, fleurinp_Ni]

options = Dict(dict={'resources' : {"num_machines": 1, "num_mpiprocs_per_machine" : 2},
                     'withmpi' : True,
                     'max_wallclock_seconds' : 600})

calc_parameters = Dict(dict={
    'kpt': {
        'div1': 12,
        'div2' : 10,
        'div3' : 1
        }})

for fleuinp in fleurinp_data_list:
    workchain_pk = submit(FleurSSDispWorkChain,
                          fleur=fleur_code,
                          calc_parameters=calc_parameters,
                          wf_parameters=wf_para,
                          fleurinp=fleurinp)
    print('Submitted SSDisp workchain pk={}'.format(workchain_pk))
