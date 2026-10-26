# ibrv.py - discrete and continuous random variables (AA 4.7, AHL 4.14)
from ibcore import *

TITLE = 'Random variables'
_M = {'d': 0, 'g': 0}
KN = ('x', 'pi', 'e', 'sqrt', 'ln', 'exp', 'abs', 'sin', 'cos', 'tan', 'asin',
      'acos', 'atan', 'log10', 'inf', 'sec', 'csc', 'cot')


def _q(s):
    # decimal literals -> exact fractions: 0.35 -> (35/100)
    o = ''
    i = 0
    n = len(s)
    while i < n:
        j = i
        while j < n and (s[j] in DIG or s[j] == '.'):
            j += 1
        if j == i:
            o += s[i]
            i += 1
            continue
        t = s[i:j]
        if '.' in t and (i == 0 or s[i - 1] not in LET):
            a = t.split('.')
            t = '(' + str(int(a[0] + a[1] or '0')) + '/1' + '0' * len(a[1]) + ')'
            _M['d'] = 1
        o += t
        i = j
    return o


def _n(s):
    # kx(4-x): norm() would read 'kx(' as a function call
    o = ''
    for c in rhs(s):
        if c == '(' and o and o[-1] in 'abkmqxyz':
            o += '*'
        o += c
    return _q(norm(o))


def _e(s):
    s = _n(s)
    return S(s) if s else ''


def _s3(v):
    return sf3(float('%.2e' % v))


def _f(r):
    # display value: exact (decimal if inputs were decimals) + 3 s.f.
    r = str(r)
    s = pp(r)
    v = F(r)
    if v is None or has_var(r):
        return s
    t = _s3(v)
    if '.' in r:
        return t
    if isnum(r):
        if '/' not in r:
            return s
        q = int(r.split('/')[1])
        for k in range(80):
            if q % 2 == 0:
                q //= 2
            elif q % 5 == 0:
                q //= 5
        if q == 1:
            if not _M['d']:
                return s
            d = G('evalf(' + r + ')')
            if len(d) < 10 and 'e' not in d:
                return d
    return s + ' (' + t + ')' if len(s) < 18 else t


def _g(r):
    return _f(r).split(' (')[0]


def _A(lbl, r):
    out('ANS: ' + lbl + ' = ' + _f(r))


def _c(r):
    # exact if a plain number, otherwise 3 s.f. only
    s = _g(r)
    return s if isnum(s) and '/' not in s else _s3(F(r))


def _k(s):
    return s if s.isdigit() else '(' + s + ')'


def _unk(L):
    u = []
    for s in L:
        i = 0
        n = len(s)
        while i < n:
            if s[i] in LET:
                j = i
                while j < n and s[j] in LET:
                    j += 1
                w = s[i:j]
                if w not in KN and w not in u:
                    u.append(w)
                i = j
            else:
                i += 1
    return u


def _xl(xs, pv):
    return ' + '.join([_p(xs[j]) + '(' + _g(pv[j]) + ')' for j in range(len(xs)) if xs[j] != '0']) or '0'


def _p(x):
    x = _g(x)
    return '(' + x + ')' if x[0] == '-' else x


def _solve(eqs, U, chk):
    # solve system; keep solutions where chk(dict) is True -> dict or None
    r = GL('solve([' + ','.join(eqs) + '],[' + ','.join(U) + '])')
    g = None
    for z in r:
        z = parse_list(z)
        if len(z) != len(U) or bad(''.join(z)):
            continue
        d = {}
        for j in range(len(U)):
            d[U[j]] = z[j]
        if chk(d):
            g = g or d
        else:
            out(', '.join([U[j] + ' = ' + _g(z[j]) for j in range(len(U))]) + ' rejected')
    return g


def _sb(e, d):
    for k in d:
        e = G('subst(' + e + ',' + k + '=' + d[k] + ')')
    return _ne(S(e))


