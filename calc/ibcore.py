# ibcore.py - shared runtime for the IB AA HL step solver
# KhiCAS MicroPython 1.12: no f-strings, no re, no recursion.
import math

# ---------- settings (edit here or via Settings menu) ----------
CFG = {'w': 32, 'pg': 10, 'uni': 1, 'pause': 1}

# ---------- Giac bridge ----------
_ce = None
try:
    from cas import caseval as _ce
except ImportError:
    try:
        from xcas import caseval as _ce
    except ImportError:
        _ce = None


class GErr(Exception):
    pass


ST = {'wrap': 0, 'im': '', 'ln': 0, 'dirty': 0, 'code': '', 'again': 0}
SETUP = ('shell off', 'angle_radian:=1', 'complex_mode:=0', 'approx_mode:=0')


def _setup():
    for c in SETUP:
        try:
            _ce(c)
        except Exception:
            pass


def reset():
    ST['last'] = ''
    # Giac keeps hidden state after rootof results (changes factor());
    # restart its context between solvers when that happened
    if ST['dirty']:
        try:
            _ce('restart')
        except Exception:
            pass
        _setup()
        ST['dirty'] = 0


def init():
    if _ce is None:
        raise GErr('cas module not found')
    _setup()
    r = str(_ce('[1,2]')).strip()
    ST['wrap'] = 1 if r[:2] == '[[' else 0
    r = str(_ce('sqrt(-1)')).strip()
    ST['im'] = r if r != 'i' else ''


def _clean(r):
    r = r.strip()
    if ST['wrap'] and r[:2] == '[[' and r[-2:] == ']]':
        r = r[1:-1].replace('][', '],[')
    r = r.replace('**', '^')
    if ST['im']:
        r = r.replace(ST['im'], 'i')
    return r


def G(c):
    r = str(_ce(c)).strip()
    if r == 'Large_object':
        r = str(_ce('string(' + c + ')')).strip()
        if len(r) > 1 and r[0] == '"' and r[-1] == '"':
            r = r[1:-1]
    if r[:10] == 'GIAC_ERROR' or 'Error' in r or (r[:1] == '"' and c[:7] != 'string('):
        raise GErr(r.replace('GIAC_ERROR:', '').strip('" ')[:60])
    if 'rootof' in r:
        ST['dirty'] = 1
    return _clean(_negden(r))


def _negden(r):
    # Giac's subst can leave 'a/-b': rewrite numeric cases as -a/b
    k = r.find('/-')
    n = 0
    while k > 0 and n < 9:
        n += 1
        i = k
        while i > 0 and (r[i - 1] in DIG or r[i - 1] == '.'):
            i -= 1
        j = k + 2
        while j < len(r) and (r[j] in DIG or r[j] == '.'):
            j += 1
        # also skip a numerator that follows '^' (x^2/-3 must stay as is)
        if (i == k or j == k + 2 or r[i - 1:i] == '^'
                or (r[i - 1:i] in ('+', '-') and r[i - 2:i - 1] == '^')):
            k = r.find('/-', k + 2)
            continue
        q = r[i:k] + '/' + r[k + 2:j]
        p = r[i - 1] if i > 0 else ''
        if p == '+' or p == '-':
            r = r[:i - 1] + ('-' if p == '+' else '+') + q + r[j:]
        else:
            r = r[:i] + '-' + q + r[j:]
        k = r.find('/-')
    return r


def Gs(c):
    # like G but returns '' instead of raising
    try:
        return G(c)
    except GErr:
        return ''


def _trig(s):
    return 'sin(' in s or 'cos(' in s or 'tan(' in s


def S(e):
    # shortest of raw / normal / simplify (simplify skipped for trig:
    # it rewrites into tan(x/2) forms and is memory-hungry on the TI)
    best = G(e)
    for f in ('normal(', 'ratnormal(', 'simplify('):
        if f == 'simplify(' and _trig(best):
            continue
        r = Gs(f + e + ')')
        if r and len(r) < len(best) and not ('tan(' in r and 'tan(' not in best)                 and not _nprod(r):
            best = r
    return best


def _nprod(r):
    # unevaluated number*number (ratnormal can leave '50*4')
    for i in range(1, len(r) - 1):
        if r[i] == '*' and r[i - 1] in DIG and r[i + 1] in DIG:
            j = i - 1
            while j >= 0 and (r[j] in DIG or r[j] == '.'):
                j -= 1
            k = i + 1
            while k < len(r) and (r[k] in DIG or r[k] == '.'):
                k += 1
            if (j < 0 or r[j] not in '^/') and (k >= len(r) or r[k] != '^'):
                return True
    return False


