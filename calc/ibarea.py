# ibarea.py - definite integrals, areas, volumes, kinematics (AA 5.5, 5.9, 5.11, 5.17)
from ibcore import *
import math

TITLE = 'Areas/volumes'


def _dd(r):
    # chained division such as pi/3/2
    for k in range(len(r) - 2):
        j = k + 1
        while r[k] == '/' and j < len(r) and r[j] in DIG:
            j += 1
        if j > k + 1 and r[j:j + 1] == '/':
            return 1
    return 0


def _S(e):
    r = S(e)
    if not has_var(r):
        for c in ('expand(', 'normal(texpand(' * ('ln(' in r)):
            x = Gs(c + r + ')' * (1 + (c[0] == 'n'))) if c else ''
            if x and (len(x) < len(r) or _dd(r)):
                r = x
    return r.replace('exp(1)', 'e')


def _var(f):
    for c in 'xtyu':
        if has(f, c):
            return c
    return 'x'


def _g(z):
    return '%.12g' % z


def _fl(s):
    try:
        return float(s)
    except ValueError:
        return None


def _q(s):
    # display a value: 3 s.f. if it is a decimal
    if '.' in s:
        z = F(s)
        if z is not None:
            return sf3(z)
    return ps(s)


def _lb(a):
    # integral limit for display
    if '.' in a:
        a = _q(a)
        return '(' + a + ')' if a[0] == '-' else a
    for c in a:
        if c not in LET and c not in DIG:
            return '(' + pp(a) + ')'
    return pp(a)


def _wr(g, k=1):
    # display g, in brackets if it is a sum (or negative)
    p = ps(g)
    return '(' + p + ')' if len(split_terms(g)) > 1 or (k and p[:1] == '-') else p


def _pa(s):
    p = _q(s)
    return '(' + p + ')' if p[:1] == '-' or len(split_terms(s)) > 1 else p


def _ro(s):
    # a sum with a positive term first: -2ln(2) + 1 -> 1 - 2ln(2)
    ts = split_terms(s)
    p = [t for t in ts if t[:1] != '-'][:1]
    return join_signed(p + [t for t in ts if t not in p]) if p else s


def _sb(e, v, a):
    # substitute v -> a for display, with brackets only where a student writes them
    c = a[:1] == '-' or '/' in a or '*' in a or len(split_terms(a)) > 1
    o = ''
    i = 0
    n = len(e)
    while i < n:
        if e[i] in LET:
            j = i
            while j < n and e[j] in LET:
                j += 1
            w = e[i:j]
            if w == v:
                p = e[i - 1:i]
                w = a
                u = p == '-' and e[j:j + 1] == '^' and (i < 2 or e[i - 2] in '(*/^+-')
                if (c and not (p == '(' and e[j:j + 1] == ')')) or ((p == '*' or u) and a[:1] in DIG):
                    w = '(' + a + ')'
            o += w
            i = j
        else:
            o += e[i]
            i += 1
    return o.replace('(-0)', '(0)')


def _at(e, v, a):
    return _S('subst(' + e + ',' + v + '=(' + a + '))')


def _hp(t, v):
    # c v^(m/n) as a power for display: (2/3)y^(3/2) (Giac writes 2y sqrt(y)/3)
    if 'sqrt(' + v + ')' not in t and v + '^(' not in t:
        return t
    e = Gs('normal(' + v + '*diff(' + t + ',' + v + ')/(' + t + '))')
    c = Gs('normal((' + t + ')/' + v + '^(' + e + '))') if isnum(e) and e != '1/2' else ''
    if not c or has_var(c):
        return t
    ng, c = sign_body(c)
    if '/' in c:
        c = '(' + c + ')'
    return ('-' if ng else '') + ('' if c == '1' else c + '*') + v + '^(' + e + ')'


def _pf(r, v):
    return join_signed([_hp(t, v) for t in split_terms(r)])


def _ex1(a):
    # decimal input -> exact rational
    return (Gs('exact(' + a + ')') or a) if '.' in a else a


def _n(p, d='', e=1):
    return _ex1(askn(p, d, e))


