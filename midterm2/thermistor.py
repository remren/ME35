from machine import ADC
from time import sleep
import math

adcpin = 26
sensor = ADC(adcpin)

def getTemp():

    # Voltage Divider
    Vin = 3.3
    Ro = 10000  # 10k Resistor

    # Steinhart Constants
    A = 0.001129148
    B = 0.000234125
    C = 0.0000000876741
    
    adc = sensor.read_u16()
    Vout = (3.3/65535)*adc

    # Calculate Resistance
    Rt = (Vout * Ro) / (Vin - Vout) 
    
    # Steinhart - Hart Equation
    TempK = 1 / (A + (B * math.log(Rt)) + C * math.pow(math.log(Rt), 3))

    # Convert from Kelvin to Celsius
    TempC = TempK - 273.15
    
    # Convert from Celcius to Fahrenheit
    TempF = (TempC * 9/5) + 32

    return [TempF, TempC] 