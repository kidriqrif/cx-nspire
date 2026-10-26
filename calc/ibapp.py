# ibapp.py - tangents, f'(x)=k, optimisation, related rates (AA 5.4, 5.8, 5.14)
# stationary points / monotony / kinematics are in ibcurve.py
from ibcore import *

TITLE = 'Diff applications'
ALL = [[None, '-inf'], [None, 'inf']]


def _fl(r):
    # finite real float of exact r, else None
    x = F(r)
    if x is None or x != x or abs(x) > 1e300:
        return None
    return x


def _t(r):
    # tidy: exp(1) -> e, -1/2*sqrt(2) -> -sqrt(2)/2
    r = r.replace('exp(1)', 'e')
    k = r.find('*')
    j = r.find('/')
    if 0 < j < k and isnum(r[:k]) and '/' not in r[k:] and len(split_terms(r[k + 1:])) == 1:
        n = r[:j]
        r = (n[:-1] if n in ('1', '-1') else n + '*') + r[k + 1:] + r[j:k]
    return r


def _pf(r):
    # positive terms first, signs spaced: -1/e + 1 -> 1 - 1/e
    T = split_terms(r)
    P = [t for t in T if t[0] != '-']
    return join_signed(P + [t for t in T if t[0] == '-'] if r[:1] == '-' else T)


def _d(r):
    # display an exact value (3 s.f. if it is a float)
    if '.' in r:
        x = _fl(r)
        if x is not None:
            return sf3(x)
    return ps(_pf(_t(r)))


def _tk(e):
    T = []
    i = 0
    n = len(e)
    while i < n:
        j = i + 1
        if e[i] in LET:
            while j < n and e[j] in LET:
                j += 1
        T.append(e[i:j])
        i = j
    return T


def _rep(e, v, a):
    # e with v replaced by a, bracketed as a student does: 3(2)^2, 2^3, 5(10 - 2(5))
    pl = True
    for c in a:
        if c not in LET and c not in DIG and c != '.':
            pl = False
    T = _tk(e.replace(' ', ''))
    for k in range(len(T)):
        if T[k] == v:
            p = T[k - 1] if k else ''
            q = T[k + 1] if k + 1 < len(T) else ''
            n = T[k + 2] if k + 2 < len(T) else ''
            # bare in f(x), beside + - inside a bracket, or a plain value
            # that is not next to a number; else (a)
            if not (p + q == '()' or p in ('(', '') and q in ('+', '-', ')', '') or
                    pl and not (p == '*' and a[:1].isdigit() or q == '*' and n.isdigit())):
                T[k] = '(' + a + ')'
            else:
                T[k] = a
    return ''.join(T)


def _vars(e):
    T = _tk(e)
    vs = []
    for k in range(len(T)):
        w = T[k]
        if w[0] in LET and (k + 1 == len(T) or T[k + 1] != '(') and \
                w not in ('pi', 'e', 'i') and w not in vs:
            vs.append(w)
    return vs


def _getf(p, dv):
    # read f (no echo) and print it as given: f(x) = ..., or f = ... (2+ vars)
    f = norm(rhs(ask(p, '', 0)))
    vs = _vars(f)
    v = vs[0] if len(vs) == 1 else dv
    out(p[0] + ('(' + v + ')' if len(vs) < 2 else '') + ' = ' + ps(f))
    return f, v


def _eq(e):
    # equation as written: V = 4pi r^3/3
    k = e.find('=')
    return (ps(unwrap(e[:k])) + ' = ' if k >= 0 else '') + ps(e[k + 1:])


def _br(a):
    return '(' + a + ')' if len(split_terms(a)) > 1 else a


def _sub(e, v, a):
    return 'subst(' + e + ',' + v + '=(' + a + '))'


def _pm(r):
    # Giac leaves (4^(1/3))^2 outside its power: write 4^(2/3)
    if '^(1/' not in r:
        return r
    t = Gs('expand(' + r + ')') or r
    for _ in range(4):
        i = t.find('))^')
        j = t.rfind('(', 0, i)
        o = t.rfind('(', 0, j - 1)
        if i < 0 or o < 0 or t[j - 1] != '^' or t[j + 1:j + 3] != '1/' or (
                t[i + 3:i + 4] not in tuple('23456789')):
            break
        t = t[:o] + t[o + 1:j - 1] + '^(' + t[i + 3] + '/' + t[j + 3:i] + ')' + t[i + 4:]
    return t


def _ev(nm, e, v, a, q=0):
    # nm(a) = substitution = value; q: second derivative test
    r = _pm(S(_sub(e, v, a)))
    x = _fl(r)
    w = ps(_rep(e, v, _t(a)))
    d = _d(r) if x is not None else 'undefined'
    if q and x is not None:
        d += ' < 0, so max' if x < -1e-9 else (' > 0, so min' if x > 1e-9 else ', inconclusive')
    sh = w != _d(r) and '.' not in a and len(w) < 40
    out(nm + '(' + _d(a) + ') = ' + (w + (' = ' if x is not None else ' ') if sh else '') + d)
    return r


