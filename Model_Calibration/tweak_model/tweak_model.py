import os
import sys
from eppy.modeleditor import IDF


def run_single(idf_name_in, epw_name):
    dir_name = os.path.dirname(os.path.realpath(__file__))
    idd_file = "C:/EnergyPlusV8-9-0/Energy+.idd"
    IDF.setiddname(idd_file)

    idf_path = dir_name + '/' + idf_name_in
    epw_path = dir_name + '/' + epw_name

    out = dir_name + '/out_' + idf_name_in.split('.idf')[0]

    idf = IDF(idf_path, epw_path)

    idf.run(
        output_directory = out, 
        readvars = True,
        output_prefix = idf_name_in.split('.idf')[0],
        output_suffix = 'D'
        )

def print_object_names(v_objects):
    for object in v_objects:
        print(object.Name)

def modify_material_property(material, property_name, times = 1):
    if material != None and hasattr(material, property_name):
        material[property_name] *= times
    else:
        print("Warning: Material doesn't exist or the material doesn't have the specified property!")
    return material


def main():
    idf_name_in = 'tweaked_CBES_model_v0.0.idf'
    idf_name_out = 'tweaked_CBES_model_v0.1.idf'

    epw_name = 'USA_PA_Pittsburgh.Intl.AP.725200_TMY3.epw'
    
    dir_name = os.path.dirname(os.path.realpath(__file__))
    idd_file = "C:/EnergyPlusV8-9-0/Energy+.idd"
    IDF.setiddname(idd_file)
    
    idf_path = dir_name + '/' + idf_name_in
    epw_path = dir_name + '/' + epw_name
    
    out = dir_name + '/out_' + idf_name_in.split('.idf')[0]
    
    idf = IDF(idf_path, epw_path)
    

    # idf.saveas("tweaked_CBES_model_v0.0.idf")

    v_materials = idf.idfobjects['MATERIAL']
    v_window_materials = idf.idfobjects['WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM']
    v_constructions = idf.idfobjects['CONSTRUCTION']

    # print([construction.Name for construction in v_constructions])
    
    
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
            material_1st_layer = modify_material_property(material_1st_layer, 'Thickness', 5)
            material_2nd_layer = modify_material_property(material_2nd_layer, 'Thickness', 5)
            material_3rd_layer = modify_material_property(material_3rd_layer, 'Thickness', 5)
            material_4th_layer = modify_material_property(material_4th_layer, 'Thickness', 5)
            material_1st_layer = modify_material_property(material_1st_layer, 'Conductivity', 0.5)
            material_2nd_layer = modify_material_property(material_2nd_layer, 'Conductivity', 0.5)
            material_3rd_layer = modify_material_property(material_3rd_layer, 'Conductivity', 0.5)
            material_4th_layer = modify_material_property(material_4th_layer, 'Conductivity', 0.5)
    
        # Change interior wall construction
        if('int wall' in construction.Name):
            # print(construction)
            material_1st_layer = construction.get_referenced_object('Outside_Layer')
            material_2nd_layer = construction.get_referenced_object('Layer_2')
            # print(material_1st_layer)
            # print(material_2nd_layer)
            continue
            # print(construction)
        # Change exterior floor construction
        if('ext floor' in construction.Name):
            # print(construction)
            material_1st_layer = construction.get_referenced_object('Outside_Layer')
            material_2nd_layer = construction.get_referenced_object('Layer_2')
            # material_1st_layer = modify_material_property(material_1st_layer, 'Thickness', 5)
            # material_2nd_layer = modify_material_property(material_2nd_layer, 'Thickness', 5)
            # material_1st_layer = modify_material_property(material_1st_layer, 'Conductivity', 0.5)
            # material_2nd_layer = modify_material_property(material_2nd_layer, 'Conductivity', 0.5)
            continue
    
    # 2. Change the window properties
    
    
    
    # 3. Change the lighting power density
    
    
    
    # 4. Change the occupancy schedule
    
    
    ### Save the new model
    idf.saveas(idf_name_out)


main()