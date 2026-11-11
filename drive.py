from machine import Pin, PWM
import time

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

# --- Main Test Routine ---
try:
    while True:
        # 1. Drive Forward at 80% speed
        print("Moving Forward...")
        set_motors(80, 80)
        time.sleep(2)
        
        # 2. Hard Brake
        print("Braking...")
        stop()
        time.sleep(1)
        
        # 3. Drive Backward at 60% speed
        print("Moving Backward...")
        set_motors(-60, -60)
        time.sleep(2)
        
        # 4. Stop
        stop()
        time.sleep(1)
        
        # 5. Spin Left (Left back, Right forward)
        print("Spinning Left...")
        set_motors(-70, 70)
        time.sleep(1.5)
        
        # 6. Stop before repeating
        stop()
        time.sleep(2)

except KeyboardInterrupt:
    # Safely turn off motors if code is interrupted
    print("Program stopped. Turning off motors.")
    stop()
