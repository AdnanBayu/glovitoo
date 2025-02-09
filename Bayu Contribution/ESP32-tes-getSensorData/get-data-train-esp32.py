## THIS PROGRAM APPLIED TO CATCH DATA FROM SERIAL MONITOR THEN SAVE IT AS CSV FILE
## RUN THIS PROGRAM WHILE ESP32 CONNECTED TO PC VIA USB
## DON'T OPEN ARDUINO IDE SERIAL MONITOR

import serial

# Replace 'COM3' with the correct serial port of your ESP32
SERIAL_PORT = 'COM3'
BAUD_RATE = 115200      # make sure the same with .ino code baud rate
OUTPUT_FILE = r""  # determine your output file path

def save_serial_data():
    try:
        # Open the serial port
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT}")
        
        # Open the output file
        with open(OUTPUT_FILE, 'w') as file:
            file.write("Sample\n")  # Write CSV header
            # print("Waiting for data...")

            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:  # If there's data
                    file.write(f"{line}\n")  # Write to file
                    print(line)  # Optionally print to console

    #terminat catching data by pressing ctrl + c on terminal
    except KeyboardInterrupt:
        print("\nData saving stopped.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()
        print(f"Data saved to {OUTPUT_FILE}")

# Run the function
save_serial_data()