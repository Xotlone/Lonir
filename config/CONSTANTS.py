import math

DEBUG = True
DEBUG_GUILD = 786678434922233868

TOKEN = "ODkwMjM0MjQ1NTY0NDc3NDYw.YUs1Pw.MU8yzFBX-TV5qbWhkTJH-FIivXo"

DATABASE_SETTINGS = {
    'name': 'd7i41rqke8dj72',
    'user': 'miqfrhwtbfglqo',
    'password': '4b917477d1677ac65d06959a41cfbaf30836ff2a197c91a56908d236c4798bfd',
    'url': 'ec2-34-242-89-204.eu-west-1.compute.amazonaws.com'
}

COOLDOWN_RATE = 1
COOLDOWN_TIME = 3

CLR = (56, 46, 57)

EMOJI_FILTER = r'<:[\w]*:[0-9]*>'
MAX_LEN = 2000
MAX_SCORES = 300
MAX_LEVEL = 2 ** 15 - 1
LEVEL_UP = lambda level: level ** 2 * 5 + 100
SCORES_TO_LEVEL = lambda scores: int(math.sqrt(abs(scores - 100) / 5))
COEFFICIENT_OF_LINEAR = (1 / 1.75) # (sqrt) Easy > 1.5 > hard
SCORES_FROM_LEN = lambda msg_len: int(msg_len ** COEFFICIENT_OF_LINEAR * (MAX_SCORES / MAX_LEN ** COEFFICIENT_OF_LINEAR))