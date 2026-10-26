# ibfun3.py - polynomial/rational inequalities with sign table, modulus
# equations and inequalities (AA 2.15, 2.16)
from ibcore import *

TITLE = 'Inequalities'


def _pf(s):
    # pretty a product a*(..)*(..)^n with spaced sums
    ng, fs = split_factors(s)
    o = '-' if ng else ''
    for op, f in fs:
        e = ''
        k = f.rfind('^')
        if k > 0 and f[k - 1] == ')':
            e = f[k:]
            f = f[:k]
        f = unwrap(f)
        t = ps(f)
        if (len(split_terms(f)) > 1 or e and f != 'x') and (len(fs) > 1 or ng or e) or op == '/' and o:
            t = '(' + t + ')'
        o += ('/' if op == '/' else '') + t + e
    return o


def _zs(e):
    # real zeros of e (exact, else numeric GDC), sorted
    r = GL('solve(' + e + '=0,x)')
    for t in r:
        if bad(t):
            r = GL('fsolve(' + e + '=0,x)')
            out('(GDC for zeros of ' + ps(e) + ')')
            break
    r.sort(key=lambda t: F(t))
    return r


def _dn(s):
    # zeros of every denominator in s before cancelling (holes stay excluded)
    z = []
    for t in split_terms(s):
        for o, u in split_factors(t)[1]:
            if o == '/' and has(u):
                z += [c for c in _zs(u) if c not in z]
    return z


def _rel(s):
    s = s.replace('≤', '<=').replace('≥', '>=')
    for o in ('<=', '>=', '<', '>', '='):
        k = s.find(o)
        if k > 0:
            return norm(s[:k]), o, norm(s[k + len(o):])
    return norm(s), '=', '0'


def _d(t):
    # display a value: exact, or 3 s.f. if decimal
    return sf3(F(t)) if '.' in t else pp(t)


def _lst(r):
    return ', '.join([_d(t) for t in r])


def _iv(lo, hi, a, b):
    # (inequality text, interval text)
    inf = '∞' if CFG['uni'] else 'inf'
    le = ' <= ' if a else ' < '
    re = ' <= ' if b else ' < '
    if lo is None and hi is None:
        return 'all real x', ']-' + inf + ', ' + inf + '['
    if hi is None:
        return 'x' + le.replace('<', '>') + _d(lo), ('[' if a else ']') + _d(lo) + ', ' + inf + '['
    h = _d(hi) + (']' if b else '[')
    if lo is None:
        return 'x' + re + _d(hi), ']-' + inf + ', ' + h
    if lo == hi:
        return 'x = ' + _d(lo), '{' + _d(lo) + '}'
    return _d(lo) + le + 'x' + re + _d(hi), ('[' if a else ']') + _d(lo) + ', ' + h


def _z0(h, t):
    # h(t) = 0 (numerically)
    v = F('subst(' + h + ',x=' + str(t) + ')')
    return v is not None and abs(v) < 1e-9


