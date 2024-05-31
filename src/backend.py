from flask import Flask, request, jsonify
import mysql.connector as mysql
import bcrypt
from datetime import datetime, timedelta, date

app = Flask(__name__)

class StudentTable:
    def __init__(self, db, cursor):
        self.db = db
        self.mycursor = cursor
    
    def calculate_days(self, uddannelses_Hold_ID):
        query = """
        SELECT navn, opstartsDato
        FROM Students
        WHERE uddannelseID = %s
        """
        self.mycursor.execute(query, (uddannelses_Hold_ID,))
        results = self.mycursor.fetchall()
        
        if not results:
            return []
        
        today = datetime.now().date()
        days_diff_list = []
        
        for result in results:
            navn = result['navn']
            start_date = result['opstartsDato']  # Already a date object
            
            # Calculate weekdays difference
            days_difference = self.count_weekdays(start_date, today)
            
            days_diff_list.append({'navn': navn, 'days_difference': days_difference})
        
        return days_diff_list

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

    def amount_Of_Checkins(self, uddannelses_Hold_ID):
        query = """
        SELECT s.navn, COUNT(c.studentID) AS antal
        FROM Students s
        LEFT JOIN Checkind c ON s.studentID = c.studentID
        WHERE s.uddannelseID = %s
        GROUP BY s.studentID, s.navn
        """
        self.mycursor.execute(query, (uddannelses_Hold_ID,))
        result = self.mycursor.fetchall()
        
        # Convert the result to the desired dictionary format
        checkin_counts = [{'navn': row['navn'], 'antal': row['antal']} for row in result]
        
        return checkin_counts

    def calc_attendance(self, checkin_counts, days_difference):
        if not days_difference:
            return {}

        # Create a dictionary from days_difference for quick lookup
        days_diff_dict = {entry['navn']: entry['days_difference'] for entry in days_difference}

        # Create a dictionary for check-in counts for quick lookup, defaulting to 0 if not found
        checkin_counts_dict = {entry['navn']: entry['antal'] for entry in checkin_counts}

        calced_attendance = {}
        for navn, days_diff in days_diff_dict.items():
            antal = checkin_counts_dict.get(navn, 0)  # Default to 0 if not found in checkin_counts
            diff_procent = (days_diff - antal) / days_diff * 100
            diff_procent=float("{:.2f}".format(diff_procent))
            calced_attendance[navn] = diff_procent

        return calced_attendance

    def checkedin_today(self, uddannelses_Hold_ID):
        # Get today's date
        today_date = datetime.now().date()
        
        # Query to check if each student has checked in today
        query = """
        SELECT s.navn, CASE WHEN COUNT(c.checkin) > 0 THEN TRUE ELSE FALSE END AS checked_in_today
        FROM Students s
        LEFT JOIN Checkind c ON s.studentID = c.studentID AND DATE(c.checkin) = %s
        WHERE s.uddannelseID = %s
        GROUP BY s.navn
        """
        
        self.mycursor.execute(query, (today_date, uddannelses_Hold_ID))
        result = self.mycursor.fetchall()
        
        # Create a dictionary to store checked-in status for each student
        checked_in_today = {entry['navn']: entry['checked_in_today'] for entry in result}
        
        return checked_in_today

    def get_attend_table(self, uddannelses_Hold_ID):
        # Calculate the days difference for students in the educational group
        days_diff_list = self.calculate_days(uddannelses_Hold_ID)
        
        # Get the number of check-ins for students in the educational group
        checkin_counts = self.amount_Of_Checkins(uddannelses_Hold_ID)
        
        # Calculate attendance difference percentage
        calced_attendance = self.calc_attendance(checkin_counts, days_diff_list)
        
        # Check if students have checked in today
        checks = self.checkedin_today(uddannelses_Hold_ID)
        
        # Combine all data into a single dictionary
        attendance_table = []
        for student in days_diff_list:
            navn = student['navn']
            days_difference = student['days_difference']
            attendance_percentage = calced_attendance.get(navn, 100.0)  # Default to 100% if not found
            checked_in_today = checks.get(navn, False)  # Default to False if not found
            attendance_table.append({
                'navn': navn,
                'attendance_percentage': attendance_percentage,
                'checked_in_today': checked_in_today
            })
        
        return attendance_table

