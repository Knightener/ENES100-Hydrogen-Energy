import time
from machine import Pin

# --- Pin Configurations ---
s0 = Pin(13, Pin.OUT)
s1 = Pin(12, Pin.OUT)
s2 = Pin(14, Pin.OUT)
s3 = Pin(27, Pin.OUT)
out_pin = Pin(35, Pin.IN)

# Set frequency scaling to 20%
s0.value(1)
s1.value(0)

# --- Configuration & Filters ---
WINDOW_SIZE = 7
history = []

def read_color_pulse(filter_s2, filter_s3):
    s2.value(filter_s2)
    s3.value(filter_s3)
    time.sleep_ms(10)
    pulse = machine.time_pulse_us(out_pin, 1, 20000)
    if pulse <= 0:
        return 99999
    return pulse

def get_raw_rgb():
    r_pulse = read_color_pulse(0, 0) # Red
    b_pulse = read_color_pulse(0, 1) # Blue
    g_pulse = read_color_pulse(1, 1) # Green
    return r_pulse, g_pulse, b_pulse

def map_pulse_to_rgb(r_raw, g_raw, b_raw):
    # Adjust these values based on your physical calibration setup
    MIN_PULSE = 10   
    MAX_PULSE = 300  
    
    def scale(val):
        if val > MAX_PULSE: return 0
        if val < MIN_PULSE: return 255
        return int(((MAX_PULSE - val) / (MAX_PULSE - MIN_PULSE)) * 255)

    return scale(r_raw), scale(g_raw), scale(b_raw)

def identify_color(r, g, b):
    """
    Analyzes the averaged RGB signatures to classify the color.
    Tolerance thresholds may need slight adjustments depending on target material.
    """
    # Threshold definition: Is the color channel strong?
    HIGH_THRESHOLD = 140
    LOW_THRESHOLD = 100
    
    # 1. Yellow Detection: Red and Green are strong, Blue is noticeably lower
    if r > HIGH_THRESHOLD and g > HIGH_THRESHOLD and b < LOW_THRESHOLD:
        return "YELLOW"
        
    # 2. Basic fallback color classifications
    elif r > HIGH_THRESHOLD and g < LOW_THRESHOLD and b < LOW_THRESHOLD:
        return "RED"
    elif g > HIGH_THRESHOLD and r < LOW_THRESHOLD and b < LOW_THRESHOLD:
        return "GREEN"
    elif b > HIGH_THRESHOLD and r < LOW_THRESHOLD and g < LOW_THRESHOLD:
        return "BLUE"
    elif r < 50 and g < 50 and b < 50:
        return "BLACK"
    elif r > 200 and g > 200 and b > 200:
        return "WHITE"
    else:
        return "UNKNOWN / MIXED"

# --- Main Program Loop ---
print("TCS3200 active with Moving Average + Yellow Detection...")

while True:
    # 1. Read instant physical values
    r_raw, g_raw, b_raw = get_raw_rgb()
    r_inst, g_inst, b_inst = map_pulse_to_rgb(r_raw, g_raw, b_raw)
    
    # 2. Maintain history pipeline
    history.append((r_inst, g_inst, b_inst))
    if len(history) > WINDOW_SIZE:
        history.pop(0)
        
    # 3. Compute steady averages
    current_count = len(history)
    avg_r = sum(read for read in history) // current_count
    avg_g = sum(read for read in history) // current_count
    avg_b = sum(read for read in history) // current_count
    
    # 4. Classify based on the clean averaged values
    detected_color = identify_color(avg_r, avg_g, avg_b)
    
    # 5. Output filtered results
    print(f"Avg RGB: ({avg_r}, {avg_g}, {avg_b}) -> [ DETECTED: {detected_color} ]")
    
    time.sleep(0.1)


