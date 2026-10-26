# ibtrig.py - triangles, arcs/sectors, 3D solids (AA 3.1-3.4)
from ibcore import *
import math

TITLE = 'Trig/geometry'
LS = 'abc'
LA = 'ABC'
DS = ['']  # degree sign after angles (uni + degree mode only)


def _isx(r):
    for k in ('asin', 'acos', 'atan', 'sin(', 'cos(', 'tan(', '.'):
        if k in r:
            return False
    return True


def _S(e):
    r = S(e)
    if has_var(r):
        return r
    if not _isx(r):
        t = Gs('normal(texpand(' + r + '))')
        if t and _isx(t):
            r = t
    if '+' in r[1:] or '-' in r[1:]:
        f = Gs('factor(' + r + ')')
        if f and len(f) < len(r):
            r = f
    return r


def _ok(r, a=0):
    # a clean exact value: short, no decimals/trig, no nested roots (a: an answer, nested roots stay)
    if not _isx(r) or len(r) > 23:
        return False
    if a:
        return True
    i = r.find('sqrt(')
    while i >= 0:
        d = 0
        for j in range(i + 4, len(r)):
            d += (r[j] == '(') - (r[j] == ')')
            if d == 0:
                break
        if 'sqrt(' in r[i + 5:j]:
            return False
        i = r.find('sqrt(', i + 5)
    return True


def _ps(r):
    # exact value with spaced signs, a leading negative term last: -sqrt(3)+3 -> 3 - sqrt(3)
    t = split_terms(r)
    if len(t) == 2 and t[0][0] == '-' and t[1][0] != '-':
        t.reverse()
    return join_signed([pp(x) for x in t])


def _q(r, a=0):
    # exact if clean, else 3 s.f.
    if _ok(r, a):
        return _ps(r)
    v = F(r)
    return pp(r) if v is None else sf3(v)


def _n(x, a=0):
    # a value as typed if short (3.0 -> 3), else as _q
    if isnum(x) and len(x) < 7:
        return pp(x[:-2] if x[-2:] == '.0' else x)
    return _q(x, a)


def _ag(r):
    return _n(r) + DS[0]


def _br(x):
    return '(' + _n(x) + ')'


def _pa(v):
    # bracketed unless a plain positive number
    return pp(v) if isnum(v) and '/' not in v and v[:1] != '-' else '(' + pp(v) + ')'


def _p2(x):
    # x^2 as written: 3^2 (11.6^2 for a decimal), else the value of the square
    if isnum(x) and '/' not in x or not _ok(x):
        return _n(x) + '^2'
    return _q(_S('(' + x + ')^2'))


def _sh(l, e, u='', z='', d=1):
    # working line: label = exact (= 3sf), or 3sf when not exact
    # u: unit after the numbers, z: note at the end, d=0: no decimal after exact
    r = _S(e)
    v = F(r)
    t = l + ' = '
    if _ok(r):
        t += _ps(r) + u
        if d and not isnum(r) and v is not None:
            t += ' = ' + sf3(v) + u
    elif v is not None:
        t += sf3(v) + u
    else:
        t += pp(r)
    if z and len(t) <= CFG['w'] < len(t + z):
        out(t)
        t = z
        z = ''
    out(t + z)
    return r


def _dc(a, s):
    # '~' line: 3 s.f. of the exact irrational values in a = [(label, value)]
    d = [n + s + sf3(F(v)) for n, v in a if _ok(v, 1) and not isnum(v) and F(v) is not None]
    if d:
        out('     ~ ' + ', '.join(d))


def _dg(d):
    return ask('Deg or rad (d/r)', d, 0).lower()[:1] == 'd'


def _dgs():
    return '°' if CFG['uni'] else ' deg'


def _o2(k):
    return [i for i in range(3) if i != k]


# ---------- triangle ----------
def _sr(s, g, i, j, U, z=''):
    # sine rule: side j from known pair i
    s[j] = _sh(LS[j] + ' = ' + pp(s[i]) + 'sin(' + _ag(g[j]) + ')/sin(' + _ag(g[i]) + ')',
               '(' + s[i] + ')*sin((' + g[j] + ')' + U + ')/sin((' + g[i] + ')' + U + ')', '', z)


