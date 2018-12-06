import eco_connect
from eco_connect import FactsService

facts_service = FactsService()

# df_data = facts_service.get_facts(building_id = 60,
#     start_date = '2018-1-1 8:00',
#     end_date = '2018-1-1 12:00',
#     result_format = 'pandas')

# df_point_mapping = facts_service.get_point_mapping(building_id = 60, result_format = 'pandas')
# df_equipments = facts_service.get_equipment(building_id = 60, result_format = 'pandas')
df_native_names = facts_service.get_native_names(building_id = 60, result_format = 'pandas')

# df_point_mapping.to_csv('point_mapping.csv', index = False)
# df_equipments.to_csv('equipments.csv', index = False)
# df_native_names.to_csv('native_names.csv', index = False)

s_date = '2018-5-2'
e_date = '2018-5-3'

df_data = facts_service.get_facts(
    building_id=60, 
    start_date=s_date + ' 0:00', 
    end_date=e_date + ' 23:55', 
    # start_hour='', 
    # end_hour='', 
    equipment_names=[], 
    equipment_types=[], 
    excluded_days=[], 
    excluded_dates=[], 
    point_classes=[], 
    eco_point_ids=[], 
    display_names=[], 
    native_names=[], 
    point_class_expression=[], 
    native_name_expression=[], 
    display_name_expression=[], 
    result_format='pandas'
    )

# print(df_data.tail(10))

df_data.to_csv(s_date + '~' + e_date + '_sample_data.csv', index = False)

