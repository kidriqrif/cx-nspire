# ibfun.py - polynomial roots, quadratics, factor/remainder thm
# (AA 2.6-2.7, 2.12); odd/even test lives in ibfun2.py
from ibcore import *

TITLE = 'Functions/roots'


def _ex(s):
    # 'y=..'/'f(x)=..' -> rhs, 'a=b' -> a-b
    k = s.find('=')
    if k < 0:
        return norm(s)
    l = s[:k].strip()
    if l == 'y' or l[-3:] == '(x)':
        return norm(s[k + 1:])
    return norm(lhs0(s))


def _no(m):
    out(m)
    wait()


def _sb(s, v):
    # substitute x = v in the raw expression s, as a student writes it:
    # 2^3 - 2(2), (-1)^3 + a(-1)^2, and for x = 1: 1 + a + b - 6
    o = ''
    n = len(s)
    i = 0
    while i < n:
        c = s[i]
        if c == 'x' and (i == 0 or s[i - 1] not in LET) and \
                (i + 1 >= n or s[i + 1] not in LET):
            p = s[i - 1] if i else '+'
            j = i + 1
            if v == '1':
                if j < n and s[j] == '^':
                    j += 1
                    while j < n and s[j] in DIG:
                        j += 1
                o = o[:-1] if p == '*' else o + '1'
                i = j
                continue
            if p in '(+-' and v.isdigit() or (p == '(' and s[i + 1:i + 2] == ')'):
                o += v
            else:
                o += '(' + v + ')'
        else:
            o += c
        i += 1
    return o


def _sd(s):
    # display a substituted expression: '*' dropped, spaced signs (a(-1)^2 - 4(-1) + b)
    t = join_signed([w.replace('*', '') for w in split_terms(s)])
    return t.replace('sqrt(', '√(').replace('pi', 'π') if CFG['uni'] else t


def _qs(a, b, c):
    # a x^2 + b x + c as a student writes it
    t = []
    for w, m in ((a, 'x^2'), (b, 'x'), (c, '')):
        if w != '0':
            q = pp(w)
            if m and w in ('1', '-1'):
                q = w[:-1]
            elif m and (len(split_terms(w)) > 1 or '/' in w):
                q = '(' + q + ')'
            t.append(q + m)
    return join_signed(t)


def _pa(v):
    v = pp(v)
    return v if v in LET or isnum(v) and v[0] != '-' and '/' not in v else '(' + v + ')'


def _gcd(a, b):
    a = abs(a)
    b = abs(b)
    for i in range(200):
        if b == 0:
            break
        a, b = b, a % b
    return a