# ---------- discrete ----------
def discrete_rv():
    hdr('Discrete RV')
    _M['d'] = 0
    fm = ask('Form 1=table 2=P(X=x)=f(x)', '1', 0)
    xs = [_e(a) for a in askv('x values', '', 0)]
    if fm == '2':
        f = _n(ask('P(X=x) =', '', 0))
        out('P(X=x) = ' + pp(f))
        pv = []
        for x in xs:
            pv.append(S('subst(' + f + ',x=' + x + ')'))
            out('P(X=' + _g(x) + ') = ' + _g(pv[-1]))
    else:
        pv = [_e(a) for a in askv('P values (may use k)', '', 0)]
    n = len(xs)
    if n != len(pv) or n < 1 or n > 12:
        out('Error: list lengths (<=12)')
        wait()
        return
    ex = ask('Extra 1=E(X) given 2=fair game 0=none', '0', 0)
    U = _unk(xs + pv)
    if len(U) > 2:
        out('Too many unknowns')
        wait()
        return
    xp = ['(' + xs[j] + ')*(' + pv[j] + ')' for j in range(n)]
    xl = _xl(xs, pv)
    eqs = []
    if U:
        if _unk(pv):
            sm = N('+'.join(['(' + p + ')' for p in pv]))
            out(' + '.join([_g(p) for p in pv]) + ' = 1')
            if len(split_terms(sm)) != n:
                out(ps(sm) + ' = 1')
            eqs.append(sm + '=1')
        if ex in ('1', '2'):
            v = '0' if ex == '2' else _e(ask('E(X) =', '', 0))
            out('E(X) = ' + _g(v))
            out(xl + ' = ' + _g(v))
            eqs.append(N('+'.join(xp)) + '=' + v)
        if len(eqs) < len(U):
            out('Need another condition (E(X))')
            wait()
            return

        def ok(d):
            for p in pv:
                w = F(_sb(p, d))
                if w is None or w < -1e-12 or w > 1 + 1e-12:
                    return False
            return True
        d = _solve(eqs, U, ok)
        if d is None:
            out('No valid solution')
            wait()
            return
        for k in U:
            _A(k, d[k])
        xs = [_sb(x, d) for x in xs]
        pv = [_sb(p, d) for p in pv]
        xp = ['(' + xs[j] + ')*(' + pv[j] + ')' for j in range(n)]
        xl = _xl(xs, pv)
    out('x : ' + '  '.join([_g(x) for x in xs]))
    out('P : ' + '  '.join([_g(p) for p in pv]))
    if G('simplify(' + '+'.join(['(' + p + ')' for p in pv]) + '-1)') != '0':
        out('Warning: sum of P is not 1')
    E = S('+'.join(xp))
    out('E(X) = ' + xl)
    out('  = ' + _f(E))
    E2 = S('+'.join(['(' + xs[j] + ')^2*(' + pv[j] + ')' for j in range(n)]))
    out('E(X^2) = ' + (' + '.join([_g(S('(' + xs[j] + ')^2')) + '(' + _g(pv[j]) + ')' for j in range(n) if xs[j] != '0']) or '0'))
    out('  = ' + _f(E2))
    V = S(E2 + '-(' + E + ')^2')
    out('Var(X) = ' + _g(E2) + ' - ' + _k(_g(E)) + '^2 = ' + _f(V))
    out('sd = ' + pp('sqrt(' + _g(V) + ')') + ' = ' + _c(S('sqrt(' + V + ')')))
    q = ask('Query e.g. X>=2 (blank skip)', '', 0).replace(' ', '').upper()
    if q:
        op = ''
        for o in ('>=', '<=', '>', '<', '='):
            if o in q:
                op = o
                break
        c = F(_q(q.split(op)[1]))
        sel = []
        for j in range(n):
            w = F(xs[j])
            if (op == '>=' and w >= c) or (op == '<=' and w <= c) or (op == '>' and w > c) or (op == '<' and w < c) or (op == '=' and w == c):
                sel.append(j)
        pq = S('+'.join(['(' + pv[j] + ')' for j in sel]) if sel else '0')
        lb = 'P(' + q + ')'
        if len(sel) > 1:
            out(lb + ' = ' + ' + '.join(['P(X=' + _g(xs[j]) + ')' for j in sel]))
            out('  = ' + ' + '.join([_g(pv[j]) for j in sel]))
        _A(lb, pq)
    ab = askv('a,b for aX+b (blank skip)', '', 0)
    if ab[0]:
        _ab([_e(z) for z in ab], E, V)
    _A('E(X)', E)
    _A('Var(X)', V)
    wait()


def _ab(ab, E, V):
    a, b = (ab + ['0'])[:2]
    Ea = S('(' + a + ')*(' + E + ')+(' + b + ')')
    Va = S('(' + a + ')^2*(' + V + ')')
    out('E(aX+b) = aE(X) + b = ' + join_signed([_g(E) if _g(a) == '1' else _g(a) + '(' + _g(E) + ')', _g(b)]))
    _A('E(aX+b)', Ea)
    out('Var(aX+b) = a^2 Var(X) = ' + _k(_g(a)) + '^2(' + _g(V) + ')')
    _A('Var(aX+b)', Va)


# ---------- continuous ----------
def _br(e):
    return '(' + pp(e) + ')' if len(split_terms(e)) > 1 else pp(e)


