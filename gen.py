# Generates random numbers of specified lengths
import random
import string
import sys

while c := sys.stdin.readline():
    c = c.strip()
    if not c.isdigit():
        continue
    for _ in range(int(c)):
        sys.stdout.write(str(random.choice(string.digits)))
    sys.stdout.write('\n')
    sys.stdout.flush()