def _dv(n):
    n = abs(n)
    r = []
    i = 1
    while i * i <= n and i < 3000:
        if n % i == 0:
            r.append(i)
            if i * i != n:
                r.append(n // i)
        i += 1
    r.sort()
    return r


def _fr(a, b):
    g = _gcd(a, b)
    if b < 0:
        g = -g
    a //= g
    b //= g
    return str(a) if b == 1 else str(a) + '/' + str(b)


def _co(p):
    s = G('coeff(' + p + ',x)')
    s = s[s.find('['):].replace('[', '').replace(']', '')
    return [int(t) for t in s.split(',')]


def _P(c):
    return G('expand(poly2symb([' + ','.join([str(a) for a in c]) + '],x))')


# module is re-imported per topic, so these follow the Unicode setting
DL = 'Δ' if CFG['uni'] else 'D'
PM = '±' if CFG['uni'] else '+/-'


def _cx(re, im, sg):
    # re +/- (im)i for display
    m = pp(im)
    if im == '1':
        m = ''
    elif '/' in m or len(split_terms(im)) > 1:
        m = '(' + m + ')'
    if re == '0':
        return ('' if sg > 0 else '-') + m + 'i'
    return pp(re) + (' + ' if sg > 0 else ' - ') + m + 'i'


def _qr(a, b, c):
    # discriminant, 2a, roots (Giac) and display roots of ax^2 + bx + c
    d = N('(' + b + ')^2-4*(' + a + ')*(' + c + ')')
    t = N('2*(' + a + ')')
    re = S('-(' + b + ')/(' + t + ')')
    s = S('sqrt(abs(' + d + '))/abs(' + t + ')')
    if F(d) < 0:
        g = ['(' + re + ')' + o + '(' + s + ')*i' for o in '-+']
        ds = [_cx(re, s, -1), _cx(re, s, 1)]
    else:
        g = [G('(' + re + ')' + o + '(' + s + ')') for o in '-+']
        g.sort(key=lambda r: F(r))
        ds = [pp(r) for r in g]
    return d, t, g, ds


def _qf(a, b, c, v='x', fin=1):
    # quadratic formula working -> (disc, [giac roots], [display roots])
    # fin=0: the caller prints the roots (as its ANS line)
    d, t, g, ds = _qr(a, b, c)
    fd = F(d)
    out(DL + ' = b^2 - 4ac = ' + _pa(b) + '^2 - 4(' + pp(a) + ')(' + pp(c) + ') = ' + pp(d))
    bb = pp(N('-(' + b + ')'))
    if fd == 0:
        out(v + ' = ' + bb + '/' + _pa(t))
    else:
        r = S('sqrt(' + d + ')') if fd > 0 else ''
        r = pp(r) if isnum(r) else pp('sqrt(' + d + ')')
        out(v + ' = (' + (bb + ' ' if bb != '0' else '') + PM + ' ' + r + ')/' + _pa(t))
    if fin:
        out(v + ' = ' + (ds[0] + ' (repeated)' if fd == 0 else ' or '.join(ds)))
    return d, g, ds


def _rk(f):
    # sort key: x first, then by root of a linear factor, others last
    if f == 'x':
        return -99999
    if G('degree(' + f + ',x)') != '1':
        return 99999
    return F('-subst(' + f + ',x=0)/coeff(' + f + ',x,1)')


def _fp(fs, srt=0):
    # collated product of factors
    if srt:
        fs = sorted(fs, key=_rk)
    o = ''
    seen = []
    for f in fs:
        if f in seen:
            continue
        seen.append(f)
        m = fs.count(f)
        o += (f if len(f) < 2 else '(' + ps(f) + ')') + ('^' + str(m) if m > 1 else '')
    return o


def _fl(s, v='x'):
    # Giac factor() string -> (constant, [factor, ...] with repeats)
    ng, fs = split_factors(s)
    k = '-1' if ng else '1'
    o = []
    for op, f in fs:
        if not has(f, v):
            k += op + f
            continue
        m = 1
        j = f.rfind('^')
        if j > 0 and f[j + 1:].isdigit() and (f[j - 1] == ')' or j < 2):
            m = int(f[j + 1:])
            f = f[:j]
        o += [G('expand(' + f + ')')] * m
    return S(k), o


def _pre(k):
    if k == '1':
        return ''
    if k == '-1':
        return '-'
    return pp(k) if isnum(k) and '/' not in k else '(' + pp(k) + ')'


def _abc(P):
    return [G('coeff(' + P + ',x,' + j + ')') for j in '210']


def _sol(P):
    # solve one factor P = 0 -> [roots, display, factors, multiplier, exact]
    n = G('degree(' + P + ',x)')
    a, b, c = _abc(P)
    if n == '1':
        r = S('-(' + c + ')/(' + b + ')')
        return [[r], [pp(r)], [P], '1', 1, 0]
    if n == '2':
        d, t, g, ds = _qr(a, b, c)
        if F(d) >= 0 and isnum(a + b + c) and isnum(S('sqrt(' + d + ')')):
            # rational roots: factorise, no formula
            e, l = _fl(G('factor(' + P + ')'))
            return [g, ds, l, e, 1, 0]
        out(ps(P) + ' = 0')
        _qf(a, b, c)
        if F(d) < 0:
            return [g, ds, [P], '1', 1, 1]
        return [g, ds, [G('x-(' + r + ')') for r in g], a, 1, 1]
    g = GL('proot(' + P + ')')
    ds = []
    for r in g:
        x = F('re(' + r + ')')
        y = F('im(' + r + ')')
        ds.append(sf3(x) if abs(y) < 1e-9 else _cx('0' if abs(x) < 1e-9 else sf3(x), sf3(abs(y)), y))
    return [g, ds, [P], '1', 0, 0]


def roots():
    hdr('Polynomial roots')
    p = G('expand(exact(' + _ex(ask('f(x) =', '', 0)) + '))')
    if G('is_polynomial(' + p + ',x)') != 'true' or GL('lname(' + p + ')') != ['x']:
        return _no('Polynomial in x only')
    q = G('numer(normal(' + p + '))')
    k = S('(' + p + ')/(' + q + ')')
    try:
        c = _co(q)
    except ValueError:
        return _no('Rational coefficients only')
    m = 0
    for a in c:
        m = _gcd(m, a)
    if c[0] < 0:
        m = -m
    c = [a // m for a in c]
    k = S('(' + k + ')*' + str(m))
    C = c[:]
    n0 = len(c) - 1
    lc = ps(p)
    if k != '1':
        lc = _pre(k) + '(' + ps(_P(c)) + ')'
    if k != '1' and '/' in p:
        # fractions: f(x) = (1/2)(x^2 - 4), not x^2/2 - 2
        out('f(x) = ' + lc)
    else:
        out('f(x) = ' + ps(p))
        if k != '1':
            out(' = ' + lc)
    fs = []
    g = []
    while len(c) > 1 and c[-1] == 0:
        c = c[:-1]
        fs.append('x')
        g.append('0')
    if fs:
        t = _pre(k) + _fp(fs) + ('(' + ps(_P(c)) + ')' if len(c) > 1 else '')
        if t != lc:
            out(' = ' + t)
        lc = t
    pf = ' = '
    for it in range(8):
        n = len(c) - 1
        if n <= 2:
            break
        cd = []
        for b in _dv(c[0]):
            for a in _dv(c[-1]):
                if _gcd(a, b) == 1:
                    cd.append((a, b))
        hit = None
        for a, b in cd:
            for s in (a, -a):
                v = 0
                for j in range(n + 1):
                    v += c[j] * s ** (n - j) * b ** j
                if v == 0:
                    hit = (s, b)
                    break
            if hit:
                break
        if not hit:
            break
        a, b = hit
        L = G(str(b) + '*x-(' + str(a) + ')')
        out(('q(' if fs or k != '1' else 'f(') + _fr(a, b) + ') = ' + _sd(_sb(_P(c), _fr(a, b))) +
            ' = 0, so (' + ps(L) + ') is a factor (factor theorem)')
        nc = []
        pv = 0
        for j in range(n):
            pv = (c[j] + a * pv) // b
            nc.append(pv)
        c = nc
        fs.append(L)
        g.append(_fr(a, b))
        lc = _pre(k) + _fp(fs) + '(' + ps(_P(c)) + ')'
        out('f(x) = ' + lc)
        pf = ' = '
    n = len(c) - 1
    P = _P(c)
    l = []
    if n > 2:
        e, l = _fl(G('factor(' + P + ')'))
        k = S('(' + k + ')*(' + e + ')')
        if len(l) > 1:
            lc = _pre(k) + _fp(fs + l, 1)
            out(pf + lc)
    elif n:
        l = [P]
    else:
        k = S('(' + k + ')*' + str(c[0]))
    ds = [pp(r) for r in g]
    ex = 1
    sv = {}
    for P in l:
        if P not in sv:
            sv[P] = _sol(P)
        g2, d2, f2, e, x, w = sv[P]
        if w:
            pf = 'f(x) = '
        g += g2
        ds += d2
        fs += f2
        k = S('(' + k + ')*(' + e + ')')
        ex = ex and x
    fin = _pre(k) + _fp(fs, 1)
    if ex and sorted(fin) != sorted(lc) and (len(fs) > 1 or k != '1'):
        out(pf + fin)
    pr = [(abs(F('im(' + g[j] + ')')) > 1e-9, F('re(' + g[j] + ')'), ds[j]) for j in range(len(g))]
    pr.sort(key=lambda t: t[:2])
    u = []
    ap = []
    for w, v, d in pr:
        if d not in u:
            u.append(d)
            if ex and not w and not isnum(d):
                ap.append(sf3(v))
    out('ANS: x = ' + ', '.join([d + {1: '', 2: ' (double)', 3: ' (triple)'}.get(
        ds.count(d), ' (multiplicity ' + str(ds.count(d)) + ')') for d in u]) + ('' if ex else ' (GDC)'))
    if ap:
        out('     ~ ' + ', '.join(ap))
    if yes('Sum/product of roots', 'n'):
        out('Sum = -a' + str(n0 - 1) + '/a' + str(n0) + ' = ' + _fr(-C[1], C[0]))
        out('Product = (-1)^' + str(n0) + ' a0/a' + str(n0) + ' = ' + _fr((-1) ** n0 * C[-1], C[0]))
    wait()


def quad():
    hdr('Quadratic')
    f = G('expand(exact(' + _ex(ask('f(x) =', '', 0)) + '))')
    if G('is_polynomial(' + f + ',x)') != 'true' or G('degree(' + f + ',x)') != '2':
        return _no('Quadratic in x only')
    a, b, c = _abc(f)
    ks = [v for v in GL('lname(' + f + ')') if v != 'x']
    out('f(x) = ' + _qs(a, b, c))
    out('a = ' + pp(a) + ', b = ' + pp(b) + ', c = ' + pp(c))
    if ks:
        return _par(a, b, c, ks[0])
    hp = N('(' + b + ')/(2*(' + a + '))')
    h = N('-(' + hp + ')')
    k = N('(' + c + ')-(' + b + ')^2/(4*(' + a + '))')
    A = _pre(a)
    sq = 'x^2' if hp == '0' else '(' + ps(G('x+(' + hp + ')')) + ')^2'
    t = join_signed([sq, '-' + pp(N('(' + hp + ')^2'))])
    cs = join_signed([A + sq, pp(k)])
    L = []
    if hp != '0':
        if a != '1':
            L.append(join_signed([A + '(' + ps(N('x^2+(' + b + ')/(' + a + ')*x')) + ')', pp(c)]))
            t = A + '[' + t + ']'
        L.append(join_signed([t, pp(c)]))
    L.append(cs)
    while L and L[-1] == cs:
        L.pop()
    for j in range(len(L)):
        out(('f(x)' if j == 0 else '') + ' = ' + L[j])
    out('ANS: f(x) = ' + cs)
    out('axis x = ' + pp(h))
    ans('vertex', '(' + h + ', ' + k + ')', 0)
    mx = F(a) < 0
    out(('Max' if mx else 'Min') + ' value ' + pp(k) + ', range y ' + ('<= ' if mx else '>= ') + pp(k))
    out('y-intercept (0, ' + pp(c) + ')')
    d, g, ds = _qf(a, b, c, 'x', 0)
    if F(d) < 0:
        fz = 'not possible over R'
    elif isnum(S('sqrt(' + d + ')')) and isnum(a + b + c):
        e, l = _fl(G('factor(' + f + ')'))
        fz = _pre(e) + _fp(l, 1)
    else:
        fz = A + _fp([G('x-(' + r + ')') for r in g])
    out('Factorised: ' + ('f(x) = ' if F(d) >= 0 else '') + fz)
    if F(d) < 0:
        out('ANS: no real roots (x = ' + ', '.join(ds) + ')')
    else:
        out('ANS: x = ' + ', '.join(ds[:2 - (F(d) == 0)]))
        if not isnum(g[0]):
            out('     ~ ' + ', '.join([sf3(F(r)) for r in g]))
    wait()


def _iq(t, v):
    # Giac solve item -> 'a < k <= b' / 'k > a' / 'k = a'
    t = unwrap(t).replace('&&', ' and ')
    if t == v:
        return 'all real ' + v
    o = []
    for u in t.split(' and '):
        u = unwrap(u)
        j = len(v)
        if u[:j] != v or u[j:j + 1] not in ['<', '>']:
            return v + ' = ' + pp(S(u))
        op = u[j:j + 2] if u[j + 1:j + 2] == '=' else u[j]
        o.append([op, pp(S(u[j + len(op):]))])
    if len(o) == 2:
        return o[0][1] + ' ' + o[0][0].replace('>', '<') + ' ' + v + ' ' + o[1][0] + ' ' + o[1][1]
    return v + ' ' + o[0][0] + ' ' + o[0][1]


def _cp(op, w):
    return {'=': w == 0, '>': w > 0, '>=': w >= 0, '<': w < 0}[op]


def _par(a, b, c, k):
    # discriminant condition on parameter k
    d = N('(' + b + ')^2-4*(' + a + ')*(' + c + ')')
    out(DL + ' = b^2 - 4ac = ' + _pa(b) + '^2 - 4(' + pp(a) + ')(' + pp(c) + ') = ' + ps(d))
    m = ask('1 equal 2 distinct 3 real 4 no real', '1', 0)
    op, w = {'2': ('>', 'Distinct'), '3': ('>=', 'Real'), '4': ('<', 'No real')}.get(m, ('=', 'Equal'))
    out(w + ' roots: ' + DL + ' ' + op + ' 0')
    e, l = _fl(G('collect(' + d + ')'), k)
    out(ps(d) + ' ' + op + ' 0')
    h = has(d, k)
    if h and (len(l) > 1 or e != '1'):
        out(_pre(e) + _fp(l) + ' ' + op + ' 0')
    c = GL('solve(' + d + '=0,' + k + ')') if h else []
    if op != '=':
        out('Critical values: ' + (k + ' = ' + ', '.join([pp(S(r)) for r in c]) if c else 'none'))
    s = GL('solve(' + d + op + '0,' + k + ')') if h else [k] * _cp(op, F(d))
    z = GL('solve(' + a + '=0,' + k + ')') if has(a, k) else []
    x = []
    for r in z:
        out('a != 0: ' + k + ' != ' + pp(r))
        if op != '=' and _cp(op, F('subst(' + d + ',' + k + '=' + r + ')')):
            x.append(', ' + k + ' != ' + pp(r))
    if op == '=':
        s = [r for r in s if r not in z]
    t = ' or '.join([_iq(r, k) for r in s])
    if len(s) == 2 and s[0].replace('<', '>') == s[1]:
        t = 'all real ' + k if '=' in s[0] else k + ' != ' + pp(S(s[0][len(k) + 1:]))
    out('ANS: ' + (t + ''.join(x) if s else 'no ' + k))
    wait()


def remthm():
    hdr('Remainder/factor')
    p0 = _ex(ask('p(x) =', '', 0))
    p = G('expand(' + p0 + ')')
    u = [v for v in GL('lname(' + p + ')') if v != 'x']
    U = ','.join(u)
    if G('is_polynomial(' + p + ',x)') != 'true':
        return _no('Polynomial p(x) only')
    if not u:
        p0 = p
    out('p(x) = ' + ps(p0))
    if not u:
        d = G('expand(' + norm(ask('Divisor', '', 0)) + ')')
        n = int(G('degree(' + d + ',x)'))
        if n < 1:
            return _no('Divisor must contain x')
        if n == 1:
            c = S('-subst(' + d + ',x=0)/coeff(' + d + ',x,1)')
            out(ps(d) + ' = 0 => x = ' + pp(c))
            out('R = p(' + pp(c) + ')  (remainder theorem)')
            out(' = ' + _sd(_sb(p, c)))
            r = S('subst(' + p + ',x=' + c + ')')
            out(' = ' + pp(r))
            if r == '0':
                out('R = 0, so (' + ps(d) + ') is a factor (factor theorem)')
        else:
            out('p(x)/(' + ps(d) + '):')
            r = p
            for it in range(12):
                m = int(G('degree(' + r + ',x)'))
                if r == '0' or m < n:
                    break
                t = S('lcoeff(' + r + ',x)/lcoeff(' + d + ',x)*x^' + str(m - n))
                r = G('expand(' + r + '-(' + t + ')*(' + d + '))')
                out(' - (' + ps(G('expand((' + t + ')*(' + d + '))')) + ') = ' + ps(r))
        out('p(x) = ' + join_signed(['(' + ps(d) + ')(' + ps(G('quo(' + p + ',' + d + ',x)')) + ')',
                                     '(' + ps(r) + ')' if len(split_terms(r)) > 1 else r]))
        ans('Remainder', r)
        wait()
        return
    eqs = []
    for i in range(3):
        if len(eqs) >= len(u):
            break
        d = norm(ask('Divisor ' + str(i + 1), '', 0))
        r = norm(ask('Remainder', '0', 0))
        for c in GL('solve(' + d + '=0,x)'):
            # p(c) = r(c), cleared of fractions
            t = S('subst(' + r + ',x=' + c + ')')
            e = G('numer(normal(subst(' + p + ',x=' + c + ')-(' + t + ')))')
            z = G('subst(' + e + ',[' + U + '],[' + ','.join(['0'] * len(u)) + '])')
            out('p(' + pp(c) + ') = ' + _sd(_sb(p0, c)) + ' = ' + pp(t))
            lh = ps(N(e + '-(' + z + ')'))
            if len(u) > 1 or lh != u[0]:
                out(' => ' + lh + ' = ' + pp(N('-(' + z + ')')))
            eqs.append(e + '=0')
    s = GL('solve([' + ','.join(eqs) + '],[' + U + '])')
    if not s:
        out('No solution')
    else:
        v = parse_list(s[0])
        for j in range(len(u)):
            ans(u[j], v[j])
        q = G('expand(subst(' + p + ',[' + U + '],[' + ','.join(v) + ']))')
        out('p(x) = ' + ps(q))
        e, l = _fl(G('collect(' + q + ')'))
        if len(l) > 1:
            out(' = ' + _pre(e) + _fp(l, 1))
    wait()


ITEMS = [('Polynomial roots', roots), ('Quadratic', quad),
         ('Remainder/factor', remthm)]
