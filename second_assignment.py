import RPi.GPIO as GPIO
import time

# Pin definitions
but = 17      # Button pin
b = 27        # Blue LED pin
g = 22        # Green LED pin
r = 10        # Red LED pin
clk = 9       # Rotary encoder CLK pin
dt = 11       # Rotary encoder DT pin

# Setup GPIO
GPIO.setmode(GPIO.BCM)

# Button setup
GPIO.setup(but, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button with pull-up resistor

# LED setup
GPIO.setup(b, GPIO.OUT)  # Blue
GPIO.setup(g, GPIO.OUT)  # Green
GPIO.setup(r, GPIO.OUT)  # Red

# Rotary encoder setup
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Clock pin with pull-up
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Data pin with pull-up

# PWM setup for LED brightness control with higher frequency (1kHz)
r_pwm = GPIO.PWM(r, 1000)  # Red PWM, 1kHz
g_pwm = GPIO.PWM(g, 1000)  # Green PWM, 1kHz
b_pwm = GPIO.PWM(b, 1000)  # Blue PWM, 1kHz

# Start PWM at 0% brightness for each color
r_pwm.start(0)
g_pwm.start(0)
b_pwm.start(0)

# Variables to track brightness and current color
r_brightness = 0
g_brightness = 0
b_brightness = 0
cur_color = 0  # 0 = red, 1 = green, 2 = blue

# Function to set brightness for the current color
def SetBrightness(color, value):
    global r_brightness, g_brightness, b_brightness
    
    if color == 0:
        r_pwm.ChangeDutyCycle(value)
        r_brightness = value
    elif color == 1:
        g_pwm.ChangeDutyCycle(value)
        g_brightness = value
    elif color == 2:
        b_pwm.ChangeDutyCycle(value)
        b_brightness = value

# Rotary encoder callback
def EncoderCallback(channel):
    global cur_color, r_brightness, g_brightness, b_brightness

    if GPIO.input(clk) == GPIO.input(dt):  # Clockwise rotation
        if cur_color == 0 and r_brightness < 100:
            r_brightness += 2  # Smoother transition with smaller step size
            SetBrightness(cur_color, r_brightness)
        elif cur_color == 1 and g_brightness < 100:
            g_brightness += 2
            SetBrightness(cur_color, g_brightness)
        elif cur_color == 2 and b_brightness < 100:
            b_brightness += 2
            SetBrightness(cur_color, b_brightness)
    else:  # Counterclockwise rotation
        if cur_color == 0 and r_brightness > 0:
            r_brightness -= 2
            SetBrightness(cur_color, r_brightness)
        elif cur_color == 1 and g_brightness > 0:
            g_brightness -= 2
            SetBrightness(cur_color, g_brightness)
        elif cur_color == 2 and b_brightness > 0:
            b_brightness -= 2
            SetBrightness(cur_color, b_brightness)

    print(f'Current brightness for color {cur_color}: {r_brightness if cur_color == 0 else g_brightness if cur_color == 1 else b_brightness}')

# Button callback to switch between colors
def ButtonCallback(channel):
    global cur_color
    cur_color = (cur_color + 1) % 3  # Cycle through colors: 0 -> 1 -> 2 -> 0
    print(f'Color changed to: {"red" if cur_color == 0 else "green" if cur_color == 1 else "blue"}')

# Setup event detection for rotary encoder and button
GPIO.add_event_detect(clk, GPIO.BOTH, callback=EncoderCallback)  # Detect both edges for rotation
GPIO.add_event_detect(but, GPIO.FALLING, callback=ButtonCallback, bouncetime=300)  # Debounce button

# Main loop
try:
    while True:
        time.sleep(0.1)  # Keep the program running
finally:
    GPIO.cleanup()  # Clean up GPIO pins when done
