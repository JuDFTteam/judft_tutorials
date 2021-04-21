from aiida.orm import Dict, load_node, load_code
from aiida.engine import submit

# import the FleurinpgenCalculation
from aiida_fleur.calculation.fleur import FleurCalculation

# load Fleur Code
fleur_code = load_code('fleur@localhost')

# load remote_data
remote = load_node(REMOTE_DATA_PK)

# load fleurinpData
fleurinp = load_node(FLEURINP_PK)

# import FleurinputModifier and create a new FleurinpData
from aiida_fleur.data.fleurinpmodifier import FleurinpModifier

modifier = FleurinpModifier(fleurinp)
modifier.set_inpchanges({'imax': 30, 'alpha' : 0.015})
new_fleurinp = modifier.freeze()


# options
options = {'resources' : {"num_machines": 1, "num_mpiprocs_per_machine" : 2}, 'withmpi' : True}

# assemble inputs in a single dictionary
inputs = FleurCalculation.get_builder()
inputs.code = fleur_code
inputs.parent_folder = remote
inputs.metadata.options = options
inputs.fleurinpdata = new_fleurinp


# submit
fleur_calc = submit(FleurCalculation, **inputs)
print('The PK of submitted fleur job is'.format(fleur_calc.pk)