def _bp(e):
    # x outside a function call that is present -> by parts (substitution if
    # the argument is not linear)
    o = ''
    d = 0
    a = ''
    for j in range(len(e)):
        c = e[j]
        if c == '(' and (d or (j and e[j - 1] in LET and e[j - 4:j] != 'sqrt' and e[j - 3:j] != 'abs')):
            d += 1
        elif c == ')' and d:
            d -= 1
        elif not d:
            o += c
        if d:
            a += c
    if o == e or not has(o, 'x'):
        return ''
    return ' (substitution)' if '^' in a else ' (by parts)'


def _xx(e):
    # a term with a bare x twice (x*2*x/e^(x^2)): normal() merges them
    for t in split_terms(e):
        d = 0
        c = 0
        for i in range(len(t)):
            d += 1 if t[i] == '(' else (-1 if t[i] == ')' else 0)
            if d == 0 and t[i] == 'x' and (i == 0 or t[i - 1] not in LET) and (i + 1 == len(t) or (t[i + 1] not in LET and t[i + 1] != '^')):
                c += 1
        if c > 1:
            return 1
    return 0


def _ev(E, nm):
    # prints '= value' unless the GDC line already gave it; 0 if it does not exist
    if F(E) is None or abs(F(E)) > 1e300:
        out(nm + ' does not exist')
        return 0
    if not _M['g']:
        out('  = ' + _f(E))
    return 1


def _fv(s):
    return 1e300 if s == 'inf' else (-1e300 if s == '-inf' else F(s))


def _at(F_, b):
    if b == 'inf':
        return G('limit(' + F_ + ',x,inf)')
    if b == '-inf':
        return G('limit(' + F_ + ',x,-inf)')
    return S('subst(' + F_ + ',x=' + b + ')')


def _bd(s):
    # a limit as displayed
    if s[-3:] == 'inf':
        return ('-' if s[0] == '-' else '') + ('∞' if CFG['uni'] else 'inf')
    return _g(s)


def _dm(lo, hi):
    u = CFG['uni']
    if hi == 'inf':
        return 'x' + ('≥' if u else '>=') + _g(lo)
    return _g(lo) + ('≤' if u else '<=') + 'x' + ('≤' if u else '<=') + _g(hi)


def _il(lo, hi, e):
    return INT() + '_' + _bd(lo) + '^' + _bd(hi) + ' ' + e + ' dx'


def _sx(e, v):
    # pretty e with x replaced by v: 3x^4 -> 3(2)^4, x^3/27 -> 2^3/27, sin(x) -> sin(2)
    o = ''
    n = len(e)
    for i in range(n):
        a = e[i - 1] if i else '@'
        b = e[i + 1] if i + 1 < n else '@'
        if e[i] == 'x' and a not in LET and (b not in LET or (b == 'e' and e[i + 2:i + 3] == '^')):
            if a in '@(' and b in '@)+-':
                o += v
            elif not v.isalnum() or (a in DIG + ')' and v[0] in DIG):
                o += '(' + v + ')'
            else:
                o += v
        else:
            o += e[i]
    return o


def _sv(B, v):
    # B at x = v as a student writes it, signs spaced
    e = _sx(pp(B), v)
    o = ''
    d = 0
    for i in range(len(e)):
        c = e[i]
        d += 1 if c in OPN else (-1 if c in CLS else 0)
        o += ' ' + c + ' ' if c in '+-' and d == 0 and i and e[i - 1] not in '^*/([{,+- ' else c
    return o


def _ne(s):
    # N/exp(x) -> N*exp(-x), the way a student writes it
    o = ''
    i = 0
    while i < len(s):
        j = s.find(')', i)
        if s[i:i + 5] == '/exp(' and j > 0 and s[j + 1:j + 2] not in ('^', '*', '/'):
            u = s[i + 5:j]
            if u and not [c for c in u if c not in LET and c not in DIG and c not in '*^']:
                o += '*exp(-' + u + ')'
                i = j + 1
                continue
        o += s[i]
        i += 1
    return o


def _sl(A, l, h, Fh, Fl):
    # the bounds substituted: k(3^3/3), 2^3/27 - 1^3/27, 0 - (-k)
    if 'inf' in l + h:
        return '' if Fl == '0' else _g(Fh) + ' - ' + _p(Fl)
    u = _unk([A])
    B = A
    if len(u) == 1:
        B = S('(' + A + ')/' + u[0])
    if len(u) > 1 or (u and has(B, u[0])):
        return ''
    t = _sv(B, _g(h))
    if _at(B, l) != '0':
        z = _sv(B, _g(l))
        t += ' - ' + ('(' + z + ')' if z[0] == '-' or len(split_terms(z)) > 1 else z)
    t = u[0] + '(' + t + ')' if u else t
    return t if len(t) < 41 else ''


