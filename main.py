import traceback
import sys
import os

"""
- loop as decorator?
- button to go back to ~/Documents/data
"""

# I for some reason have to do this to auto connect to my headset on startup
MAC_ADDR = "FC:58:FA:4F:D3:D0:" # mac addr of my bluetooth headset

def connect():
    os.system("pulseaudio --start -D")
    os.system(f"connect {MAC_ADDR}")

connect() # start pulseaudio and connect to bluetooth device
os.system("pacmd set-default-sink 1") # set default output to the second channel, in this case first one was some other output
os.system("pulseaudio -k") # kill pulseaudio
connect() # re-establish connection

# There is 100% a better way of connection to a bluetooth device automaticly, but this will do for now

# the core system
class core:
    def __init__(self):
        from speaker import speaker
        self.speaker = speaker(rate=150)

        from piController import joystick
        self.joystick = joystick()

        self.base_path = os.path.abspath("./Desktop/mp3Controller/data") # TODO: replace this with not absolute path

        self.current_path = self.base_path

    @staticmethod
    def get_options(c_path:"path") -> list:
        # list of options currently available
        return os.listdir(c_path) + [".."]

    def main(self, selected):
        path = os.path.abspath(f"{self.current_path}/{selected}")

        if selected.endswith(".txt"): # speak text content
            self.speaker.speak_file(path)
        elif selected.endswith(".py"): # run python program (as subloop if available)
            try:
                import importlib.util

                spec = importlib.util.spec_from_file_location(selected[:len(selected)-3], path)

                pyfile = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(pyfile)

                import pyclbr

                sys.path.append(self.current_path)
                file_cls = pyclbr.readmodule(pyfile.__name__).keys()
                cls = list(file_cls)[0]

                instance = getattr(pyfile, cls)(joystick=self.joystick, speaker=self.speaker)
                instance.start_sub_loop()
            except Exception as e:
                print(f"Something went wrong. Fallback to core. Exc: {e}")
                traceback.print_exception(*sys.exc_info()) # maybe save the exc. to a file?
                self.speaker.speak("Etwas ist schief gelaufen. Gehe zurück zum Core System.")
        else:
            self.current_path = path

    def start_main_loop(self):
        import time

        prev_selected = None
        last_option = None

        while True:
            options = self.get_options(self.current_path)
            selected = self.joystick.get_selected(options)

            print(options)

            if selected == None and prev_selected != None: # selected something
                option = options[prev_selected] # selected option
                self.main(option) # open selected option
            elif selected != None: # currently selecting
                option = options[selected]
                print(option)

                # filter the selected option:
                if option == "..": # If "go back" is selected "cd .."
                    option = "zurück." # speak "go back" ("zurück") instead of ".."
                elif option.endswith(".txt"):
                    option = option[:len(option)-4] # cut of the ".txt"

                if option != last_option: # only say the word once
                    self.speaker.speak(str(option))
                    last_option = option

            prev_selected = selected

            time.sleep(.3)

if __name__ == "__main__":
    system = core()
    system.start_main_loop()
