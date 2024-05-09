import mysql.connector

# Establish a connection to the database
try:
    conn = mysql.connector.connect(
        host='79.171.148.163',       # Host ip på DB
        port='3306', # Host portnummer
        user='user',   # your MySQL username
        passwd='password', # your MySQL password
        database='DBSimpel'     # the name of the database
    )
    cursor = conn.cursor()
    
    insert_query = "INSERT INTO students (firstName, surname) VALUES (%s, %s)"
    value = ("Navn", "Navnsen")
    
    cursor.execute(insert_query, value)
    conn.commit()

    print("Name inserted successfully.")

except mysql.connector.Error as error:
    print(f"Failed to insert data into MySQL table: {error}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed")

