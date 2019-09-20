"""
    pdf2image filename generators
"""

import uuid


def uuid_generator():
    "Returns a UUID4"
    while True:
        yield str(uuid.uuid4())


def counter_generator(prefix="", suffix="", padding_goal=4):
    "Returns a joined prefix, iteration number, and suffix"
    i = 0
    while True:
        i += 1
        yield str(prefix) + str(i).zfill(padding_goal) + str(suffix)
