import os
import sys
from eppy.modeleditor import IDF


def run_single(idf_name, epw_name):
    dir_name = os.path.dirname(os.path.realpath(__file__))
    idd_file = "C:/EnergyPlusV8-9-0/Energy+.idd"
    IDF.setiddname(idd_file)

    idf_path = dir_name + '/' + idf_name
    epw_path = dir_name + '/' + epw_name

    out = dir_name + '/out_' + idf_name.split('.idf')[0]

    idf = IDF(idf_path, epw_path)

    idf.run(
        output_directory = out, 
        readvars = True,
        output_prefix = idf_name.split('.idf')[0],
        output_suffix = 'D'
        )


def change_wall():
    return

def main():
    # run_single('original_CBES_model.idf', 'USA_PA_Pittsburgh.Intl.AP.725200_TMY3.epw')
    # run_single('tweaked_CBES_model.idf', 'USA_PA_Pittsburgh.Intl.AP.725200_TMY3.epw')
    return

# main()
def print_object_names(v_objects):
    for object in v_objects:
        print(object.Name)

idf_name = 'tweaked_CBES_model_v0.0.idf'
epw_name = 'USA_PA_Pittsburgh.Intl.AP.725200_TMY3.epw'

dir_name = os.path.dirname(os.path.realpath(__file__))
idd_file = "C:/EnergyPlusV8-9-0/Energy+.idd"
IDF.setiddname(idd_file)

idf_path = dir_name + '/' + idf_name
epw_path = dir_name + '/' + epw_name

out = dir_name + '/out_' + idf_name.split('.idf')[0]

idf = IDF(idf_path, epw_path)


v_materials = idf.idfobjects['MATERIAL']
v_window_materials = idf.idfobjects['WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM']
v_constructions = idf.idfobjects['CONSTRUCTION']



# print_object_names(v_materials)
# print_object_names(v_window_materials)
# print_object_names(v_constructions)


############################## Tweak the model #################################
# 1. Change the exterior wall construction
for construction in v_constructions:
    # Change exterior wall construction
    if('ext wall' in construction.Name):
        # print(construction)
        # Find and change the material of the outside layer
        material_1st_layer = construction.get_referenced_object('Outside_Layer')
        material_2nd_layer = construction.get_referenced_object('Layer_2')
        material_3rd_layer = construction.get_referenced_object('Layer_3')
        material_4th_layer = construction.get_referenced_object('Layer_4')

    # Change interior wall construction
    if('int wall' in construction.Name):
        print(construction)
        material_1st_layer = construction.get_referenced_object('Outside_Layer')
        material_2nd_layer = construction.get_referenced_object('Layer_2')

        print(material_1st_layer)
        continue
        # print(construction)
    # Change exterior floor construction
    if('ext floor' in construction.Name):
        # print(construction)
        continue

# 2. Change the window properties



# 3. Change the lighting power density



# 4. Change the occupancy schedule

