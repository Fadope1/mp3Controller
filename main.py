# the core system
class core:
    # TODO: Add custom exceptions

    def __init__(self):
        from loop_system import loop
        import os

        from speaker import speaker
        self.speaker = speaker(rate=150)

        self.base_path = os.path.abspath("./data")

        self.current_path = self.base_path

    @staticmethod
    def get_options(c_path):
        # list of options currently available
        return os.listdir(c_path) + [".."]

    def main(self, selected):
        path = os.path.abspath(f"{self.current_path}/{selected}")

        if selected.endswith(".txt"):
            self.speaker.speak_file(path)
        else:
            self.current_path = path

    @loop
    def start_main_loop(self, func):
        return self.get_options(self.current_path)

if __name__ == "__main__":
    system = core()
    system.start_main_loop(system.main)
