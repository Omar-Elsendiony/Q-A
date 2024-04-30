# import sqlite3
# # Open the file in read mode
# # with open('o:/DriveFiles/GP_Projects/Bug-Repair/fp/lol.txt', 'r') as file:
# #     # Read the contents of the file
# #     contents = file.read()

# # Print the contents of the file
# # print(contents)
# # Connect to the database
# conn = sqlite3.connect('o:/DriveFiles/GP_Projects/Bug-Repair/fp/common.db')

# # Create a cursor object
# cursor = conn.cursor()

# sql_query = """SELECT name FROM sqlite_master 
#     WHERE type='table';"""

# # Execute a query to fetch data from a table
# # cursor.execute(sql_query)

# sql_query = """SELECT * from FunctionInformation"""
# cursor.execute(sql_query)


# # Fetch all the rows from the result set
# rows = cursor.fetchall()

# # Iterate over the rows and print the data
# for row in rows:
#     print(row)

# # Close the cursor and the connection
# cursor.close()
# conn.close()