def _D(f, v):
    # derivative, tidiest of S(), expand(normal()) and regroup() (keeps (x+1)^2)
    d = 'diff(' + f + ',' + v + ')'
    r = S(d)
    b = Gs('expand(normal(' + d + '))')
    if b and len(b) <= len(r):
        r = b
    b = Gs('regroup(' + d + ')')
    return b if b and len(b) < len(r) else r


def _dv(f, v, nm):
    r = _D(f, v)
    out(nm + '(' + v + ') = ' + ps(r))
    return r


def _bd(s):
    s = s.strip()
    if s in ('inf', '-inf', '+inf'):
        return s.replace('+', '')
    return norm(s)


def _dom(f, v, p='Domain', dft=''):
    # read a,b; print it as a student states it: 0 <= x <= 5, x > 0
    s = ask(p + ' a,b (blank=all)', dft, 0).strip('[]() ')
    if not s:
        return ALL
    L = [_bd(a) for a in split_top(s, ',')]
    D = [[_fl(L[0]), L[0]], [_fl(L[1]), L[1]]]
    le = ' ≤ ' if CFG['uni'] else ' <= '
    o = [(le if _fl(_sub(f, v, L[k])) is not None else ' < ')
         if D[k][0] is not None else '' for k in (0, 1)]
    if o[0] and o[1]:
        out(_d(L[0]) + o[0] + v + o[1] + _d(L[1]))
    elif o[0]:
        out(v + o[0].replace('<', '>').replace('≤', '≥') + _d(L[0]))
    elif o[1]:
        out(v + o[1] + _d(L[1]))
    return D


def _in(x, dom, eps):
    return (dom[0][0] is None or x > dom[0][0] - eps) and \
        (dom[1][0] is None or x < dom[1][0] + eps)


def _roots(e, v, dom):
    # real roots of e=0 in dom -> sorted [[float, exact], ...]
    c = e + '=0'
    rg = ''
    for k in (0, 1):
        if dom[k][0] is not None:
            c += ' and ' + v + ('>=' if k == 0 else '<=') + dom[k][1]
    if dom[0][0] is not None and dom[1][0] is not None:
        rg = '=' + dom[0][1] + '..' + dom[1][1]
    L = parse_list(Gs('solve(' + c + ',' + v + ')'))
    if L == [''] or [r for r in L if bad(r)]:
        L = parse_list(Gs('fsolve(' + e + '=0,' + v + rg + ')'))
    P = []
    for r in L:
        x = _fl(r)
        if x is not None and _in(x, dom, 1e-9):
            if '.' in r and abs(x) < 1e-9:
                r = '0'
                x = 0.0
            if '.' in r or _fl(_sub(e, v, r)) is not None:
                P.append([x, r])
    P.sort(key=lambda p: p[0])
    Q = []
    for p in P:
        if not Q or p[0] - Q[-1][0] > 1e-9:
            Q.append(p)
    return Q


def _ne():
    return ' ≠ ' if CFG['uni'] else ' != '


def _lst(P, v):
    if not P:
        return 'no real solution'
    s = v + ' = ' + ', '.join([_d(p[1]) for p in P])
    return s + (' (GDC)' if [p for p in P if '.' in p[1]] else '')


def _solve0(e, v, dom, nm='', pv=''):
    # working for e = 0 (nm: what e is called; pv: line just printed); returns roots
    if e == '0':
        out(' true for all ' + v)
        return []
    if isnum(e):
        out(' ' + (nm + ' = ' if nm else '') + _d(e) + _ne() + '0')
        return []
    nu = e
    if has(Gs('denom(' + e + ')'), v):
        nu = G('numer(' + e + ')')
        if isnum(nu):
            # constant numerator: never zero
            out(' ' + (nm or ps(e)) + _ne() + '0')
            return []
    if ps(nu) + ' = 0' != pv:
        out(' ' + ps(nu) + ' = 0')
    fa = Gs('factor(' + nu + ')')
    if fa != nu and (')*' in fa or '*(' in fa) and '/' not in fa and len(split_terms(fa)) == 1:
        out(' ' + pp(fa) + ' = 0')
    P = _roots(e, v, dom)
    Q = _roots(e, v, ALL) if not P and dom != ALL else []
    out(' ' + _lst(Q or P, v) + (' not in domain' if Q else ''))
    return P


