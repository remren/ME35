"""
Raspberry Pi Pico/MicroPython exercise
240x240 ST7789 SPI LCD
using MicroPython library:
https://github.com/russhughes/st7789py_mpy

ST7789		Raspberry Pi Pico - ORIGINAL WIRING
=================================
VCC		3V3			   On Pico
GND		GND
SCL		GP10 (pin 14) = SPI1 SCK
SDA		GP11 (pin 15) = SPI1 MOSI (TX)
RES		GP12 (pin 16) = SPI1 MISO (RX)
DC		GP13 (pin 17) = SPI1 CS
BLK		3V3

MY WIRING
display|pico
VCC 	3V3
GND 	GND
DIN 	GP11 (pin 15) = SPI1 MOSI (TX)
CLK		GP10 (pin 14) = SPI1 SCK
CS		GND (A low CS indicates OK operation!)
DC		GP13 (pin 17) = SPI1 CS
RST		GP12 (pin 16) = SPI1 MISO (RX)

"""

# GOD: https://helloraspberrypi.blogspot.com/2021/02/raspberry-pi-picomicropython-st7789-spi.html

import uos
import machine
import st7789py as st7789
import vga2_8x8 as font1
import vga1_16x32 as font2
import random

class Display():
    def __init__(self):
        #SPI(1) default pins
        spi1_sck=10
        spi1_mosi=11
        spi1_miso=8     #not use
        st7789_res = 12
        st7789_dc  = 13
        disp_width = 320
        disp_height = 240
        CENTER_Y = int(disp_width/2)
        CENTER_X = int(disp_height/2)

        print(uos.uname())
        spi1 = machine.SPI(1, baudrate=40000000, polarity=1)
        print(spi1)
        self.display = st7789.ST7789(spi1, disp_width, disp_height,
                                     reset=machine.Pin(st7789_res, machine.Pin.OUT),
                                     dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                                     rotation=1)
        
    def return_display(self):
        return self.display

        # # Color definitions
        # BLACK = const(0x0000)
        # BLUE = const(0x001F)
        # RED = const(0xF800)
        # GREEN = const(0x07E0)
        # CYAN = const(0x07FF)
        # MAGENTA = const(0xF81F)
        # YELLOW = const(0xFFE0)
        # WHITE = const(0xFFFF)
    def displaytext(self, text, x, y, fillcolor="black", font=2):
#         if fillcolor == "black":
#             self.display.fill(st7789.BLACK)
        if font == 1:
            self.display.text(font1, text, x, y)
        else:
            self.display.text(font2, text, x, y)
        
    def changebg(self, bg):
        if bg == 0:
            self.display.fill(st7789.BLACK)
        elif bg == 1:
            self.display.fill(st7789.BLUE)
            self.display.text(font2, "TT_TT", 130, 120, background=st7789.BLUE)
        elif bg == 2:
            self.display.fill(st7789.RED)
            self.display.text(font2, "D:<", 130, 120, background=st7789.RED)
        elif bg == 3:
            self.display.fill(st7789.GREEN)
        elif bg == 4:
            self.display.fill(st7789.CYAN)
            self.display.text(font2, ":3", 135, 120, background=st7789.CYAN)
        elif bg == 4:
            self.display.fill(st7789.MAGENTA)
            self.display.text(font2, ":O  woaaah", 100, 120, background=st7789.MAGENTA)
        elif bg == 5:
            self.display.fill(st7789.YELLOW)
            self.display.text(font2, ".____.", 110, 120, background=st7789.YELLOW)
        elif bg == 6:
            self.display.fill(st7789.WHITE)
            self.display.text(font2, "o____o", 110, 120, background=st7789.WHITE)
        else:
            self.display.fill(st7789.BLACK)