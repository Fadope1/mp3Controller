from loop_system import loop

class calc:
    def __init__(self):
        from speaker import speaker
        self.speaker = speaker()

    @staticmethod
    def get_options():
        # list of options currently available
        return None

    def main(self, selected):
        pass

    @loop
    def start_sub_loop(self, func):
        return self.get_options()