def _ptans(lbl, x, y):
    out('ANS: ' + lbl + ' (' + _d(x) + ', ' + _d(y) + ')')
    if not (isnum(x) and isnum(y)) and '.' not in x + y:
        a = _fl(x)
        b = _fl(y)
        if a is not None and b is not None:
            out('     ~ (' + (x if isnum(x) and '/' not in x else sf3(a)) + ', ' +
                (y if isnum(y) and '/' not in y else sf3(b)) + ')')


def _mn(v, c):
    # 'v - c' with tidy sign
    if c == '0':
        return v
    if len(split_terms(c)) > 1:
        return v + ' - (' + pp(c) + ')'
    if c[0] == '-':
        return v + ' + ' + pp(c[1:])
    return v + ' - ' + pp(c)


def _line(m, a, y1, nm):
    # point-gradient form, then y = mx + c
    ms = _d(m)
    if '/' in m or len(split_terms(m)) > 1:
        ms = '(' + ms + ')'
    ms = '' if m == '1' else ('-' if m == '-1' else ms)
    w = _mn('x', a)
    out(_mn('y', y1) + ' = ' + ms + (w if w == 'x' else '(' + w + ')'))
    ans(nm + ': y', join_signed([ps(_t(S('(' + m + ')*x'))), ps(_t(
        G('expand((' + y1 + ')-(' + m + ')*(' + a + '))')))]))


def tangent():
    hdr('Tangent & normal')
    f = _getf('f(x) =', 'x')[0]
    a = askn('At x =', '', 0)
    y1 = _ev('y1 = f', f, 'x', a)
    if _fl(y1) is None:
        wait()
        return
    fp = _dv(f, 'x', "f'")
    m = _ev("m = f'", fp, 'x', a)
    mf = _fl(m)
    if mf is None:
        out('vertical tangent')
        ans('tangent: x', a)
        ans('normal: y', _t(y1))
    elif mf == 0:
        ans('tangent: y', _t(y1))
        out('normal is vertical')
        ans('normal: x', a)
    else:
        _line(m, a, y1, 'tangent')
        n = S('-1/(' + m + ')')
        out('normal gradient = -1/m = ' + _d(n))
        _line(n, a, y1, 'normal')
    wait()


def gradk():
    hdr("Solve f'(x) = k")
    f = _getf('f(x) =', 'x')[0]
    k = norm(ask('k (or line y=mx+c)', '', 0))
    if has(k, 'x'):
        k = S('diff(' + rhs(k) + ',x)')
        out('line gradient = ' + pp(k))
    dom = _dom(f, 'x')
    fp = _dv(f, 'x', "f'")
    ln = ps(fp) + ' = ' + pp(k)
    e = N('(' + fp + ')-(' + k + ')')
    if isnum(e):
        out(ps(fp) + (' = ' if e == '0' else _ne()) + pp(k) + (' for all x' if e == '0' else ', no solution'))
        wait()
        return
    out(ln)
    P = _solve0(e, 'x', dom, '', ln)
    for p in P:
        _ptans('point', p[1], _ev(' f', f, 'x', p[1]))
    wait()


def _endv(f, v, b, k):
    # value (or one-sided limit) of f at end b; k=0 left end
    r = Gs(_sub(f, v, b))
    if _fl(r) is not None:
        r = _ev('f', f, v, b)
        return r, _fl(r), 0
    r = G('limit(' + f + ',' + v + ',' + b +
          ('' if 'inf' in b else (',1' if k == 0 else ',-1')) + ')')
    t = v + ' -> ' + _d(b) + ': f -> ' + pp(r)
    out(t.replace(' -> ', ' → ').replace('infinity', '∞').replace('inf', '∞') if CFG['uni'] else t)
    x = _fl(r)
    if 'inf' in r:
        x = -1e301 if r[0] == '-' else 1e301
    return r, x, 1


def optim():
    hdr('Optimisation')
    f, v = _getf('f(x) =', 'x')
    c = ask('Constraint (blank=none)', '', 0)
    if c:
        c = norm(c)
        out(_eq(c))
        w = ask('Eliminate', 'y', 0)
        s = [r for r in GL('solve(' + lhs0(c) + ',' + w + ')')
             if not (_fl(r) is not None and _fl(r) < 0)]
        s.sort(key=lambda r: r[0] == '-')
        out(w + ' = ' + pp(s[0]))
        out('f = ' + ps(_rep(f, w, s[0])))
        sb = 'subst(' + f + ',' + w + '=(' + s[0] + '))'
        f = G('expand(normal(' + sb + '))')
        b = S(sb)
        if len(b) < len(f):
            f = b
        vs = _vars(f)
        v = vs[0] if len(vs) == 1 else 'x'
        out('f(' + v + ') = ' + ps(f))
    dom = _dom(f, v, 'Interval')
    fp = _dv(f, v, "f'")
    f2 = _D(fp, v)
    out("f'(" + v + ') = 0:')
    C = []
    P = [p for p in _solve0(fp, v, dom, "f'(" + v + ')') if _in(p[0], dom, -1e-9)]
    if P:
        out("f''(" + v + ') = ' + ps(f2))
    for p in P:
        y = _ev('f', f, v, p[1])
        _ev("f''", f2, v, p[1], 1)
        C.append([_fl(y), y, p[1], 0])
    for k in (0, 1):
        r, x, lim = _endv(f, v, dom[k][1], k)
        if x is not None:
            C.append([x, r, dom[k][1], lim])
    for k in (1, -1):
        nm = 'max' if k > 0 else 'min'
        C = [q for q in C if q[0] is not None]
        if not C:
            break
        b = C[0]
        for q in C:
            if q[0] * k > b[0] * k:
                b = q
        X = [q for q in C if abs(q[0] - b[0]) < 1e-9 and not q[3]]
        if not X:
            out(nm + ': none (not attained)')
        else:
            ans(nm + ' f', _t(b[1]))
            out('     at ' + v + ' = ' + ', '.join([_d(q[2]) for q in X]))
    wait()


