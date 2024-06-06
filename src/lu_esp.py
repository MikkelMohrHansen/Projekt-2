from machine import Pin, SPI
import mfrc522
from time import sleep
import wifi_connection
import urequests
import ujson as json

def decimal_to_ascii(string):
	ascii_string = ''.join(chr(num) for num in string if num != 0)
	return ascii_string

class Hardware:
	def __init__(self):
		# Initialize the MFRC522 module with the appropriate pins
		self.rdr = mfrc522.MFRC522(36, 35, 37, 0, 8)  # sck, mosi, miso, rst, cs
		
		self.red_led = Pin(13, Pin.OUT)
		self.green_led = Pin(14, Pin.OUT)
		self.yellow_led = Pin(15, Pin.OUT)

	def connect_to_wifi(self):
		try:
			while True:
				(stat, tag_type) = self.rdr.request(self.rdr.REQIDL)

				if stat == self.rdr.OK:

					(stat, raw_uid) = self.rdr.anticoll()

					if stat == self.rdr.OK:
						print("New card detected")
						print("  - tag type: 0x%02x" % tag_type)
						print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
						print("")

						if self.rdr.select_tag(raw_uid) == self.rdr.OK:

							key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

							if self.rdr.auth(self.rdr.AUTHENT1A, 8, key, raw_uid) == self.rdr.OK:
								ssid = decimal_to_ascii(self.rdr.read(8))
								password = decimal_to_ascii(self.rdr.read(9))

								print(f"SSID: {ssid} PASSWORD: {password}")
								print(wifi_connection.activate(ssid, password))
								self.yellow_led.on()
								sleep(5)

								self.rdr.stop_crypto1()
							else:
								print("Authentication error")
						else:
							print("Failed to select tag")

					break

				else:
					self.yellow_led.on()
					sleep(1)
					self.yellow_led.off()
					sleep(1)

		except KeyboardInterrupt:
			print("Bye")
	
	def blink_led(self, arg_led, times=10, delay=0.25):
		if arg_led == 'red':
			led = self.red_led
		elif arg_led == 'green':
			led = self.green_led
		elif arg_led == 'yellow':
			led = self.yellow_led
		else:
			print('[!] Invalid LED specified.')
		
		for _ in range(times):
			led.on()
			sleep(delay)
			led.off()
			sleep(delay)

	def read_card(self):
		
		try:
			while True:
				(stat, tag_type) = self.rdr.request(self.rdr.REQIDL)

				if stat == self.rdr.OK:

					(stat, raw_uid) = self.rdr.anticoll()

					if stat == self.rdr.OK:
						print("New card detected")
						print("  - tag type: 0x%02x" % tag_type)
						print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
						print("")

						if self.rdr.select_tag(raw_uid) == self.rdr.OK:

							key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

							if self.rdr.auth(self.rdr.AUTHENT1A, 8, key, raw_uid) == self.rdr.OK:
								student_id = decimal_to_ascii(self.rdr.read(8))
								self.rdr.stop_crypto1()
								sleep(2)
								return student_id
							else:
								print("Authentication error")
						else:
							print("Failed to select tag")

		except KeyboardInterrupt:
			print("Bye")

class HTTPClient:
	def __init__(self, server_url, room_id):
		self.server_url = server_url
		self.room_id = room_id

		self.hardware = Hardware()

	def send_data(self, student_id):
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
				response_data = response.json()
				if response_data[0]['status'] == 'success':
					self.hardware.blink_led('green')
				else:
					self.hardware.blink_led('red')
			
			except Exception as e:
				print(f"Unhandled exception: {e}")

if __name__ == "__main__":
	SERVER_URL = "https://79.171.148.163/api"
	room_id = int("7913")
	
	hardware = Hardware()
	hardware.connect_to_wifi()
	http_client = HTTPClient(SERVER_URL, room_id)
	
	while True:
		# Read the card and get the student ID
		student_id = hardware.read_card()
		print(f"Checked in student ID: {student_id}")
		if student_id:
			# Send the student ID to the server
			http_client.send_data(student_id)
		sleep(1)

