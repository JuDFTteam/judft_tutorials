from aiida.orm import Dict, load_node
from aiida.engine import submit

# import the FleurinpgenCalculation
from aiida_fleur.calculation.fleur import FleurCalculation

# load Fleur Code
inpgen_code = load_node(8)

# load remote_data
remote = load_node(???)

# load fleurinpData
fleurinp = load_node(146)

# import FleurinputModifier and create a new FleurinpData
from aiida_fleur.data.fleurinpmodifier import FleurinputModifier

modifier = FleurinputModifier(fleurinp)
modifier.set_inpchanges({'imax': 30, 'alpha' : 0.015})
new_fleurinp = modifier.freeze()


# options
options = {'resources' : {"num_machines": 1, "num_mpiprocs_per_machine" : 2}, 'withmpi' : True}

# assemble inputs in a single dictionary
inputs = FleurCalculation.get_builder()
inputs.code = inpgen_code
inputs.parent_folder = structure
inputs.metadata.options = options
inputs.fleurinpdata = new_fleurinp


# submit
inpgen_pk = submit(FleurinputgenCalculation, **inputs)
print('The PK of submitted inpgen job is'.format(res_pk)

