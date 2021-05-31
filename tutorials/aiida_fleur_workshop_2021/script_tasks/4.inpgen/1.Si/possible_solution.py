from aiida.orm import Dict, load_code
from aiida.engine import submit
from aiida.plugins import DataFactory

# import the FleurinpgenCalculation
from aiida_fleur.calculation.fleurinputgen import FleurinputgenCalculation

# load ingpen Code
inpgen_code = load_code('inpgen@localhost')
StructureData = DataFactory('structure')

# create a StuctureData
# first we need to export it from .cif file using verdi
# for this run in a terminal:
# verdi data cif import "PATH_TO_CIF"

cif = load_node(STRUCTURE_PK)
structure = StructureData(ase=cif.get_ase())

# create a parameters Dict
parameters = Dict(dict={
    'comp': {
        'kmax': 3.84
        },
    'kpt': {
        'div1': 2,
        'div2' : 2,
        'div3' : 2
        }})

# options

options = {'resources' : {"num_machines": 1, "num_mpiprocs_per_machine" : 1}, 'withmpi' : False}

# assemble inputs in a single dictionary

inputs = FleurinputgenCalculation.get_builder()
inputs.parameters = parameters
inputs.code = inpgen_code
inputs.structure = structure
inputs.metadata.options = options


# submit

inpgen_pk = submit(FleurinputgenCalculation, **inputs)
print('The PK of submitted inpgen job is {}'.format(inpgen_pk))