def _tab(h, cs, op, dz, lb=''):
    # sign table of h over critical values cs; prints solution of h op 0
    # (lb: how h is displayed, e.g. factorised)
    n = len(cs)
    fv = [F(c) for c in cs]
    sq = []
    if op != '=':
        out('Sign of ' + (lb or ps(h)) + ':')
    for j in range(n + 1):
        if n == 0:
            t = 0.0
            rg = 'all x'
        elif j == 0:
            t = fv[0] - 1
            rg = 'x < ' + _d(cs[0])
        elif j == n:
            t = fv[-1] + 1
            rg = 'x > ' + _d(cs[-1])
        else:
            t = (fv[j - 1] + fv[j]) / 2
            rg = _d(cs[j - 1]) + ' < x < ' + _d(cs[j])
        v = F('subst(' + h + ',x=' + str(t) + ')') or 0
        z = _z0(h, t)
        if op != '=':
            out(' ' + rg + ': ' + ('0' if z else '+' if v > 0 else '-'))
        sq.append('=' in op if z else op != '=' and v != 0 and (v > 0) == (op[0] == '>'))
        if j < n:
            sq.append(cs[j] not in dz and (len(op) == 2 or op == '=' and _z0(h, cs[j])))
    m = len(sq)
    A = []
    B = []
    i = 0
    for it in range(m):
        if i >= m:
            break
        if not sq[i]:
            i += 1
            continue
        j = i
        while j + 1 < m and sq[j + 1]:
            j += 1
        lo = None if i == 0 else cs[(i - 1) // 2 if i % 2 else i // 2 - 1]
        hi = None if j == m - 1 else cs[(j - 1) // 2 if j % 2 else j // 2]
        a, b = _iv(lo, hi, i % 2, j % 2)
        A.append(a)
        B.append(b)
        i = j + 1
    out('ANS: ' + (' or '.join(A) if A else 'no solution'))
    if B:
        out('     x in ' + (' ∪ ' if CFG['uni'] else ' U ').join(B))


def _pl(s, w):
    # print working line s unless it repeats the previous one (w = [previous])
    if s.replace(' ', '') != w[0].replace(' ', ''):
        out(s)
    w[0] = s


def ineq():
    hdr('Inequality')
    L, op, R = _rel(ask('Inequality', '', 0))
    h = N('(' + L + ')-(' + R + ')')
    nu = G('numer(' + h + ')')
    de = G('denom(' + h + ')')
    if op == '=' or G('is_polynomial(' + nu + ',x)') != 'true' or \
            G('is_polynomial(' + de + ',x)') != 'true' or GL('lname(' + h + ')') != ['x']:
        out('Polynomial/rational in x with <, > only')
        wait()
        return
    fn = _pf(G('factor(' + nu + ')'))
    dz = _dn(L) + _dn(R)
    w = ['']
    lb = fn
    _pl(ps(L) + ' ' + op + ' ' + ps(R), w)
    if de == '1' and not dz:
        if R != '0':
            _pl(ps(h) + ' ' + op + ' 0', w)
        _pl(fn + ' ' + op + ' 0', w)
        dz = []
    else:
        if R != '0':
            _pl(ps(G('(' + L + ')-(' + R + ')')) + ' ' + op + ' 0', w)
        if de != '1' and (len(split_terms(fn)) > 1 or '*' in fn or '/' in fn):
            fn = '(' + fn + ')'
        fd = _pf(G('factor(' + de + ')'))
        if len(split_terms(fd)) > 1 or '*' in fd or ')(' in fd:
            fd = '(' + fd + ')'
        lb = fn + ('/' + fd if de != '1' else '')
        _pl(lb + ' ' + op + ' 0', w)
        dz += [c for c in _zs(de) if c not in dz]
        dz.sort(key=lambda t: F(t))
        out('x != ' + _lst(dz))
    cs = [c for c in _zs(nu) if c not in dz]
    out('Critical values: ' + ('x = ' + _lst(cs) if cs else 'none'))
    cs += dz
    cs.sort(key=lambda t: F(t))
    _tab(h, cs, op, dz, lb)
    wait()


def _ab(s, sg=None):
    # abs(...) arguments of s; with signs sg, replace abs(u) by (+-(u))
    a = []
    o = ''
    i = 0
    for it in range(len(s)):
        k = s.find('abs(', i)
        if k < 0:
            break
        d = 0
        j = k + 3
        for j in range(k + 3, len(s)):
            if s[j] == '(':
                d += 1
            elif s[j] == ')':
                d -= 1
                if d == 0:
                    break
        u = s[k + 4:j]
        if sg:
            o += s[i:k] + '(' + ('-' if sg[len(a)] < 0 else '') + '(' + u + '))'
        a.append(u)
        i = j + 1
    return a if sg is None else o + s[i:]


def _neg(R):
    # display -(R)
    return pp(N('-(' + R + ')')) if len(split_terms(R)) < 2 else '-(' + ps(R) + ')'


def modeq():
    hdr('Modulus eq/ineq')
    L, op, R = _rel(ask('Eq/ineq', '', ''))
    if 'abs(' not in L + R:
        out('No |..| found')
        wait()
        return
    if 'abs(' in R and 'abs(' not in L:
        L, R = R, L
        op = {'<': '>', '>': '<', '<=': '>=', '>=': '<='}.get(op, op)
    aL = _ab(L)
    aR = _ab(R)
    one = len(aL) == 1 and L == 'abs(' + aL[0] + ')'
    rs = []
    idn = 0
    dz = []
    for u in [L, R] + aL + aR:
        dz += [c for c in _dn(u) if c not in dz]
    e = N('(' + aL[0] + ')^2-(' + (aR + ['0'])[0] + ')^2')
    if one and len(aR) == 1 and R == 'abs(' + aR[0] + ')' and e != '0':
        f, g = aL[0], aR[0]
        out('(square both sides)')
        q = [(u if len(u) < 2 else '(' + ps(u) + ')') + '^2' for u in (f, g)]
        out(q[0] + ' ' + op + ' ' + q[1])
        out(ps(e) + ' ' + op + ' 0')
        e2 = _pf(G('factor(' + e + ')'))
        if e2 != ps(e):
            out(e2 + ' ' + op + ' 0')
        rs = _zs(e)
    elif one and not aR and N(aL[0] + '-(' + R + ')') != '0' and N(aL[0] + '+' + R) != '0':
        f = aL[0]
        for k in (1, -1):
            r = _zs('(' + f + ')-(' + (R if k > 0 else '-(' + R + ')') + ')')
            t = ps(f) + ' = ' + (ps(R) if k > 0 else _neg(R))
            s = 'x = ' + _lst(r) if r else 'no solution'
            out(t if t == s else t + ' => ' + s)
            rs += [t for t in r if t not in rs]
    else:
        a = aL + aR
        cs = []
        for u in a:
            cs += [t for t in _zs(u) if t not in cs]
        cs.sort(key=lambda t: F(t))
        fv = [F(c) for c in cs]
        e = '(' + L + ')-(' + R + ')'
        for j in range(len(cs) + 1):
            lo = fv[j - 1] if j else -1e300
            hi = fv[j] if j < len(cs) else 1e300
            t = (lo + hi) / 2 if 0 < j < len(cs) else (0 if not cs else (hi - 1 if j == 0 else lo + 1))
            sg = [F('subst(' + u + ',x=' + str(t) + ')') for u in a]
            w = N(_ab(e, sg))
            r = [z for z in _zs(w) if lo - 1e-9 <= F(z) <= hi + 1e-9] if has(w) else []
            if w == '0':
                idn = 1
            out(('x < ' + _d(cs[0]) if j == 0 and cs else (_d(cs[j - 1]) + ' <= x' if j else 'all x') +
                 (' < ' + _d(cs[j]) if j and j < len(cs) else '')) + ': ' + ps(w) + ' = 0' +
                (' => x = ' + _lst(r) if r else ' (all x)' if idn and w == '0' else ' no sol'))
            rs += [z for z in r if z not in rs]
    ok = []
    for r in rs:
        a = S('subst(' + L + ',x=' + r + ')')
        b = S('subst(' + R + ',x=' + r + ')')
        v = F(a)
        w = F(b)
        v = v is not None and w is not None and abs(v - w) < 1e-6 * (1 + abs(v))
        if v:
            ok.append(r)
        else:
            out('x = ' + _d(r) + ': LHS = ' + _d(a) + ', RHS = ' + _d(b) + ' reject')
    ok.sort(key=lambda t: F(t))
    h = G('(' + L + ')-(' + R + ')')
    if dz:
        out('x != ' + _lst(dz))
    if op == '=' and not idn:
        out('ANS: ' + ('x = ' + _lst(ok) if ok else 'no solution'))
    else:
        if op != '=':
            out('Critical values: ' + ('x = ' + _lst(ok) if ok else 'none'))
        else:
            ok += [c for c in cs if c not in ok]
        ok += [c for c in dz if c not in ok]
        ok.sort(key=lambda t: F(t))
        _tab(h, ok, op, dz)
    wait()


ITEMS = [('Inequality', ineq), ('Modulus eq/ineq', modeq)]
