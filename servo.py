import time
from machine import Pin, PWM

# On ESP32, avoid GPIO 6-11 (flash memory pins). 
# We'll use GPIO 4, which safely supports hardware PWM.
servo_pin = Pin(25)
servo = PWM(servo_pin, freq=50)

def set_angle(angle):
    # ESP32 standard 16-bit hardware PWM mapping for a 50Hz servo cycle:
    # 0 degrees   -> ~0.5ms pulse -> duty cycle ~1638
    # 180 degrees -> ~2.5ms pulse -> duty cycle ~8192
    min_duty = 1638
    max_duty = 8192
    
    # Calculate the precise 16-bit duty value
    duty = int(min_duty + (angle / 180.0) * (max_duty - min_duty))
    servo.duty_u16(duty)

# Continuous sweeping loop (0 to 105 degrees)
while True:
    # Sweep forward from 0 to 105 degrees
    for pos in range(0, 106, 1):
        set_angle(pos)
        time.sleep_ms(15)
        
    # Sweep backward from 105 down to 0 degrees
    for pos in range(105, -1, -1):
        set_angle(pos)
        time.sleep_ms(15)
