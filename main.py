from loop_system import loop

# the core system
class core:
    # TODO: Add custom exceptions

    def __init__(self):
        import os

        from speaker import speaker
        self.speaker = speaker(rate=150)

        self.base_path = os.path.abspath("./data")

        self.current_path = self.base_path

    @staticmethod
 def get_options(c_path:path) -> list:
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
                instance.start_sub_loop(instance.main)
            except Exception:
                print("Something went wrong. Fallback to core.")
                self.speaker.say("Etwas ist schief gelaufen. Gehe zurück zum Core System.")
        else:
            self.current_path = path

    @loop
    def start_main_loop(self, func):
        return self.get_options(self.current_path)

if __name__ == "__main__":
    system = core()
    system.start_main_loop(system.main)
