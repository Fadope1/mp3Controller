class calc:
    def __init__(self, joystick=None, speaker=None):
        if joystick == None or speaker == None:
            raise Exception("I/O missing.")

        # from speaker import speaker
        self.speaker = speaker

        # from piController import joystick
        self.joystick = joystick

    @staticmethod
    def get_options():
        # list of options currently available
        return None

    def main(self, selected):
        pass

    def start_sub_loop(self):
        import time

        while True:
            print("NOW IN CALC")
            time.sleep(.3)