def _as(g, m, H):
    i, j = _o2(m)
    g[m] = _sh(LA[m] + ' = ' + pp(H) + DS[0] + ' - ' + _ag(g[i]) + ' - ' + _ag(g[j]),
               H + '-(' + g[i] + ')-(' + g[j] + ')', DS[0])


def _ca(s, g, j, D, z=''):
    # cosine rule for angle j
    p, q = _o2(j)
    c = _sh('cos' + LA[j] + ' = (' + _p2(s[p]) + ' + ' + _p2(s[q]) + ' - ' + _p2(s[j]) + ')/(2'
            + _br(s[p]) + _br(s[q]) + ')',
            '((' + s[p] + ')^2+(' + s[q] + ')^2-(' + s[j] + ')^2)/(2*(' + s[p] + ')*(' + s[q] + '))', '', z)
    g[j] = _sh(LA[j] + ' = arccos(' + _q(c) + ')', 'acos(' + c + ')' + D, DS[0])


def _cs(s, g, j, U, z=''):
    # cosine rule for side j
    p, q = _o2(j)
    J = LS[j]
    a2 = _sh(J + '^2 = ' + _p2(s[p]) + ' + ' + _p2(s[q]) + ' - 2' + _br(s[p]) + _br(s[q]) + 'cos(' + _ag(g[j]) + ')',
             '(' + s[p] + ')^2+(' + s[q] + ')^2-2*(' + s[p] + ')*(' + s[q] + ')*cos((' + g[j] + ')' + U + ')', '', z)
    s[j] = _sh(J, 'sqrt(' + a2 + ')')


def _fin(s, g, U, t=''):
    i = 0
    for k in range(3):
        if len(g[k]) < len(g[i]):
            i = k
    p, q = _o2(i)
    ar = _sh('Area = (1/2)' + _br(s[p]) + _br(s[q]) + 'sin(' + _ag(g[i]) + ')',
             '(' + s[p] + ')*(' + s[q] + ')*sin((' + g[i] + ')' + U + ')/2', '', '', 0)
    out('ANS' + t + ': ' + ', '.join([LS[k] + '=' + _n(s[k], 1) for k in range(3)]))
    out('  ' + ', '.join([LA[k] + '=' + _ag(g[k]) for k in range(3)]) + ', Area=' + _q(ar, 1))
    _dc([(LS[k], s[k]) for k in range(3)] + [(LA[k], g[k]) for k in range(3)] + [('Area', ar)], '=')


def _tn(bs, n, g, s, j):
    # triangle n + 1 of those in bs: copies of g, s with angle j = bs[n], heading printed
    g2 = g[:]
    g2[j] = bs[n]
    t = ' ' + str(n + 1) if len(bs) > 1 else ''
    if t:
        out('Triangle' + t + ': ' + LA[j] + ' = ' + _ag(bs[n]))
    return g2, s[:], t


