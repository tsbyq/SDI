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

# functions to add the hybrid modeling objects
def add_Sch_File(idf_file):
    with open(idf_file, 'a') as file:
        file.write('\n\n\n')
        file.write('! Schedule:Files for the hybrid modeling\n')
        file.write('Schedule:File,S2_front_T,Any Number,HybridZoneModel_Measurements.csv,2,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_left_T,Any Number,HybridZoneModel_Measurements.csv,3,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_right_T,Any Number,HybridZoneModel_Measurements.csv,4,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_back_T,Any Number,HybridZoneModel_Measurements.csv,5,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_front_Inlet_T,Any Number,HybridZoneModel_Measurements.csv,6,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_left_Inlet_T,Any Number,HybridZoneModel_Measurements.csv,7,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_right_Inlet_T,Any Number,HybridZoneModel_Measurements.csv,8,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_back_Inlet_T,Any Number,HybridZoneModel_Measurements.csv,9,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_front_Inlet_m,Any Number,HybridZoneModel_Measurements.csv,10,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_left_Inlet_m,Any Number,HybridZoneModel_Measurements.csv,11,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_right_Inlet_m,Any Number,HybridZoneModel_Measurements.csv,12,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_back_Inlet_m,Any Number,HybridZoneModel_Measurements.csv,13,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,obFMU_PeopleGroundTruth,People Fraction,HybridZoneModel_Measurements.csv,14,1,8760,Comma,No,10;\n')
        file.write('Schedule:Compact,Dummy People Activity Schedule,Any Number,Through: 12/31,For: AllDays,Until: 24:00,100;\n')

# S2_front_T
# S2_left_T
# S2_right_T
# S2_back_T

def add_Sch_File_calibrating(idf_file):
    with open(idf_file, 'a') as file:
        file.write('\n\n\n')
        file.write('! ###########################################################\n')
        file.write('! Schedule:Files for the hybrid modeling\n')
        file.write('Schedule:File,S2_front_People_sch,Any Number,HM_out.csv,2,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_left_People_sch,Any Number,HM_out.csv,3,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_right_People_sch,Any Number,HM_out.csv,4,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_back_People_sch,Any Number,HM_out.csv,5,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_front_ACH_sch,Any Number,HM_out.csv,6,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_left_ACH_sch,Any Number,HM_out.csv,7,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_right_ACH_sch,Any Number,HM_out.csv,8,1,8760,Comma,No,10;\n')
        file.write('Schedule:File,S2_back_ACH_sch,Any Number,HM_out.csv,9,1,8760,Comma,No,10;\n')

