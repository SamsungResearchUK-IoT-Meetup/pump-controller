import pyb
import time
import ultrasonic


switch = pyb.Switch()
#sensor = ultrasonic.Ultrasonic(pyb.Pin.board.X3, pyb.Pin.board.X4)
sensor = drivers.usonic.ultrasonic.Ultrasonic(pyb.Pin.board.X3, pyb.Pin.board.X4)

while not switch.value():
    try:
        dist = sensor.distance_in_cm()
        print("Dist = {}".format(dist))

    except drivers.usonic.ultrasonic.MeasurementTimeout as e:
            # ultrasonic.MeasurementTimeout as e:
        print("{}".format(e))

    time.sleep(1)
