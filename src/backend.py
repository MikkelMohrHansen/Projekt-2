from flask import Flask, request, jsonify
import mysql.connector as mysql

app = Flask(__name__)

class DataHandler:
    def __init__(self):
        self.db = mysql.connect(
        host="79.171.148.163",
        user="user",
        passwd="password",
        database="LogunitDB"
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
            
            self.mycursor.execute('INSERT INTO Checkind (studentName, roomName, studentID) VALUES (%s, %s, %s)', (student_name, room_name, student_id))
            self.db.commit()
        
        except Exception as e:
            return e
        
    def login_procedure(self, username, password):
        try:
            self.mycursor.execute('SELECT email, password FROM Underviser WHERE (email, password) = (%s, %s)', (username, password))
            result = self.mycursor.fetchone()

            response_data = ''

            if result:
                response_data = {
                    'status': 'Login: Credentials accepted'
                }
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
            self.mycursor.execute("SELECT studentID, navn FROM Students WHERE navn LIKE %s", (search_term,))
            result = self.mycursor.fetchall()

            return result
            
        except Exception as e:
            return e

    def profile(self, id):
        try:
            self.mycursor.execute("SELECT uddannelseID FROM Students WHERE studentID = %s", (id,))
            uddannelse_id = self.mycursor.fetchone()['uddannelseID']

            self.mycursor.execute("SELECT uddannelseNavn FROM UddannelsesHold WHERE uddannelseID = %s", (uddannelse_id,))
            uddannelse_navn = self.mycursor.fetchone()['uddannelseNavn']

            self.mycursor.execute("SELECT navn FROM Students WHERE studentID = %s", (id,))
            student_info = self.mycursor.fetchone()['navn']

            response_data = ''

            if uddannelse_navn and student_info:
                response_data = {
                    'navn': student_info,
                    'uddannelseNavn': uddannelse_navn  
                }
            else:
                response_data = {
                    'status': 'Error: Student not found'
                }

            return response_data

        except Exception as e:
            return e

class SessionHandler:
    def __init__(self, database, cursor):
        self.db = database
        self.mycursor = cursor

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

            result = data_handler.generate_student(room_id, student_id)
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
        
        case 'profile':
            student_id = data.get('id')

            if not student_id:
                return jsonify(error="No 'studentID' specified in JSON data."), 400

            result = data_handler.profile(student_id)
            return jsonify(result), 200

        case _:
            return jsonify(error=f"Data '{subject}' not supported."), 400



if __name__ == "__main__":
    app.run(debug=True, port=13371)