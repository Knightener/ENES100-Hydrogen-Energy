from machine import time_pulse_us
import time

#Ultrasonic sensor
def respond():
    # Clears the trigPin
    trig.value(0)
    time.sleep_us(2)
    
    # Sets the trigPin on HIGH state for 10 micro seconds
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    
    # Reads the echoPin, returns the sound wave travel time in microseconds
    # We set a timeout of 30000us (30ms) so the code doesn't freeze if it misses the pulse
    duration = time_pulse_us(echo, 1, 30000)
    
    # If the reading is valid (greater than 0)
    if duration > 0:
        # Calculating the distance
        distance = duration * 0.034 / 2
        
        # Prints the distance on the Serial Monitor
        print("Distance:", int(distance), "cm")
        return int(distance)
    else:
        print("Out of range or sensor error")
        return -1;
        
    # Wait a bit before taking the next reading
    time.sleep_ms(200)

while True:
    respond()
    
    