def _fx(p, d='', e=1):
    # function input; decimals -> exact so the working stays exact
    return _ex1(norm(rhs(ask(p, d, e))))


def _two(s):
    p = [_ex1(norm(z)) for z in split_top(s.strip('()[] '), ',')]
    if len(p) != 2 or not p[0] or not p[1]:
        raise GErr('enter two values a,b')
    return p


def _pt(a):
    z = F(a)
    if z is None:
        raise GErr('limits must be numbers')
    return [a, z, 0]


def _il(a, b):
    # integral sign with limits
    return INT() + '_' + _lb(a) + '^' + _lb(b) + ' '


def _lm(a, b):
    # limits as [A, B], lower first
    A = _pt(a)
    B = _pt(b)
    return [B, A] if A[1] > B[1] else [A, B]


def _dv(r):
    return sf3(r[1]) if r[2] else pp(r[0])


def _rv(r):
    return _dv(r) + (' (GDC)' if r[2] else '')


def _lv(r):
    return _lb(_g(r[1]) if r[2] else r[0])


def _anti(f, v, suf=''):
    # antiderivative term by term; '' if not elementary. Shows the rewrite
    # (expansion, partial fractions, division) and each non-power term;
    # suf (' + C') also shows the result
    ts = split_terms(f)
    for c in ('partfrac(' + f + ',' + v + ')') * ('/' in f), 'expand(lin(expand(' + f + ')))':
        p = Gs(c) if c and len(ts) < 2 else ''
        if p and c[0] == 'e' and len(split_terms(p)) >                 len(split_terms(Gs('integrate(' + f + ',' + v + ')'))):
            continue
        if len(split_terms(p)) > 1 and not bad(p):
            out(ps(f) + ' = ' + ps(p))
            ts = split_terms(p)
            break
    rs = []
    for t in ts:
        r = Gs('integrate(' + t + ',' + v + ')')
        if bad(r) or [k for k in ('sign(', 'W(', 'Ei(', 'Li(') if k in r]:
            out('No elementary antiderivative')
            return ''
        r = _S(r)
        x = Gs('factor(' + r + ')')
        if x and (len(x) < len(r) or _dd(r)):
            r = x
        if len(ts) > 1 and Gs('is_polynomial(' + t + ',' + v + ')') != 'true':
            out(' ' + INT() + pp(t.lstrip('+')) + ' d' + v + ' = ' + ps(_hp(r, v)))
        rs.append('(' + r + ')')
    r = _S('+'.join(rs))
    if suf:
        out('= ' + ps(_pf(r, v)) + suf)
    return r


def _sv(Fx, v, x, fx):
    # F(x) for display; a trivial F(0) = 0 is just 0
    if x == '0' and fx == '0' and not [k for k in ('ln(', 'sin(', 'cos(', 'tan(', 'exp(', 'abs(') if k in Fx]:
        return '0'
    return _sb(Fx, v, x)


def _fab(Fx, v, a, b, pre='', fin=0, ab=0):
    # [F]_a^b = F(b) - F(a): bracket, substitution, values.
    # pre: factor outside (pi); ab: region below the axis, shown as |..|;
    # fin: the last value is the ANS line, so it is not repeated
    Fd = _pf(Fx, v)
    bar = '|' * ab
    out('= ' + bar + pre + '[' + ps(Fd) + ']_' + _lb(a) + '^' + _lb(b) + bar)
    fb = _at(Fx, v, b)
    fa = _at(Fx, v, a)
    r = _ro(_S('(' + fb + ')-(' + fa + ')'))
    if '.' not in a + b:
        s1 = _sv(Fd, v, b, fb)
        s2 = _wr(_sv(Fd, v, a, fa))
        out('= ' + bar + (pre + '(' + ps(s1) + ' - ' + s2 + ')' if pre else _wr(s1, 0) + ' - ' + s2) + bar)
    t = _q(_ro(fb)) + ('' if fa == '0' else ' - ' + _pa(fa))
    q = _q(r)
    if ab and (F(r) or 0) < 0:
        r = _ro(_S('-(' + r + ')'))
    d = t.replace(' ', '') != q.replace(' ', '')
    if ab:
        out('= |' + t + '|')
        if d:
            out('= |' + q + '|')
    elif pre:
        if d or not isnum(r):
            out('= ' + pre + '(' + t + ')')
    elif d:
        out('= ' + t)
    if not fin:
        out('= ' + _q(r))
    return r


