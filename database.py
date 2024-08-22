import pyodbc
import sys
import json
# Define the connection string
conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=TUANMR;'
    'Database=Sale;'
    'Trusted_Connection=yes;'
)

# Create a cursor object using the connection
cursor = conn.cursor()

def fetch_all_sales():
    cursor.execute('SELECT * FROM dbo.Sales_v11')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
fetch_all_sales()

def insert_sale(*values):
    # Replace with the actual column names in your database
    columns = [
        'Segment', 'Country', 'Product', 'Discount_Band', 'Units_Sold', 
        'Manufacturing_Price', 'Sale_Price', 'Gross_Sales', 'Discounts', 
        'Sales', 'COGS', 'Profit', 'Date', 'Month_Number', 'Month_Name', 'Year'
    ]

    if len(values) != len(columns):
        raise ValueError("Number of values must match the number of columns")

    placeholders = ', '.join(['?' for _ in columns])
    column_names = ', '.join(columns)
    sql = f'''
        INSERT INTO dbo.Sales_v11 ({column_names})
        VALUES ({placeholders})
    '''
    cursor.execute(sql, values)
    conn.commit()
    print("Record inserted successfully.")

def delete_sale(id):
    cursor.execute('DELETE FROM dbo.Sales_v11 WHERE ID = ?', id)
    conn.commit()
    print(f"Record with ID {id} deleted successfully.")

def update_sale(id, **kwargs):
    columns_to_update = []
    values = []
    for column, value in kwargs.items():
        if value is not None:
            columns_to_update.append(f"{column} = ?")
            values.append(value)
    if not columns_to_update:
        raise ValueError("No columns to update.")
    set_clause = ", ".join(columns_to_update)
    sql = f"UPDATE dbo.Sales_v11 SET {set_clause} WHERE ID = ?"
    values.append(id)
    cursor.execute(sql, *values)
    conn.commit()
    print(f"Record with ID {id} updated successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python database.py <action> [<params>]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "fetch_all":
        fetch_all_sales()
    elif action == "insert":
        if len(sys.argv) < 3:
            print("Usage: python database.py insert <values>")
            sys.exit(1)
        values = sys.argv[2:]
        insert_sale(*values)
    elif action == "delete":
        if len(sys.argv) < 3:
            print("Usage: python database.py delete <id>")
            sys.exit(1)
        id = sys.argv[2]
        delete_sale(id)
    elif action == "update":
        if len(sys.argv) < 4:
            print("Usage: python database.py update <id> <json_file_path>")
            sys.exit(1)
        
        id = sys.argv[2]
        json_file_path = sys.argv[3]

        try:
            with open(json_file_path, 'r') as f:
                kwargs = json.load(f)
        except Exception as e:
            print(f"Error reading JSON from file: {e}")
            sys.exit(1)

        update_sale(id, **kwargs) # Call update_sale after kwargs is populated

    else:
        print("Unknown action:", action)
        print("Usage: python database.py <fetch_all|insert|delete|update> [<params>]")
        sys.exit(1)

cursor.close()
conn.close()
