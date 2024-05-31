from machine import Pin, SPI
import test.mfrc522
from os import uname

def do_write():
    # Define the pins for SPI
    sck = Pin(36, Pin.OUT)
    copi = Pin(35, Pin.OUT)  # Controller out, peripheral in (MOSI)
    cipo = Pin(37, Pin.OUT)  # Controller in, peripheral out (MISO)
    sda = Pin(8, Pin.OUT)
    rst = Pin(0, Pin.OUT)

    # Initialize SPI interface
    spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=copi, miso=cipo)
                  
    rdr = test.mfrc522.MFRC522(36, 35, 37, 0, 8)

    print("")
    print("Place card before reader to write address 0x08")
    print("")

    try:
        while True:
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid    : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")
                    if rdr.select_tag(raw_uid) == rdr.OK:
                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                        if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                            data_to_write = b"\x05" + b"\x00" * 15
                            stat = rdr.write(8, data_to_write)
                            rdr.stop_crypto1()
                            if stat == rdr.OK:
                                print("Data written to card")
                            else:
                                print("Failed to write data to card")
                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")
    except KeyboardInterrupt:
        print("Bye")

# Run the write function
do_write()