def _gdc(h, v, a, b):
    z = F('int(' + h + ',' + v + ',' + a + ',' + b + ')')
    if z is None:
        raise GErr('cannot integrate')
    out('= ' + sf3(z) + ' (GDC)')
    return _g(z)


def _ans(lbl, r):
    ans(lbl, sf3(F(r)) if '.' in r else _ro(r))


def _scan(h, v, a, b):
    # 49 values of h on [a,b]
    return parse_list(Gs('evalf(seq(subst(' + h + ',' + v + '=(' + a + ')+zzk*((' +
                         b + ')-(' + a + '))/48),zzk,0,48))'))


def _oos(f, v, a, b):
    # improper integrals are outside AA HL
    if 'inf' in a + b or 'i*n*f' in a + b:
        out('Infinite limit: not in AA')
        return 1
    x0 = F(a)
    x1 = F(b)
    if x0 is None or x1 is None or [c for c in GL('lname(' + f + ')') if c != v]:
        return 0
    m = ''
    dn = Gs('denom(tan2sincos(' + f + '))')
    if has(dn, v):
        for p in _sol(dn, v):
            if min(x0, x1) <= p[1] <= max(x0, x1):
                m = ' at ' + v + ' = ' + pp(p[0])
    for y in _scan(f, v, a, b):
        if not m and (_fl(y) is None or 'inf' in y):
            m = ' on [' + pp(a) + ', ' + pp(b) + ']'
    if m:
        out('f undefined' + m)
        out('Improper integral: not in AA')
        return 1
    return 0


def _sol(h, v):
    # usable real exact roots of h = 0 -> [[str, float], ...]
    o = []
    for r in parse_list(Gs('solve(' + h + '=0,' + v + ')')):
        z = None
        if r and not bad(r) and 'W(' not in r and '.' not in r and len(r) < 40:
            z = F(r)
        if z is not None:
            o.append([r, z])
    return o


def _ex(z, h, v, pr):
    # recognise a numeric root as k/12 or (exact root) + m*pi
    cs = ['%d/12' % round(z * 12)]
    for p in pr:
        cs.append(p[0] + '+(' + str(round((z - p[1]) / math.pi)) + ')*pi')
    for c in cs:
        t = F(c)
        if t is not None and abs(t - z) < 1e-7:
            y = F('subst(' + h + ',' + v + '=(' + c + '))')
            if y is not None and abs(y) < 1e-9:
                return _S(c)
    return ''


def _roots(h, v, A, B):
    # roots of h strictly inside (A,B): exact, else GDC numeric
    a = A[0]
    b = B[0]
    x0 = A[1]
    w = (B[1] - x0) / 48
    e = abs(w) * 1e-6
    pr = _sol(h, v)
    rs = [[_S(p[0]), p[1], 0] for p in pr if x0 + e < p[1] < B[1] - e]
    ys = _scan(h, v, a, b)
    for k in range(min(48, len(ys) - 1)):
        y0 = _fl(ys[k])
        y1 = _fl(ys[k + 1])
        if y0 is None or y1 is None:
            continue
        if abs(y0) < 1e-11:
            y0 = 0
        if abs(y1) < 1e-11:
            y1 = 0
        if y0 * y1 < 0 or (y1 == 0 and k < 47):
            lo = x0 + k * w
            hi = lo + w
            dup = 0
            for r in rs:
                if min(lo, hi) - e <= r[1] <= max(lo, hi) + e:
                    dup = 1
            if dup:
                continue
            z = hi
            if y1:
                q = parse_list(Gs('fsolve(' + h + '=0,' + v + '=' + _g(min(lo, hi)) +
                                  '..' + _g(max(lo, hi)) + ')')) + ['']
                z = _fl(q[0])
            if z is None:
                z = _fl(Gs('fsolve(' + h + '=0,' + v + '=' + _g(lo + w / 2) + ')'))
                if z is not None and abs(z - lo - w / 2) > abs(w):
                    z = None
            if z is None or not (min(x0, B[1]) + e < z < max(x0, B[1]) - e):
                continue
            c = _ex(z, h, v, pr)
            rs.append([c, z, 0] if c else [_g(z), z, 1])
    rs.sort(key=lambda r: r[1])
    return rs


