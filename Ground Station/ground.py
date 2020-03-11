"""
Author: Sharome Burton for SAR-UAV Project
"""

# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x
# Import National Marine Electronics Association Standards
import pynmea2

import serial
import string
import config

# PubNub libraries
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException

# Configuring PubNub realtime communication infrastructure
pnChannel = "raspi-tracker";
pnconfig = PNConfiguration()
pnconfig.subscribe_key = config.subkey
pnconfig.publish_key = config.pubkey
pnconfig.ssl = False
pubnub = PubNub(pnconfig)
pubnub.subscribe().channels(pnChannel).execute()

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP
 
# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP
 
# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP
 
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
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None

## port="/dev/ttyACM0"       # Serial port of GPS Receiver
## ser=serial.Serial(port, baudrate=9600, timeout=0.5)
## dataout = pynmea2.NMEAStreamReader()

doa, head = 0, 0  # Line of Bearing and Heading of Aircraft initialized at zero

# Reading raw data from GPS Receiver and LoRa Receiver
while True:
    ## # TX: Read GPS data
    ## newdata=ser.readline()
    ## newdata = newdata.decode("utf-8")

    packet = None
    
    # RX: check for packet rx
    packet = rfm9x.receive(timeout=1.0)
    if packet is None:
        # draw a box to clear the image
        display.show()
        display.fill(0)
        display.text('SAR UAV LoRa RX', 35, 0, 1)
        display.text('- Waiting for PKT -', 15, 20, 1)
        print('No data received yet... Listening again...')
        # time.sleep(.25)
    else:
        # RX: Converting packet from bytes
        prev_packet = packet.decode('utf-8')
        lat = float(prev_packet[0:8])
        lng = float(prev_packet[8:16])
        doa = float(prev_packet[16:19])
        conf = float(prev_packet[19:22])
        pwr = float(prev_packet[22:30])
        head = float(prev_packet[30:38])
        
        # RX: Acquire received signal strength
        rssi = str(rfm9x.rssi)
        
        # RX: Update display
        display.show()
        display.fill(0)
        display.text('- Receiving PKT -', 15, 20, 1)
        # time.sleep(.25)

        # RX: Publishing data points to PubNub server
        try:
            envelope = pubnub.publish().channel(pnChannel).message({
                'lat': lat,
                'lng': lng,
                'doa': doa,
                'conf': conf,
                'pwr': pwr,
                'head': head,
                'rssi': rssi
            }).sync()
            print("publish timetoken: %d" % envelope.result.timetoken)
        except PubNubException as e:
            pass
            # handle_exception(e)

        # TX: Converting acknowledgement to array of bytes
        air_packet = bytearray("Acknowledged by RX!", "utf-8")
              
        # TX: Sending acknowledgement via LoRa
        rfm9x.send(air_packet)

        # RX: Display the data on screen
        lat_text = str(lat)
        lng_text = str(lng)
        doa_text = str(doa)
        head_text = str(head)
        
        display.fill(0)
        display.text('lat: ', 0, 0, 1)
        display.text('lng: ', 0, 8, 1)
        display.text('doa: ', 0, 16, 1)
        display.text('head: ', 0, 24, 1)
        display.text(lat_text, 25, 0, 1) # Latitude
        display.text(lng_text, 25, 8, 1) # Longitude
        display.text(doa_text, 25, 16, 1) # Direction of Arrival
        display.text(head_text, 32, 24, 1) # Aircraft Heading
        display.text('rssi: ', 82, 16, 1) 
        display.text(rssi, 82, 24, 1) # Received Signal Strength
        print(f'Latitude: {lat_text}')
        print(f'Longitude: {lng_text}')
        print(f'Direction of Arrival: {doa_text}')
        print(f'Aircraft Heading: {head_text}')
        print(f'Received Signal Strength: {rssi} dBM')
        # time.sleep(.25)
        
    ##TX: Parsing data from GPS receiver
    #if newdata[0:6] == "$GPRMC":
    #    newmsg=pynmea2.parse(newdata)
    #    lat=newmsg.latitude
    #    lng=newmsg.longitude
    #    gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
    #    print(gps)
    #
    #    # TX: Converting data to array of bytes
    #    air_packet = bytearray([lat, lng, doa, head])
    #          
    #    # TX: Sending data via LoRa
    #    rfm9x.send(air_packet)