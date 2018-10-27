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

def modify_object_property(material, property_name, times = 1, new_val = None):
    if material != None and hasattr(material, property_name):
        if new_val == None:
            material[property_name] *= times
        else:
            material[property_name] = new_val
    # else:
    #     print("Warning: Material doesn't exist or the material doesn't have the specified property!")
    return material


def main():
    idf_name_in = 'Baseline_V0.0.idf'
    idf_name_out_1 = './simulations/tweaked_CBES_model_v0.1.idf'
    idf_name_out_2 = 'tweaked_CBES_model_v0.2.idf'
    idf_name_out_3 = 'tweaked_CBES_model_v0.3.idf'

    epw_name = 'in.epw'
    
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
    v_lights = idf.idfobjects['LIGHTS']
    v_equipment = idf.idfobjects['ELECTRICEQUIPMENT']
    v_people = idf.idfobjects['PEOPLE']

    v_boilers = idf.idfobjects['BOILER:HOTWATER']
    v_waterHeaters = idf.idfobjects['WATERHEATER:MIXED']
    v_infiltrations = idf.idfobjects['ZONEINFILTRATION:DESIGNFLOWRATE']

    # print([construction.Name for construction in v_constructions])

    # Calibrating settings
    t_ext_wall_thickness = 0.8
    t_ext_wall_conductivity = 3
    t_ext_floor_thickness = 0.8
    t_ext_floor_conductivity = 3
    t_LPD = 0.8
    t_EPD = 0.8
    t_occ_density = 0.7
    n_boiler_eff = 0.6
    n_waterHeater_eff = 0.6
    t_infiltration = 2


    ############################## Tweak the model #################################
    for construction in v_constructions:
        # 1. Change the exterior wall construction
        # Change exterior wall construction
        if('ext wall' in construction.Name):
            # print(construction)
            # Find and change the material of the outside layer
            material_1st_layer = construction.get_referenced_object('Outside_Layer')
            material_2nd_layer = construction.get_referenced_object('Layer_2')
            material_3rd_layer = construction.get_referenced_object('Layer_3')
            material_4th_layer = construction.get_referenced_object('Layer_4')
            material_1st_layer = modify_object_property(material_1st_layer, 'Thickness', times=t_ext_wall_thickness)
            material_2nd_layer = modify_object_property(material_2nd_layer, 'Thickness', times=t_ext_wall_thickness)
            material_3rd_layer = modify_object_property(material_3rd_layer, 'Thickness', times=t_ext_wall_thickness)
            material_4th_layer = modify_object_property(material_4th_layer, 'Thickness', times=t_ext_wall_thickness)
            material_1st_layer = modify_object_property(material_1st_layer, 'Conductivity', times=t_ext_wall_conductivity)
            material_2nd_layer = modify_object_property(material_2nd_layer, 'Conductivity', times=t_ext_wall_conductivity)
            material_3rd_layer = modify_object_property(material_3rd_layer, 'Conductivity', times=t_ext_wall_conductivity)
            material_4th_layer = modify_object_property(material_4th_layer, 'Conductivity', times=t_ext_wall_conductivity)
    
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
            material_1st_layer = modify_object_property(material_1st_layer, 'Thickness', times=t_ext_floor_thickness)
            material_2nd_layer = modify_object_property(material_2nd_layer, 'Thickness', times=t_ext_floor_thickness)
            material_1st_layer = modify_object_property(material_1st_layer, 'Conductivity', times=t_ext_floor_conductivity)
            material_2nd_layer = modify_object_property(material_2nd_layer, 'Conductivity', times=t_ext_floor_conductivity)
            continue
    
    
    # 2. Change the window properties
    for construction in v_constructions:
        if('glazing' in construction.Name):
            material_1st_layer = construction.get_referenced_object('Outside_Layer')
            # material_1st_layer = modify_object_property(material_1st_layer, 'UFactor', new_val=2)
            # material_1st_layer = modify_object_property(material_1st_layer, 'Solar_Heat_Gain_Coefficient', new_val=0.8)
    

    # idf.saveas(idf_name_out_2)

    # 3. Change the lighting power density
    for light in v_lights:
        light = modify_object_property(light, 'Watts_per_Zone_Floor_Area', times=t_LPD)
        continue

    # 4. Change the interior equipment power density
    for equipment in v_equipment:
        equipment = modify_object_property(equipment, 'Watts_per_Zone_Floor_Area', times=t_EPD)
        continue
    
    # idf.saveas(idf_name_out_3)
    
    # 5. Change the occupancy settings
    for people in v_people:
        people = modify_object_property(people, 'People_per_Zone_Floor_Area', times=t_occ_density)
        continue


    # 6. Change HVAC equipment
    for boiler in v_boilers:
        boiler = modify_object_property(boiler, 'Nominal_Thermal_Efficiency', new_val=n_boiler_eff)
        continue

    for waterHeater in v_waterHeaters:
        waterHeater = modify_object_property(waterHeater, 'Heater_Thermal_Efficiency', new_val=n_waterHeater_eff)
        continue

    # Change infiltration settings
    for infiltration in v_infiltrations:
        infiltration = modify_object_property(infiltration, 'Flow_per_Exterior_Surface_Area', times=t_infiltration)
        continue

    idf.saveas(idf_name_out_1)



main()