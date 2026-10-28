from machine import Pin
import time
import drive
import ultrasonic

speed = 1
strafe_speed = 0.5
curr_y = 0
min_y = 0
max_y = 10
min_distance = 0.05
read_interval = 1000

# 1: forward, 2: left, 3: backwards, 4: right
orientation = 1

def nav():
    drive.motors_stand_tall_lean_back()
    
    while (True):
            if (ultrasonic.read() < min_distance):
                drive.motors_halt()
                drive.motors_left()
                go_down = True
                while(curr_y < max_y):
                    curr_y += strafe_speed * read_interval
                    time.sleep(read_interval)
                    if (ultrasonic.read() > min_distance):
                        drive.motors_stand_tall_lean_back()
                        go_down = False
                        break
                if (go_down):
                    drive.motors_halt()
                    drive.motors_left()
                    while(curr_y > min_y):
                        curr_y -= strafe_speed * read_interval
                        time.sleep(read_interval)
                        if (ultrasonic.read() > min_distance):
                            drive.motors_stand_tall_lean_back()
                            break
                
            
