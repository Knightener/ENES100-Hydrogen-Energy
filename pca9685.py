# pca9685.py
import time

class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self.reset()
        self.set_pwm_freq(50) # Default 50Hz for motor/servo control

    def reset(self):
        self.i2c.writeto_mem(self.address, 0x00, b'\x00')

    def set_pwm_freq(self, freq_hz):
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 1.0
        prescale = int(prescaleval + 0.5)
        
        oldmode = self.i2c.readfrom_mem(self.address, 0x00, 1)[0]
        newmode = (oldmode & 0x7F) | 0x10 # Sleep mode
        self.i2c.writeto_mem(self.address, 0x00, bytes([newmode]))
        self.i2c.writeto_mem(self.address, 0xFE, bytes([prescale]))
        self.i2c.writeto_mem(self.address, 0x00, bytes([oldmode]))
        time.sleep_ms(5)
        self.i2c.writeto_mem(self.address, 0x00, bytes([oldmode | 0xa1]))

    def set_pwm(self, channel, on, off):
        self.i2c.writeto_mem(self.address, 0x06 + 4 * channel, bytes([on & 0xFF, (on >> 8) & 0xFF, off & 0xFF, (off >> 8) & 0xFF]))

    def set_duty_cycle(self, channel, duty_percent):
        # duty_percent: 0 to 100
        if duty_percent <= 0:
            self.set_pwm(channel, 0, 0)
        elif duty_percent >= 100:
            self.set_pwm(channel, 4096, 0)
        else:
            value = int(duty_percent * 40.95)
            self.set_pwm(channel, 0, value)

# 4 motors, only single pins, 3 per motor