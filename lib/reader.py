from machine import Pin, SoftSPI

from test.driver import MFRC522

sck = Pin(36, Pin.OUT)
copi = Pin(35, Pin.OUT)  # Controller out, peripheral in
cipo = Pin(37, Pin.OUT)  # Controller in, peripheral out
spi = SoftSPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=copi, miso=cipo)
sda = Pin(8, Pin.OUT)
reader = MFRC522(spi, sda)

print("Place Card In Front Of Device To Read Unique Address")
print("")

last_uid = None
while True:
    try:
        (status, tag_type) = reader.request(reader.CARD_REQIDL)
        if status == reader.OK:
            (status, raw_uid) = reader.anticoll()
            if raw_uid == last_uid:
                continue
            if status == reader.OK:
                print("New Card Detected")
                print("  - Tag Type: 0x%02x" % tag_type)
                print(
                    "  - uid: 0x%02x%02x%02x%02x"
                    % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                )
                print("")
                if reader.select_tag(raw_uid) == reader.OK:
                    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                    if reader.auth(reader.AUTH, 8, key, raw_uid) == reader.OK:
                        print("Address Data: %s" % reader.read(8))
                        reader.stop_crypto1()
                    else:
                        print("AUTH ERROR")
                else:
                    print("FAILED TO SELECT TAG")
                last_uid = raw_uid
    except KeyboardInterrupt:
        break