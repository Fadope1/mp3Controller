import time

class loop:
    def __init__(self, func):
        self.func = func

        from speaker import speaker
        self.speaker = speaker(rate=150)

        from piController import joystick
        self.controller = joystick()

    def __call__(self, run_func):
        prev_selected = None

        while True:
            options = self.func(self, run_func)
            selected = self.controller.get_selected(options)

            option = options[selected]

            if selected == None and prev_selected != None:
                run_func(option)
            else:
                if option.endswith(".txt"):
                    option = option[:len(option)-4]
                self.speaker.speak(str(option))

            prev_selected = selected

            time.sleep(.3)
