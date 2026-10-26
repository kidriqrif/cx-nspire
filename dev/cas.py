"""Desktop stand-in for KhiCAS's `cas` module, backed by real Giac (giacpy).

Emulates what caseval returns on the calculator with `shell off`:
errors as 'GIAC_ERROR: ...', powers as '^', top-level lists wrapped as
'[[a,b]]' with '],[' rewritten to ']['.
"""
import os
import sys

_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
try:
    from giacpy import giac as _giac
finally:
    sys.stderr.close()
    sys.stderr = _stderr

EMU = {'wrap': True, 'calls': 0, 'log': None}


def _toplist(r):
    if not r.startswith('['):
        return False
    d = 0
    for k, c in enumerate(r):
        if c == '[':
            d += 1
        elif c == ']':
            d -= 1
            if d == 0:
                return k == len(r) - 1
    return False


def caseval(*a):
    if not a or not isinstance(a[0], str):
        raise TypeError('caseval needs a str')
    s = a[0] if len(a) == 1 else a[0] + '(' + ','.join(str(x) for x in a[1:]) + ')'
    EMU['calls'] += 1
    if EMU['log'] is not None:
        EMU['log'].append(s)
    if s.strip() in ('shell off', 'shell on'):
        return s.strip()
    try:
        r = str(_giac(s))
    except Exception as e:  # giacpy raises on parse errors
        return 'GIAC_ERROR: ' + str(e)
    if r.startswith('"') and not s.startswith(('string(', 'latex(')):
        return 'GIAC_ERROR: ' + r.strip('"')
    if 'Error' in r:
        return 'GIAC_ERROR: ' + r
    r = r.replace('**', '^')
    for pre in ('list[', 'set[', 'matrix['):
        if r.startswith(pre):
            r = r[len(pre) - 1:]
    if EMU['wrap'] and _toplist(r):
        r = '[' + r.replace('],[', '][') + ']'
    return r


xcas = eval_expr = caseval
