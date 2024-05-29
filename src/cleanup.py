from flask import Flask, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
import mysql.connector as mysql
import bcrypt

def delete_old_students():
    # Connect to the database
    db = mysql.connect(
    host="172.17.0.2",
    user="user",
    passwd="MaaGodt*7913!",
    database="LogunitDB"
    )
    cursor = db.cursor()

    # Calculate the date three years ago from today
    three_years_ago = datetime.now() - timedelta(days=3*365)

    # Delete students who were added more than three years ago
    delete_query = "DELETE FROM Students WHERE created_at < %s"
    cursor.execute(delete_query, (three_years_ago,))

    # Commit the transaction
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    delete_old_students()