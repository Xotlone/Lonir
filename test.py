import math

from config import CONSTANTS

test = lambda scores: int(math.sqrt((scores - 100) / 5))
for i in range(10):
    score = CONSTANTS.LEVEL_UP(i + 1)
    print(test(score), score)