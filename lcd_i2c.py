#!/usr/bin/python

#
# http://www.raspberrypi-spy.co.uk/
#
# Copyright 2015 Matt Hawkins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#--------------------------------------


import smbus
import time

import os
import temp_CPU as temp_cpu
import i2c_czuj as term_higr
import DT       as ti_da

#import led_first as LedTog




#dane[2] = {0, 0}

# Define some device parameters
I2C_ADDR  = 0x3f # I2C device address
LCD_WIDTH = 20   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

#global LCD_BACKLIGHT
#LCD_BACKLIGHT = 0x08# On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init(LCD_BACKLIGHT):
  # Initialise display
  lcd_byte(0x33,LCD_CMD,LCD_BACKLIGHT) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD,LCD_BACKLIGHT) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD,LCD_BACKLIGHT) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD,LCD_BACKLIGHT) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD,LCD_BACKLIGHT) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD,LCD_BACKLIGHT) # 000001 Clear display
  time.sleep(E_DELAY)

#LCD_BACKLIGHT(0x08)-ON,LCD_BACKLIGHT(0x00)-0FF   
#def backlight(self, state): #for state, 1=on, 2=off
 # if state == 1:
 #  LCD_BACKLIGHT
 #   self.lcd_byte(0x0C, LCD_CMD)
  #elif state == 0:
  #  LCD_NOBACKLIGHT
  #  self.lcd_byte(0x0C, LCD_CMD)
#def backlight(flag):
  



def lcd_byte(bits, mode,LCD_BACKLIGHT):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line,LCD_BACKLIGHT):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD,LCD_BACKLIGHT)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR,LCD_BACKLIGHT)



def main():
  # Main program block

  # Initialise display
  lcd_init(0x08)

  while True:
    dane = []
    dane = term_higr.getTHD()
    data = []
    data = ti_da.timeDate()
    CPU_temp = temp_cpu.getCPUtemperature()
    if ((data[3] > 10 and data[3] < 15) and (data[4]>= 0 and data[4] <=59)):
   # if((data[5]%2)>0):
   # lcd_string("      DI_3000 " , LCD_LINE_1)
    # przedstawienie wilgotnosci powietrza, temp. procesora RPi oraz temp. otoczenia
      lcd_string("Humi.:%.2f%%" %dane[0]+"  tCPU" ,LCD_LINE_1,0x08)
      lcd_string("Temp.:%.2f`C"%dane[1]+" "+CPU_temp ,LCD_LINE_2,0x08)
      
      lcd_string("%i/"%data[2]+"%i/"%data[1]+"%i"%data[0]+
      "   %i:"%data[3]+"%i:"%data[4]+"%i"%data[5],LCD_LINE_4,0x08)
      print ("jeden")
   # lcd_byte(0x06,LCD_CMD,0x00)
    else:
      lcd_string("Humi.:%.2f%%" %dane[0]+"  tCPU" ,LCD_LINE_1,0x00)
      lcd_string("Temp.:%.2f`C"%dane[1]+" "+CPU_temp ,LCD_LINE_2,0x00)

      lcd_string("%i/"%data[2]+"%i/"%data[1]+"%i"%data[0]+
      "   %i:"%data[3]+"%i:"%data[4]+"%2i"%data[5],LCD_LINE_4,0x00)
      print ("zero")
    print (data[4])
    time.sleep(0.5)
    LCD_BACKLIGHT = 0x00
    #lcd_init(0x00)
   
  
    
if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD,0x00)

