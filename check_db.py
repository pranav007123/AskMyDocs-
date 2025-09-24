import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('Tables:', tables)

# Check if user table exists with different name
for table_name in ['user', 'users', 'User']:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"Table '{table_name}' has {count} records")
    except:
        print(f"Table '{table_name}' does not exist")

conn.close()
