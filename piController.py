# this class is for getting the input/ angle etc. from the joystick
class joystick:
    NORM_BUFFER = 1_000
    X_BUFFER = 0.008
    Y_BUFFER = 0.02

    def __init__(self):
        from adafruit_mcp3xxx.analog_in import AnalogIn
        import adafruit_mcp3xxx.mcp3008 as MCP
        from math import atan, degrees
        import digitalio
        import board
        import busio

        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        self.cs = digitalio.DigitalInOut(board.D22)
        self.mcp = MCP.MCP3008(self.spi, self.cs)

        # TODO: check which pins are used, instead of hard coding it
        self.x_channel = AnalogIn(self.mcp, MCP.P6)
        self.y_channel = AnalogIn(self.mcp, MCP.P7)

    def __normalize(self, p):
        # this will normalize the analog input into range -1 to 1
        low = 64
        middle = 32_500
        high = 65_500

        if p > middle + self.NORM_BUFFER and p < middle - self.NORM_BUFFER:
            return 0
        elif p > middle:
            return (p-middle) / middle

        return -(((high-p)-middle) / middle)

    @staticmethod
    def __calc_angle(x, y):
        # this will convert a point (x, y) (-1 to 1) into an angle from y axis
        angle = None
        angle = abs(degrees(atan(x/y)))

        if y < 0 and x < 0: # bottom left
            angle += 180
        elif y < 0: # bottom right
            angle = 180 - angle
        elif x < 0: # top left
            angle = 360 - angle
        # else: # top right -> nothing to change

        return angle

    @staticmethod
    def __calc_angle_per_option(options):
        return 360/len(options)

    def get_selected(self, options:list)->int:
        # this will get the currently selected index from options
        x = self.__normalize(self.x_channel.value)
        y = self.__normalize(self.y_channel.value)

        angle = self.__calc_angle(x, y)

        angle_per_option = self.__calc_angle_per_option(options)

        # return selected options, else return None
        if all([x < self.X_BUFFER, x > -self.X_BUFFER, y < self.Y_BUFFER, y > -self.Y_BUFFER]):
            return None

        count = 0
        while True:
            if  angle <= angle_per_option:
                return count
            else:
                angle -= angle_per_option
                count += 1
