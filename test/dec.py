class testdec:
    def __init__(self, func, class_instance, run_func):
        self.func = func
        self.run_func = run_func
        self.class_instance = class_instance

    def __call__(self):
        while True:
            self.class_instance, x = self.func(self.class_instance, self.run_func)

            self.run_func(x)

def wrapper(function, class_instance, run_func):
    return testdec(function, class_instance, run_func)