def N(e):
    return G('normal(' + e + ')')


def D(e, v='x'):
    return G('diff(' + e + ',' + v + ')')


def I(e, v='x'):
    return G('integrate(' + e + ',' + v + ')')


def bad(r):
    # result unusable for exam working
    for k in ('undef', 'integrate(', 'erf', 'rootof', 'Int(', 'Si(', 'Ci('):
        if k in r:
            return True
    return r == ''


def F(e):
    # float value of a Giac expression, or None
    r = Gs('evalf(' + e + ')')
    try:
        return float(r)
    except ValueError:
        return None


# ---------- string helpers ----------
LET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
DIG = '0123456789'
OPN = '([{'
CLS = ')]}'
FUNCS = ['arcsin', 'arccos', 'arctan', 'cosec', 'log10', 'asin', 'acos',
         'atan', 'sinh', 'cosh', 'tanh', 'sqrt', 'sin', 'cos', 'tan', 'sec',
         'csc', 'cot', 'exp', 'log', 'abs', 'ln']
ALIAS = {'arcsin': 'asin', 'arccos': 'acos', 'arctan': 'atan',
         'cosec': 'csc', 'log': 'log10'}


def _word(w, nxt, toks):
    if w in FUNCS:
        toks.append(['F', ALIAS.get(w, w)])
        return
    if w == 'pi' or len(w) == 1:
        toks.append(['V', w])
        return
    if nxt == '(':
        known = False
        for f in FUNCS:
            if len(w) > len(f) and w[len(w) - len(f):] == f:
                known = True
                break
        if not known:
            toks.append(['F', w])
            return
    i = 0
    while i < len(w):
        hit = ''
        for f in FUNCS:
            if w[i:i + len(f)] == f:
                hit = f
                break
        if hit:
            toks.append(['F', ALIAS.get(hit, hit)])
            i += len(hit)
        elif w[i:i + 2] == 'pi':
            toks.append(['V', 'pi'])
            i += 2
        else:
            toks.append(['V', w[i]])
            i += 1


def _lex(s):
    toks = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == ' ':
            i += 1
            continue
        if c in DIG or (c == '.' and i + 1 < n and s[i + 1] in DIG):
            j = i
            while j < n and (s[j] in DIG or s[j] == '.'):
                j += 1
            toks.append(['N', s[i:j]])
            i = j
            continue
        if c in LET:
            j = i
            while j < n and s[j] in LET:
                j += 1
            w = s[i:j]
            i = j
            k = i
            while k < n and s[k] == ' ':
                k += 1
            _word(w, s[k] if k < n else '', toks)
            continue
        if c in OPN:
            toks.append(['L', c])
        elif c in CLS:
            toks.append(['R', c])
        elif c == ',':
            toks.append(['C', c])
        else:
            toks.append(['O', c])
        i += 1
    return toks


def _bars(s):
    # |u| -> abs(u), non-nested
    if '|' not in s:
        return s
    o = ''
    op = False
    for c in s:
        if c == '|':
            o += ')' if op else 'abs('
            op = not op
        else:
            o += c
    return o


def _fpow(t):
    # sin^2(x) -> (sin(x))^2 ; sin^-1(x) -> asin(x) (also cos, tan)
    n = len(t)
    o = []
    i = 0
    while i < n:
        x = t[i]
        m = i + 2
        if (x[0] == 'F' and x[1] in ('sin', 'cos', 'tan', 'sec', 'csc', 'cot')
                and i + 1 < n and t[i + 1] == ['O', '^'] and m < n):
            sg = ''
            if t[m] == ['O', '-']:
                sg = '-'
                m += 1
            if m < n and t[m][0] == 'N' and t[m][1].isdigit():
                e = sg + t[m][1]
                m += 1
                j = m
                if j < n and t[j] == ['L', '(']:
                    # parenthesised argument: find the matching ')'
                    d = 0
                    while j < n:
                        if t[j][0] == 'L':
                            d += 1
                        elif t[j][0] == 'R':
                            d -= 1
                        j += 1
                        if d == 0:
                            break
                    if d:
                        j = m
                else:
                    # bare argument: numbers/variables joined by ^
                    ip = ''
                    while j < n:
                        a = t[j][0]
                        if a == 'N' or a == 'V':
                            ip = a
                            j += 1
                        elif (a == 'O' and t[j][1] == '^' and ip and j + 1 < n
                              and t[j + 1][0] in ('N', 'V')):
                            j += 2
                        else:
                            break
                if j > m:
                    if e == '-1' and x[1] in ('sin', 'cos', 'tan'):
                        o += [['F', 'a' + x[1]]] + t[m:j]
                    else:
                        o += [['L', '('], x] + t[m:j] + [['R', ')'], ['O', '^'], ['N', e]]
                    i = j
                    continue
        o.append(x)
        i += 1
    return o


