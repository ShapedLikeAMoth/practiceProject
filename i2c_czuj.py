import smbus
import time

I2C_ADDR_2 = 0x27

bus = smbus.SMBus(1)
# PODEJSCIE NR 2,
def getTHD(): #THD - temperature humidity data
    
    data = bus.read_i2c_block_data(I2C_ADDR_2, 0x00, 4)
    
    #konwersja danych na 14 bitowe
    humidity = ((((data[0] & 0x3F) * 256) + data[1]) * 100.0)/16383.0
    temp = (((data[2] & 0xFF) * 256) + (data[3] & 0xFC))/4
    cTemp = (temp / 16384.0) * 165.0 - 40.0
    return (humidity, cTemp)

