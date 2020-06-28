# Generates numbers made of a specified amount of sevens
import random
import sys

while c := sys.stdin.readline():
    if not c.isdigit():
        continue
    sys.stdout.write('7' * int(c) + '\n')
    sys.stdout.flush()
