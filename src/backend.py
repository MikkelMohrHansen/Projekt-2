from flask import Flask, request, jsonify
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
        self.mycursor = self.db.cursor()

        self.session = SessionHandler(self.db, self.mycursor)
        print("connected to database")

    def generate_room(self, operation_type=None, room_name=None):
        try: 
            if "add" == operation_type:
                self.mycursor.execute('INSERT INTO rooms (roomName) VALUES (%s)', (room_name,))
                self.db.commit()
            elif "delete" == operation_type:
                self.mycursor.execute('DELETE FROM rooms WHERE roomName = %s', (room_name,)) # 
                self.db.commit()
            
        except Exception as e:
            return e

    def generate_student(self, operation_type=None, student_name=None):
        try:
            if "add" == operation_type:
                self.mycursor.execute('INSERT INTO students (studentName) VALUES (%s)', (student_name,))
                self.db.commit()
            elif "delete" == operation_type:
                self.mycursor.execute('DELETE FROM students WHERE studentName = %s', (student_name,)) # 
                self.db.commit()

        except Exception as e:
            return e

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


class SessionHandler:
    def __init__(self, database, cursor):
        self.db = database
        self.mycursor = cursor

data_handler = DataHandler()

@app.route('/', methods=['POST'])
def handle():
    data = request.json
    if not data:
        return jsonify(error="No JSON data received."), 400

    subject = data.get('Subject')
    if not subject:
        return jsonify(error="No 'Subject' specified in JSON data."), 400

    if subject == 'generate_room':
        room_name = data.get('room_name')
        if not room_name:
            return jsonify(error="No 'room_name' specified in JSON data."), 400
        
        operation_type = data.get('operation_type')

        result = data_handler.generate_room(operation_type, room_name)
        return jsonify(result=result), 200

    elif subject == 'generate_student':
        student_name = data.get('student_name')
        if not student_name:
            return jsonify(error="No 'student_name' specified in JSON data."), 400

        operation_type = data.get('operation_type')

        result = data_handler.generate_student(operation_type, student_name)
        return jsonify(result=result), 200

    elif subject == 'check_in':
        # Room id, student id / card id
        room_id = data.get('room_id')
        student_id = data.get('student_id')

        if not room_id or not student_id:
            return jsonify(error="No 'room_id' or 'student_id' specified in JSON data."), 400

        result = data_handler.generate_student(room_id, student_id)
        return jsonify(result=result), 200

    return jsonify(error=f"Subject '{subject}' not supported."), 400

if __name__ == "__main__":
    app.run(debug=True, port=13371)