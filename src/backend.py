from flask import Flask, request, jsonify
import mysql.connector as mysql
from mysql.connector import Error, OperationalError
import bcrypt
from datetime import datetime, timedelta

app = Flask(__name__)

class DatabaseConnection:
    def __init__(self):
        self.db = None
        self.mycursor = None
        self.connect()

    def connect(self):
        try:
            self.db = mysql.connect(
                host="79.171.148.163",
                user="user",
                passwd="MaaGodt*7913!",
                database="LogunitDB",
                connection_timeout=300
            )
            self.mycursor = self.db.cursor(dictionary=True)
            print("Connected to database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def reconnect(self):
        if self.db is None or not self.db.is_connected():
            self.connect()

    def execute_query(self, query, params=None):
        self.reconnect()
        try:
            self.mycursor.execute(query, params)
        except OperationalError as err:
            if err.errno in (mysql.connector.errorcode.CR_SERVER_LOST, mysql.connector.errorcode.CR_SERVER_GONE_ERROR):
                print("Lost connection to MySQL server, attempting to reconnect...")
                self.reconnect()
                self.mycursor.execute(query, params)
            else:
                print(f"Error executing query: {err}")
                raise

    def fetchall(self):
        return self.mycursor.fetchall()

    def fetchone(self):
        return self.mycursor.fetchone()

    def fetchone_column(self, column):
        row = self.fetchone()
        if row:
            return row.get(column)
        return None

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

db_connection = DatabaseConnection()

class StudentTable:
    def __init__(self):
        self.db_connection = db_connection

    def count_weekdays(self, start_date, end_date):
    # Ensure start_date is before end_date
        if start_date > end_date:
            return 0

        weekdays_count = 0

    # Loop through each day from start_date to end_date
        while start_date <= end_date:
        # Check if start_date is a weekday (Monday to Friday)
            if start_date.weekday() < 5:
                weekdays_count += 1

        # Move to the next day
        start_date += timedelta(days=1)

        return weekdays_count

    def get_attend_table(self, uddannelses_Hold_ID):
        # Get today's date
        today_date = datetime.now().date()

        # Combined query to get all required data
        query = """
        SELECT s.navn, s.opstartsDato, 
               COUNT(c.studentID) AS antal,
               MAX(CASE WHEN DATE(c.checkin) = %s THEN c.checkin ELSE NULL END) AS checked_in_today_timestamp
        FROM Students s
        LEFT JOIN Checkind c ON s.studentID = c.studentID
        WHERE s.uddannelseID = %s
        GROUP BY s.studentID, s.navn, s.opstartsDato
        """
        self.db_connection.execute_query(query, (today_date, uddannelses_Hold_ID))
        result = self.db_connection.fetchall()

        today = datetime.now().date()
        attendance_table = []

        for row in result:
            navn = row['navn']
            start_date = row['opstartsDato']
            antal = row['antal']
            checked_in_today_timestamp = row['checked_in_today_timestamp']
            days_difference = self.count_weekdays(start_date, today)
            attendance_percentage = (days_difference - antal) / days_difference * 100 if days_difference > 0 else 0
            checked_in_today = 1 if checked_in_today_timestamp is not None else 0

            attendance_table.append({
                'navn': navn,
                'attendance_percentage': attendance_percentage,
                'checked_in_today': checked_in_today,
                'checked_in_today_timestamp': checked_in_today_timestamp.time() if checked_in_today_timestamp else None
            })

        return attendance_table

class DataHandler:
    def __init__(self):
        self.db_connection = db_connection

    def check_in(self, room_id=None, student_id=None):
        try:
            query = "SELECT lokaleNavn FROM Lokaler WHERE lokaleID = %s"
            self.db_connection.execute_query(query, (room_id,))
            room_name = self.db_connection.fetchone()

            if not room_name:
                return {"status": "error", "message": "Room not found"}, 404

            query = "SELECT navn FROM Students WHERE studentID = %s"
            self.db_connection.execute_query(query, (student_id,))
            student_name = self.db_connection.fetchone()

            if not student_name:
                return{"status": "error", "message": "Student not found"}, 404
            
            query = "INSERT INTO Checkind (studentID, lokaleID, checkIn) VALUES (%s, %s, NOW())"
            self.db_connection.execute_query(query, (student_id, room_id))
            self.db_connection.commit()

            return {"status": "success", "message": "Check-in successful"}, 200
        
        except Exception:
            self.db_connection.rollback()
            return {'status': 'Error during check-in'}
        
    def login_procedure(self, username, password):
        try:
            query = "SELECT email, password FROM Underviser WHERE (email, password) = (%s, %s)"
            self.db_connection.execute_query(query, (username, password))
            result = self.db_connection.fetchone()

            if result and bcrypt.checkpw(password.encode('utf-8'), result['password'].encode('utf-8')):
                return {'status': 'Login: Credentials accepted'}
            else:
                return {'status': 'Error: Invalid credentials'}
            
        except Exception:
            return {'status': 'Error during handeling of login procedure'}

    def search(self, query):
        try:
            search_term = f"%{query}%"

            query = "SELECT studentID, navn FROM Students WHERE navn LIKE %s"
            self.db_connection.execute_query(query, (search_term,))
            result = self.db_connection.fetchall()

            return result
            
        except Exception:
            return {'status': 'Error during search'}

    def search_uddannelse(self, query):
        try:
            search_term = f"%{query}%"

            query = "SELECT uddannelseNavn FROM UddannelsesHold WHERE uddannelseNavn LIKE %s"
            self.db_connection.execute_query(query, (search_term,))
            result = self.db_connection.fetchall()

            return result
            
        except Exception:
            return {'status': 'Error searching for team'}

    def profile(self, id):
        try:
            query = "SELECT uddannelseID FROM Students WHERE studentID = %s"
            self.db_connection.execute_query(query, (id,))
            uddannelse_id = self.db_connection.fetchone_column("uddannelseID")



            query = "SELECT uddannelseNavn FROM UddannelsesHold WHERE uddannelseID = %s"
            self.db_connection.execute_query(query, (uddannelse_id,))
            uddannelse_navn = self.db_connection.fetchone_column("uddannelseNavn")



            query = "SELECT navn FROM Students WHERE studentID = %s"
            self.db_connection.execute_query(query, (id,))
            student_info = self.db_connection.fetchone_column("navn")

            if uddannelse_navn and student_info:
                return {
                    'navn': student_info,
                    'uddannelseNavn': uddannelse_navn  
                }
            else:
                return {'status': 'Error loading profile'}

        except Exception:
            return {'status': 'Error registering user'}
    
    def register_user(self, username, password):
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            query = "INSERT INTO Underviser (email, password (%s, %s)"
            self.db_connection.execute_query(query, (username, hashed_password.decode('utf-8')))
            self.db_connection.commit()

            return {'status': 'Create User: Success'}
        
        except Exception:
            return {'status': 'Error registering user'}

    def create_team(self, new_team_name, meet_time):
        try:
            query = "INSERT INTO UddannelsesHold (uddannelseNavn, tidsPunkt) VALUES (%s, %s)"
            self.db_connection.execute_query(query, (new_team_name, meet_time))
            self.db_connection.commit()
            
            return {'status': 'Create Team: Success'}
        
        except Exception:
            return {'status': 'Error creating team'}

    def create_student(self, student_name, student_team, student_startdate):
        try:

            query = "SELECT uddannelseID FROM UddannelsesHold WHERE uddannelseNavn = %s"
            self.db_connection.execute_query(query, (student_team,))
            uddannelse_id = self.db_connection.fetchone_column("uddannelseID")

            query = "INSERT INTO Students (navn, uddannelseID, opstartsDato) VALUES (%s, %s, %s)"
            self.db_connection.execute_query(query, (student_name, uddannelse_id, student_startdate))
            self.db_connection.commit()
            
            return {'status': 'Create student: Success'}
        
        except Exception:
            return {'status': 'Error creating student'}

    def delete_students(self, students):
        try:
            placeholders = ', '.join(['%s'] * len(students))

            query = f"DELETE FROM Students WHERE navn IN ({placeholders})"
            self.db_connection.execute_query(query, students)
            self.db_connection.commit()

            if self.mycursor.rowcount > 0:
                return {'status': 'Students deleted'}
            else:
                return {'status': 'Error: No students deleted'}

        except Exception:
            return {'status':'Error deleting student'}

    def retrieve_team(self):
        try:
            query = "SELECT uddannelseNavn FROM UddannelsesHold"
            self.db_connection.execute_query(query)
            result = self.db_connection.fetchall()

            if result:
                return {
                    'status': 'Retrieved team list',
                    'team_list': result  
                }
            else:
                return {'status': 'Error: team not found'}
        
        except Exception:
            return {'status': 'Error retrieving team'}
        
    def retrieve_students(self):
        try:
            query = """
            SELECT Students.navn, Students.studentID, UddannelsesHold.uddannelseNavn, Students.opstartsDato
            FROM Students
            LEFT JOIN UddannelsesHold ON Students.uddannelseID = UddannelsesHold.uddannelseID
            """
            self.db_connection.execute_query(query)
            result = self.db_connection.fetchall()

            if result:
                return {
                    'status': 'Retrieved student list',
                    'student_list': result  
                }
            else:
                return {'status': 'Error: Student not found'}
        
        except Exception:
            return {'status': 'Error retrieving students'}

    def get_student_checkin(self, student_id):
        query = "SELECT checkIn FROM Checkind WHERE studentID = %s"
        self.db_connection.execute_query(query, (student_id,))
        result = self.db_connection.fetchall()

        if result:
            return {
                'status': 'Session: data update',
                'student_data': result
            }
        else:
            return {'status': 'Checkin data not found'}

    def get_student_average(self, student_id):
        try:
            query = "SELECT checkIn FROM Checkind WHERE studentID = %s"
            self.db_connection.execute_query(query, (student_id,))
            team_id = self.db_connection.fetchone()


            query = "SELECT navn FROM Students WHERE studentID = %s"
            self.db_connection.execute_query(query, (student_id,))     
            navn = self.db_connection.fetchone()


            result = self.table.get_attend_table(team_id)
            for student in result:
                if student['navn'] == navn:
                    attendance = student['attendance_percentage']
                    checked_in_today = student['checked_in_today']
                    checked_in_timestamp = ['checked_in_today_timestamp']
                    break
            return {'attendance': attendance, 'checked_in_today': checked_in_today, 'checked_in_today_timestamp': checked_in_timestamp}
       
        except Exception:
            return {'status': 'Student average data not found'}
    

data_handler = DataHandler()
@app.route('/', methods=['POST'])
def handle():
    data = request.json

    print(data)

    subject = data.get('data')
    match(subject):
        case 'check_in':
            # Room id, student id / card id
            room_id = data.get('room_id')
            student_id = data.get('student_id')

            if not room_id or not student_id:
                return jsonify({'error':'No "room_id" or "student_id" specified in JSON data.'}), 400

            result = data_handler.check_in(room_id, student_id)
            return jsonify(result), 200
        
        case 'login':
            print("Recieved login request")
            username = data.get('user')
            password = data.get('pass')

            if not username or not password:
                return jsonify({'error':'No "user" or "pass" specified in JSON data.'}), 400

            result = data_handler.login_procedure(username, password)
            return jsonify(result), 200

        case 'search':
            query = data.get('search', '')

            if not query:
                return jsonify([])

            result = data_handler.search(query)
            return jsonify(result), 200
        
        case 'search uddannelse':
            query = data.get('search', '')

            if not query:
                return jsonify([]), 200

            result = data_handler.search_uddannelse(query)
            return jsonify(result), 200
        
        case 'profile':
            student_id = data.get('id')

            if not student_id:
                return jsonify({'error':'No "studentID" specified in JSON data.'}), 400

            result = data_handler.profile(student_id)
            return jsonify(result), 200
        
        case 'create user request':
            username = data.get('user')
            password = data.get('pass')

            if not username or not password:
                return jsonify({'error':'No "user" or "pass" specified in JSON data'}), 400
            
            result = data_handler.register_user(username, password)
            return jsonify(result), 200

        case 'create team request':
            team_name = data.get('team_name')
            team_meet_time = data.get('team_meet')

            result = data_handler.create_team(team_name, team_meet_time)
            return jsonify(result), 200

        case 'create student request':
            student_name = data.get('student_name')
            student_team = data.get('student_team')
            student_start = data.get('student_start')

            result = data_handler.create_student(student_name, student_team, student_start)
            return jsonify(result), 200

        case 'delete students':
            students = data.get('students')

            result = data_handler.delete_students(students)
            return jsonify(result), 200

        case 'request teams':
            result = data_handler.retrieve_team()
            return jsonify(result), 200
        
        case 'request students':
            result = data_handler.retrieve_students()
            return jsonify(result), 200

        case 'session get data':
            student_id = data.get('id')
            result = data_handler.get_student_checkin(student_id)
            return jsonify(result), 200
        
        case 'session get student table':
            student_id = data.get('id')
            result = data_handler.get_student_average(student_id)
            return jsonify(result), 200

        case _:
            return jsonify({'error':'Data "subject" not supported.'}), 400
        
        

if __name__ == "__main__":
    app.run(debug=True, port=13371)