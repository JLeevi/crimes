def create_insert_crimes_sql_query(columns, rows, sql_file_path):
    create_table_sql = _create_crime_table_query(columns)
    insert_queries = _create_insert_query(rows)
    with open(sql_file_path, "w") as f:
        f.write(create_table_sql + "\n")
        f.write("\n".join(insert_queries))


def _create_crime_table_query(columns):
    columns = [c for c in columns if c != "incident_id"]
    columns = [
        f"{column_name} VARCHAR(255)"
        for column_name in columns
    ]
    columns = ",\n".join(columns)
    create_table_sql = f"""
CREATE TABLE IF NOT EXISTS crime (
incident_id VARCHAR(255) PRIMARY KEY,
{columns}
);
"""
    return create_table_sql


def _create_insert_query(rows):
    inserts = []
    for row in rows:
        row = ", ".join([f"'{value}'" for value in row])
        inserts.append(f"INSERT INTO crime VALUES ({row})\
 ON CONFLICT DO NOTHING;")
    return inserts
