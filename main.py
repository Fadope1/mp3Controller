from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_mcp3xxx.mcp3008 as MCP
from math import atan, degrees
import digitalio
import board
import busio
import time
import os

NORM_BUFFER = 1_000

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

    low = 0
    middle = 30_000
    high = 60_000

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

    if all([x==0, y==0]):
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

        if selected == None:
            if prev_selected != None:
                # change to selected path
                current_path = os.path.abspath(f"{current_path}/{options[selected]}")
        else:
            print(selected, options)


        print(f"current_path = {current_path}")

        prev_selected = selected

        time.sleep(1)

        os.system('clear')

if __name__ == "__main__":
    main()
