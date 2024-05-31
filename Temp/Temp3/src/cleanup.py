from flask import Flask, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
import mysql.connector as mysql
import bcrypt

def delete_old_students():
    # Connect to the database
    db = mysql.connect(
    host="79.171.148.163",
    user="user",
    passwd="MaaGodt*7913!",
    database="LogunitDB"
    )
    cursor = db.cursor()
    six_months = datetime.now() - timedelta(days=180)
    query = "SELECT id, slutDato FROM Students WHERE slutDato <= %s"
    cursor.execute(query, (six_months,))
    old_students = cursor.fetchall()
    for student_id, _ in old_students:
        delete_query = "DELETE FROM Students WHERE id = %s"
        cursor.execute(delete_query, (student_id,))
        db.commit()
    db.close()
if __name__ == "__main__":
    delete_old_students()

