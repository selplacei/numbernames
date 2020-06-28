# This script finds the English name of a number according to the algorithm
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

name_of_cache = {}

def name_of(n: str, use_cache=True) -> str:
    # Returns the English name of a number according to the short scale
    if use_cache and n in name_of_cache:
        return name_of_cache[n]
    if not n.isdigit():
        return 'not a number'
    if set(n) <= {'0'}:
        return 'zero'
    n = n.lstrip('0')
    n = '0' * (3 - (len(n) % 3 or 3)) + n
    n_els = [n[i:i+3] for i in range(0, len(n), 3)]
    name_els = []
    if len(n_els) > 1:
        for i, m in enumerate(n_els[:-1]):
            name_els.append(amount_prefix(m) + ' ' + zillion_suffix(len(n_els) - i - 2))
    name_units = amount_prefix(n_els[-1])
    if name_els and name_units and ' and ' not in name_units:
        name_units = 'and ' + name_units
    name_els.append(name_units)
    name = ('\n' if '-n' in sys.argv else ' ').join(name_els)
    if use_cache:
        name_of_cache[n] = name
    return name
        

zillion_suffix_cache = {
    0: 'thousand', 1: 'million', 2: 'billion', 3: 'trillion', 4: 'quadrillion',
    5: 'quintillion', 6: 'sextillion', 7: 'septillion', 8: 'octillion', 9: 'nonillion'
}

def zillion_suffix(n: int) -> str:
    # Returns the complete name of the zillion such that 10^(3n + 3) is 1 such zillion
    # E.g. 0 = thousand, 1 = million, 2 = billion, etc.
    if n in zillion_suffix_cache:
        return zillion_suffix_cache[n]
    parts = []
    while n > 0:
        parts.append(partial_zillion_prefix(n % 1000))
        n //= 1000
    return ''.join(parts[::-1]) + 'on'


partial_zillion_prefix_cache = {n: s[:-2] for n, s in zillion_suffix_cache.items()}
partial_zillion_prefix_cache[0] = 'nilli'

def partial_zillion_prefix(n: int) -> str:
    # Returns the partial name of the nth zillion (i.e. ending in "illi"), where n is at most 999
    if n in partial_zillion_prefix_cache:
        return partial_zillion_prefix_cache[n]
    S = {'viginti', 'triginta', 'quadraginta', 'quinquaginta',
         'trecenti', 'quadringenti', 'quingenti'}
    X = {'octoginta', 'centi', 'octigenti'}
    M = {'viginti', 'octoginta', 'octigenti'}
    N = {'deci', 'triginta', 'quadraginta', 'quinquaginta', 'sexaginta',
         'centi', 'ducenti', 'trecenti', 'quadrigenti', 'quingenti', 'sescenti', 'septigenti'}
    els = []
    els.append({
        0: '', 1: 'centi', 2: 'ducenti', 3: 'trecenti', 4: 'quadrigenti',
        5: 'quingenti', 6: 'sescenti', 7: 'septigenti', 8: 'octigenti', 9: 'nongenti'
    }[n // 100])
    els.append({
        0: '', 1: 'deci', 2: 'viginti', 3: 'triginta', 4: 'quadraginta',
        5: 'quinquaginta', 6: 'sexaginta', 7: 'septuaginta', 8: 'octoginta', 9: 'nonaginta'
    }[n % 100 // 10])
    els.append({
        0: '', 1: 'un', 2: 'duo', 3: 'tre', 4: 'quattuor',
        5: 'quinqua', 6: 'se', 7: 'septe', 8: 'octo', 9: 'nove'
    }[n % 10])
    unbr = 1 if els[1] else 0 if els[0] else -1
    if els[2] and unbr != -1:
        if els[2] == 'tre' and (els[unbr] in S or els[unbr] in X):
            els[2] += 's'
        elif els[2] == 'se':
            if els[unbr] in S:
                els[2] += 's'
            elif els[unbr] in X:
                els[2] += 'x'
        elif els[2] in {'setpe', 'nove'}:
            if els[unbr] in M:
                els[2] += 'm'
            elif els[unbr] in N:
                els[2] += 'n'
    prefix = ''.join(els[::-1])[:-1] + 'illi'
    partial_zillion_prefix_cache[n] = prefix
    return prefix
    

amount_prefix_cache = {}

def amount_prefix(n: str) -> str:
    # Returns the name of a three-digit number (assumes zero-padding)
    unit_names = {
        '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five',
        '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
    }
    teen_names = {
        '1': 'eleven', '2': 'twelve', '3': 'thirteen', '4': 'fourteen', '5': 'fifteen',
        '6': 'sixteen', '7': 'seventeen', '8': 'eighteen', '9': 'nineteen'
    }
    tens_names = {
        '1': 'ten', '2': 'twenty', '3': 'thirty', '4': 'forty', '5': 'fifty',
        '6': 'sixty', '7': 'seventy', '8': 'eighty', '9': 'ninety'
    }
    if n in amount_prefix_cache:
        return amount_prefix_cache[n]
    u, t, h = tuple(n[::-1])
    p = ''
    if h != '0':
        p += unit_names[h] + ' hundred'
        if not {t, u} <= {'0'}:
            p += ' and '
    if u != '0' and t == '1':
        p += teen_names[u]
    else:
        if c := tens_names.get(t, None):
            p += c
        if d := unit_names.get(u, None):
            p += ' ' + d if c else d
    return p


if __name__ == '__main__':
    while s := sys.stdin.readline():
        if '-s' in sys.argv:
            sys.stderr.write(s)
        sys.stdout.write(name_of(s.strip()) + '\n')
        if '-s' in sys.argv:
            sys.stderr.write('Done')
            sys.stderr.flush()
    
