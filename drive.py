from machine import Pin
import time

# DriveTrain

# All motors move forward

def motors_stand_tall_lean_back():
    print("Moving 4 motors forward...")
    # Motor 1 Forward
    M1_IN1.value(1)
    M1_IN2.value(0)
    
    # Motor 2 Forward
    M2_IN1.value(1)
    M2_IN2.value(0)
    
    # Motor 3 Forward
    M3_IN1.value(1)
    M3_IN2.value(0)
    
    # Motor 4 Forward
    M4_IN1.value(1)
    M4_IN2.value(0)

# All motors move forward

def motors_left():
    print("Moving 4 motors forward...")
    # Motor 1 Forward
    M1_IN1.value(1)
    M1_IN2.value(0)
    
    # Motor 2 Forward
    M2_IN1.value(1)
    M2_IN2.value(0)
    
    # Motor 3 Forward
    M3_IN1.value(1)
    M3_IN2.value(0)
    
    # Motor 4 Forward
    M4_IN1.value(1)
    M4_IN2.value(0)

# All motors move forward

def motors_right():
    print("Moving 4 motors forward...")
    # Motor 1 Forward
    M1_IN1.value(1)
    M1_IN2.value(0)
    
    # Motor 2 Forward
    M2_IN1.value(1)
    M2_IN2.value(0)
    
    # Motor 3 Forward
    M3_IN1.value(1)
    M3_IN2.value(0)
    
    # Motor 4 Forward
    M4_IN1.value(1)
    M4_IN2.value(0)

# all motors move backwards
def motors_about_face():
    print("Moving 4 motors backward...")
    # Motor 1 Forward
    M1_IN1.value(0)
    M1_IN2.value(1)
    
    # Motor 2 Forward
    M2_IN1.value(0)
    M2_IN2.value(1)
    
    # Motor 3 Forward
    M3_IN1.value(0)
    M3_IN2.value(1)
    
    # Motor 4 Forward
    M4_IN1.value(0)
    M4_IN2.value(1)
    
# Right Face

# Left Face
# stop all motors
def motors_halt():
    print("Stopping all motors.")
    # Setting both pins to 0 stops the motor
    M1_IN1.value(0)
    M1_IN2.value(0)
    M2_IN1.value(0)
    M2_IN2.value(0)
    M3_IN1.value(0)
    M3_IN2.value(0)
    M3_IN1.value(0)
    M4_IN2.value(0)

# --- MAIN EXECUTION ---
#try:
 #   move_forward()
 #   time.sleep(5)  # Keep moving forward for 5 seconds
    
  #  stop_motors()

#except KeyboardInterrupt:
    # Safely stop motors if you press Ctrl+C in your IDE
 #   stop_motors()

# About Face

# Right Face

# Left Face