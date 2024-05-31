import mfrc522

def pad_with_null(user_input):
    # Convert user input to string
    user_string = str(user_input)
    
    # Calculate the number of null characters needed for padding
    padding_needed = 16 - len(user_string)
    
    # Pad the string with null characters
    padded_string = user_string + '\0' * padding_needed
    
    return padded_string

def do_write(string_a, string_b=None):

    rdr = mfrc522.MFRC522(36, 35, 37, 0, 8)

    while True:
        (stat, tag_type) = rdr.request(rdr.REQIDL)

        if stat == rdr.OK:

            (stat, raw_uid) = rdr.anticoll()

            if stat == rdr.OK:
                print("Card detected")
                print("  - tag type: 0x%02x" % tag_type)
                print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                print("")

                if rdr.select_tag(raw_uid) == rdr.OK:

                    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                    if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                        stat = rdr.write(8, bytes(string_a, 'utf-8'))
                        if string_b:
                            stat = rdr.write(9, bytes(string_b, 'utf-8'))
                        rdr.stop_crypto1()
                        if stat == rdr.OK:
                            print("Data written to card")
                            break
                        else:
                            print("Failed to write data to card")
                    else:
                        print("Authentication error")
                else:
                    print("Failed to select tag")

        
if __name__ == "__main__":
    option = input("Configure student card or Wifi card? [S/W]: ")
    
    if option == 's' or option == 'S':
        student_id = input("Enter student ID (up to 16 characters): ")
        
        do_write(pad_with_null(student_id))
        
    elif option == 'w' or option == 'W':
        ssid_input = input("Enter SSID (up to 16 characters): ")
        password_input = input("Enter Password (up to 16 characters): ")
    
        do_write(pad_with_null(ssid_input), pad_with_null(password_input))
        
    else:
        print("Unknown Input.")