def _tri():
    dg = _dg('d')
    DS[0] = '°' if dg and CFG['uni'] else ''
    U = '*pi/180' if dg else ''
    D = '*180/pi' if dg else ''
    H = '180' if dg else 'pi'
    s = [askn(c + ' (blank) =', '', 0) for c in LS]
    g = [askn(c + ' (blank) =', '', 0) for c in LA]
    gv = [LS[i] + ' = ' + pp(s[i]) for i in range(3) if s[i]]
    gv += [LA[i] + ' = ' + pp(g[i]) + DS[0] for i in range(3) if g[i]]
    if gv:
        out(', '.join(gv))
    for v in s + g:
        if v and (F(v) or 0) <= 0:
            out('Values must be > 0')
            return
    ks = [i for i in range(3) if s[i]]
    ka = [i for i in range(3) if g[i]]
    sm = 0
    for i in ka:
        sm += F(g[i])
    h = F(H)
    if (len(ka) == 3 and abs(sm - h) > 1e-9) or (len(ka) < 3 and sm >= h - 1e-9):
        out('Bad angle sum (' + pp(H) + DS[0] + ')')
        return
    if len(ks) == 3:
        x = [F(v) for v in s]
        k = x.index(max(x))
        if 2 * x[k] >= sum(x) - 1e-12:
            p, q = _o2(k)
            out('No triangle: ' + pp(s[p]) + ' + ' + pp(s[q]) + (' < ' if 2 * x[k] > sum(x) + 1e-12 else ' = ') + pp(s[k]))
            return
        _ca(s, g, k, D, '  (cosine rule)')
        j = (k + 1) % 3
        _ca(s, g, j, D)
        _as(g, 3 - k - j, H)
        _fin(s, g, U)
        return
    if len(ka) >= 2 and ks:
        if len(ka) == 2:
            _as(g, 3 - ka[0] - ka[1], H)
        z = '  (sine rule)'
        for j in range(3):
            if not s[j]:
                _sr(s, g, ks[0], j, U, z)
                z = ''
        _fin(s, g, U)
        return
    ar = askn('Area (blank)', '', 0) if len(ks) == 2 and not ka else ''
    if ar:
        # two sides + area: sinC = 2 Area/(ab), two possible C
        p, q = ks
        m = 3 - p - q
        out('(1/2)' + _br(s[p]) + _br(s[q]) + 'sin' + LA[m] + ' = ' + pp(ar))
        sv = _sh('sin' + LA[m], '2*(' + ar + ')/((' + s[p] + ')*(' + s[q] + '))')
        bs = _amb(sv, m, '', D, H, h)
        for n in range(len(bs)):
            g2, s2, t = _tn(bs, n, g, s, m)
            _cs(s2, g2, m, U, '' if n else '  (cosine rule)')
            _ca(s2, g2, p, D)
            _as(g2, q, H)
            _fin(s2, g2, U, t)
        return
    if len(ks) != 2 or len(ka) != 1:
        out('Not enough data (need 3 incl. a side)')
        return
    k = ka[0]
    if not s[k]:
        _cs(s, g, k, U, '  (cosine rule)')
        j = _o2(k)[0]
        _ca(s, g, j, D)
        _as(g, 3 - k - j, H)
        _fin(s, g, U)
        return
    j = ks[0] if ks[0] != k else ks[1]
    m = 3 - k - j
    sv = _sh('sin' + LA[j] + ' = ' + pp(s[j]) + 'sin(' + _ag(g[k]) + ')/' + pp(s[k]),
             '(' + s[j] + ')*sin((' + g[k] + ')' + U + ')/(' + s[k] + ')', '', '  (sine rule)')
    bs = _amb(sv, j, g[k], D, H, h)
    for n in range(len(bs)):
        g2, s2, t = _tn(bs, n, g, s, j)
        _as(g2, m, H)
        _sr(s2, g2, k, m, U)
        _fin(s2, g2, U, t)


def _amb(sv, j, gk, D, H, h):
    # angle j from sin value sv: arcsin or H - arcsin; check sum with angle gk
    x = F(sv)
    if x > 1 + 1e-9:
        out('sin' + LA[j] + ' > 1: no triangle')
        return []
    if abs(x - 1) < 1e-9:
        c = [_S(H + '/2')]
        out(LA[j] + ' = ' + pp(c[0]) + DS[0] + ' (right angle)')
    else:
        b1 = _S('asin(' + sv + ')' + D)
        c = [b1, _S(H + '-(' + b1 + ')')]
        out(LA[j] + ' = arcsin(' + _q(sv) + ') = ' + _ag(b1))
        out('or ' + LA[j] + ' = ' + pp(H) + DS[0] + ' - ' + _ag(b1) + ' = ' + _ag(c[1]))
    bs = []
    for b in c:
        ok = 1
        if gk:
            t = F(gk + '+' + b)
            ok = t < h - 1e-9
            out(_ag(gk) + ' + ' + _ag(b) + ' = ' + sf3(t) + DS[0] + (' < ' if ok else ' >= ')
                + pp(H) + DS[0] + ('' if ok else ': reject'))
        if ok:
            bs.append(b)
    if not bs:
        out('No triangle')
    if len(bs) == 2:
        out('Two triangles')
    return bs


def tri_solve():
    hdr('Triangle')
    _tri()
    wait()


# ---------- arc / sector ----------
EQ = {'l': 'r*t', 'A': 'r^2*t/2', 'P': '2*r+r*t'}


def _th():
    return 'θ' if CFG['uni'] else 'theta'


def _eq(n):
    # sector equation for display (l = r theta ...)
    T = _th()
    s = '' if CFG['uni'] else ' '
    return {'l': 'r' + s + T, 'A': 'r^2 ' + T + '/2', 'P': '2r + r' + s + T}[n]


