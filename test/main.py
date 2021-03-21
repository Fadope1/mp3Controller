from dec import testdec

class core:
    def __init__(self):
        self.name = "xxx"

    def main(self, value):
        print(self.name, value)

    @testdec
    def run(self, func):
        import random
        return random.random()

s = core()
s.run(s.main)
