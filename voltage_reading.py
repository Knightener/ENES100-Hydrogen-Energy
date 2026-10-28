from machine import Pin
import time
#Voltage reading
def knowledge():
    # Initialize analog pin
    analog_pin = Pin(34)
    adc = ADC(analog_pin)

    # Configure the ESP32 to read the full voltage range up to ~3.3V
    adc.atten(ADC.ATTN_11DB)

# The loop routine runs over and over again forever:
while True:
    # Read the input (returns a value from 0 to 4095)
    sensor_value = adc.read()
    
    # Convert the analog reading to a voltage (0 to 3.3V)
    # ESP32 uses 12-bit resolution (4095) and operates at 3.3V max
    voltage = sensor_value * (3.3 / 4095.0)
    
    # Print out the value you read
    print(voltage)
    
    # Tiny delay to prevent flooding the serial monitor
    time.sleep_ms(100)
