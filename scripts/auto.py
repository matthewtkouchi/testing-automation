import time
import serial
import pyvisa
import os
# import user defined functions
from setup import _get_csv_folder_path, _select_instrument_resource
from csv_files import rename_csv_files
# import user defined data structures
from setup import setup_items

# Number of times to run the increment system
samples = 86
center_freq = 28   # GHz
freq_span = 600     # MHz
average_passes = 1

# Create a measurements folder to store data
file_path = os.path.join(_get_csv_folder_path(setup_items['meas_foldername']), time.strftime("%Y%m%d%H%M%S") + ".csv")
setup_items['meas_folderpath'] = file_path

# Connect with spectrum analyzer
rm = pyvisa.ResourceManager()  
_select_instrument_resource(setup_items, rm)
my_instrument = rm.open_resource(setup_items['instrument'])

# Configure the serial connection to the motion controller
ser = serial.Serial(
    port='COM3',
    baudrate=9600,
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
# Set Speeds 
cmd = '2UV 15;' 
ser.write(cmd.encode('ascii'))
# Reading the data from the serial port
# Start arm at -90 degrees
cmd = '2UP -86; 2WS\r\n'
angle = -86
ser.write(cmd.encode('ascii'))

# Create a file to store data
f = open(file_path, "w")
f.write("Angle,Power(dBm)\n")
print("Arm at: ", angle)

f.close()


# Set center freq then frequency span markers
my_instrument.write(':sens:freq:cent %fe9' % center_freq)
my_instrument.write(':sens:freq:span %fe6' % freq_span)
#my_instrument.write(':sens:bwid 100')
my_instrument.write(':sens:aver:coun %f' % average_passes)
my_instrument.write('CALC:MARK:FUNC:MAX')



# Wait for arm to move to -90 degrees
time.sleep(7)
cmd = '2UV 8;' 
ser.write(cmd.encode('ascii'))


# Read all markers
time.sleep(4)   # Wait for averaging to finish 
value = my_instrument.query_ascii_values(':calc:mark:y?')
print(f"Freq: {center_freq}")
print(f"Value: {value} dB")

# Write to file
f = open(file_path, "a")
f.write(str(angle) + "," + str(value).strip("[]") + "\n")
f.close()

# Increment the arm by 10 degrees
cmd = '2UR 2; 2WS\r\n'
i = 0

while i < samples:
    try:
        # Send command to increment arm by 2 degrees
        ser.write(cmd.encode('ascii'))
        angle += 2
        i += 1
        print("Arm at: ", angle)
        # Wait for arm to move + NA to finish averaging
        time.sleep(4)
        # Read all markers
        value = my_instrument.query_ascii_values(':calc:mark:y?')
        print(f"Freq: {center_freq}")
        print(f"Value: {value} dB")
        time.sleep(0.1)
        f = open(file_path, "a")
        #Write to file
        f.write(str(angle) + "," + str(value).strip("[]") + "\n")
        f.close()
        # Buffer time for the file to be written to
        time.sleep(3)
    except KeyboardInterrupt:
        print("Program stopped, arm at: ", angle)
        break
# Reset arm back to 0 degrees
cmd = '2UV 15;' 
ser.write(cmd.encode('ascii'))
cmd = '2UP 0; 2WS\r\n'
angle = 0
ser.write(cmd.encode('ascii'))
print("Arm at: ", angle)

csv_dir = _get_csv_folder_path(setup_items['meas_foldername'])
setup_items['meas_folderpath'] = csv_dir
rename_csv_files(csv_dir)