def _eq(h, fg, v, rs=0):
    # the equation whose roots split the region, and its roots
    out(ps(fg[0]) + ' = ' + ps(fg[1]) if fg else ps(h) + ' = 0')
    if rs:
        out(v + ' = ' + ', '.join([_rv(r) for r in rs]))


def _area(h, v, A, B, Fx=None, L='A', fg=None, pr=1):
    # sum of the areas of the pieces of h between its roots on [A,B];
    # fg = [f, g]: region between two curves (h = f - g, top - bottom)
    rs = _roots(h, v, A, B)
    gd = A[2] or B[2]
    if rs and pr:
        _eq(h, fg, v, rs)
    for r in rs:
        gd = gd or r[2]
    if Fx is None:
        Fx = _anti(h, v)
    pts = [A] + rs + [B]
    tot = []
    for k in range(len(pts) - 1):
        lo = pts[k]
        hi = pts[k + 1]
        y = F('subst(' + h + ',' + v + '=' + _g((lo[1] + hi[1]) / 2) + ')')
        up = y is not None and y > 0
        t = h
        Ft = Fx
        ab = 1 - up
        if fg:
            ab = 0
            c = fg
            if not up:
                c = [fg[1], fg[0]]
                t = _S('(' + c[0] + ')-(' + c[1] + ')')
                Ft = Fx and _S('-(' + Fx + ')')
            out(_dv(lo) + ' < ' + v + ' < ' + _dv(hi) + ': ' + ps(c[0]) + ' > ' + ps(c[1]))
        lim = INT() + '_' + _lv(lo) + '^' + _lv(hi) + ' ' + _pa(t) + ' d' + v
        out(L + str(k + 1) + ' = ' + ('|' + lim + '|' if ab else lim))
        if Fx:
            r = _fab(Ft, v, lo[0], hi[0], '', len(pts) < 3, ab)
        else:
            r = _gdc('-(' + t + ')' if ab else t, v, lo[0], hi[0])
            gd = 1
        tot.append(r)
    if len(tot) > 1:
        out(L + ' = ' + ' + '.join([_pa(t) for t in tot]))
    r = _S('+'.join(['(' + t + ')' for t in tot]))
    return _g(F(r)) if gd else r


def _reg(f, g):
    # area between y = f and y = g (g = '' -> x-axis)
    v = _var(f + '+' + g)
    d = _S('(' + f + ')-(' + g + ')') if g else f
    fg = [f, g] if g else None
    if d == '0':
        out('Same curve: no region')
        wait()
        return
    pr = 1
    s = ask('Limits a,b (blank=roots)', '', 0)
    if s:
        A, B = _lm(*_two(s))
    else:
        pr = 0
        rs = [[_S(p[0]), p[1], 0] for p in _sol(d, v)]
        rs.sort(key=lambda r: r[1])
        if len(rs) < 2:
            w = _two(ask('GDC search a,b', '-10,10', 0))
            rs = _roots(d, v, _pt(w[0]), _pt(w[1]))
        if len(rs) < 2:
            _eq(d, fg, v)
            out('Fewer than 2 roots: give limits')
            wait()
            return
        _eq(d, fg, v, rs)
        A = rs[0]
        B = rs[-1]
    if _oos(d, v, A[0], B[0]):
        wait()
        return
    _ans('A', _area(d, v, A, B, None, 'A', fg, pr))
    wait()