def norm(s):
    # tidy user input: implicit *, ** -> ^, IB log = log10
    s = str(s).strip()
    for a, b in (('**', '^'), ('π', 'pi'), ('√', 'sqrt'),
                 ('−', '-'), ('×', '*'), ('÷', '/'),
                 ('θ', 't')):
        s = s.replace(a, b)
    s = _bars(s)
    t = _fpow(_lex(s))
    o = ''
    prev = ''
    i = 0
    n = len(t)
    while i < n:
        ty = t[i][0]
        tx = t[i][1]
        if ty == 'F' and not (i + 1 < n and t[i + 1][0] == 'L'):
            j = i + 1
            inner = ''
            ip = ''
            while j < n:
                a = t[j][0]
                if a == 'N' or a == 'V':
                    if ip:
                        inner += '*'
                    inner += t[j][1]
                    ip = a
                    j += 1
                elif a == 'O' and t[j][1] == '^' and ip and j + 1 < n \
                        and t[j + 1][0] in ('N', 'V'):
                    inner += '^' + t[j + 1][1]
                    j += 2
                else:
                    break
            if prev in ('N', 'V', 'R'):
                o += '*'
            if inner == '':
                o += tx
                prev = 'F'
                i += 1
                continue
            o += tx + '(' + inner + ')'
            prev = 'R'
            i = j
            continue
        if ty == 'O' and tx == '^' and prev == 'V' and o[-1:] == 'e' \
                and i + 2 < n and t[i + 1][0] == 'N' and t[i + 2][0] == 'V':
            o += '^(' + t[i + 1][1] + '*' + t[i + 2][1] + ')'
            prev = 'R'
            i += 3
            continue
        if prev in ('N', 'V', 'R') and ty in ('N', 'V', 'F', 'L'):
            o += '*'
        o += tx
        prev = ty
        i += 1
    return o


def rhs(s):
    k = s.find('=')
    return s[k + 1:] if k >= 0 else s


def lhs0(s):
    # 'a=b' -> '(a)-(b)'
    k = s.find('=')
    if k < 0:
        return s
    return '(' + s[:k] + ')-(' + s[k + 1:] + ')'


def split_terms(s):
    terms = []
    cur = ''
    d = 0
    p1 = ''
    for c in s:
        if c == ' ':
            continue
        if c in OPN:
            d += 1
        elif c in CLS:
            d = max(0, d - 1)
        if (c == '+' or c == '-') and d == 0 and p1 != '' \
                and p1 not in '^*/([{,+-=':
            if cur:
                terms.append(cur)
            cur = c
        else:
            cur += c
        p1 = c
    if cur:
        terms.append(cur)
    return terms


def sign_body(t):
    neg = False
    t = t.strip()
    while t and t[0] in '+-':
        if t[0] == '-':
            neg = not neg
        t = t[1:].strip()
    return neg, t


def join_signed(parts):
    s = ''
    for p in parts:
        neg, p = sign_body(str(p))
        if p == '' or p == '0':
            continue
        if s == '':
            s = ('-' + p) if neg else p
        else:
            s += (' - ' if neg else ' + ') + p
    return s if s else '0'


def unwrap(s):
    s = s.strip()
    while len(s) > 1 and s[0] == '(' and s[-1] == ')':
        d = 0
        m = len(s)
        ok = True
        for j in range(m):
            if s[j] in OPN:
                d += 1
            elif s[j] in CLS:
                d -= 1
            if d == 0 and j < m - 1:
                ok = False
                break
        if not ok:
            break
        s = s[1:-1].strip()
    return s


def split_top(s, ch):
    out = []
    cur = ''
    d = 0
    for c in s:
        if c in OPN:
            d += 1
        elif c in CLS:
            d -= 1
        if c == ch and d == 0:
            out.append(cur.strip())
            cur = ''
        else:
            cur += c
    out.append(cur.strip())
    return out


