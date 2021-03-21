import importlib.util

spec = importlib.util.spec_from_file_location("basic_calc", "./data/Taschenrechner/basic_calc.py")

foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)

test = foo.calc()
test.run()
