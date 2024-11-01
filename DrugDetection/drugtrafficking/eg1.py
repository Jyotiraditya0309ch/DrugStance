import pymysql
import json

# Connect to the Instagram database
def get_data():
    database = pymysql.connect(
        host='localhost',
        user='root',
        passwd='Chillal@123',
        database='instagram'  # specify the database name here
    )
    
    # Create a cursor object
    cursor = database.cursor(pymysql.cursors.DictCursor)  # Use DictCursor to get     results as dictionaries
    
    # SQL query to fetch all data from the posts table
    query = """
        SELECT id, username,firstname,surname, email, isOnline, lastOnline, ipaddress, location FROM users;
    """
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all rows from the executed query
    all_entries = cursor.fetchall()
    database.close()
   
    return all_entries

#print(get_data())
# return json_data