def split_factors(s):
    # -> (neg, [[op, factor], ...]) op is '*' or '/'
    neg = False
    for rep in range(3):
        s = unwrap(s)
        if len(split_terms(s)) > 1:
            break
        n2, s = sign_body(s)
        if n2:
            neg = not neg
    if len(split_terms(s)) > 1:
        return neg, [['*', s]]
    f = []
    cur = ''
    op = '*'
    d = 0
    for c in s:
        if c in OPN:
            d += 1
        elif c in CLS:
            d -= 1
        if (c == '*' or c == '/') and d == 0:
            if cur:
                f.append([op, cur])
            op = c
            cur = ''
        else:
            cur += c
    if cur:
        f.append([op, cur])
    return neg, f


def has(s, v='x'):
    n = len(s)
    m = len(v)
    i = s.find(v)
    while i >= 0:
        a = s[i - 1] if i > 0 else ''
        b = s[i + m] if i + m < n else ''
        if (a == '' or a not in LET) and (b == '' or b not in LET):
            return True
        i = s.find(v, i + 1)
    return False


def parse_list(r):
    s = str(r).strip()
    k = s.find('[')
    if k < 0:
        return [s]
    for ch in s[:k]:
        if ch not in LET:
            return [s]
    d = 0
    end = -1
    for j in range(k, len(s)):
        ch = s[j]
        if ch in OPN:
            d += 1
        elif ch in CLS:
            d -= 1
            if d == 0:
                end = j
                break
    if end < 0 or s[end + 1:].strip():
        return [s]
    inner = s[k + 1:end]
    if inner.strip() == '':
        return []
    return split_top(inner, ',')


def GL(c):
    return parse_list(G(c))


def isnum(r):
    for c in r:
        if c not in DIG and c not in '-./':
            return False
    return r != ''


# ---------- display ----------
def _absbars(s):
    i = s.find('abs(')
    while i >= 0:
        d = 0
        j = i + 3
        while j < len(s):
            if s[j] == '(':
                d += 1
            elif s[j] == ')':
                d -= 1
                if d == 0:
                    break
            j += 1
        if j >= len(s):
            break
        a = i
        b = j + 1
        if i > 1 and s[i - 1] == '(' and s[i - 2] in LET and b < len(s) and s[b] == ')':
            a = i - 1
            b += 1
        s = s[:a] + '|' + s[i + 4:j] + '|' + s[b:]
        i = s.find('abs(')
    return s


def _mono(f):
    # 0 number, 1 constant (pi, sqrt(3)), 2 x^n, 3 other
    if isnum(f):
        return 0
    if not has_var(f):
        return 1
    if f[0] in LET and (len(f) == 1 or (f[1] == '^' and isnum(f[2:]))):
        return 2
    return 3


def _ord(s):
    # display a sum: per term, numbers then constants then x^n then
    # functions over a gathered denominator (1/e/2 -> 1/(2e))
    o = ''
    for t in split_terms(s):
        neg, b = sign_body(t)
        fs = split_top(b, '*')
        skip = '1' in fs[1:]
        for c in '=<>,':
            if c in b:
                skip = True
        if not skip:
            nu = []
            de = []
            for f in fs:
                q = split_top(f, '/')
                if q[0] != '1':
                    nu.append(q[0])
                de += q[1:]
            if len([f for f in nu if _mono(f) == 0]) > 1 or '' in nu + de:
                skip = True
        if not skip and (len(fs) > 1 or len(de) > 1):
            r = []
            for k in (0, 1, 2, 3):
                r += [f for f in nu if _mono(f) == k]
            d = [f for f in de if _mono(f) == 0] + [f for f in de if _mono(f) > 0]
            b = '*'.join(r) if r else '1'
            if d:
                b += '/' + (d[0] if len(d) == 1 else '(' + '*'.join(d) + ')')
        if o == '':
            o = ('-' if neg else '') + b
        else:
            o += ('-' if neg else '+') + b
    return o if o else s


