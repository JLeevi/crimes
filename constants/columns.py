columns_to_keep = [
    'incident_id',
    'property_value',
    'prop_desc_name',
    'prop_loss_desc',
    'crime_against',
    'offense_category_name',
    'location_name',
    'criminal_act_name',
    'age_num',
    'race_desc',
    'sex_code',
    'relationship_name'
]

map_original_column_to_target = {
    'incident_id': 'incident_id',
    'property_value': 'property_value',
    'prop_desc_name': 'property_description',
    'prop_loss_desc': 'property_loss_description',
    'crime_against': 'crime_against',
    'offense_category_name': 'offense_category',
    'location_name': 'location',
    'criminal_act_name': 'criminal_act',
    'age_num': 'age',
    'race_desc': 'race_description',
    'sex_code': 'sex',
    'relationship_name': 'relationship'
}
