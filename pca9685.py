# Save this file as pca9685.py
import time

class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self.reset()
        self.set_pwm_freq(1000) # 1kHz is excellent for L298N motors

    def reset(self):
        self.i2c.writeto_mem(self.address, 0x00, b'\x00')

    def set_pwm_freq(self, freq_hz):
        prescaleval = 25000000.0
        prescaleval /= 4096.0
        prescaleval /= float(freq_hz)
        prescaleval -= 1.0
        prescale = int(prescaleval + 0.5)
        
        oldmode = self.i2c.readfrom_mem(self.address, 0x00, 1)[0]
        newmode = (oldmode & 0x7F) | 0x10
        self.i2c.writeto_mem(self.address, 0x00, bytes([newmode]))
        self.i2c.writeto_mem(self.address, 0xFE, bytes([prescale]))
        self.i2c.writeto_mem(self.address, 0x00, bytes([oldmode]))
        time.sleep_ms(5)
        self.i2c.writeto_mem(self.address, 0x00, bytes([oldmode | 0xA1]))

    def set_pwm(self, channel, on, off):
        buf = bytes([0x06 + 4 * channel, on & 0xFF, (on >> 8) & 0xFF, off & 0xFF, (off >> 8) & 0xFF])
        self.i2c.writeto(self.address, buf)

    def set_pin(self, channel, value):
        """Helper to force a pin fully HIGH (4096) or fully LOW (0)"""
        if value == 1:
            self.set_pwm(channel, 4096, 0)
        else:
            self.set_pwm(channel, 0, 4096)
