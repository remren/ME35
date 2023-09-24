# Blinks morse word on LED and asynchronously measures light sensor values
# Code finishes after word is blinked once, and at end prints array
# of light sensor vals
import uasyncio as asyncio
from machine import Pin, PWM
from utime import sleep

TIME_UNIT = .1

class AsyncLED:
    # PIN SETUP
    def __init__(self):
        self.morseLed = Pin(15, Pin.OUT) #LED flashing morse name
        self.morseLed.low()
        self.photo_pin = machine.ADC(28) #analog reading for light sensor

        # SETUP
        self.light_vals = []
        self.done_check = False

        # MORSE SETUP
        self.morse_dict =  {'A':'.-', 'B':'-...',
                            'C':'-.-.', 'D':'-..', 'E':'.',
                            'F':'..-.', 'G':'--.', 'H':'....',
                            'I':'..', 'J':'.---', 'K':'-.-',
                            'L':'.-..', 'M':'--', 'N':'-.',
                            'O':'---', 'P':'.--.', 'Q':'--.-',
                            'R':'.-.', 'S':'...', 'T':'-',
                            'U':'..-', 'V':'...-', 'W':'.--',
                            'X':'-..-', 'Y':'-.--', 'Z':'--..'}

        self.name = "lydia"

    async def dot(self):
        self.morseLed.on()
        await asyncio.sleep(TIME_UNIT)
        #await photo_led()
        self.morseLed.off()
        await asyncio.sleep(TIME_UNIT)

    async def dash():
        self.morseLed.on()
        await asyncio.sleep(TIME_UNIT*2)
        self.morseLed.off()
        await asyncio.sleep(TIME_UNIT)

    async def pause(): # 2 time units between letters
        await asyncio.sleep(TIME_UNIT*2)

    async def morse(name):
        global done_check
        self.name = self.name.upper()
        for i in self.name: # iterate through morse of each letter
            print(i, ": ", self.morse_dict[i])
            for symbol in self.morse_dict[i]:
                if symbol == "-":
                    await self.dash()
                elif symbol == ".":
                    await self.dot()
                await self.pause()
        self.done_check = True
        
    async def photo_led():
        while True:
            val = photo_pin.read_u16()
            #print(val)
            self.light_vals.append(val)
            await asyncio.sleep(.1)
        
    async def main():
        global done_check
        while not done_check:
            asyncio.create_task(photo_led())
            await morse(name)
        print(light_vals)