def defint():
    hdr('Definite integral')
    f = _fx('f(x) =', '', 0)
    a = _n('Lower limit a', '', 0)
    b = _n('Upper limit b', '', 0)
    v = _var(f)
    out(_il(a, b) + _pa(f) + ' d' + v)
    if _oos(f, v, a, b):
        wait()
        return
    if f[:4] == 'abs(' and unwrap(f[3:]) != f[3:]:
        g = unwrap(f[3:])
        A = _pt(a)
        B = _pt(b)
        if A[1] > B[1]:
            out('= -' + _il(b, a) + _pa(f) + ' d' + v)
            r = _S('-(' + _area(g, v, B, A, None, 'I') + ')')
        else:
            r = _area(g, v, A, B, None, 'I')
    else:
        Fx = _anti(f, v)
        r = _fab(Fx, v, a, b, '', 1) if Fx else _gdc(f, v, a, b)
    _ans('I', r)
    t = norm(ask('Set I = (blank=skip)', '', 0)) if has_var(r) else ''
    for c in 'kabmnpq':
        if t and has(r, c):
            out(pp(r) + ' = ' + pp(t))
            for p in _sol('(' + r + ')-(' + t + ')', c):
                ans(c, p[0])
            break
    wait()


def _bc(fp, v, x0, y0, nm):
    # integrate, + C, use the given point to find C
    out(nm + '(' + v + ') = ' + INT() + _pa(fp) + ' d' + v)
    Fx = _anti(fp, v, ' + C')
    if not Fx:
        return ''
    out(nm + '(' + pp(x0) + ') = ' + pp(y0))
    s = ps(_sb(_pf(Fx, v), v, x0)) + ' + C = ' + pp(y0)
    out(s)
    fv = _at(Fx, v, x0)
    t = ps(fv) + ' + C = ' + pp(y0)
    if fv != '0' and t.replace(' ', '') != s.replace(' ', ''):
        out(t)
    c = _S('(' + y0 + ')-(' + fv + ')')
    out('C = ' + pp(c))
    r = join_signed([Fx, c])
    ans(nm + '(' + v + ')', ps(_pf(r, v)))
    return r


def antider():
    hdr("f from f' + point")
    fp = _fx("f'(x) =")
    p = _two(ask('Point (x0,y0)', '', 0))
    _bc(fp, _var(fp), p[0], p[1], 'f')
    wait()


def area_x():
    hdr('Area curve/x-axis')
    _reg(_fx('y = f(x) =', '', 0), '')


def area_2():
    hdr('Area between curves')
    f = _fx('y1 = f(x) =', '', 0)
    _reg(f, _fx('y2 = g(x) =', '', 0))


def _xofy(e, c, d):
    # rearrange curve to x = g(y): real branches on [c,d]
    k = e.find('=')
    if k < 0:
        e = 'y=' + e
        k = 1
    if e[:k].strip() == 'x' and not has(e[k + 1:], 'x'):
        return [e[k + 1:]]
    m = '((' + c + ')+(' + d + '))/2'
    bs = []
    for b in parse_list(Gs('solve(' + lhs0(e) + '=0,x)')):
        if b and not bad(b) and not has(b, 'x') and \
                F('subst(' + b + ',y=' + m + ')') is not None:
            bs.append(b)
    if bs:
        out('x = ' + ' or '.join([ps(b) for b in bs]))
    else:
        out('Cannot make x the subject')
    return bs


def _pick(bs, c, d):
    if len(bs) < 2:
        return bs[0]
    m = '((' + c + ')+(' + d + '))/2'
    df = 1
    for i in range(len(bs)):
        if F('subst(' + bs[i] + ',y=' + m + ')') > 0:
            df = i + 1
            break
    i = int(ask('Which x (1-' + str(len(bs)) + ')', str(df), 0)) - 1
    g = bs[max(0, min(i, len(bs) - 1))]
    out('x = ' + ps(g))
    return g


def area_y():
    hdr('Area curve/y-axis')
    e = _ex1(norm(ask('Curve (y=.. or x=..)', '', '')))
    c = _n('y from', '', 0)
    d = _n('y to', '', 0)
    bs = _xofy(e, c, d)
    if bs:
        g = _pick(bs, c, d)
        A, B = _lm(c, d)
        if not _oos(g, 'y', c, d):
            _ans('A', _area(g, 'y', A, B))
    wait()