class DataHandler:
    def __init__(self):
        self.db = mysql.connect(
        host="79.171.148.163",
        user="user",
        passwd="MaaGodt*7913!",
        database="LogunitDB"
        )
        self.mycursor = self.db.cursor(dictionary=True)

        print("connected to database")

        self.table = StudentTable(self.db, self.mycursor)


    def check_in(self, room_id=None, student_id=None):
        try:
            self.mycursor.execute('SELECT lokaleNavn FROM Lokaler WHERE lokaleID = %s', (room_id,))
            room_name = self.mycursor.fetchone()

            if not room_name:
                return {"status": "error", "message": "Room not found"}, 404

            self.mycursor.execute('SELECT navn FROM Students WHERE studentID = %s', (student_id,))
            student_name = self.mycursor.fetchone()

            if not student_name:
                return{"status": "error", "message": "Student not found"}, 404
            
            self.mycursor.execute('INSERT INTO Checkind (studentID, lokaleID, checkIn) VALUES (%s, %s, NOW())', (student_id, room_id))
            self.db.commit()
            return {"status": "success", "message": "Check-in successful"}, 200
        
        except Exception:
            self.db.rollback()
            return {'status': 'Error during check-in'}
        
    def login_procedure(self, username, password):
        try:
            self.mycursor.execute('SELECT email, password FROM Underviser WHERE (email, password) = (%s, %s)', (username, password))
            result = self.mycursor.fetchone()

            if result and bcrypt.checkpw(password.encode('utf-8'), result['password'].encode('utf-8')):
                return {'status': 'Login: Credentials accepted'}
            else:
                return {'status': 'Error: Invalid credentials'}
            
        except Exception:
            return {'status': 'Error during handeling of login procedure'}

    def search(self, query):
        try:
            search_term = f"%{query}%"
            self.mycursor.execute("SELECT studentID, navn FROM Students WHERE navn LIKE %s", (search_term,))
            result = self.mycursor.fetchall()

            return result
            
        except Exception:
            return {'status': 'Error during search'}

    def search_uddannelse(self, query):
        try:
            search_term = f"%{query}%"
            self.mycursor.execute("SELECT uddannelseNavn FROM UddannelsesHold WHERE uddannelseNavn LIKE %s", (search_term,))
            result = self.mycursor.fetchall()

            return result
            
        except Exception:
            return {'status': 'Error searching for team'}

    def profile(self, id):
        try:
            self.mycursor.execute("SELECT uddannelseID FROM Students WHERE studentID = %s", (id,))
            uddannelse_id = self.mycursor.fetchone()['uddannelseID']

            self.mycursor.execute("SELECT uddannelseNavn FROM UddannelsesHold WHERE uddannelseID = %s", (uddannelse_id,))
            uddannelse_navn = self.mycursor.fetchone()['uddannelseNavn']

            self.mycursor.execute("SELECT navn FROM Students WHERE studentID = %s", (id,))
            student_info = self.mycursor.fetchone()['navn']

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
            self.mycursor.execute('INSERT INTO Underviser (email, password (%s, %s)', (username, hashed_password.decode('utf-8')))
            self.db.commit()

            return {'status': 'Create User: Success'}
        
        except Exception:
            return {'status': 'Error registering user'}

    def create_team(self, new_team_name, meet_time):
        try:
            self.mycursor.execute('INSERT INTO UddannelsesHold (uddannelseNavn, tidsPunkt) VALUES (%s, %s)', (new_team_name, meet_time))
            self.db.commit()
            
            return {'status': 'Create Team: Success'}
        
        except Exception:
            return {'status': 'Error creating team'}

    def create_student(self, student_name, student_team, student_startdate):
        try:
            self.mycursor.execute("SELECT uddannelseID FROM UddannelsesHold WHERE uddannelseNavn = %s", (student_team,))
            uddannelse_id = self.mycursor.fetchone()['uddannelseID']

            self.mycursor.execute('INSERT INTO Students (navn, uddannelseID, opstartsDato) VALUES (%s, %s, %s)', (student_name, uddannelse_id, student_startdate))
            self.db.commit()
            
            return {'status': 'Create student: Success'}
        
        except Exception:
            return {'status': 'Error creating student'}

    def delete_students(self, students):
        try:
            placeholders = ', '.join(['%s'] * len(students))
            query = f"DELETE FROM Students WHERE navn IN ({placeholders})"
            self.mycursor.execute(query, students)
            self.db.commit()

            if self.mycursor.rowcount > 0:
                return {'status': 'Students deleted'}
            else:
                return {'status': 'Error: No students deleted'}

        except Exception:
            return {'status':'Error deleting student'}

    def retrieve_team(self):
        try:
            self.mycursor.execute("SELECT uddannelseNavn FROM UddannelsesHold")
            result = self.mycursor.fetchall()

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
            self.mycursor.execute("""
            SELECT Students.navn, Students.studentID, UddannelsesHold.uddannelseNavn, Students.opstartsDato
            FROM Students
            LEFT JOIN UddannelsesHold ON Students.uddannelseID = UddannelsesHold.uddannelseID
            """)
            result = self.mycursor.fetchall()

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
        self.mycursor.execute("SELECT checkIn FROM Checkind WHERE studentID = %s", (student_id,))
        result = self.mycursor.fetchall()

        if result:
            return {
                'status': 'Session: data update',
                'student_data': result
            }
        else:
            return {'status': 'Checkin data not found'}

    def get_student_average(self, student_id):
        try:
            team_id = self.mycursor.execute("SELECT uddannelseID FROM Students WHERE studentID = %s", (student_id))
            result = self.table.get_attend_table(team_id)
            navn = self.mycursor.execute("SELECT navn FROM Students WHERE studentID = %s", (student_id))
            for student in result:
                if student['navn'] == navn:
                    attendance = student['attendance_percentage']
                    checked_in_today = student['checked_in_today']
                    break
            return {'attendance': attendance, 'checked_in_today': checked_in_today}
        
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
                return jsonify(error="No 'room_id' or 'student_id' specified in JSON data."), 400

            result = data_handler.check_in(room_id, student_id)
            return jsonify(result), 200
        
        case 'login':
            print("Recieved login request")
            username = data.get('user')
            password = data.get('pass')

            if not username or not password:
                return jsonify(error="No 'user' or 'pass' specified in JSON data."), 400

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
                return jsonify({'error':"No 'studentID' specified in JSON data."}), 400

            result = data_handler.profile(student_id)
            return jsonify(result), 200
        
        case 'create user request':
            username = data.get('user')
            password = data.get('pass')

            if not username or not password:
                return jsonify("No 'user' or 'pass' specified in JSON data"), 400
            
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
            result = data_handler.get_student_average(id)
            return jsonify(result), 200

        case _:
            return jsonify({'error':"Data 'subject' not supported."}), 400
        
        

if __name__ == "__main__":
    app.run(debug=True, port=13371)