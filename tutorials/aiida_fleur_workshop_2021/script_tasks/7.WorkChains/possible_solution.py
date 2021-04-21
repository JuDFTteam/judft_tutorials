from aiida.orm import Dict, load_node, load_code
from aiida.engine import submit

# import the workchain
from aiida_fleur.workflows.ssdisp import FleurSSDispWorkChain

# load Fleur Code
fleur_code = load_code('fleur@localhost')

fleurinp_Fe = load_node(xxx)
fleurinp_Co = load_node(xxx)
fleurinp_Ni = load_node(xxx)

fleurinp_data_list = [fleurinp_Fe, fleurinp_Co, fleurinp_Ni]

options = Dict(dict={'resources' : {"num_machines": 1, "num_mpiprocs_per_machine" : 2},
                     'withmpi' : True,
                     'max_wallclock_seconds' : 600})

wf_para = Dict(dict={'beta' : {'all' : 1.57079},            # sets beta angle for all atoms
                     'q_vectors': [[0.0, 0.0, 0.0],         # set q-vectors to calculate
                                   [0.125, 0.125, 0.0],     
                                   [0.250, 0.250, 0.0],     
                                   [0.375, 0.375, 0.0],     
                                   [0.500, 0.500, 0.0]],     
                     'ref_qss' : [0.0, 0.0, 0.0],            # sets a q-vector of the reference calc
                     'inpxml_changes': []
                    })

wf_para_scf = Dict(dict={'fleur_runmax' : 3,                    # passed to SCF workchain
                         'itmax_per_run' : 30,                  # passed to SCF workchain
                         'density_converged' : 0.002,           # passed to SCF workchain
                         'serial' : False,                      # passed to SCF workchain
                        })

for fleurinp in fleurinp_data_list:
    workchain = submit(FleurSSDispWorkChain,
                       scf={'fleur': fleur_code,
                            'fleurinp': fleurinp,
                            'wf_parameters': wf_para_scf},
                       fleur=fleur_code,
                       wf_parameters=wf_para)
    print('Submitted SSDisp workchain pk={}'.format(workchain.pk))