def _di(P, g, a=None, b=None, pre='', eq=''):
    # integrals of g(f) over the pieces (clipped to [a,b]): prints the integral,
    # the antiderivative and the bounds substituted; eq ends each line (an equation)
    I1 = []
    B1 = []
    V1 = []
    sl = ''
    _M['g'] = 0
    for f, lo, hi in P:
        l = lo
        h = hi
        if a is not None:
            if _fv(a) > _fv(lo):
                l = a
            if _fv(b) < _fv(hi):
                h = b
            if _fv(l) >= _fv(h):
                continue
        e = _ne(S(g.replace('F', '(' + f + ')')))
        if _xx(e):
            e = _ne(N(e))
        A = _ne(S(I(e)))
        x = Gs('expand(' + A + ')')
        if x and len(pp(x)) <= len(pp(A)):
            A = _ne(x)
        if bad(A):
            v = G('evalf(integrate(' + e + ',x,' + l + ',' + h + '))')
            I1.append(_il(l, h, _br(e)))
            B1.append(_s3(float(v)) + ' (GDC)')
            V1.append(v)
            _M['g'] = 1
            continue
        Fh = _at(A, h)
        Fl = _at(A, l)
        I1.append(_il(l, h, _br(e)) + _bp(e))
        B1.append('[' + ps(A) + ']_' + _bd(l) + '^' + _bd(h))
        sl = _sl(A, l, h, Fh, Fl)
        V1.append(S('(' + Fh + ')-(' + Fl + ')'))
    if not V1:
        return '0'
    L = [' + '.join(I1), ' + '.join(B1)]
    if len(V1) > 1:
        L.append(join_signed([_g(z) for z in V1]))
    elif sl:
        L.append(sl)
    for j in range(len(L)):
        out((pre if j == 0 else '' if eq else '  = ') + L[j] + eq)
    return S('+'.join(['(' + z + ')' for z in V1]))


def _fl(p):
    return 'f(x) = ' + ps(p[0]) + ', ' + _dm(p[1], p[2])


def continuous_rv():
    hdr('Continuous RV')
    _M['d'] = 0
    P = []
    for i in range(min(3, max(1, int(ask('Pieces (1-3)', '1', 0))))):
        f = _n(ask('f(x), piece ' + str(i + 1) + ' =', '', 0))
        lh = [z.strip() if 'inf' in z else _e(z) for z in split_top(ask('lower, upper', '', 0).strip('()[] '), ',')]
        P.append([f, lh[0], lh[1]])
    U = _unk([p[0] for p in P])
    if len(U) > 2:
        out('Too many unknowns')
        wait()
        return
    c = ask('Extra cond e.g. E=2 or f(1)=0', '', 0).replace(' ', '') if len(U) == 2 else ''
    if len(U) == 2 and '=' not in c:
        out('Need a condition with =')
        wait()
        return
    tk = ask('Tasks 1 k 2 P 3 E,Var 4 median 5 mode 6 aX+b (0=all)', '0', 0)
    if tk == '0':
        tk = '123456'
    if U:
        for p in P:
            out(_fl(p))
        L = _di(P, 'F', eq=' = 1')
        if pp(N(L)) not in U:
            out(pp(N(L)) + ' = 1')
        eqs = [L + '=1']
        if c:
            k = c.find('=')
            v = _e(c[k + 1:])
            cx = c[:2]
            if cx == 'E=':
                c = _di(P, 'x*F', pre='E(X) = ', eq=' = ' + _g(v))
            elif cx == 'f(':
                t = _e(c[2:c.find(')')])
                c = [p for p in P if F(p[1]) <= F(t) <= _fv(p[2])][0][0]
                c = G('subst(' + c + ',x=' + t + ')')
                out('f(' + _g(t) + ') = ' + pp(N(c)) + ' = ' + _g(v))
            else:
                c = _q(norm(c[:k]))
            eqs.append(c + '=' + v)
            if cx != 'f(' and pp(N(c)) not in U:
                out(pp(N(c)) + ' = ' + _g(v))

        def ok(d):
            for f, lo, hi in P:
                for s in range(5):
                    a = F(lo)
                    b = _fv(hi) if hi != 'inf' else a + 10
                    w = F('subst(' + _sb(f, d) + ',x=' + repr(a + (b - a) * (s + 0.5) / 5) + ')')
                    if w is None or w < -1e-12:
                        return False
            return True
        d = _solve(eqs, U, ok)
        if d is None:
            out('No valid solution (f>=0)')
            wait()
            return
        for k in U:
            _A(k, d[k])
        for p in P:
            p[0] = _sb(p[0], d)
    for p in P:
        out(_fl(p))
    if '2' in tk:
        cd = [_e(z) for z in askv('P(c<X<d): c,d', '', 0)]
        lb = 'P(' + _g(cd[0]) + '<X<' + _g(cd[1]) + ')'
        _A(lb, _di(P, 'F', cd[0], cd[1], lb + ' = '))
    E = V = ''
    if '3' in tk or '6' in tk:
        E = _di(P, 'x*F', pre='E(X) = ')
        if _ev(E, 'E(X)'):
            E2 = _di(P, 'x^2*F', pre='E(X^2) = ')
            if _ev(E2, 'E(X^2)'):
                V = S(E2 + '-(' + E + ')^2')
                out('Var(X) = ' + _g(E2) + ' - ' + _k(_g(E)) + '^2 = ' + _f(V))
                out('sd = ' + pp('sqrt(' + _g(V) + ')') + ' = ' + _c(S('sqrt(' + V + ')')))
                _A('E(X)', E)
                _A('Var(X)', V)
    if '4' in tk:
        _median(P)
    if '5' in tk:
        _mode(P)
    if '6' in tk:
        ab = askv('a,b for aX+b', '', 0)
        if ab[0] and V:
            _ab([_e(z) for z in ab], E, V)
    wait()


