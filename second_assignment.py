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

# PWM setup for LED brightness control
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

# Rotary encoder variables
last_clk_state = GPIO.input(clk)
debounce_time = 0.01  # 10 ms debounce

# Function to set brightness for the current color
def SetBrightness(color, value):
    global r_brightness, g_brightness, b_brightness
    
    value = max(0, min(100, value))  # Ensure brightness stays within 0-100 range
    
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
    global last_clk_state, r_brightness, g_brightness, b_brightness, cur_color

    clk_state = GPIO.input(clk)
    dt_state = GPIO.input(dt)
    
    # If the previous and current state of the clk pin differ, we have a valid rotation
    if clk_state != last_clk_state:
        # Clockwise rotation
        if dt_state != clk_state:
            if cur_color == 0:
                r_brightness += 1  # Increment brightness by 1
                SetBrightness(cur_color, r_brightness)
            elif cur_color == 1:
                g_brightness += 1
                SetBrightness(cur_color, g_brightness)
            elif cur_color == 2:
                b_brightness += 1
                SetBrightness(cur_color, b_brightness)
        # Counterclockwise rotation
        else:
            if cur_color == 0:
                r_brightness -= 1  # Decrement brightness by 1
                SetBrightness(cur_color, r_brightness)
            elif cur_color == 1:
                g_brightness -= 1
                SetBrightness(cur_color, g_brightness)
            elif cur_color == 2:
                b_brightness -= 1
                SetBrightness(cur_color, b_brightness)
        
        print(f'Current brightness for color {cur_color}: {r_brightness if cur_color == 0 else g_brightness if cur_color == 1 else b_brightness}')
    
    # Update the last state of clk pin
    last_clk_state = clk_state

# Button callback to switch between colors
def ButtonCallback(channel):
    global cur_color
    cur_color = (cur_color + 1) % 3  # Cycle through colors: 0 -> 1 -> 2 -> 0
    print(f'Color changed to: {"red" if cur_color == 0 else "green" if cur_color == 1 else "blue"}')

# Setup event detection for rotary encoder and button
GPIO.add_event_detect(clk, GPIO.BOTH, callback=EncoderCallback, bouncetime=int(debounce_time * 1000))  # Debounce the rotary encoder
GPIO.add_event_detect(but, GPIO.FALLING, callback=ButtonCallback, bouncetime=300)  # Debounce button

# Main loop
try:
    while True:
        time.sleep(0.1)  # Keep the program running
finally:
    GPIO.cleanup()  # Clean up GPIO pins when done



"""
try:
    while True:
        clk_state = GPIO.input(clk)
        dt_state = GPIO.input(dt)
        if clk_state != rotation_state:
            if dt_state != clk_state:
                if (counter >= 0 and counter < 100):
                    counter += 1
            else:
                if (counter > 0 and counter <= 100):
                    counter -= 1
            print(counter)
        rotation_state = clk_state
       # if GPIO.input(but): #not pressed
        # select color
        if not GPIO.input(but): #pressed
            if color > 1:
                color = 0
            else:
                color += 1
        


        #time.sleep(0.01)
finally:
    GPIO.cleanup()


while True:

    if GPIO.input(17):
        print('Input was HIGH')
        time.sleep(1)
        high_count+=1
        print("high"+str(high_count))
        GPIO.output(22,1)
    else:
        print('Input was LOW')
        time.sleep(1)
        low_count+=1
        print("low"+str(low_count))
        GPIO.output(22,0)

    if not GPIO.input(17):
        GPIO.output(21,1)
        """