def _tt(s):
    # the variable t -> theta (not the t of sqrt)
    o = ''
    for i in range(len(s)):
        if s[i] == 't' and (i == 0 or s[i - 1] not in LET) and (i == len(s) - 1 or s[i + 1] not in LET):
            o += _th()
        else:
            o += s[i]
    return o


def _cv(t):
    # degrees -> radians working line
    return _sh(_th() + ' = ' + pp(t) + (' × ' if CFG['uni'] else ' x ') + pp('pi/180'),
               '(' + t + ')*pi/180', '', '', 0)


def _sec(r, t):
    R = _br(r)
    l = _sh('l = ' + _pa(r) + _br(t), '(' + r + ')*(' + t + ')', '', '', 0)
    a = _sh('A = (1/2)' + R + '^2' + _br(t), '(' + r + ')^2*(' + t + ')/2', '', '', 0)
    p = _sh('P = 2' + R + ' + ' + _n(l), '2*(' + r + ')+' + l, '', '', 0)
    h = _S('(' + t + ')/2')
    _sh('chord = 2' + R + 'sin(' + pp(h) + ')', '2*(' + r + ')*sin(' + h + ')')
    _sh('Segment = (1/2)' + R + '^2(' + pp(t) + ' - sin(' + pp(t) + '))',
        '(' + r + ')^2*((' + t + ')-sin(' + t + '))/2')
    out('ANS: l = ' + _q(l, 1) + ', A = ' + _q(a, 1) + ', P = ' + _q(p, 1))
    _dc([('l', l), ('A', a), ('P', p)], ' = ')


def _sec2(dg):
    T = _th()
    s = ask('Known e.g. l=5,A=10', '', 0)
    kv = {}
    for p in split_top(s, ','):
        k = p.find('=')
        n = p[:k].strip()
        if n in ('theta', 't', 'θ'):
            n = 't'
        if k < 1 or n not in 'rtlAP':
            out('Names: r,theta,l,A,P')
            return []
        kv[n] = norm(p[k + 1:])
    if len(kv) != 2:
        out('Give exactly two values')
        return []
    out(', '.join([(T if n == 't' else n) + ' = ' + pp(kv[n]) + (DS[0] if n == 't' else '') for n in 'rtlAP' if n in kv]))
    if 't' in kv and dg:
        kv['t'] = _cv(kv['t'])
    ns = [n for n in 'lPA' if n in kv]
    for n in ns:
        out(_eq(n) + ' = ' + pp(kv[n]))
    if 'r' in kv and 't' in kv:
        return [[kv['r'], kv['t'], 0]]
    n = ns[0]
    if 'r' in kv or 't' in kv:
        k = 'r' if 'r' in kv else 't'
        v = 't' if k == 'r' else 'r'
        e = _S('subst(' + EQ[n] + ',' + k + '=' + kv[k] + ')')
        out(_tt(pp(e)) + ' = ' + pp(kv[n]))
        rs = GL('solve(' + e + '=' + kv[n] + ',' + v + ')')
        prs = [[kv['r'], x, 1] if k == 'r' else [x, kv['t'], 0] for x in rs]
    else:
        m = ns[1]
        ts = GL('solve(' + EQ[n] + '=' + kv[n] + ',t)')[0]
        out(T + ' = ' + pp(ts))
        e = _S('subst(' + EQ[m] + ',t=' + ts + ')')
        out(pp(e) + ' = ' + pp(kv[m]))
        rs = GL('solve(' + e + '=' + kv[m] + ',r)')
        prs = [[x, _S('subst(' + ts + ',r=' + x + ')'), 1] for x in rs]
    ok = []
    for x in prs:
        a = F(x[0])
        b = F(x[1])
        g = a is not None and b is not None and a > 0 and 0 < b <= 2 * math.pi + 1e-9
        out('r = ' + _q(x[0]) + ', ' + T + ' = ' + _q(x[1]) + ('' if g else ' (rejected)'))
        if g:
            ok.append(x)
    if not ok:
        out('No valid sector')
    return ok


