from flask import Flask, request
import mysql.connector
import json

app = Flask(__name__)

class DataHandler:
    def __init__(self):
        self.db = mysql.connector.connect(
        host="127.0.0.1",
        user="administrator",
        passwd="MaaGodt*7913",
        database="DBSimpel"
        )
        self.mycursor = self.db.cursor()

        self.session = SessionHandler(self.db, self.mycursor)

    def generate_room(self, room_name):
        return

class SessionHandler:
    def __init__(self, database, cursor):
        self.db = database
        self.mycursor = cursor

class RouteCommunication:
    def __init__(self):
        self.data_handler = DataHandler()

    def handle_json(self):
        data = request.json

        print(f"[i] Modtaget JSON data: {data}")    

        if data and data.get('Subject') == 'generate_room':
            room_name = data.get('room_name')
            if room_name:
                result = self.data_handler.generate_room(room_name)
                return result
            else:
                return "[!] Manglende 'room_name' i JSON key felt."
        
route_communication = RouteCommunication()

@app.route('/', methods=['POST'])
def handle():
    return route_communication.handle_json()

if __name__ == "__main__":
    app.run(debug=True, port=13371)