def add_HM_ach(idf_file):
    with open(idf_file, 'a') as file:
        file.write('\n\n\n')
        file.write('! ###########################################################\n')
        file.write('ZoneInfiltration:DesignFlowRate,\n')
        file.write('    S2 office front infiltration,            !- Name\n')
        file.write('    S2 office front,                  !- Zone or ZoneList Name\n')
        file.write('    S2_front_ACH_sch,             !- Schedule Name\n')
        file.write('    AirChanges/Hour,         !- Design Flow Rate Calculation Method\n')
        file.write('    ,                        !- Design Flow Rate {m3/s}\n')
        file.write('    ,                        !- Flow per Zone Floor Area {m3/s-m2}\n')
        file.write('    ,                        !- Flow per Exterior Surface Area {m3/s-m2}\n')
        file.write('    1.0,                     !- Air Changes per Hour {1/hr}\n')
        file.write('    1.0000,                  !- Constant Term Coefficient\n')
        file.write('    0.0000,                  !- Temperature Term Coefficient\n')
        file.write('    0.0000,                  !- Velocity Term Coefficient\n')
        file.write('    0.0000;                  !- Velocity Squared Term Coefficient\n')

        file.write('ZoneInfiltration:DesignFlowRate,\n')
        file.write('    S2 office left infiltration,            !- Name\n')
        file.write('    S2 office left,                  !- Zone or ZoneList Name\n')
        file.write('    S2_left_ACH_sch,             !- Schedule Name\n')
        file.write('    AirChanges/Hour,         !- Design Flow Rate Calculation Method\n')
        file.write('    ,                        !- Design Flow Rate {m3/s}\n')
        file.write('    ,                        !- Flow per Zone Floor Area {m3/s-m2}\n')
        file.write('    ,                        !- Flow per Exterior Surface Area {m3/s-m2}\n')
        file.write('    1.0,                     !- Air Changes per Hour {1/hr}\n')
        file.write('    1.0000,                  !- Constant Term Coefficient\n')
        file.write('    0.0000,                  !- Temperature Term Coefficient\n')
        file.write('    0.0000,                  !- Velocity Term Coefficient\n')
        file.write('    0.0000;                  !- Velocity Squared Term Coefficient\n\n')

        file.write('ZoneInfiltration:DesignFlowRate,\n')
        file.write('    S2 office right infiltration,            !- Name\n')
        file.write('    S2 office right,                  !- Zone or ZoneList Name\n')
        file.write('    S2_right_ACH_sch,             !- Schedule Name\n')
        file.write('    AirChanges/Hour,         !- Design Flow Rate Calculation Method\n')
        file.write('    ,                        !- Design Flow Rate {m3/s}\n')
        file.write('    ,                        !- Flow per Zone Floor Area {m3/s-m2}\n')
        file.write('    ,                        !- Flow per Exterior Surface Area {m3/s-m2}\n')
        file.write('    1.0,                     !- Air Changes per Hour {1/hr}\n')
        file.write('    1.0000,                  !- Constant Term Coefficient\n')
        file.write('    0.0000,                  !- Temperature Term Coefficient\n')
        file.write('    0.0000,                  !- Velocity Term Coefficient\n')
        file.write('    0.0000;                  !- Velocity Squared Term Coefficient\n\n')

        file.write('ZoneInfiltration:DesignFlowRate,\n')
        file.write('    S2 office back infiltration,            !- Name\n')
        file.write('    S2 office back,                  !- Zone or ZoneList Name\n')
        file.write('    S2_back_ACH_sch,             !- Schedule Name\n')
        file.write('    AirChanges/Hour,         !- Design Flow Rate Calculation Method\n')
        file.write('    ,                        !- Design Flow Rate {m3/s}\n')
        file.write('    ,                        !- Flow per Zone Floor Area {m3/s-m2}\n')
        file.write('    ,                        !- Flow per Exterior Surface Area {m3/s-m2}\n')
        file.write('    1.0,                     !- Air Changes per Hour {1/hr}\n')
        file.write('    1.0000,                  !- Constant Term Coefficient\n')
        file.write('    0.0000,                  !- Temperature Term Coefficient\n')
        file.write('    0.0000,                  !- Velocity Term Coefficient\n')
        file.write('    0.0000;                  !- Velocity Squared Term Coefficient\n\n')

        file.write('ZoneInfiltration:DesignFlowRate,\n')
        file.write('    non_HM_spaces infiltration,      !- Name\n')
        file.write('    non_HM_spaces,        !- Zone or ZoneList Name\n')
        file.write('    office infiltration year,    !- Schedule Name\n')
        file.write('    Flow/ExteriorArea,        !- Design Flow Rate Calculation Method\n')
        file.write('    ,                         !- Design Flow Rate\n')
        file.write('    ,                         !- Flow per Zone Floor Area\n')
        file.write('    0.001133,                 !- Flow per Exterior Surface Area\n')
        file.write('    ,                         !- Air Changes per Hour\n')
        file.write('    0.0,                      !- Constant Term Coefficient\n')
        file.write('    ,                         !- Temperature Term Coefficient\n')
        file.write('    0.224051539,              !- Velocity Term Coefficient\n')
        file.write('    0.0;                      !- Velocity Squared Term Coefficient\n\n')

