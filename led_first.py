from tkinter import *
import tkinter.font
from gpiozero import LED
import RPi.GPIO

RPi.GPIO.setmode(RPi.GPIO.BCM)

#hardware
led = LED(14)

#GUI DEFINITIONS
win = Tk()
win.title("LED Toggler")
myFont = tkinter.font.Font(family = 'Helvetica', size =12, weight = "bold")

##EVENT FUNCTION
def ledToggle():
    if led.is_lit:
        led.off()
        ledButton["text"]="Turn LED on"
    else:
        led.on()
        ledButton["text"]="Turn LED off"

def close():
    RPi.GPIO.cleanup()
    win.destroy()

##WIDGETS
ledButton = Button(win, text = 'Turn LED On', font = myFont,command = ledToggle,bg='bisque2',height = 1,width=24)
ledButton.grid(row=0,column=1)

#EXIT button
exitButton = Button(win, text = 'Exit', font = myFont,command = close,bg='red',height = 1,width=6)
exitButton.grid(row=1,column=1)