def _dt(c, d):
    # c times d as written: 2x dx/dt, (x + y)dy/dt, 2x(3)
    if c in ('1', '-1'):
        return c[:-1] + d
    if len(split_terms(c)) > 1 or '/' in c:
        return '(' + ps(c) + ')' + d
    return pp(c) + (' ' if d[0] in LET else '') + d


def rates():
    hdr('Related rates')
    e = norm(ask('Relation (e.g. V=4/3pi r^3)', '', 0))
    out(_eq(e))
    vs = _vars(e)
    if len(vs) > 2:
        z = norm(ask('Substitute (e.g. h=2r)', '', 0))
        out(_eq(z))
        e = G('subst(' + e + ',' + z + ')')
        e = e[:e.find('=') + 1] + S(rhs(e))
        out(_eq(e))
        vs = _vars(e)
    p = ask('Known rate d?/dt for', vs[-1], 0)
    q = [w for w in vs if w != p][0]
    rp = askn('d' + p + '/dt =')
    W = norm(ask('When (e.g. ' + vs[-1] + '=3)', '', 0)).split('=')
    if len(W) < 2:
        W = [p] + W
    out(W[0] + ' = ' + _d(W[1]))
    k = e.find('=')
    L = e[:k]
    dp = 'd' + p + '/dt'
    dq = 'd' + q + '/dt'
    r = '(' + pp(rp) + ')'
    if L in vs and not has(e[k + 1:], L):
        x = q if L == p else p
        gd = _D(e[k + 1:], x)
        dx = 'd' + x + '/dt'
        out('d' + L + '/d' + x + ' = ' + ps(gd))
        if 'x' in (L, x) and not CFG['uni']:
            ch = 'd' + L + '/dt = (d' + L + '/d' + x + ')(' + dx + ')'
        else:
            ch = 'd' + L + '/dt = d' + L + '/d' + x + (' × ' if CFG['uni'] else ' x ') + dx
        if p == x:
            res = '(' + gd + ')*(' + rp + ')'
            out(ch + ' = ' + _dt(gd, r) + ' = ' + ps(S(res)))
        else:
            out(ch)
            out(pp(rp) + ' = ' + _dt(gd, dx))
            res = '(' + rp + ')/(' + gd + ')'
            out(dq + ' = ' + pp(S(res)))
    else:
        Fe = lhs0(e)
        a = _D(Fe, p)
        b = _D(Fe, q)
        out(join_signed([_dt(a, dp), _dt(b, dq)]) + ' = 0')
        out(join_signed([_dt(a, r), _dt(b, dq)]) + ' = 0')
        res = '-(' + a + ')*(' + rp + ')/(' + b + ')'
        out(dq + ' = ' + pp(S(res)))
    rs = S(res)
    X = [W]
    o = [w for w in vs if w != W[0]][0]
    if has(rs, o):
        c = G(_sub(lhs0(e), W[0], W[1]))
        out(_eq(_rep(e, W[0], W[1])))
        s = GL('solve(' + c + ',' + o + ')')
        s = [r for r in s if _fl(r) is not None and _fl(r) >= 0] or s
        if not s:
            out('no real ' + o + ' when ' + W[0] + ' = ' + _d(W[1]))
            wait()
            return
        out(o + ' = ' + _d(s[0]))
        X.append([o, s[0]])
    w = rs
    for z in X:
        w = _rep(w, z[0], z[1])
        rs = _sub(rs, z[0], z[1])
    A = _t(N(rs))
    if pp(w) != pp(A):
        out(dq + ' = ' + pp(w))
    ans(dq, A)
    wait()


ITEMS = [('Tangent & normal', tangent), ("Solve f'(x)=k", gradk),
         ('Optimisation', optim), ('Related rates', rates)]