def _median(P):
    cp = '0'
    hf = _g('1/2')
    ge = '≥' if CFG['uni'] else '>='
    for f, lo, hi in P:
        A = S(I(f))
        ci = S('(' + _at(A, hi) + ')-(' + _at(A, lo) + ')')
        if len(P) > 1:
            out(_il(lo, hi, 'f') + ' = ' + _g(ci) + (' ' + ge + ' ' if F(cp + '+' + ci) >= 0.5 - 1e-12 else ' < ') + hf)
        if F(cp + '+' + ci) < 0.5 - 1e-12:
            cp = S(cp + '+' + ci)
            continue
        rh = S('1/2-(' + cp + ')')
        out(_il(lo, 'm', pp(f)) + ' = ' + (hf if cp == '0' else hf + ' - ' + _g(cp)))
        Am = G('subst(' + A + ',x=m)')
        out('[' + pp(A) + ']_' + _bd(lo) + '^m = ' + _g(rh))
        eq = S(Am + '-(' + _at(A, lo) + ')')
        out(pp(eq) + ' = ' + _g(rh))
        rs = [z for z in GL('solve(' + eq + '=' + rh + ',m)') if not bad(z) and F(z) is not None and _fv(lo) - 1e-9 <= F(z) <= _fv(hi) + 1e-9]
        if not rs:
            rs = GL('fsolve(' + eq + '=' + rh + ',m=' + lo + '..' + (hi if hi != 'inf' else '1e6') + ')')
            out('By GDC:')
        if rs:
            _A('median', rs[0])
        return
    out('median not found')


def _mode(P):
    best = None
    bv = -1e300
    tie = 0
    for f, lo, hi in P:
        df = S('diff(' + f + ',x)')
        out("f'(x) = " + ps(df) + (' on [' + _g(lo) + ',' + _g(hi) + ']' if len(P) > 1 else ''))
        if df == '0':
            tie = 1
            continue
        cs = [lo] + ([hi] if hi != 'inf' else [])
        for z in GL('solve(' + df + '=0,x)'):
            w = F(z)
            if w is not None and _fv(lo) < w < _fv(hi):
                d2 = S('subst(diff(' + f + ',x,2),x=' + z + ')')
                out("f'(x) = 0 => x = " + _g(z) + ", f''(" + _g(z) + ') = ' + _g(d2) + (' < 0 max' if F(d2) < 0 else ''))
                cs.append(z)
        for z in cs:
            fz = S('subst(' + f + ',x=' + z + ')')
            v = F(fz)
            if v is not None:
                if abs(v - bv) < 1e-12 and best is not None and F(z) != F(best):
                    tie = 1
                if v > bv + 1e-12:
                    bv = v
                    best = z
                    fb = fz
                    tie = 0
    if best is None or tie:
        out('mode: not unique')
    else:
        out('max f(' + _g(best) + ') = ' + _g(fb))
        _A('mode', best)


ITEMS = [('Discrete RV', discrete_rv), ('Continuous RV', continuous_rv)]
