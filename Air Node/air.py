"""
Author: Sharome Burton for SAR-UAV Project
"""
# Import Python System Libraries
import time
# Import Blinka (CircuitPython) Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x radio module
import adafruit_rfm9x
# Import National Marine Electronics Association Standards
import pynmea2

import serial
import string
import config

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
 
# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height
 
# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0) # 915 Mhz
rfm9x.tx_power = 23 # Maximum 
prev_packet = None

# Configure GPS Receiver
port = "/dev/ttyACM0"       # Serial port of GPS Receiver
ser = serial.Serial(port, baudrate=9600, timeout=0.5)
dataout = pynmea2.NMEAStreamReader()

doa, head = 0.0, 0.0  # Line of Bearing and Heading of Aircraft initialized at zero
txdoa, txhead = 0.0, 0.0

# Reading raw data from GPS Receiver and LoRa Receiver
while True:

    # Receiver Packet
    packet = None

    # TX: GPS data
    newdata=ser.readline()
    newdata = newdata.decode("utf-8")

    # TX: Parsing data from GPS receiver
    if newdata[0:6] == "$GPRMC":
        newmsg = pynmea2.parse(newdata)
        txlat = str(newmsg.latitude).ljust(8, '0')[0:8] # Latitude to be transferred 8 chars long
        txlng = str(newmsg.longitude).ljust(8, '0')[0:8] # Longitude to be transferred 8 chars long
        gps = "Latitude=" + txlat + " and Longitude=" + txlng
        print(gps)
        
        # TX: Read Data from KerberosSDR
        
        try:
            with open("/ram/DOA_value.html",mode = 'r') as DOA:
                
                txdoa = DOA.read()[12:15]  # DOA / degrees
                print('DOA: ' + txdoa + '\n') 
                DOA.seek(0)
                txconf = DOA.read()[28:31]  # Confidence / percentage
                print('Confidence: ' + txconf + '\n') 
                DOA.seek(0)
                txpwr = DOA.read()[44:52]  # Signal power / decibels
                print('Power: ' + txpwr + '\n') 
                DOA.seek(0)
                            
        except FileNotFoundError as e1:
            print('DOA: Check file name or location\n\n')
            
            
        # TX: Read Heading
        
        txhead += 0 # Aircraft hard-coded to maintain initial heading (north)

        # TX: Converting data to string by concatenation (string lengths: lat:8, lng:8, doa:3, conf:3, pow:8, head:8)
        air_packet = txlat + txlng + txdoa + txconf + txpwr + str(txhead).ljust(8, '0')[0:8]

        # TX: Sending data via LoRa as bytes
        rfm9x.send(bytearray(air_packet, 'utf-8'))

        # TX: Display the data on screen
        display.show()
        # Box is drawn to clear the image
        display.fill(0)
        
        display.text('lat: ', 0, 0, 1)
        display.text('lng: ', 0, 8, 1)
        display.text('doa: ', 0, 16, 1)
        display.text('head: ', 0, 24, 1)
        display.text(str(txlat), 25, 0, 1)
        display.text(str(txlng), 25, 8, 1)
        display.text(str(txdoa), 25, 16, 1)
        display.text(str(txhead), 32, 24, 1)
        print(f'Packet sent was {air_packet}')
        # time.sleep(.25)

    # RX: Check for acknowledgement from ground station
    packet = rfm9x.receive(timeout=0.5)
    if packet is None:
        display.show()
        display.fill(0)
        display.text('SAR UAV LoRa TX', 35, 0, 1)
        display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        # RX: Converting packet from bytes
        prev_packet = str(packet, "utf-8")

        # RX: Display the data on screen
        display.show()
        display.fill(0)
        display.text(prev_packet, 15, 20, 1)
        time.sleep(.5)