import time

class loop:
    def __init__(self, func):
        self.func = func

        from speaker import speaker
        self.speaker = speaker(rate=150)

        from piController import joystick
        self.controller = joystick()

    def __call__(self, other, run_func):
        prev_selected = None

        while True:
            options = self.func(other)
            selected = self.controller.get_selected(options)

            if selected == None and prev_selected != None:
                run_func(other, selected)
            else:
                self.speaker.speak(options[selected])

            prev_selected = selected

            time.sleep(.3)
