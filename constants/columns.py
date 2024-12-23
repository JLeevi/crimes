# Columns for crimes.parquet
columns_for_crimes = [
    'incident_id',
    'data_year',
    'offense_code',
    'offense_name',
    'location_id',
    'location_name',
    'property_description',
    'property_value'
]

# Columns for offender.parquet
columns_for_offender = [
    'incident_id',
    'offender_id',
    'age_num',
    'sex_code',
    'race_id',
    'ethnicity_id'
]

# Columns for victim.parquet
columns_for_victim = [
    'incident_id',
    'victim_id',
    'victim_type_id',
    'assignment_type_id',
    'activity_type_id',
    'age_num',
    'sex_code',
    'race_id',
    'ethnicity_id'
]

# Columns for relationship.parquet
columns_for_relationship = [
    'incident_id',
    'victim_id',
    'offender_id',
    'relationship_id',
    'relationship_code',
    'relationship_name'
]

# Mapping for column renaming (if needed)
map_original_column_to_target = {
    'incident_id': 'incident_id',
    'data_year': 'year',
    'offense_code': 'offense_code',
    'offense_name': 'offense_name',
    'location_id': 'location_id',
    'location_name': 'location',
    'property_description': 'property_description',
    'property_value': 'property_value',
    'offender_id': 'offender_id',
    'victim_id': 'victim_id',
    'victim_type_id': 'victim_type_id',
    'assignment_type_id': 'assignment_type_id',
    'activity_type_id': 'activity_type_id',
    'age_num': 'age',
    'sex_code': 'sex',
    'race_id': 'race_id',
    'ethnicity_id': 'ethnicity_id',
    'relationship_id': 'relationship_id',
    'relationship_code': 'relationship_code',
    'relationship_name': 'relationship_name'
}
