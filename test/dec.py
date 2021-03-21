class testdec:
    def __init__(self, func):
        self.func = func

    def __call__(self, run_func):
        while True:
            x = self.func(self, run_func)

            run_func(x)