def _sq(z):
    r = G('expand(lin(expand((' + z + ')^2)))')
    n = Gs('normal(' + r + ')')
    return n if n and len(n) < len(r) else r


def _sq1(z):
    # z^2 as written: x^2, sin(x)^2, (sqrt(x))^2
    k = z.find('(')
    c = k > 0 and z[:k].isalpha() and z[:k] not in ('sqrt', 'exp') and unwrap(z[k:]) != z[k:]
    return z + '^2' if isnum(z) or z.isalpha() or c else '(' + z + ')^2'


def volume():
    hdr('Volume of revolution')
    pi = pp('pi')
    if ask('Axis (x/y)', 'x', 0)[:1].lower() == 'y':
        e = _ex1(norm(ask('Curve (y=.. or x=..)', '', '')))
        a = _n('y from', '', 0)
        b = _n('y to', '', 0)
        v = 'y'
        fd = 'x^2'
        bs = _xofy(e, a, b)
        if not bs:
            wait()
            return
        sq = [_sq(z) for z in bs]
        ns = [N(q) for q in sq]
        if ns.count(ns[0]) < len(ns):
            sq = [_sq(_pick(bs, a, b))]
        sq.sort(key=len)
        R = sq[0]
    else:
        f = _fx('y = f(x) =', '', 0)
        a = _n('x from', '', 0)
        b = _n('x to', '', 0)
        g = _fx('Inner y2 = (blank=none)', '', 0)
        v = _var(f + '+' + g)
        R = _sq(f)
        fd = pp(_sq1(f))
        if g:
            fd = '(' + ps(_sq1(f) + '-' + _sq1(g)) + ')'
            R = G('(' + R + ')-(' + _sq(g) + ')')
    lim = pi + ' ' + _il(a, b)
    out('V = ' + lim + fd + ' d' + v)
    if fd.replace(' ', '') != _pa(R).replace(' ', ''):
        out('= ' + lim + _pa(R) + ' d' + v)
    if _oos(R, v, a, b):
        wait()
        return
    Fx = _anti(R, v)
    if Fx:
        r = _fab(Fx, v, a, b, pi, 1)
    else:
        r = _gdc(R, v, a, b)
        out('= ' + pi + '(' + _q(r) + ')')
    _ans('V', _S('(' + r + ')*pi'))
    wait()


def kin_v():
    hdr('Kinematics from v(t)')
    h = _fx('v(t) =', '', 0)
    a = _n('t from', '0', 0)
    b = _n('t to', '', 0)
    A = _pt(a)
    B = _pt(b)
    if A[1] > B[1]:
        out('Need t1 < t2')
        wait()
        return
    lim = _il(a, b)
    out('Displacement = ' + lim + _pa(h) + ' dt')
    if _oos(h, 't', a, b):
        wait()
        return
    Fx = _anti(h, 't')
    r = _fab(Fx, 't', a, b, '', 1) if Fx else _gdc(h, 't', a, b)
    _ans('displacement', r)
    out('Distance = ' + lim + '|' + ps(h) + '| dt')
    if _roots(h, 't', A, B):
        _ans('distance', _area(h, 't', A, B, Fx, 'd'))
    else:
        out('v does not change sign: d = |displacement|')
        _ans('distance', r if (F(r) or 0) >= 0 else _S('-(' + r + ')'))
    wait()


def kin_a():
    hdr('Kinematics from a(t)')
    h = _fx('a(t) =')
    t0 = _n('t0', '0', 0)
    v0 = _n('v(t0) =', '', 0)
    r = _bc(h, 't', t0, v0, 'v')
    s0 = ask('s(t0) = (blank=skip)', '', 0)
    if r and s0:
        _bc(r, 't', t0, _ex1(norm(s0)), 's')
    wait()


ITEMS = [('Definite integral', defint), ("f from f' & point", antider),
         ('Area curve/x-axis', area_x), ('Area two curves', area_2),
         ('Area curve/y-axis', area_y), ('Volume revolution', volume),
         ('Kinematics v(t)', kin_v), ('Kinematics a(t)', kin_a)]
