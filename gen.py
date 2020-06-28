# Generates random numbers of specified lengths
import random
import sys

while c := sys.stdin.readline():
    if not c.isdigit():
        continue
    for _ in range(int(c)):
        sys.stdout.write(str(random.randint(0, 10)))
    sys.stdout.write('\n')
    sys.stdout.flush()
