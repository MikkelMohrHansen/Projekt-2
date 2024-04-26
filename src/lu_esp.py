from machine import Pin, SPI
from mfrc522 import MFRC522
from time import sleep
import wifi_connection
import socket
import ujson as json

class RC522_RFID:
    
    def __init__(self):

        self.led_pin = Pin(12, Pin.OUT)

        spi = SPI(1, baudrate=2500000, polarity=0, phase=0)
        sda = 8
        rst = 0
        spi.init()
        
        self.rdr = MFRC522(spi=spi, gpioRst=rst, gpioCs=sda)

        print("Placer kortet...")

    def read_card(self):

        self.led_pin.value(0)
        (stat, tag_type) = self.rdr.request(self.rdr.REQIDL)
        if stat == self.rdr.OK:
            (stat, raw_uid) = self.rdr.anticoll()
            if stat == self.rdr.OK:
                card_id = "UID: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                self.led_pin.value(1)
                print(card_id)
                
                sleep(2)
                return card_id
        
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
    logunit_ip = wifi_connection.connect()
    RFID = RC522_RFID()
    
    socket = Socket()
    
    while True:
        socket.send_data(RFID.read_card())
