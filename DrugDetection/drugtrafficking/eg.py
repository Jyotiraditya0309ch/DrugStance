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
        SELECT 
    p.post_id,
    p.user,
    p.description,
    p.imgSrc,
    p.location,
    GROUP_CONCAT(c.text ORDER BY c.text SEPARATOR ' , ') AS comments,
    GROUP_CONCAT(c.comment_by ORDER BY c.text SEPARATOR ' , ') AS comment_authors
FROM 
    posts p
LEFT JOIN 
    comments c ON p.post_id = c.post_id
LEFT JOIN 
    suspicious_users s ON p.user = s.user_id
LEFT JOIN 
    safe_posts sp ON p.post_id = sp.post_id
WHERE 
    s.user_id IS NULL   -- Include only users not in suspicious_users
    AND sp.post_id IS NULL  -- Include only posts not in safe_posts
    AND p.description REGEXP '#(drug|powder|cocaine|stuff|marijuana|heroin|stash)'
GROUP BY 
    p.post_id, p.user, p.description, p.imgSrc, p.location;

    """
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all rows from the executed query
    all_entries = cursor.fetchall()
    
    # Print raw fetched entries for debugging
    
    
    # Convert each row to a dictionary, using column names as keys
    data = []
    for entry in all_entries:
        # Convert comments and comment_authors to lists
        comments = entry['comments'].split(' , ') if entry['comments'] else []
        comment_authors = entry['comment_authors'].split(' , ') if entry    ['comment_authors'] else []
        
        # Create a new dictionary with lists for comments and authors
        entry_dict = {
            'post_id': entry['post_id'],
            'user': entry['user'],
            'description': entry['description'],
            'imgSrc': entry['imgSrc'],
            'location': entry['location'],
            'comments': comments,
            'comment_authors': comment_authors
        }
        
        data.append(entry_dict)
    
    # Convert the list of dictionaries to JSON
    
    
    # Close the database connection
    database.close()
    return data

# return json_data
