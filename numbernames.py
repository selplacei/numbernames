# This script finds the short scale English name of a number according to the algorithm
# described in The Book of Numbers by J. H. Conway and R. K. Guy (pages 14-15).
# The -s flag prints the input number to stderr and tells you when the calculation
# is complete (useful when not running interactively).
# The -n flag separates every zillion in the output by a newline, e.g.
#   three million
#   two thousand
#   and fifty one
# instead of
#   three million two thousand and fifty one
import sys

class ZillionNames:
    HUNDREDS = {
        0: '', 1: 'centi', 2: 'ducenti', 3: 'trecenti', 4: 'quadrigenti',
        5: 'quingenti', 6: 'sescenti', 7: 'septigenti', 8: 'octigenti', 9: 'nongenti'
    }
    TENS = {
        0: '', 1: 'deci', 2: 'viginti', 3: 'triginta', 4: 'quadraginta',
        5: 'quinquaginta', 6: 'sexaginta', 7: 'septuaginta', 8: 'octoginta', 9: 'nonaginta'
    }
    UNITS = {
        0: '', 1: 'un', 2: 'duo', 3: 'tre', 4: 'quattuor',
        5: 'quinqua', 6: 'se', 7: 'septe', 8: 'octo', 9: 'nove'
    }
    S = {TENS[2], TENS[3], TENS[4], TENS[5], HUNDREDS[3], HUNDREDS[4], HUNDREDS[5]}
    X = {TENS[8], HUNDREDS[1], HUNDREDS[8]}
    M = {TENS[2], TENS[8], HUNDREDS[8]}
    # The following code doesn't work. This bug has been marked as wontfix because obscure generator expressions where the local
    # context goes away at evaluation are the priority for Python devs, and just capturing the value is too hard.
    # N = {TENS[1], TENS[3], TENS[4], TENS[5], TENS[6], *(HUNDREDS[i] for i in range(1, 8))}
    N = {
        TENS[1], TENS[3], TENS[4], TENS[5], TENS[6],
        HUNDREDS[1], HUNDREDS[2], HUNDREDS[3], HUNDREDS[4], HUNDREDS[5], HUNDREDS[6], HUNDREDS[7] 
    }


class UnitNames:
    UNITS = {
        '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five',
        '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
    }
    TEENS = {
        '1': 'eleven', '2': 'twelve', '3': 'thirteen', '4': 'fourteen', '5': 'fifteen',
        '6': 'sixteen', '7': 'seventeen', '8': 'eighteen', '9': 'nineteen'
    }
    TENS = {
        '1': 'ten', '2': 'twenty', '3': 'thirty', '4': 'forty', '5': 'fifty',
        '6': 'sixty', '7': 'seventy', '8': 'eighty', '9': 'ninety'
    }


name_of_cache = {}


def name_of(n: str, use_cache=True, sep=' ') -> str:
    # Main function. Returns the complete name of a number
    if use_cache and n in name_of_cache:
        return name_of_cache[n]
    if not n.isdigit():
        return 'not an integer'
    if set(n) <= {'0'}:
        return 'zero'
    n = n.lstrip('0')
    n_split = list(reversed([n[max(0, i - 3):i] for i in range(len(n), 0, -3)]))
    if len(n_split[0]) != 3:
        n_split[0] = '0' * (3 - len(n_split[0])) + n_split[0]
    zillion_amount = len(n_split)
    zillion_names = []
    if zillion_amount > 1:
        for i, part in enumerate(n_split[:-1]):
            zillion_names.append(name_of_units(part) + ' ' + zillion_suffix(zillion_amount - i - 2))
    units_name = name_of_units(n_split[-1])
    if (zillion_names and units_name) and ' and ' not in units_name:
        units_name = 'and ' + units_name
    zillion_names.append(units_name)
    n_name = sep.join(zillion_names)
    if use_cache:
        name_of_cache[n] = n_name
    return n_name
        

zillion_suffix_cache = {
    0: 'thousand', 1: 'million', 2: 'billion', 3: 'trillion', 4: 'quadrillion',
    5: 'quintillion', 6: 'sextillion', 7: 'septillion', 8: 'octillion', 9: 'nonillion'
}


def zillion_suffix(n: int) -> str:
    # Returns the name of a zillion such that one of it equals 10^(3n + 3)
    # E.g. 0 = thousand, 1 = million, 2 = billion, etc.
    if n in zillion_suffix_cache:
        return zillion_suffix_cache[n]
    parts = []
    while n > 0:
        parts.append(partial_single_zillion_suffix(n % 1000))
        n //= 1000
    return ''.join(parts[::-1]) + 'on'


partial_single_zillion_suffix_cache = {n: s[:-2] for n, s in zillion_suffix_cache.items()}
partial_single_zillion_suffix_cache[0] = 'nilli'


def partial_single_zillion_suffix(n: int) -> str:
    # Returns the partial name of the nth zillion (i.e. ending in "illi"), where n is at most 999
    if n in partial_single_zillion_suffix_cache:
        return partial_single_zillion_suffix_cache[n]
    parts = [ZillionNames.UNITS[n % 10], ZillionNames.TENS[n % 100 // 10], ZillionNames.HUNDREDS[n // 100]]
    parts = list(filter(None, parts))
    if len(parts) > 1:
        if parts[0] == 'tre' and parts[1] in ZillionNames.S | ZillionNames.X:
            parts[0] += 's'
        elif parts[0] == 'se':
            if parts[1] in ZillionNames.S:
                parts[0] += 's'
            elif parts[1] in ZillionNames.X:
                parts[0] += 'x'
        elif parts[0] in {'setpe', 'nove'}:
            if parts[1] in ZillionNames.M:
                parts[0] += 'm'
            elif parts[1] in ZillionNames.N:
                parts[0] += 'n'
    suffix = ''.join(parts)[:-1] + 'illi'
    partial_single_zillion_suffix_cache[n] = suffix
    return suffix
    

name_of_units_cache = {}


def name_of_units(n: str) -> str:
    # Returns the name of a three-digit number (zeroes on the left are mandatory if the number is less than 100)
    if n in name_of_units_cache:
        return name_of_units_cache[n]
    units, tens, hundreds = tuple(n[::-1])
    name = ''
    if hundreds != '0':
        name += UnitNames.UNITS[hundreds] + ' hundred'
        if not {tens, units} <= {'0'}:
            name += ' and '
    if units != '0' and tens == '1':
        name += UnitNames.TEENS[units]
    else:
        if t_name := UnitNames.TENS.get(tens, None):
            name += t_name
        if u_name := UnitNames.UNITS.get(units, None):
            name += (' ' + u_name) if t_name else u_name
    return name


if __name__ == '__main__':
    s = '-s' in sys.argv
    sep = '\n' if '-n' in sys.argv else ' '
    while n := sys.stdin.readline():
        if s:
            sys.stderr.write(n)
        sys.stdout.write(name_of(n.strip(), sep=sep) + '\n')
        if s:
            sys.stderr.write('Done\n')
            sys.stderr.flush()