def arc_sector():
    hdr('Arc/sector')
    m = ask('1)r,theta 2)any two known', '1', 0)
    dg = _dg('r')
    DS[0] = '°' if dg and CFG['uni'] else ''
    if m == '2':
        prs = _sec2(dg)
    else:
        r = askn('r =', '', 0)
        t = askn('theta =', '', 0)
        out('r = ' + pp(r) + ', ' + _th() + ' = ' + pp(t) + DS[0])
        if dg:
            t = _cv(t)
        prs = [[r, t, 0]]
    for x in prs:
        if (F(x[0]) or 0) <= 0 or not 0 < (F(x[1]) or 0) <= 2 * math.pi + 1e-9:
            out('Need r > 0, 0 < theta <= 2pi')
            break
        if len(prs) > 1:
            out('r = ' + _q(x[0]) + ':')
        _sec(x[0], x[1])
        if dg and x[2]:
            out('  ' + _th() + ' = ' + sf3(F(x[1]) * 180 / math.pi) + _dgs())
    wait()


# ---------- 3D solids ----------
SOL = (('Cuboid', 'lwh', ('V=l w h', 'SA=2(l w + l h + w h)')),
       ('Cylinder', 'rh', ('V=pi r^2 h', 'SA=2pi r^2 + 2pi r h')),
       ('Cone', 'rh', ('l=sqrt(r^2 + h^2)', 'V=(1/3)pi r^2 h', 'SA=pi r^2 + pi r l')),
       ('Sphere', 'r', ('V=(4/3)pi r^3', 'SA=4pi r^2')),
       ('Hemisphere', 'r', ('V=(2/3)pi r^3', 'SA=2pi r^2 + pi r^2')),
       ('Pyramid', 'lwh', ('s=sqrt(h^2 + (w/2)^2)', 't=sqrt(h^2 + (l/2)^2)',
                                'edge=sqrt(h^2 + (l/2)^2 + (w/2)^2)', 'V=(1/3)l w h',
                                'SA=l w + l s + w t')))


def _sub(f, v):
    # formula with values put in: a plain number is bare beside an operator
    # (x*y in a product without pi), else values are bracketed
    o = ''
    n = len(f)
    for i in range(n):
        c = f[i]
        if c in v and (i == 0 or f[i - 1] not in LET) and (i == n - 1 or f[i + 1] not in LET):
            a = f[:i].rstrip()[-1:]
            b = f[i + 1:].lstrip()[:1]
            x = v[c]
            pl = isnum(x) and '/' not in x and x[:1] != '-'
            if pl and a in '(+-/' and b in ')^+-/':
                o += x
            elif pl and 'pi' not in f:
                o += ('*' if a and a in LET + ')' else '') + x
            else:
                o += '(' + x + ')'
        elif c != ' ':
            o += c
    return o


def _solid():
    k = ask('Solid 1)cuboid 2)cyl 3)cone 4)sphere 5)hemi 6)pyramid', '1', 0)
    if k not in '123456' or len(k) != 1:
        out('Choose 1-6')
        return
    k = int(k) - 1
    nm, vs, ls = SOL[k]
    v = {}
    for c in vs:
        v[c] = askn(c + (' (blank: slant)' if k == 2 and c == 'h' else '') + ' =', '', 0)
    ls = list(ls)
    if k == 1:
        e = ask('Ends (0/1/2)', '2', 0)
        ls[1] = 'SA=' + ('' if e == '0' else (e + 'pi r^2 + ').replace('1pi', 'pi')) + '2pi r h'
        if e != '2':
            nm += ' (' + e + (' end)' if e == '1' else ' ends)')
    if k == 2 and not v['h']:
        del v['h']
        v['l'] = askn('l =', '', 0)
        ls[0] = 'h=sqrt(l^2 - r^2)'
    out(nm + ': ' + ', '.join([c + ' = ' + pp(v[c]) for c in vs + 'l' * (k == 2) if c in v and v[c]]))
    for c in v:
        if (F(v[c]) or 0) <= 0:
            out('Bad input')
            return
    if k == 2 and 'l' in v and F(v['l']) <= F(v['r']):
        out('Need l > r')
        return
    for f in ls:
        i = f.find('=')
        lb = f[:i]
        x = f[i + 1:]
        e = norm(x)
        ks = [c for c in v if has(e, c)]
        sb = 'subst(' + e + ',[' + ','.join(ks) + '],[' + ','.join(['(' + v[c] + ')' for c in ks]) + '])'
        t = lb + ' = ' + ps(_sub(x, v))
        if lb in ('V', 'SA'):
            out(t)
            ans(lb, join_signed(split_terms(_S(sb))))
        else:
            r = _sh(t, sb)
            if len(lb) == 1:
                v[lb] = r