def pp(s):
    s = _ord(str(s).replace('**', '^')).replace('exp(1)', 'e')
    for a, b in (('asin(', 'arcsin('), ('acos(', 'arccos('),
                 ('atan(', 'arctan('), ('log10(', 'log('), ('csc(', 'cosec(')):
        s = s.replace(a, b)
    s = _absbars(s)
    # exp(u) -> e^(u), exp(x) -> e^x
    i = s.find('exp(')
    while i >= 0 and (i == 0 or s[i - 1] not in LET):
        d = 0
        j = i + 3
        while j < len(s):
            if s[j] == '(':
                d += 1
            elif s[j] == ')':
                d -= 1
                if d == 0:
                    break
            j += 1
        inner = s[i + 4:j]
        simple = len(inner) > 0
        for c in inner:
            if c not in LET and c not in DIG:
                simple = False
        if simple:
            s = s[:i] + 'e^' + inner + s[j + 1:]
        else:
            s = s[:i] + 'e^(' + inner + ')' + s[j + 1:]
        i = s.find('exp(')
    o = ''
    n = len(s)
    i = 0
    while i < n:
        c = s[i]
        if c == '*' and 0 < i < n - 1:
            a = s[i - 1]
            b = s[i + 1]
            if a in DIG and (b in LET or b == '('):
                j = i - 1
                while j >= 0 and (s[j] in DIG or s[j] == '.'):
                    j -= 1
                if j < 0 or s[j] not in '^/':
                    i += 1
                    continue
                if s[j] == '^':
                    # x^2*y -> x^2 y
                    o += ' '
                    i += 1
                    continue
            if a == ')' and (b == '(' or b in LET):
                i += 1
                continue
            if a in LET and (b in LET or b == '('):
                # 3x*(x-2) -> 3x(x-2), x*e^x -> xe^x, x*sin(x) -> x sin(x)
                j = i - 1
                while j >= 0 and s[j] in LET:
                    j -= 1
                k = i + 1
                while k < n and s[k] in LET:
                    k += 1
                q = s[j] if j >= 0 else ''
                if q != '/':
                    wa = s[j + 1:i]
                    wb = s[i + 1:k]
                    u = CFG['uni']
                    if (q != '^' and (len(wa) == 1 or u and wa == 'pi')
                            and (b == '(' or len(wb) == 1 or u and wb == 'pi')):
                        i += 1
                        continue
                    o += ' '
                    i += 1
                    continue
            if CFG['uni'] and a in DIG + ')' and b in DIG:
                o += '×'
                i += 1
                continue
        o += c
        i += 1
    if CFG['uni']:
        o = o.replace('sqrt(', '√(').replace('pi', 'π')
    return o


def ps(s):
    # pretty a sum with spaced signs
    return join_signed([pp(t) for t in split_terms(str(s))])


def INT():
    return '∫' if CFG['uni'] else 'int '


def out(s=''):
    w = max(8, CFG['w'])  # guard: a tiny width would wrap forever
    line = str(s)
    while True:
        if CFG['pause'] and ST['ln'] >= CFG['pg']:
            input('-- more: [enter] --')
            ST['ln'] = 0
        if len(line) <= w:
            print(line)
            ST['ln'] += 1
            return
        # break after a space or operator in the right half of the line
        k = w
        for ch in (' ', '+-,=*'):
            j = w
            while j > w // 2 and line[j - 1] not in ch:
                j -= 1
            if j > w // 2:
                k = j
                break
        print(line[:k])
        ST['ln'] += 1
        line = '  ' + line[k:].lstrip(' ')


def hdr(t):
    # solver title with its jump code, e.g. == Differentiate [511] ==
    ST['ln'] = 0
    out('== ' + t + (' [' + ST['code'] + ']' if ST['code'] else '') + ' ==')


def wait():
    # any answer but 0 (including a KhiCAS pre-filled one) repeats the solver
    ST['again'] = input('[enter] = again, 0 = menu').strip() != '0'
    ST['ln'] = 0


def sf3(v, n=3):
    if v == 0:
        return '0'
    a = abs(v)
    e = int(math.floor(math.log(a) / math.log(10) + 1e-12))
    # rounding to (n-1-e) places can push a across a power of ten
    # (9.996 -> 10.0, not 10.00); bump the exponent so we keep n sig figs
    if round(a, n - 1 - e) >= 10 ** (e + 1):
        e += 1
    if a >= 1e6 or a < 1e-3:
        m = v / (10 ** e)
        return ('%.' + str(n - 1) + 'f') % m + ' x 10^' + str(e)
    d = n - 1 - e
    if d < 0:
        q = 10 ** (-d)
        return str(int(round(v / q)) * q)
    return ('%.' + str(d) + 'f') % v


