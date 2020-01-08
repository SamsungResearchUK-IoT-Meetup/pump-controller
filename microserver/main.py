"""
GPL 3 License
Copyright (c) 2020 Samsung. n.herriot@samsung.com
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__version__ = '0.1.0'
__author__ = 'Nicholas Herriot'
__license__ = "GPL3"

from pyb import LED, Switch, Pin
from drivers.usonic.ultrasonic import Ultrasonic, MeasurementTimeout
from wifi.wifi_connect import *
import time
import ujson

# Create variables to control on board LED Lights.
led1 = LED(1)   # RED coloured LED - used to indicate that the pump controller can not connect to WiFi
led2 = LED(2)   # Green coloured LED - used to indicate that the pump controller can connect to WiFi and the tank has water
led3 = LED(3)   # Blue coloured LED - used to indicate that the pump controller can connect to WiFi but is empty.
status_led = led2
# Create variable for the ultrasonic sensor.
sensor = Ultrasonic(Pin.board.X3, Pin.board.X4)

# Create variable which detects the USR button being pressed.
switch = Switch()

# Read configuration values from our json config file
config_file = open('config.json', 'r')
config = ujson.loads(config_file.read())
print("Config file read")
print("Pump controller version: {}".format(config['pump_controller_version']))
print("Pump sensor read time period is: {}".format(config['ultrasonic_time_period']))
time_period = config['ultrasonic_time_period']
wifi_ssid = config['wifi_ssid']
wifi_password = config['wifi_password']
static_ip = config["network"]["ip"]
network_mask = config["network"]["network_mask"]
gateway = config["network"]["gateway_address"]
dns = config["network"]["dns"]



# ============================================================================
# ===( Create WiFi Manager =)=================================================
# ============================================================================
myWifi = Wifi_manager()                                 # Create our WiFi manager object
print("Network config settings are:\n - static ip: {};\n - network mask: {};\n - gateway: {};\n - dns: {}\n ".format(static_ip, network_mask, gateway, dns))
myWifi.retries(8)                                       # Try connect 8 times since WiFi is so poor for machine areas
myWifi._wifi.active(True)                               # Use private member virables of the class to access the low layer functions. We want to setup a static IP for this connection
myWifi._wifi.ifconfig((static_ip,network_mask,gateway,dns))         # Request our connection to be a static IP address


# ============================================================================
# ===( Create A WiFi Connection and Start Web Server )========================
# ============================================================================
print("Attempting to connect to SSID: {}".format(wifi_ssid))
status = myWifi.connect(wifi_ssid, wifi_password)       # TODO pull the password and SSID from an encrypted file on FLASH
#status = myWifi.connect(wifi_ssid, "rubbish")       # TODO pull the password and SSID from an encrypted file on FLASH

if status[0]:
    print('We have a WiFi connection.')
    print("\nTo disconnect first import all objects from start.py: '>>> from start import * ' ")
    print("Then to disconnect do: '>>> myWifi.disconnect()' at your repl prompt\n")
    status_led = led2       # Change the status LED to GREEN
    #srv= create_web_server()
    #print("*** Server now running! ***")
else:
    print('There is no active WiFi manager. Something went wrong.')
    print('Maybe the password or SSID is incorrect?')
    status_led = led1       # Change the status LED to RED





# ============================================================================
# ===( Start Pump Controller/Monitor =)=======================================
# ============================================================================

print("***Starting pump controller! ****")
print("USR switch value is: {}".format(switch.value()))
counter = 1

while not switch.value():
    status_led.toggle()
    print('*** Pump controller active! ***')

    if counter >= time_period:

        try:
            dist = sensor.distance_in_cm()
            print("Dist = {}".format(dist))
        except MeasurementTimeout as e:
            print("{}".format(e))
        counter = 1

    time.sleep(1)
    counter = counter + 1

status_led.off()
print("USR switch value is: {}".format(switch.value()))
print("\n*** Pump controller stopped due to USR switch being pressed")