def _pt(n):
    p = askv(n + ' (x,y,z)', '', 0)
    while len(p) < 3:
        p.append('0')
    return p


def _gv(*a):
    # given points: A(1, 2, 3), B(4, 6, 15)
    out(', '.join([n + '(' + ', '.join([pp(c) for c in p]) + ')' for n, p in a]))


def _df(A, B):
    return [_S('(' + B[i] + ')-(' + A[i] + ')') for i in range(3)]


def _ng(v):
    # bracketed when negative
    return '(' + pp(v) + ')' if v[:1] == '-' else pp(v)


def _dd(b, a):
    # (x2 - x1) as typed
    return _pa(b) if a == '0' else '(' + pp(b) + ' - ' + _ng(a) + ')'


def _ds(lb, A, B):
    d = _df(A, B)
    z = [x for x in d if F(x) != 0]
    return _sh(lb + ' = sqrt(' + (' + '.join([_pa(x) + '^2' for x in z]) if z else '0') + ')',
               'sqrt(' + '+'.join(['(' + x + ')^2' for x in d]) + ')')


def _an(lb, fn, v):
    r = _S(fn + '(' + v + ')')
    x = F(r)
    t = 'ANS: ' + lb + ' = arc' + fn[1:] + '(' + _q(v) + ')'
    if _isx(r):
        t += ' = ' + pp(r)
    out(t)
    out('  = ' + sf3(x) + ' rad = ' + sf3(x * 180 / math.pi) + _dgs())


def solid_3d():
    hdr('3D solids')
    o = ask('1)dist/mid 2)vol/SA 3)line-plane angle 4)angle PQR', '1', 0)
    if o == '2':
        _solid()
    elif o == '3':
        P = _pt('P')
        Q = _pt('Q')
        _gv(('P', P), ('Q', Q))
        out('F = (' + pp(Q[0]) + ', ' + pp(Q[1]) + ', ' + pp(P[2]) + ')  (below Q)')
        qf = _sh('QF = |' + pp(Q[2]) + ' - ' + _ng(P[2]) + '|', 'abs((' + Q[2] + ')-(' + P[2] + '))')
        pf = _ds('PF', P, [Q[0], Q[1], P[2]])
        if F(pf) == 0:
            out('ANS: ' + _th() + ' = 90' + _dgs() + ' (PQ vertical)')
        else:
            tn = _sh('tan ' + _th(), '(' + qf + ')/(' + pf + ')')
            _an(_th(), 'atan', tn)
    elif o == '4':
        P = _pt('P')
        Q = _pt('Q')
        R = _pt('R')
        _gv(('P', P), ('Q', Q), ('R', R))
        a = _ds('PQ', P, Q)
        b = _ds('QR', Q, R)
        c = _ds('PR', P, R)
        cv = _sh('cos PQR = (' + _p2(a) + ' + ' + _p2(b) + ' - ' + _p2(c) + ')/(2' + _br(a) + _br(b) + ')',
                 '((' + a + ')^2+(' + b + ')^2-(' + c + ')^2)/(2*(' + a + ')*(' + b + '))', '', '  (cosine rule)')
        _an('PQR', 'acos', cv)
    else:
        A = _pt('A')
        B = _pt('B')
        _gv(('A', A), ('B', B))
        d = _df(A, B)
        out('d = sqrt(' + ' + '.join([_dd(B[i], A[i]) + '^2' for i in range(3)]) + ')')
        sq = [_S('(' + x + ')^2') for x in d]
        out(' = sqrt(' + ' + '.join([_n(x) for x in sq]) + ')')
        ans('d', _S('sqrt(' + '+'.join(sq) + ')'))
        out('M = (' + ', '.join(['(' + pp(A[i]) + ' + ' + _ng(B[i]) + ')/2' for i in range(3)]) + ')')
        out('ANS: M = (' + ', '.join([pp(_S('((' + A[i] + ')+(' + B[i] + '))/2')) for i in range(3)]) + ')')
    wait()


ITEMS = [('Triangle solver', tri_solve), ('Arc/sector', arc_sector), ('3D solids', solid_3d)]
