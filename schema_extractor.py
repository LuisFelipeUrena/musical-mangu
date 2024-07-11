import snowflake.connector
from dotenv import load_dotenv
import os
def connect_to_snowflake():
    # get all credentials from your .env file!
    load_dotenv()
    credentials = {
        'your_account': os.environ.get('SNOWFLAKE_ACCOUNT'),
        'your_username': os.environ.get('SNOWFLAKE_USER'),
        'your_password': os.environ.get('SNOWFLAKE_PASSWORD'),
        'your_warehouse': os.environ.get('SNOWFLAKE_WAREHOUSE'),
        'your_database': os.environ.get('SNOWFLAKE_DATABASE'),
    }
    try:
        conn = snowflake.connector.connect(
            account=credentials['your_account'],
            user=credentials['your_username'],
            password=credentials['your_password'],
            warehouse=credentials['your_warehouse'],
            database=credentials['your_database']
        )
        return conn
    except Exception as e:
        return f'An error has occurred: {e}'

def extract_schema():
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    
    # Get all schemas
    cursor.execute("SHOW SCHEMAS")
    schemas = cursor.fetchall()
    
    schema_info = {}
    for schema in schemas:
        schema_name = schema[1]
        schema_info[schema_name] = {}
        
        # Get all tables in the schema
        cursor.execute(f"SHOW TABLES IN {schema_name}")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[1]
            schema_info[schema_name][table_name] = []
            
            # Get column information for each table
            cursor.execute(f"DESCRIBE TABLE {schema_name}.{table_name}")
            columns = cursor.fetchall()
            
            for column in columns:
                column_name = column[0]
                data_type = column[1]
                schema_info[schema_name][table_name].append({
                    "name": column_name,
                    "type": data_type
                })
    
    conn.close()
    return schema_info

if __name__ == "__main__":
    # Usage
    schema_info = extract_schema()
    print(schema_info)