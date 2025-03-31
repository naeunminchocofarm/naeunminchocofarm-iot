import spidev

LDR_CHANNEL = 0

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 100000

def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, (8 + adcnum) << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

class Adc:
    def __init__(self):
        None
        
    def read_ldr_value(self):
        return readadc(LDR_CHANNEL)
        