import Adafruit_BMP.BMP085 as BMP085

SENSOR = BMP085.BMP085(busnum=1)

class Bmp180:
    def __init__(self):
        None
    
    def read_temperature(self):
        return SENSOR.read_temperature()
    
    def read_pressure(self):
        return SENSOR.read_pressure()
    
    def read_altitude(self):
        return SENSOR.read_altitude()