def ans(lbl, r, approx=1):
    # final answer: exact, then 3 s.f. if not a plain rational;
    # strings with spaces are already formatted; decimals -> 3 s.f.
    r = str(r)
    t = pp(r)
    for i in range(1, len(r) - 1):
        if r[i] == ' ':
            t = ps(r)
            if r[i - 1] in LET and r[i + 1] in LET:
                t = r
                break
    if '.' in r and isnum(r):
        t = sf3(float(r))
        approx = 0
    out('ANS: ' + (lbl + ' = ' if lbl else '') + t)
    if approx and not isnum(r) and not has_var(r):
        # pretty strings ('(sqrt(3) - 1)i') need '*' back before Giac
        v = F(norm(r))
        if v is not None:
            out('     ~ ' + sf3(v))


def has_var(r):
    i = 0
    n = len(r)
    while i < n:
        if r[i] in LET:
            j = i
            while j < n and r[j] in LET:
                j += 1
            w = r[i:j]
            if w not in ('pi', 'e', 'sqrt', 'ln', 'exp', 'sin', 'cos', 'tan',
                         'asin', 'acos', 'atan', 'abs', 'log10', 'i', 'sec',
                         'csc', 'cot'):
                return True
            i = j
        else:
            i += 1
    return False


# ---------- input ----------
def ask(p, dft='', e=1):
    # e: 1 echo 'prompt: value', 0 no echo (menu/setting choices),
    # str: echo 'e = value' as a student writes it ('' = value alone)
    sep = ' ' if p[-1:] == '=' else ': '
    t = p + (' [' + dft + ']' if dft else '') + sep
    s = input(t).strip()
    # KhiCAS pre-fills input with the previous answer: an unedited repeated
    # expression on a prompt that allows blank/default counts as blank
    if s == '"':
        # ditto mark: repeat the previous answer
        s = ST.get('last', '')
    elif s == ST.get('last') and len(s) > 2 and (dft or 'blank' in p):
        s = ''
        out('(same=blank; type " to repeat)')
    if s:
        ST['last'] = s
    if ':=' in s or ';' in s:
        raise GErr('bad input')
    v = s if s else dft
    if v and e != 0:
        out(p + sep + v if e == 1 else (e + ' = ' + v if e else v))
    return v


def askx(p, dft='', e=1):
    return norm(ask(p, dft, e))


def askn(p, dft='', e=1):
    # exact numeric expression, e.g. 1/2, sqrt(3), pi/6
    return norm(ask(p, dft, e))


def askv(p, dft, e=1):
    # comma list -> list of normalised strings
    s = ask(p, dft, e).strip()
    if s[:1] in '([' and s[-1:] in ')]':
        s = s[1:-1]
    return [norm(a) for a in split_top(s, ',')]


def yes(p, dft='y', e=0):
    return ask(p + ' (y/n)', dft, e).lower()[:1] == 'y'


# ---------- menus ----------
RAW = (('invalid literal', 'enter a number'), ('could not convert', 'enter a number'),
       ('unpack', 'wrong number of values'), ('NoneType', 'values must be numbers'),
       ('not supported', 'values must be numbers'), ('index', 'missing value(s)'),
       ('iterable', 'missing value(s)'), ('empty', 'missing value(s)'))


def _msg(e):
    # plain-language text for raw Python errors; module messages kept
    m = str(e)
    for k, t in RAW:
        if k in m:
            return t
    if isinstance(e, ZeroDivisionError):
        return 'division by zero'
    if isinstance(e, (KeyError, TypeError)):
        return 'unexpected input'
    return m if m else type(e).__name__


def run(fn):
    reset()
    try:
        fn()
    except GErr as e:
        out('Giac error: ' + str(e))
        wait()
    except MemoryError:
        out('Out of memory: restart KhiCAS')
        wait()
    except Exception as e:
        if isinstance(e, ValueError) and 'nterrupt' in str(e):
            raise
        out('Error: ' + _msg(e))
        wait()


def go(items, k, code=''):
    # run solver k; [enter] at its end runs it again
    while True:
        ST['code'] = code + str(k + 1) if code else ''
        ST['again'] = 0
        run(items[k][1])
        if not ST['again']:
            ST['code'] = ''
            return


def menu(title, items, code=''):
    # items: [(label, fn), ...]; 0 = back; code = jump-code prefix
    while True:
        ST['ln'] = 0
        print('== ' + title + (' [' + code + ']' if code else '') + ' ==')
        for k in range(len(items)):
            print(str(k + 1) + ' ' + items[k][0])
        print('0 Back')
        c = input('Choice: ').strip()
        if c == '0' or c == '':
            return
        try:
            k = int(c) - 1
        except ValueError:
            continue
        if 0 <= k < len(items):
            go(items, k, code)
