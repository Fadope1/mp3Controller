import os

# the core system
class core:
    # TODO: Add custom exceptions

    def __init__(self):
        from speaker import speaker
        self.speaker = speaker(rate=150)

        from piController import joystick
        self.joystick = joystick()

        self.base_path = os.path.abspath("./data")

        self.current_path = self.base_path

    @staticmethod
    def get_options(c_path:"path") -> list:
        # list of options currently available
        return os.listdir(c_path) + [".."]

    def main(self, selected):
        path = os.path.abspath(f"{self.current_path}/{selected}")

        if selected.endswith(".txt"):
            self.speaker.speak_file(path)
        elif selected.endswith(".py"):
            try:
                import importlib.util

                spec = importlib.util.spec_from_file_location(selected[:len(selected)-3], path)

                pyfile = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(pyfile)

                import pyclbr

                instance = getattr(pyfile, list(pyclbr.readmodule(pyfile.__name__).keys())[0])()
                instance.start_sub_loop()
            except Exception:
                print("Something went wrong. Fallback to core.")
                self.speaker.say("Etwas ist schief gelaufen. Gehe zurück zum Core System.")
        else:
            self.current_path = path

    def start_main_loop(self):
        import time

        prev_selected = None

        while True:
            options = self.get_options(self.current_path)
            selected = self.joystick.get_selected(options)

            print(options)

            if selected == None and prev_selected != None:
                option = options[prev_selected]
                self.main(option)
            elif selected != None:
                option = options[selected]
                print(option)
                if option.endswith(".txt"):
                    option = option[:len(option)-4]
                self.speaker.speak(str(option))

            prev_selected = selected

            time.sleep(.3)

if __name__ == "__main__":
    system = core()
    system.start_main_loop()
