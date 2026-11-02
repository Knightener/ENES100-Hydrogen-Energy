# Save this file as main.py
from machine import Pin, I2C
from pca9685 import PCA9685
import time

# Initialize I2C and PCA9685 Expander
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
pwm_ext = PCA9685(i2c, address=0x40)

# Define Pin Configurations for all 4 Motors (PCA9685 Yellow Pins)
LF_SPEED = 0; LF_D1 = 1; LF_D2 = 2   # Left Front
RF_SPEED = 4; RF_D1 = 5; RF_D2 = 6   # Right Front
LR_SPEED = 8; LR_D1 = 9; LR_D2 = 10  # Left Rear
RR_SPEED = 12; RR_D1 = 13; RR_D2 = 14 # Right Rear

def set_motor(speed, spd_pin, d1_pin, d2_pin):
    """Core function to set direction and 12-bit speed for a single motor slot"""
    if speed == 0:
        pwm_ext.set_pin(d1_pin, 0)
        pwm_ext.set_pin(d2_pin, 0)
        pwm_ext.set_pwm(spd_pin, 0, 0)
        return
        
    # Cap values strictly within motor constraints
    speed = max(-100, min(100, speed))
    raw_pwm = int(abs(speed) * 40.95)
    
    if speed > 0:
        pwm_ext.set_pin(d1_pin, 1)
        pwm_ext.set_pin(d2_pin, 0)
    else:
        pwm_ext.set_pin(d1_pin, 0)
        pwm_ext.set_pin(d2_pin, 1)
    pwm_ext.set_pwm(spd_pin, 0, raw_pwm)

# ==========================================
# ADVANCED MECANUM VECTOR MATH ENGINE
# ==========================================

def drive_vector(x, y, turn):
    """
    Computes and sends vector forces to all 4 Mecanum wheels.
    x:    Sideways movement (-100 = Full Left, 100 = Full Right)
    y:    Forward movement (-100 = Full Backward, 100 = Full Forward)
    turn: Rotational movement (-100 = Full CCW, 100 = Full CW)
    """
    # Mecanum kinematic equations mapping vectors to motor outputs
    lf_speed = y + x + turn
    rf_speed = y - x - turn
    lr_speed = y - x + turn
    rr_speed = y + x - turn
    
    # Normalize speeds if any calculation exceeds 100% boundary
    max_val = max(abs(lf_speed), abs(rf_speed), abs(lr_speed), abs(rr_speed))
    if max_val > 100:
        lf_speed = (lf_speed / max_val) * 100
        rf_speed = (rf_speed / max_val) * 100
        lr_speed = (lr_speed / max_val) * 100
        rr_speed = (rr_speed / max_val) * 100

    # Write vectors directly to hardware pins
    set_motor(lf_speed, LF_SPEED, LF_D1, LF_D2)
    set_motor(rf_speed, RF_SPEED, RF_D1, RF_D2)
    set_motor(lr_speed, LR_SPEED, LR_D1, LR_D2)
    set_motor(rr_speed, RR_SPEED, RR_D1, RR_D2)

def stop_rover():
    """Brakes all 4 wheels instantly"""
    drive_vector(0, 0, 0)

# ==========================================
# SIMPLIFIED WRAPPER FUNCTIONS
# ==========================================

def strafe_right(speed=60):
    """Slides directly sideways to the right (x=speed, y=0, turn=0)"""
    drive_vector(speed, 0, 0)

def strafe_left(speed=60):
    """Slides directly sideways to the left (x=-speed, y=0, turn=0)"""
    drive_vector(-speed, 0, 0)

def turn_90_right(speed=50):
    """Pivots the robot roughly 90 degrees clockwise, then stops"""
    drive_vector(0, 0, speed)
    time.sleep(0.85)  # ADJUST THIS DELAY until it hits exactly 90 degrees
    stop_rover()

def turn_90_left(speed=50):
    """Pivots the robot roughly 90 degrees counter-clockwise, then stops"""
    drive_vector(0, 0, -speed)
    time.sleep(0.85)  # MATCH TO PRECISE CALIBRATION DELAY ABOVE
    stop_rover()

# ==========================================
# MAIN EXECUTION ROUTINE
# ==========================================
try:
    print("Mecanum Matrix Controller Online. Testing sequences...")
    while True:
        print("Moving Sideways Right...")
        strafe_right(60)
        time.sleep(2)
        stop_rover()
        time.sleep(1)
        
        print("Moving Sideways Left...")
        strafe_left(60)
        time.sleep(2)
        stop_rover()
        time.sleep(1)
        
        print("Pivoting 90° Right...")
        turn_90_right(50)
        time.sleep(2)
        
        print("Pivoting 90° Left...")
        turn_90_left(50)
        time.sleep(2)
        
        print("Bonus: Driving diagonally forward-right...")
        drive_vector(50, 50, 0)
        time.sleep(2)
        stop_rover()
        time.sleep(2)

except KeyboardInterrupt:
    stop_rover()
    print("Mecanum execution killed safely.")