def add_HM_occ(idf_file):
    with open(idf_file, 'a') as file:
        file.write('\n\n\n')
        file.write('! ###########################################################\n')
        file.write('People,\n')
        file.write('    S2 office front people,            !- Name\n')
        file.write('    S2 office front,        !- Zone or ZoneList Name\n')
        file.write('    S2_front_People_sch,    !- Number of People Schedule Name\n')
        file.write('    People,              !- Number of People Calculation Method\n')
        file.write('    ,                         !- Number of People\n')
        file.write('    ,                   !- People per Zone Floor Area\n')
        file.write('    ,                         !- Zone Floor Area per Person\n')
        file.write('    0.3,                      !- Fraction Radiant\n')
        file.write('    0.556,                    !- Sensible Heat Fraction\n')
        file.write('    office activity year;     !- Activity Level Schedule Name\n\n')

        file.write('People,\n')
        file.write('    S2 office left people,            !- Name\n')
        file.write('    S2 office left,        !- Zone or ZoneList Name\n')
        file.write('    S2_left_People_sch,    !- Number of People Schedule Name\n')
        file.write('    People,              !- Number of People Calculation Method\n')
        file.write('    ,                         !- Number of People\n')
        file.write('    ,                   !- People per Zone Floor Area\n')
        file.write('    ,                         !- Zone Floor Area per Person\n')
        file.write('    0.3,                      !- Fraction Radiant\n')
        file.write('    0.556,                    !- Sensible Heat Fraction\n')
        file.write('    office activity year;     !- Activity Level Schedule Name\n\n')

        file.write('People,\n')
        file.write('    S2 office right people,            !- Name\n')
        file.write('    S2 office right,        !- Zone or ZoneList Name\n')
        file.write('    S2_right_People_sch,    !- Number of People Schedule Name\n')
        file.write('    People,              !- Number of People Calculation Method\n')
        file.write('    ,                         !- Number of People\n')
        file.write('    ,                   !- People per Zone Floor Area\n')
        file.write('    ,                         !- Zone Floor Area per Person\n')
        file.write('    0.3,                      !- Fraction Radiant\n')
        file.write('    0.556,                    !- Sensible Heat Fraction\n')
        file.write('    office activity year;     !- Activity Level Schedule Name\n\n')

        file.write('People,\n')
        file.write('    S2 office back people,            !- Name\n')
        file.write('    S2 office back,        !- Zone or ZoneList Name\n')
        file.write('    S2_back_People_sch,    !- Number of People Schedule Name\n')
        file.write('    People,              !- Number of People Calculation Method\n')
        file.write('    ,                         !- Number of People\n')
        file.write('    ,                   !- People per Zone Floor Area\n')
        file.write('    ,                         !- Zone Floor Area per Person\n')
        file.write('    0.3,                      !- Fraction Radiant\n')
        file.write('    0.556,                    !- Sensible Heat Fraction\n')
        file.write('    office activity year;     !- Activity Level Schedule Name\n\n')

        file.write('People,\n')
        file.write('    non_HM_spaces people,            !- Name\n')
        file.write('    non_HM_spaces,        !- Zone or ZoneList Name\n')
        file.write('    office occupancy year,    !- Number of People Schedule Name\n')
        file.write('    People/Area,              !- Number of People Calculation Method\n')
        file.write('    ,                         !- Number of People\n')
        file.write('    0.1076,                   !- People per Zone Floor Area\n')
        file.write('    ,                         !- Zone Floor Area per Person\n')
        file.write('    0.3,                      !- Fraction Radiant\n')
        file.write('    0.556,                    !- Sensible Heat Fraction\n')
        file.write('    office activity year;     !- Activity Level Schedule Name\n')

