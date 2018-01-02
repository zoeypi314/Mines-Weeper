from collections import namedtuple

Config = namedtuple('Config', 'x y n')

EASY = Config(9, 9, 10)
INTERMEDIATE = Config(16, 16, 40)
HARD = Config(30, 16, 99)
