from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_mcp3xxx.mcp3008 as MCP
from math import atan, degrees
import digitalio
import board
import busio
import time
import os

import pyttsx3
engine = pyttsx3.init()
engine.setProperty('voice', "german")
engine.setProperty('rate', 100)

NORM_BUFFER = 1_000
X_BUFFER = 0.008
Y_BUFFER = 0.02

def point2angle(px, py):
    # this will convert a point (x, y) (-1 to 1) into an angle from y axis
    angle = None
    angle = abs(degrees(atan(px/py)))

    if py < 0 and px < 0: # bottom left
        angle += 180
    elif py < 0: # bottom right
        angle = 180 - angle
    elif px < 0: # top left
        angle = 360 - angle
    # else: # top right -> nothing to change

    return angle

def normalized(p):
    # this will normalize the analog input into range -1 to 1

    low = 64
    middle = 32_500
    high = 65_500

    if p > middle + NORM_BUFFER and p < middle - NORM_BUFFER:
        return 0
    elif p > middle:
        return (p-middle) / middle

    return -(((high-p)-middle) / middle)

def get_option_angle(options):
    # calculate the angle per option
    return 360/len(options)

def get_selected(x, y, angle, angle_per_option):
    # this will return the currently selected option

    if all([x < X_BUFFER, x > -X_BUFFER, y < Y_BUFFER, y > -Y_BUFFER]):
        return None

    current_angle = angle
    count = 0

    while True:
        if  current_angle <= angle_per_option:
            return count
        else:
            current_angle -= angle_per_option
            count += 1

def get_options(path):
    # check the current dir how many options you have to choose
    return os.listdir(path) + [".."]

def text2speech(txt): # this will convert text to speech and play it
    engine.say(txt)
    engine.runAndWait()

def open_file(path):
    # this will open file at path if .txt else return None
    # when opened it will read the content (text2speech)
    with open(path) as file:
        text = file.read()

        text2speech(text)

    exit()

def main():
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D22)
    mcp = MCP.MCP3008(spi, cs)

    # check which pins are used, instead of hard coding it!
    x_channel = AnalogIn(mcp, MCP.P6)
    y_channel = AnalogIn(mcp, MCP.P7)

    base_path = os.path.abspath("./data")

    current_path = base_path
    prev_selected = None

    while True:
        # get newest value from analog input
        x = x_channel.value
        y = y_channel.value

        # print(x, y)

        # normalize the input between -1 and 1
        x = normalized(x)
        y = normalized(y)

        # calculate the angle
        angle = point2angle(x, y)

        # which options are possible
        options = get_options(current_path) # list of all files/ folders/ possibilities

        # get angle per option
        angle_per_option = get_option_angle(options)

        # get which option is currently selected
        selected = get_selected(x, y, angle, angle_per_option)

        # print(selected, options, x, y, angle)
        # print(selected, angle, (x, y))

        # print(selected, prev_selected)
        print(selected, options, end="")

        if selected == None:
            engine.stop() # is this needed?
            if prev_selected != None:
                # change to selected path
                path = os.path.abspath(f"{current_path}/{options[prev_selected]}")
                if path.endswith(".txt"):
                     open_file(path)
                else:
                    current_path = path
        else:
            # print("", options[selected], end="")
            text2speech(str(options[selected]))

        print("")

        # print(f"current_path = {current_path}")

        prev_selected = selected

        time.sleep(.25)

        os.system('clear')

if __name__ == "__main__":
    main()