def add_HM(idf_file):
    with open(idf_file, 'a') as file:
        # file.write('\n\n\n')
        # file.write('! Hybrid:Models for the hybrid modeling\n')
        # file.write('HybridModel:Zone,\n')
        # file.write('    S2_front_HybridModel,    !- Name\n')
        # file.write('    S2 office front,         !- Zone Name\n')
        # file.write('    No,                     !- Calculate Zone Internal Thermal Mass\n')
        # file.write('    Yes,                      !- Calculate Zone Air Infiltration Rate\n')
        # file.write('    No,                      !- Calculate Zone People Count\n')
        # file.write('    S2_front_T,              !- Zone Measured Air Temperature Schedule Name\n')
        # file.write('    ,                        !- Zone Measured Air Humidity Ratio Schedule Name\n')
        # file.write('    ,                        !- Zone Measured Air CO2 Concentration Schedule Name\n')
        # file.write('    Dummy People Activity Schedule,  !- Zone Input People Activity Schedule Name\n')
        # file.write('    1,                       !- Begin Month\n')
        # file.write('    1,                       !- Begin Day of Month\n')
        # file.write('    12,                      !- End Month\n')
        # file.write('    31,                      !- End Day of Month\n')
        # file.write('    S2_front_Inlet_T,        !- Zone Input Supply Air Temperature Schedule Name\n')
        # file.write('    S2_front_Inlet_m;        !- Zone Input Supply Air Mass Flow Rate Schedule Name\n\n')

        # file.write('HybridModel:Zone,\n')
        # file.write('    S2_left_HybridModel,     !- Name\n')
        # file.write('    S2 office left,          !- Zone Name\n')
        # file.write('    No,                     !- Calculate Zone Internal Thermal Mass\n')
        # file.write('    Yes,                      !- Calculate Zone Air Infiltration Rate\n')
        # file.write('    No,                      !- Calculate Zone People Count\n')
        # file.write('    S2_left_T,               !- Zone Measured Air Temperature Schedule Name\n')
        # file.write('    ,                        !- Zone Measured Air Humidity Ratio Schedule Name\n')
        # file.write('    ,                        !- Zone Measured Air CO2 Concentration Schedule Name\n')
        # file.write('    Dummy People Activity Schedule,  !- Zone Input People Activity Schedule Name\n')
        # file.write('    1,                       !- Begin Month\n')
        # file.write('    1,                       !- Begin Day of Month\n')
        # file.write('    12,                      !- End Month\n')
        # file.write('    31,                      !- End Day of Month\n')
        # file.write('    S2_left_Inlet_T,         !- Zone Input Supply Air Temperature Schedule Name\n')
        # file.write('    S2_left_Inlet_m;        !- Zone Input Supply Air Mass Flow Rate Schedule Name\n\n')

        # file.write('HybridModel:Zone,\n')
        # file.write('    S2_right_HybridModel,    !- Name\n')
        # file.write('    S2 office right,         !- Zone Name\n')
        # file.write('    No,                     !- Calculate Zone Internal Thermal Mass\n')
        # file.write('    Yes,                      !- Calculate Zone Air Infiltration Rate\n')
        # file.write('    No,                      !- Calculate Zone People Count\n')
        # file.write('    S2_right_T,              !- Zone Measured Air Temperature Schedule Name\n')
        # file.write('    ,                        !- Zone Measured Air Humidity Ratio Schedule Name\n')
        # file.write('    ,                        !- Zone Measured Air CO2 Concentration Schedule Name\n')
        # file.write('    Dummy People Activity Schedule,  !- Zone Input People Activity Schedule Name\n')
        # file.write('    1,                       !- Begin Month\n')
        # file.write('    1,                       !- Begin Day of Month\n')
        # file.write('    12,                      !- End Month\n')
        # file.write('    31,                      !- End Day of Month\n')
        # file.write('    S2_right_Inlet_T,        !- Zone Input Supply Air Temperature Schedule Name\n')
        # file.write('    S2_right_Inlet_m;        !- Zone Input Supply Air Mass Flow Rate Schedule Name\n\n')

        # file.write('HybridModel:Zone,\n')
        # file.write('    S2_back_HybridModel,     !- Name\n')
        # file.write('    S2 office back,          !- Zone Name\n')
        # file.write('    No,                     !- Calculate Zone Internal Thermal Mass\n')
        # file.write('    Yes,                      !- Calculate Zone Air Infiltration Rate\n')
        # file.write('    No,                      !- Calculate Zone People Count\n')
        # file.write('    S2_back_T,               !- Zone Measured Air Temperature Schedule Name\n')
        # file.write('    ,                        !- Zone Measured Air Humidity Ratio Schedule Name\n')
        # file.write('    ,                        !- Zone Measured Air CO2 Concentration Schedule Name\n')
        # file.write('    Dummy People Activity Schedule,  !- Zone Input People Activity Schedule Name\n')
        # file.write('    1,                       !- Begin Month\n')
        # file.write('    1,                       !- Begin Day of Month\n')
        # file.write('    12,                      !- End Month\n')
        # file.write('    31,                      !- End Day of Month\n')
        # file.write('    S2_back_Inlet_T,         !- Zone Input Supply Air Temperature Schedule Name\n')
        # file.write('    S2_back_Inlet_m;        !- Zone Input Supply Air Mass Flow Rate Schedule Name\n\n')

        file.write('\n\n\n')
        file.write('! Hybrid:Models for the hybrid modeling\n')
        file.write('HybridModel:Zone,\n')
        file.write('    S2_front_HybridModel,    !- Name\n')
        file.write('    S2 office front,         !- Zone Name\n')
        file.write('    No,                     !- Calculate Zone Internal Thermal Mass\n')
        file.write('    No,                      !- Calculate Zone Air Infiltration Rate\n')
        file.write('    Yes,                      !- Calculate Zone People Count\n')
        file.write('    S2_front_T,              !- Zone Measured Air Temperature Schedule Name\n')
        file.write('    ,                        !- Zone Measured Air Humidity Ratio Schedule Name\n')
        file.write('    ,                        !- Zone Measured Air CO2 Concentration Schedule Name\n')
        file.write('    Dummy People Activity Schedule,  !- Zone Input People Activity Schedule Name\n')
        file.write('    1,                       !- Begin Month\n')
        file.write('    1,                       !- Begin Day of Month\n')
        file.write('    12,                      !- End Month\n')
        file.write('    31,                      !- End Day of Month\n')
        file.write('    S2_front_Inlet_T,        !- Zone Input Supply Air Temperature Schedule Name\n')
        file.write('    S2_front_Inlet_m;        !- Zone Input Supply Air Mass Flow Rate Schedule Name\n\n')

        file.write('HybridModel:Zone,\n')
        file.write('    S2_left_HybridModel,     !- Name\n')
        file.write('    S2 office left,          !- Zone Name\n')
        file.write('    No,                     !- Calculate Zone Internal Thermal Mass\n')
        file.write('    No,                      !- Calculate Zone Air Infiltration Rate\n')
        file.write('    Yes,                      !- Calculate Zone People Count\n')
        file.write('    S2_left_T,               !- Zone Measured Air Temperature Schedule Name\n')
        file.write('    ,                        !- Zone Measured Air Humidity Ratio Schedule Name\n')
        file.write('    ,                        !- Zone Measured Air CO2 Concentration Schedule Name\n')
        file.write('    Dummy People Activity Schedule,  !- Zone Input People Activity Schedule Name\n')
        file.write('    1,                       !- Begin Month\n')
        file.write('    1,                       !- Begin Day of Month\n')
        file.write('    12,                      !- End Month\n')
        file.write('    31,                      !- End Day of Month\n')
        file.write('    S2_left_Inlet_T,         !- Zone Input Supply Air Temperature Schedule Name\n')
        file.write('    S2_left_Inlet_m;        !- Zone Input Supply Air Mass Flow Rate Schedule Name\n\n')

        file.write('HybridModel:Zone,\n')
        file.write('    S2_right_HybridModel,    !- Name\n')
        file.write('    S2 office right,         !- Zone Name\n')
        file.write('    No,                     !- Calculate Zone Internal Thermal Mass\n')
        file.write('    No,                      !- Calculate Zone Air Infiltration Rate\n')
        file.write('    Yes,                      !- Calculate Zone People Count\n')
        file.write('    S2_right_T,              !- Zone Measured Air Temperature Schedule Name\n')
        file.write('    ,                        !- Zone Measured Air Humidity Ratio Schedule Name\n')
        file.write('    ,                        !- Zone Measured Air CO2 Concentration Schedule Name\n')
        file.write('    Dummy People Activity Schedule,  !- Zone Input People Activity Schedule Name\n')
        file.write('    1,                       !- Begin Month\n')
        file.write('    1,                       !- Begin Day of Month\n')
        file.write('    12,                      !- End Month\n')
        file.write('    31,                      !- End Day of Month\n')
        file.write('    S2_right_Inlet_T,        !- Zone Input Supply Air Temperature Schedule Name\n')
        file.write('    S2_right_Inlet_m;        !- Zone Input Supply Air Mass Flow Rate Schedule Name\n\n')

        file.write('HybridModel:Zone,\n')
        file.write('    S2_back_HybridModel,     !- Name\n')
        file.write('    S2 office back,          !- Zone Name\n')
        file.write('    No,                     !- Calculate Zone Internal Thermal Mass\n')
        file.write('    No,                      !- Calculate Zone Air Infiltration Rate\n')
        file.write('    Yes,                      !- Calculate Zone People Count\n')
        file.write('    S2_back_T,               !- Zone Measured Air Temperature Schedule Name\n')
        file.write('    ,                        !- Zone Measured Air Humidity Ratio Schedule Name\n')
        file.write('    ,                        !- Zone Measured Air CO2 Concentration Schedule Name\n')
        file.write('    Dummy People Activity Schedule,  !- Zone Input People Activity Schedule Name\n')
        file.write('    1,                       !- Begin Month\n')
        file.write('    1,                       !- Begin Day of Month\n')
        file.write('    12,                      !- End Month\n')
        file.write('    31,                      !- End Day of Month\n')
        file.write('    S2_back_Inlet_T,         !- Zone Input Supply Air Temperature Schedule Name\n')
        file.write('    S2_back_Inlet_m;        !- Zone Input Supply Air Mass Flow Rate Schedule Name\n\n')



