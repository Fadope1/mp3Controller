# the core system
class core:
    # TODO: Add custom exceptions

    def __init__(self):
        from loop_system import loop
        from speaker import speaker
        import os

        self.base_path = os.path.abspath("./data")

        self.current_path = self.base_path

    @staticmethod
    def get_options(c_path):
        # list of options currently available
        return os.listdir(c_path) + [".."]

    def change_dir(self, selected):
        print("changed dir")

    @loop
    def start_main_loop(self, func):
        return self.get_options(self.current_path)

if __name__ == "__main__":
    system = core()
    system.start_main_loop(system.select_option)
