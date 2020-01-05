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


import pyb
import time
from drivers.usonic.ultrasonic import Ultrasonic, MeasurementTimeout


switch = pyb.Switch()
#sensor = ultrasonic.Ultrasonic(pyb.Pin.board.X3, pyb.Pin.board.X4)
sensor = Ultrasonic(pyb.Pin.board.X3, pyb.Pin.board.X4)

while not switch.value():
    try:
        dist = sensor.distance_in_cm()
        print("Dist = {}".format(dist))

    except MeasurementTimeout as e:
        print("{}".format(e))

    time.sleep(1)