def add_Output_Var(idf_file):
    with open(idf_file, 'a') as file:
        file.write('\n\n\n')
        file.write('! Output meters\n')
        file.write('Output:Meter,Electricity:Facility,Monthly; !- [J]\n')
        file.write('Output:Meter,Gas:Facility,Monthly; !- [J]\n')
        file.write('Output:Variable,S2 office front,Zone Infiltration Air Change Rate,hourly;\n')
        file.write('Output:Variable,S2 office left,Zone Infiltration Air Change Rate,hourly;\n')
        file.write('Output:Variable,S2 office right,Zone Infiltration Air Change Rate,hourly;\n')
        file.write('Output:Variable,S2 office back,Zone Infiltration Air Change Rate,hourly;\n')
        file.write('Output:Variable,S2 office front,Zone Infiltration Hybrid Model Air Change Rate,Hourly;\n')
        file.write('Output:Variable,S2 office left,Zone Infiltration Hybrid Model Air Change Rate,Hourly;\n')
        file.write('Output:Variable,S2 office right,Zone Infiltration Hybrid Model Air Change Rate,Hourly;\n')
        file.write('Output:Variable,S2 office back,Zone Infiltration Hybrid Model Air Change Rate,Hourly;\n')
        file.write('Output:Variable,S2 office front,Zone Hybrid Model People Count,Hourly;\n')
        file.write('Output:Variable,S2 office left,Zone Hybrid Model People Count,Hourly;\n')
        file.write('Output:Variable,S2 office right,Zone Hybrid Model People Count,Hourly;\n')
        file.write('Output:Variable,S2 office back,Zone Hybrid Model People Count,Hourly;\n')
        file.write('Output:Variable,S2 office front,Zone People Occupant Count,hourly;\n')
        file.write('Output:Variable,S2 office left,Zone People Occupant Count,hourly;\n')
        file.write('Output:Variable,S2 office right,Zone People Occupant Count,hourly;\n')
        file.write('Output:Variable,S2 office back,Zone People Occupant Count,hourly;\n')

def add_Output_Var_calibrating(idf_file):
    with open(idf_file, 'a') as file:
        file.write('\n\n\n')
        file.write('! Output meters\n')
        file.write('Output:Meter,Electricity:Facility,Monthly; !- [J]\n')
        file.write('Output:Meter,Gas:Facility,Monthly; !- [J]\n')



def main():
    idf_name_in = 'Baseline_V0.0.idf'
    # idf_name_out_1 = './simulations/tweaked_CBES_model_v0.1.idf'
    idf_name_out_1 = './simulations/in.idf'
    idf_name_out_2 = './simulations/tweaked_CBES_model_w_HM.idf'
    # idf_name_out_3 = 'tweaked_CBES_model_v0.3.idf'

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
    t_occ_density = 1
    n_boiler_eff = 0.6
    n_waterHeater_eff = 0.6
    t_infiltration = 1


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
    add_HM(idf_name_out_1)
    add_Sch_File(idf_name_out_1)
    add_Output_Var(idf_name_out_1)

    idf.saveas(idf_name_out_2)
    add_HM_ach(idf_name_out_2)
    add_HM_occ(idf_name_out_2)
    add_Sch_File_calibrating(idf_name_out_2)
    add_Output_Var_calibrating(idf_name_out_2)




main()