import machine
import time
from machine import Pin, PWM

# Initialize Ultrasonic Pins 
# Trigger -> GPIO 18 (Output)
# Echo    -> GPIO 19 (Input)
trigger_pin = Pin(23, Pin.OUT)
echo_pin = Pin(19, Pin.IN)

def get_distance():
    """
    Measures distance using the HC-SR04 ultrasonic sensor.
    Returns: 
        Distance in centimeters (float).
        Returns -1.0 if the pulse times out (object too close or too far away).
    """
    # Ensure trigger starts low and clean
    trigger_pin.value(0)
    time.sleep_us(5)
    
    # Send a precise 10-microsecond high pulse to trigger the sensor burst
    trigger_pin.value(1)
    time.sleep_us(10)
    trigger_pin.value(0)
    
    # Measure the duration (in microseconds) that the Echo pin stays High (1)
    # 30000ms max timeout prevents the script from hanging if no pulse returns
    duration = machine.time_pulse_us(echo_pin, 1, 30000)
    
    # If the pulse timed out or failed, return an error flag
    if duration < 0:
        return -1.0
        
    # Sound speed math: (duration * 0.0343 cm/us) / 2 (accounting for round trip)
    distance_cm = duration * 0.01715
    return round(distance_cm, 1)

# --- LEFT MOTORS (L298N Motor A Terminal) ---
# Controlled via GPIO 21 (Speed), 22 & 26 (Direction)
ena = PWM(Pin(18), freq=20000, duty_u16=0)
in1 = Pin(16, Pin.OUT)
in2 = Pin(17, Pin.OUT)
# 3:12  4:13  2:14

# --- RIGHT MOTORS (L298N Motor B Terminal) ---
# Controlled via GPIO 32 (Speed), 25 & 33 (Direction)
enb = PWM(Pin(14), freq=20000, duty_u16=0)
in3 = Pin(12, Pin.OUT)
in4 = Pin(13, Pin.OUT)



def set_motors(left_speed, right_speed):
    """
    Controls 4WD movement. 
    Speeds range from -100 to 100.
    Positive = Forward, Negative = Backward, 0 = Stop.
    """
    # --- Left Side Logic ---
    if left_speed > 0:
        in1.value(1)
        in2.value(0)
    elif left_speed < 0:
        in1.value(0)
        in2.value(1)
    else:
        in1.value(0)
        in2.value(0)
        
    # --- Right Side Logic ---
    if right_speed > 0:
        in3.value(1)
        in4.value(0)
    elif right_speed < 0:
        in3.value(0)
        in4.value(1)
    else:
        in3.value(0)
        in4.value(0)

    # Convert 0-100% speed scale to MicroPython 16-bit PWM (0-65535)
    duty_left = int((abs(left_speed) / 100) * 65535)
    duty_right = int((abs(right_speed) / 100) * 65535)
    
    ena.duty_u16(duty_left)
    enb.duty_u16(duty_right)

def stop():
    set_motors(0, 0)

# Main test
try:
    while True:
        distance = get_distance()
        
        if distance == -1.0:
            print("Sensor Timeout: Object out of range or bad connection.")
        elif distance >= 5.0:
            print(f"Measured Distance: {distance} cm")
            # 1. Drive Forward at 80% speed
            print("Moving Forward...")
            set_motors(80, -80)
        elif distance <= 5.0:
            print(f"Measured Distance: {distance} cm")
            stop()
        
        else:
            print(f"Measured Distance: {distance} cm")
            
        # Poll the sensor 5 times a second
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nUltrasonic monitoring paused cleanly.")



