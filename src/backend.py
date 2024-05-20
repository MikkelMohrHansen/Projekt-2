from flask import Flask, request, jsonify, redirect, url_for
import mysql.connector as mysql
import json

app = Flask(__name__)

class DataHandler:
    def __init__(self):
        self.db = mysql.connect(
        host="localhost",
        user="user",
        passwd="password",
        database="DBSimpel"
        )
        self.mycursor = self.db.cursor(dictionary=True)

        self.session = SessionHandler(self.db, self.mycursor)
        print("connected to database")

    def check_in(self, room_id=None, student_id=None):
        try:
            self.mycursor.execute('SELECT roomName FROM rooms WHERE roomID = %s', (room_id,))
            room_name = self.mycursor.fetchone()

            self.mycursor.execute('SELECT studentName FROM students WHERE studentID = %s', (student_id,))
            student_name = self.mycursor.fetchone()
            
            self.mycursor.execute('INSERT INTO attendTable (studentName, roomName, studentID) VALUES (%s, %s, %s)', (student_name, room_name, student_id))
            self.db.commit()
        
        except Exception as e:
            return e
        
    def login_procedure(self, username, password):
        try:
            self.mycursor.execute('SELECT mail, passW FROM teachers WHERE (mail, passW) = (%s, %s)', (username, password)) #Kigger databasen igennem for den indtastet mail og passwd
            result = self.mycursor.fetchone()

            if result:
                response_data = {
                    'status': 'Login: Credentials accepted'
                }
                return response_data
            else:
                response_data = {
                    'status': 'Error: Invalid credentials'
                }
                return response_data
            
        except Exception as e:
            return e

    def search(self, query):
        try:
            search_term = f"%{query}%"
            self.mycursor.execute("SELECT id, name FROM student_tabel WHERE name LIKE %s", (search_term,))
            result = self.mycursor.fetchall()

            return jsonify(result)
            
        except Exception as e:
            return e

class SessionHandler:
    def __init__(self, database, cursor):
        self.db = database
        self.mycursor = cursor

data_handler = DataHandler()

@app.route('/student_profile')
def student_profile():
    student_id = request.args.get('id')
    return redirect(url_for('profile', id=student_id))

@app.route('/profile/<id>')
def profile(id):
    return f"Student Profile Page for Student ID: {id}"

@app.route('/', methods=['POST'])
def handle():
    path = request.path

    print(path)

    match(path):
        case 'check_in':
            # Room id, student id / card id
            data = request.get_json()
            room_id = data.get('room_id')
            student_id = data.get('student_id')

            if not room_id or not student_id:
                return jsonify(error="No 'room_id' or 'student_id' specified in JSON data."), 400

            result = data_handler.generate_student(room_id, student_id)
            return jsonify(result), 200
        
        case '/api/login':
            data = request.get_json()
            print("Recieved login request")
            username = data.get('user')
            password = data.get('pass')

            if not username or not password:
                return jsonify(error="No 'user' or 'pass' specified in JSON data."), 400

            result = data_handler.login_procedure(username, password)
            return jsonify(result), 200

        case '/api/search':
            data = request.get_json()
            query = data.get('search', '')

            if not query:
                return jsonify([])


            result = data_handler.search(query)
            return jsonify(result), 200
        case _:
            return jsonify(error=f"Data '{path}' not supported."), 400



if __name__ == "__main__":
    app.run(debug=True, port=13371)