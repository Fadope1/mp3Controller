from dec import wrapper

class core:
    def __init__(self):
        self.name = "xxx"

    def main(self, value):
        print(self.name, value)

    @staticmethod
    def random_number(x):
        import random
        print(x)
        return random.random()

    @wrapper
    def random_number(self):
        return self, self.random_number(self.name)

s = core()
s.run(s.main)
