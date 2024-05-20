from machine import Pin, SPI
import mfrc522
from os import uname
from time import sleep
import wifi_connection
import socket
import ujson as json

class RC522_RFID:
	
	def __init__(self):

		if uname()[0] == 'WiPy':
			self.rdr = mfrc522.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
		elif uname()[0] == 'esp8266' or uname()[0] == 'esp32':
			sel.frdr = mfrc522.MFRC522(0, 2, 4, 5, 14) # sck, mosi, miso, rst, cs
		else:
			raise RuntimeError("Unsupported platform")

		self.led_pin = Pin(12, Pin.OUT)

		print("Placer kortet...")

	def read_card(self):

		if uname()[0] == 'esp32':
			rdr = mfrc522.MFRC522(36, 35, 37, 0, 8)
		else:
			raise RuntimeError("Unsupported platform")

		print("")
		print("Place card before reader to read from address 0x08")
		print("")


		(stat, tag_type) = rdr.request(rdr.REQIDL)

		if stat == rdr.OK:

			(stat, raw_uid) = rdr.anticoll()

			if stat == rdr.OK:
				print("New card detected")
				print("  - tag type: 0x%02x" % tag_type)
				print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
				print("")

				if rdr.select_tag(raw_uid) == rdr.OK:

					key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

					if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
						print("Address 8 data: %s" % rdr.read(8))
						rdr.stop_crypto1()
					else:
						print("Authentication error")
				else:
					print("Failed to select tag")

		
class Socket:
	def __init__(self):
		srvaddr: str = '79.171.148.163'
		srvport_tcp: int = 13371 # TCP for device id requesting

		self.srvcon_tcp = (srvaddr, srvport_tcp)

		# Kontroller om der allerede er generet et device ID for ESP'en
		try:
			with open('device_id.txt', 'r') as file:
				credentials_file = file.read()
			
			# Hvis filen er tom
			if '' == credentials_file:
				print("[!] Device ID file empty, requesting...")
				self.send_data(type='device ID request')
			# Hvis Device ID'et allerede er skabt for ESP'en
			else:
				for line in credentials_file.split('\n'):
					if "DeviceID:" in line:
						self.device_id = line.split(':')[1].strip()
				print(f"[+] Device ID: {self.device_id}")
		except OSError as e:
			# Hvis filen ikke eksisterer
			if errno.ENOENT == e.errno:
				print("[!] Device ID does not exist, requesting...")
				self.send_data(type='device ID request')
			# Andre errors
			else:
				print("[!] Error: '%s' occured." % e)

	def initTCP_sock(self) -> socket:
		csocket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		csocket_tcp.connect(self.srvcon_tcp)
		return csocket_tcp
		
	def send_data(self, type=None, recording_data=None):
			try:
				if 'device ID request' == type:
					csocket_tcp = self.initTCP_sock()
					data_packet = {'data': f'{type}'}
					csocket_tcp.send(json.dumps(data_packet).encode('utf-8'))

					response_data = csocket_tcp.recv(1024).decode('utf-8')
					response_dict = json.loads(response_data)
					self.device_id = response_dict.get('device_id', '')
					self.password = response_dict.get('password', '')
					print(f"[i] Device ID recieved: {self.device_id} \n")
					print (f"[i] Password recieved: {self.password} \n")

					csocket_tcp.close()

					# Gem det genereret device id og password til 'device_id.txt'
					with open('device_id.txt', 'w') as file:
						file.write(f"DeviceID:{self.device_id}\nPassword:{self.password}")

				elif 'recording data' == type:
					csocket_tcp = self.initTCP_sock()
					card_id = recording_data
					print(f"[+] Recording data {card_id}")
					data_packet = {'data': f'{type}', 'device_id': f'{self.device_id}','card_id': f'{card_id}'}
					print(f"[+] Sending data: {json.dumps(data_packet)}")
					csocket_tcp.send(json.dumps(data_packet).encode('utf-8'))
					
					print("Recording data packet sent")

			except Exception as e:
				print(f"Unhandled exception: {e}")
		
if __name__ == "__main__":
	# logunit_ip = wifi_connection.connect()
	RFID = RC522_RFID()
	
	# socket = Socket()
	
	while True:
		RFID.read_card
		# socket.send_data(RFID.read_card())
