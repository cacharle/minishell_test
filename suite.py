import config
from test import Test

class Suite:
    available = []

    @classmethod
    def run_all(cls):
        for s in cls.available:
            s.run()

    @classmethod
    def setup(cls, asked_names: [str]):
        if len(asked_names) == 0:
            asked_names = [s.name for s in cls.available]
        for s in cls.available:
            if s.name in asked_names:
                s.generate()
        cls.available = [s for s in cls.available if s.name in asked_names]

    def __init__(self, name: str):
        self.name = name
        self.generator_func = None
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def add_generator(self, generator):
        self.generator_func = generator

    def run(self):
        if config.VERBOSE_LEVEL == 0:
            print(self.name + ": ", end="")
        else:
            print("{} {:#<41}".format("#" * 39, self.name + " "))
        for t in self.tests:
            t.run()
        if config.VERBOSE_LEVEL == 0:
            print()

    def generate(self):
        self.generator_func()


def suite(origin):
    """ decorator for a suite function (fmt: suite_[name]) """

    name = origin.__name__[len("suite_"):]
    s = Suite(name)
    def test_generator():
        def test(cmd: str, setup: str = "", files: [str] = [], exports: {str, str} = {}):
            s.add(Test(cmd, setup, files, exports))
        origin(test)
    s.add_generator(test_generator)
    Suite.available.append(s)
    return test_generator
