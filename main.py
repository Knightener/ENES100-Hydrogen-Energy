from machine import Pin, I2C
import time
from pca9685 import PCA9685

class MecanumRobot:
    def __init__(self, pca):
        self.pca = pca
        # Increase PWM frequency to 1000Hz for smoother DC motor operation
        self.pca.set_pwm_freq(1000)
        
        # Channel mapping: (PWM_Enable, IN1, IN2)
        self.motors = {
            'FL': (0, 1, 2),    # Front Left
            'FR': (3, 4, 5),    # Front Right
            'RL': (6, 7, 8),    # Rear Left
            'RR': (9, 10, 11)   # Rear Right
        }
        self.stop()

    def _set_motor(self, motor_name, speed):
        """
        Controls a single motor.
        speed: -100 (full reverse) to 100 (full forward)
        """
        pwm_ch, in1_ch, in2_ch = self.motors[motor_name]
        
        # Clamp speed between -100 and 100
        speed = max(-100, min(100, speed))
        
        if speed > 0:
            self.pca.set_duty_cycle(in1_ch, 100)
            self.pca.set_duty_cycle(in2_ch, 0)
            self.pca.set_duty_cycle(pwm_ch, speed)
        elif speed < 0:
            self.pca.set_duty_cycle(in1_ch, 0)
            self.pca.set_duty_cycle(in2_ch, 100)
            self.pca.set_duty_cycle(pwm_ch, abs(speed))
        else:
            self.pca.set_duty_cycle(in1_ch, 0)
            self.pca.set_duty_cycle(in2_ch, 0)
            self.pca.set_duty_cycle(pwm_ch, 0)

    def move(self, vx, vy, omega):
        """
        Calculates wheel speeds for omnidirectional movement.
        vx: Forward/Backward (-100 to 100)
        vy: Strafe Right/Left (-100 to 100) -> Positive is Right
        omega: Rotate Clockwise/Counter-Clockwise (-100 to 100) -> Positive is CW
        """
        fl = vx + vy + omega
        fr = vx - vy - omega
        rl = vx - vy + omega
        rr = vx + vy - omega

        # Normalize speeds if any wheel exceeds 100% duty cycle
        max_val = max(abs(fl), abs(fr), abs(rl), abs(rr), 100)
        scale = 100.0 / max_val

        self._set_motor('FL', fl * scale)
        self._set_motor('FR', fr * scale)
        self._set_motor('RL', rl * scale)
        self._set_motor('RR', rr * scale)

    def stop(self):
        for motor in self.motors:
            self._set_motor(motor, 0)

# --- Example Usage ---
if __name__ == '__main__':
    # Initialize I2C on ESP32 (Pins 21 and 22)
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
    
    # Initialize PCA9685 and Mecanum Robot
    pca = PCA9685(i2c, address=0x40)
    bot = MecanumRobot(pca)

    print("Moving Forward...")
    bot.move(vx=60, vy=0, omega=0)
    time.sleep(2)

    print("Strafing Right...")
    bot.move(vx=0, vy=60, omega=0)
    time.sleep(2)

    print("Strafing Left...")
    bot.move(vx=0, vy=-60, omega=0)
    time.sleep(2)

    print("Moving Diagonally Front-Right...")
    bot.move(vx=60, vy=60, omega=0)
    time.sleep(2)

    print("Spinning Clockwise...")
    bot.move(vx=0, vy=0, omega=60)
    time.sleep(2)

    print("Stopping...")
    bot.stop()
