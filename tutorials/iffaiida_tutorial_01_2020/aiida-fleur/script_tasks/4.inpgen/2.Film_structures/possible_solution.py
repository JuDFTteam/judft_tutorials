from aiida.orm import Dict, load_node
from aiida.engine import submit

# import the FleurinpgenCalculation
from aiida_fleur.calculation.fleurinputgen import FleurinputgenCalculation

# load ingpen Code
inpgen_code = load_node(8)

# create a StuctureData
bohr_a_0= 0.52917721092
a = 7.497*bohr_a_0
cell = [[0.7071068*a, 0.0, 0.0],
        [0.0, 1.0*a, 0.0],
        [0.0, 0.0, 0.7071068*a]]

structure = StructureData(cell=cell)
structure.append_atom(position=(0., 0., 0.0*bohr_a_0), symbols='Fe')
structure.pbc = (True, True, False)
Fe_structrure = structure
Fe_structrure.store()
print('PK of store Fe ML structure is {}'.format(Fe_structrure.pk))

structure = StructureData(cell=cell)
structure.append_atom(position=(0., 0., 0.0*bohr_a_0), symbols='Ni')
structure.pbc = (True, True, False)
Ni_structrure = structure
Ni_structrure.store()
print('PK of store Ni ML structure is {}'.format(Ni_structrure.pk))

structure = StructureData(cell=cell)
structure.append_atom(position=(0., 0., 0.0*bohr_a_0), symbols='Co')
structure.pbc = (True, True, False)
Co_structrure = structure
Co_structrure.store()
print('PK of store Co ML structure is {}'.format(Co_structrure.pk))

structures = [Fe_structrure, Ni_structrure, Co_structrure]

# create a parameters Dict
parameters = Dict(dict={
    'comp': {
        'kmax': 3.85
        },
    'kpt': {
        'div1': 4,
        'div2' : 4,
        'div3' : 1
        }})

# options

options = {'resources' : {"num_machines": 1, "num_mpiprocs_per_machine" : 1}, 'withmpi' : False}

for structure in structures:
    # assemble inputs in a single dictionary
    inputs = FleurinputgenCalculation.get_builder()
    inputs.parameters = parameters
    inputs.code = inpgen_code
    inputs.structure = structure
    inputs.metadata.options = options

    # submit
    inpgen_pk = submit(FleurinputgenCalculation, **inputs)
    print('The PK of submitted inpgen job is {} for {} structure'.format(res_pk, structure.formula)

