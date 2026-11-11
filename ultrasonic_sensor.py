import machine
import time
from machine import Pin

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

# ==========================================
# MAIN EXECUTION ROUTINE
# ==========================================
print("Ultrasonic Sensor Scan Engine Active. Press Ctrl+C to stop.")

try:
    while True:
        distance = get_distance()
        
        if distance == -1.0:
            print("Sensor Timeout: Object out of range or bad connection.")
        else:
            print(f"Measured Distance: {distance} cm")
            
        # Poll the sensor 5 times a second
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nUltrasonic monitoring paused cleanly.")



