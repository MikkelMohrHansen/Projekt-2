from machine import Pin, SPI
import test.mfrc522
from os import uname
from time import sleep
import wifi
import urequests
import ujson as json

class RC522_RFID:
    
    def __init__(self):
        # Initialize the MFRC522 module with the appropriate pins
        self.rdr = test.mfrc522.MFRC522(36, 35, 37, 0, 8)  # sck, mosi, miso, rst, cs
        self.led_pin = Pin(12, Pin.OUT)

    def read_card(self):
        #print("Place card before reader to read from address 0x08")
        
        try:
            # Request to find any RFID tag within range
            (stat, tag_type) = self.rdr.request(self.rdr.REQIDL)

            if stat == self.rdr.OK:
                # Anti-collision detection to find the UID of the card
                (stat, raw_uid) = self.rdr.anticoll()

                if stat == self.rdr.OK:
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid     : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")

                    if self.rdr.select_tag(raw_uid) == self.rdr.OK:
                        # Authentication for the specified block (0x08)
                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                        if self.rdr.auth(self.rdr.AUTHENT1A, 8, key, raw_uid) == self.rdr.OK:
                            data = self.rdr.read(8)
                            if data is not None:
                                print("Address 8 data:", data)
                                self.rdr.stop_crypto1()
                                # Return the raw UID and the first byte of data (student_id)
                                return raw_uid, data[0]
                            else:
                                print("Failed to read data from address 8")
                                self.rdr.stop_crypto1()
                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")
                else:
                    print("No card detected")
                    
        except KeyboardInterrupt:
            print("Bye")
        except Exception as e:
            print(f"Error reading card: {e}")

        return None, None

class HTTPClient:
    def __init__(self, server_url, room_id):
        self.server_url = server_url
        self.room_id = room_id

    def send_data(self, data):
        if student_id is not None:
            try:
                data_packet = {
                    'data': 'check_in',
                    'student_id': int(student_id),
                    'room_id': self.room_id
                    
                }
                print(f"[+] Sending data: {json.dumps(data_packet)}")
                response = urequests.post(self.server_url, json=data_packet)
                print(f"Server response: {response.text}")
            except Exception as e:
                print(f"Unhandled exception: {e}")

if __name__ == "__main__":
    RFID = RC522_RFID()
    server_url = "https://79.171.148.163/api"
    room_id = int("5035")
    http_client = HTTPClient(server_url, room_id)
    
    while True:
        # Read the card and get the student ID
        card_uid, student_id = RFID.read_card()
        if card_uid:
            # Send the student ID to the server
            http_client.send_data(student_id)
        sleep(1)



