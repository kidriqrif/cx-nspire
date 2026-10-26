# ibfun2.py - lines, composite/inverse, rational functions, odd/even
# (AA 2.1-2.3, 2.13, 2.14); inequalities/modulus are in ibfun3.py
from ibcore import *

TITLE = 'Lines/comp/rational'


def _sb(s, v, w='x'):
    # replace standalone w in s by v, bracketed unless it reads fine bare:
    # 2^3, 2(2), 3y, sqrt(x) + 1 but (x + 1)^2, (-1)^2
    o = ''
    n = len(s)
    k = v.find('(')
    nm = isnum(v) and v[0] != '-' and '/' not in v
    at = v.isalpha() or k > 0 and v[:k].isalpha() and unwrap(v[k:]) == v[k + 1:-1]
    for i in range(n):
        c = s[i]
        if c == w and (i == 0 or s[i - 1] not in LET) and \
                (i + 1 >= n or s[i + 1] not in LET):
            p = s[i - 1] if i else ' '
            o += v if (0 < i < n - 1 and p == '(' and s[i + 1] == ')') or \
                at or nm and p not in DIG else '(' + v + ')'
        else:
            o += c
    return o


def _rt(s):
    # sqrt of an already pretty expression
    return ('√(' if CFG['uni'] else 'sqrt(') + s + ')'


def _pa(v):
    # bracket negatives, fractions and sums
    v = pp(v)
    return '(' + v + ')' if v[:1] == '-' or '/' in v or len(split_terms(v)) > 1 else v


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


def _br(s, dn=1):
    # bracket a displayed sum (or, in a denominator, a product) for a fraction
    return '(' + s + ')' if len(split_terms(s)) > 1 or dn and ('(' in s[1:] or '*' in s or
                                                                s[:1] == '-' or s[:1] in DIG and has_var(s)) else s


def _fd(n, d):
    # factorised n/d for display
    t = _pf(G('factor(' + n + ')'))
    return _br(t, 0) + '/' + _br(_pf(G('factor(' + d + ')'))) if d != '1' else t


def _dt(s, w):
    # 'x>=(1/2)' -> 'w >= 1/2', 'x<>2' -> 'w != 2'
    for o in ('<>', '<=', '>=', '<', '>'):
        k = s.find(o)
        if k > 0 and s[:k] == 'x':
            return w + ' ' + {'<>': '!='}.get(o, o) + ' ' + pp(unwrap(s[k + len(o):]))
    return pp(s).replace('<>', ' != ').replace('x', w)


def _zs(e):
    # real zeros of e (exact, else numeric GDC), sorted
    r = GL('solve(' + e + '=0,x)')
    for t in r:
        if bad(t):
            r = GL('fsolve(' + e + '=0,x)')
            break
    r.sort(key=lambda t: F(t))
    return r


def _at(e, z):
    # exact value of e at x = z (re-parsed so Giac evaluates it)
    return S('(' + G('subst(' + e + ',x=' + z + ')') + ')')


def _lst(r):
    return ', '.join([sf3(F(t)) if '.' in t else pp(t) for t in r])


def _pt(lbl, x, y):
    # point answer, 3 s.f. if irrational
    ans(lbl, '(' + x + ', ' + y + ')', 0)
    if not (isnum(x) and isnum(y)):
        out('     ~ (' + sf3(F(x)) + ', ' + sf3(F(y)) + ')')


def _frm(m, a, b):
    # line through (a,b) gradient m: point-slope and general form, returns y = f(x)
    # (the caller's ANS line gives y = mx + c)
    if m == '0':
        return b
    k = pp(m)
    k = '' if m == '1' else '-' if m == '-1' else '(' + k + ')' if '/' in k or len(split_terms(m)) > 1 else k
    X = join_signed(['x', pp(N('-(' + a + ')'))])
    t = join_signed(['y', pp(N('-(' + b + ')'))]) + ' = ' + k + (X if X == 'x' else '(' + X + ')')
    e = N('(' + m + ')*(x-(' + a + '))+(' + b + ')')
    if 'y = ' + ps(e) != t:
        out(t)
    g = G('numer(normal(' + e + '-y))')
    c = F(G('coeff(' + g + ',x,1)'))
    if c < 0 or c == 0 and g[0] == '-':
        g = G('-(' + g + ')')
    out(ps(g) + ' = 0')
    return e


def _gy(l):
    # line eq -> y = expr (prints it, with m) or None if vertical
    e = lhs0(norm(l))
    if not has(e, 'y'):
        return None
    r = G('expand(' + GL('solve(' + e + '=0,y)')[0] + ')')
    out('y = ' + ps(r) + ', m = ' + pp(G('diff(' + r + ',x)')))
    return r


def _vx(l):
    return GL('solve(' + lhs0(norm(l)) + '=0,x)')[0]


def lines():
    hdr('Lines')
    m = ask('1 two points 2 para/perp 3 meet', '1', 0)
    if m == '2':
        l = ask('Line', '', 0)
        P = askv('Point (x1,y1)', '', 0)
        t = yes('Perpendicular', 'n')
        r = _gy(l)
        k = None
        if r is None:
            out('x = ' + pp(_vx(l)) + ': vertical line, m undefined')
            if t:
                k = '0'
        else:
            k = G('diff(' + r + ',x)')
            if t and k == '0':
                k = None
            elif t:
                k = N('-1/(' + k + ')')
                out('m2 = -1/m1 = ' + pp(k))
        if not (t and r and k):
            out(('Perpendicular' if t else 'Parallel') + ': ' +
                ('vertical' if k is None else 'm = ' + pp(k)))
        out('through (' + ', '.join([pp(u) for u in P]) + ')')
        if k is None:
            ans('x', P[0])
        elif k == '0':
            ans('y', P[1])
        else:
            ans('y', ps(_frm(k, P[0], P[1])))
    elif m == '3':
        l1 = ask('Line 1', '', 0)
        l2 = ask('Line 2', '', 0)
        r1 = _gy(l1)
        r2 = _gy(l2)
        if r1 is None and r2 is None:
            out('x = ' + pp(_vx(l1)) + ', x = ' + pp(_vx(l2)) + ': both vertical, ' +
                ('same line' if _vx(l1) == _vx(l2) else 'parallel, no intersection'))
            wait()
            return
        if r1 and r2:
            if N('diff(' + r1 + '-(' + r2 + '),x)') == '0':
                out('Same m: ' + ('same line' if N(r1 + '-(' + r2 + ')') == '0' else 'parallel, no intersection'))
                wait()
                return
            out(ps(r1) + ' = ' + ps(r2))
            x = GL('solve(' + r1 + '=' + r2 + ',x)')[0]
        else:
            x = _vx(l2 if r2 is None else l1)
            r1 = r1 or r2
            out('Vertical line x = ' + pp(x))
        out('x = ' + pp(x))
        y = S('subst(' + r1 + ',x=' + x + ')')
        out('y = ' + _sb(ps(r1), pp(x)) + ' = ' + pp(y))
        _pt('Point', x, y)
    else:
        A = askv('A (x1,y1)', '', 0)
        B = askv('B (x2,y2)', '', 0)
        dx = N('(' + B[0] + ')-(' + A[0] + ')')
        dy = N('(' + B[1] + ')-(' + A[1] + ')')
        out('A(' + ', '.join([pp(u) for u in A]) + '), B(' + ', '.join([pp(u) for u in B]) + ')')
        out('m = (y2 - y1)/(x2 - x1)')
        out(' = (' + pp(B[1]) + ' - ' + _pa(A[1]) + ')/(' + pp(B[0]) + ' - ' + _pa(A[0]) + ')')
        if dx + dy == '00':
            out('A = B: no unique line')
        elif dx == '0':
            out('x2 - x1 = 0: vertical line')
            ans('x', A[0])
        else:
            k = N('(' + dy + ')/(' + dx + ')')
            out(' = ' + ('(' + pp(dy) + ')' if '/' in dy else pp(dy)) + '/' + _pa(dx) + ' = ' + pp(k))
            ans('y', ps(_frm(k, A[0], A[1])))
        out('M = ((x1 + x2)/2, (y1 + y2)/2)')
        out(' = ((' + join_signed([pp(A[0]), pp(B[0])]) + ')/2, (' + join_signed([pp(A[1]), pp(B[1])]) + ')/2)')
        _pt('M', N('((' + A[0] + ')+(' + B[0] + '))/2'), N('((' + A[1] + ')+(' + B[1] + '))/2'))
        q = N('(' + dx + ')^2+(' + dy + ')^2')
        out('d = ' + _rt('(x2 - x1)^2 + (y2 - y1)^2'))
        out(' = ' + _rt(_pa(dx) + '^2 + ' + _pa(dy) + '^2') + ' = ' + _rt(pp(q)))
        ans('d', S('sqrt(' + q + ')'))
    wait()


def _inv(f):
    # inverse of f: swap x,y and isolate y; returns candidate list
    out('y = ' + ps(f))
    A = _sb(f, 'y')
    out('x = ' + ps(A) + '  (swap x, y)')
    B = 'x'
    for it in range(10):
        A = unwrap(A)
        if A == 'y':
            return [B]
        t = split_terms(A)
        if len(t) > 1:
            yt = [u for u in t if has(u, 'y')]
            if len(yt) != 1:
                break
            B = S('(' + B + ')-(' + '+'.join(['(' + u + ')' for u in t if not has(u, 'y')]) + ')')
            A = yt[0]
        else:
            ng, fs = split_factors(A)
            yf = [u for u in fs if has(u[1], 'y')]
            if len(yf) != 1:
                break
            c = ('-1' if ng else '1') + ''.join([o + '(' + u + ')' for o, u in fs if not has(u, 'y')])
            o, u = yf[0]
            if c != '1' or o == '/':
                B = S('(' + B + ')/(' + c + ')')
                if o == '/':
                    B = S('1/(' + B + ')')
                A = u
            else:
                u = unwrap(u)
                k = u.find('(')
                j = u.rfind('^')
                if k > 0 and u[-1] == ')' and unwrap(u[k:]) == u[k + 1:-1] and \
                        u[:k] in ('exp', 'ln', 'sqrt', 'log10'):
                    B = S({'exp': 'ln(B)', 'ln': 'exp(B)', 'sqrt': '(B)^2',
                           'log10': '10^(B)'}[u[:k]].replace('B', B))
                    A = u[k + 1:-1]
                elif j > 0 and has(u[:j], 'y') and not has(u[j + 1:], 'y'):
                    e = unwrap(u[j + 1:])
                    A = u[:j]
                    if e in ('2', '4'):
                        out(ps(unwrap(A)) + ' = ' + ('±' if CFG['uni'] else '+/-') +
                            pp(S('(' + B + ')^(1/' + e + ')')))
                        return GL('solve(x=' + _sb(f, 'y') + ',y)')
                    B = S('(' + B + ')^(1/(' + e + '))')
                elif j > 0 and has(u[j + 1:], 'y'):
                    B = S('ln(' + B + ')/ln(' + u[:j] + ')')
                    A = u[j + 1:]
                else:
                    break
        if unwrap(A) != 'y':
            out(ps(unwrap(A)) + ' = ' + ps(B))
    A = _sb(f, 'y')
    n = G('numer(' + A + ')')
    d = G('denom(' + A + ')')
    if has(d, 'y') and G('degree(' + n + ',y)') < '2' and G('degree(' + d + ',y)') == '1':
        a, b, c, e = [G('coeff(' + p + ',y,' + i + ')') for p, i in ((n, '1'), (n, '0'), (d, '1'), (d, '0'))]
        out('x(' + ps(d) + ') = ' + ps(n))
        out(ps(G('expand(x*(' + d + '))')) + ' = ' + ps(n))
        r = ps(G('expand(' + b + '-(' + e + ')*x)'))
        out(ps(G('expand(' + c + '*x*y-(' + a + ')*y)')) + ' = ' + r)
        out('y(' + ps(G(c + '*x-(' + a + ')')) + ') = ' + r)
        return [N('(' + b + '-(' + e + ')*x)/(' + c + '*x-(' + a + '))')]
    return GL('solve(x=' + A + ',y)')


def _ivl(s):
    # 'x>=a', 'x<a', '((x>a) and (x<=b))', 'x' -> [lo, lo in, hi, hi in]
    v = [None, 0, None, 0]
    s = s.replace('&&', ' and ').replace('≥', '>=').replace('≤', '<=')
    for p in unwrap(s).split(' and '):
        p = unwrap(p).replace(' ', '')
        if p == 'x':
            continue
        for o in ('<=', '>=', '<>', '<', '>'):
            k = p.find(o)
            if k > 0:
                break
        if k <= 0 or o == '<>':
            return None
        a = p[:k]
        b = p[k + len(o):]
        if b == 'x':
            a, b = b, a
            o = {'<': '>', '>': '<', '<=': '>=', '>=': '<='}[o]
        if a != 'x':
            return None
        j = 0 if o[0] == '>' else 2
        v[j] = b
        v[j + 1] = len(o) == 2
    return v


def _end(f, v, inc, sd):
    # value or one-sided limit of f at a domain end; returns [val, incl, float]
    if v is None:
        r = Gs('limit(' + f + ',x,' + ('+' if sd < 0 else '-') + 'inf)')
        inc = 0
    elif inc:
        r = _at(f, v)
    else:
        r = Gs('limit(' + f + ',x,' + v + ',' + str(sd) + ')')
    w = F(r)
    if 'inf' in r:
        w = -1e300 if r[0] == '-' else 1e300
        r = 'inf'
    return [r, inc, w]


def compinv():
    hdr('Composite/inverse')
    f = norm(rhs(ask('f(x) =', '', 0)))
    out('f(x) = ' + ps(f))
    g = ask('g(x) (blank=skip)', '', 0)
    if g:
        g = norm(rhs(g))
        out('g(x) = ' + ps(g))
        for a, b, n in ((f, g, 'f(g(x))'), (g, f, 'g(f(x))')):
            out(n + ' = ' + n[0] + '(' + ps(b) + ')')
            out(' = ' + _sb(ps(a), ps(b)))
            ans(n, ps(S('subst(' + a + ',x=' + b + ')')))
    if not yes('Inverse of f', 'y'):
        wait()
        return
    dm = norm(ask('Domain of f (blank=natural)', '', 0))
    if dm:
        out('Domain: ' + _dt(dm, 'x'))
    dn = dm or Gs('domain(' + f + ',x)')
    r = _inv(f)
    v = _ivl(dn) if dn else None
    if len(r) > 1:
        if not dm or v is None:
            out('Not 1-1: restrict domain')
            wait()
            return
        t = '0'
        if v[0] is not None and v[2] is not None:
            t = '((' + v[0] + ')+(' + v[2] + '))/2'
        elif v[0] is not None:
            t = v[0] + '+1'
        elif v[2] is not None:
            t = v[2] + '-1'
        y0 = _at(f, t)
        c0 = r
        r = [u for u in r if abs(F('subst(' + u + ',x=' + y0 + ')') - F(t)) < 1e-6] or r
        o = [u for u in c0 if u != r[0]]
        if o:
            # the chosen root is the larger one when it lies above the other at x = y0
            out(_dt(dm, 'y') + ', so ' + ('positive' if F(t) > (F('subst(' + o[0] + ',x=' + y0 + ')') or 0)
                                         else 'negative') + ' root')
        else:
            out(_dt(dm, 'y') + ', so y = ' + ps(r[0]))
    t = N(r[0])
    if r[0].count('/') > 1 and t.count('/') < 2:
        r[0] = t
    ans('f^-1(x)', ps(r[0]))
    if v is None:
        rg = _dt(Gs('domain(' + r[0] + ',x)'), 'x')
    else:
        a = _end(f, v[0], v[1], 1)
        b = _end(f, v[2], v[3], -1)
        if a[2] > b[2]:
            a, b = b, a
        rg = 'x real'
        if a[0] != 'inf' and b[0] != 'inf':
            rg = pp(a[0]) + (' <= ' if a[1] else ' < ') + 'x' + (' <= ' if b[1] else ' < ') + pp(b[0])
        elif a[0] != 'inf':
            rg = 'x ' + ('>= ' if a[1] else '> ') + pp(a[0])
        elif b[0] != 'inf':
            rg = 'x ' + ('<= ' if b[1] else '< ') + pp(b[0])
    out('Dom f^-1 = range f: ' + (rg if rg and rg != 'x' else 'x real'))
    out('Range f^-1 = dom f: ' + (_dt(dn, 'y') if dn and dn != 'x' else 'y real'))
    if N('(' + r[0] + ')-(' + f + ')') == '0':
        out('f^-1(x) = f(x): self-inverse')
    else:
        out('f^-1 != f: not self-inverse')
    wait()


def ratfn():
    hdr('Rational function')
    f = norm(rhs(ask('f(x) =', '', 0)))
    h = N(f)
    n0 = G('numer(' + h + ')')
    d0 = G('denom(' + h + ')')
    ng, fs = split_factors(f)
    if len(fs) > 1 and fs[-1][0] == '/':
        n0 = ('-' if ng else '') + '*'.join(['(' + u + ')' for o, u in fs if o == '*'])
        d0 = '*'.join(['(' + u + ')' for o, u in fs if o == '/'])
    g = G('gcd(' + n0 + ',' + d0 + ')')
    n = N('(' + n0 + ')/(' + g + ')')
    d = N('(' + d0 + ')/(' + g + ')')
    if G('is_polynomial(' + n + ',x)') != 'true' or G('is_polynomial(' + d + ',x)') != 'true' \
            or not has(d0) or GL('lname(' + h + ')') != ['x']:
        out('Rational function in x only')
        wait()
        return
    va = _zs(d)
    if has(g):
        out('f(x) = ' + _fd(n0, d0))
        for z in _zs(g):
            out('(' + ps(g) + ') cancels: hole at (' + _lst([z]) + ', ' +
                pp(_at('(' + n + ')/(' + d + ')', z)) + ')')
        va = [u for u in va if u not in _zs(g)]
    if has(d) or _fd(n, d) != ps(h):
        out(('f(x)' if not has(g) else '') + ' = ' + _fd(n, d))
    out('Domain: x != ' + ', '.join([pp(u) for u in _zs(d0)]) if _zs(d0) else 'Domain: x real')
    if not has(d):
        out('ANS: f(x) = ' + ps(h) + ', no asymptotes')
        wait()
        return
    if d != 'x':
        out(_pf(G('factor(' + d + ')')) + ' = 0')
    out('ANS: VA x = ' + (_lst(va) if va else 'none'))
    p = int(G('degree(' + n + ',x)'))
    q = int(G('degree(' + d + ',x)'))
    if p < q:
        out('x -> ' + ('±∞' if CFG['uni'] else '+/-inf') + ': f(x) -> 0  (deg num < deg den)')
        out('ANS: HA y = 0')
    else:
        Q = G('quo(' + n + ',' + d + ',x)')
        Rm = G('rem(' + n + ',' + d + ',x)')
        t = ps(N('(' + Rm + ')/(' + d + ')'))
        out('f(x) = ' + join_signed([ps(Q), t]))
        if p == q:
            out('x -> ' + ('±∞' if CFG['uni'] else '+/-inf') + ': ' + t + ' -> 0')
            out('ANS: HA y = ' + pp(Q))
            if p == 1:
                out('Range: y != ' + pp(Q))
        elif p == q + 1:
            out('x -> ' + ('±∞' if CFG['uni'] else '+/-inf') + ': ' + t + ' -> 0')
            out('ANS: oblique y = ' + ps(Q))
        else:
            out('No linear asymptote')
    y0 = _at('(' + n + ')/(' + d + ')', '0') if F('subst(' + d + ',x=0)') else ''
    out('ANS: y-int ' + ('(0, ' + pp(y0) + ')' if y0 else 'none'))
    xi = _zs(n)
    out('ANS: x-int ' + (', '.join(['(' + _lst([r]) + ', 0)' for r in xi]) if xi else 'none'))
    wait()


def oddeven():
    hdr('Odd/even test')
    f = norm(rhs(ask('f(x) =', '', 0)))
    fm = S('subst(' + f + ',x=-x)')
    t = _sb(ps(f), '-x')
    out('f(x) = ' + ps(f))
    out('f(-x) = ' + t)
    if ps(fm) != t:
        out(' = ' + ps(fm))
    out('-f(x) = ' + ps(S('-(' + f + ')')))
    z = lambda e: Gs('normal(' + e + ')') == '0' or Gs('simplify(' + e + ')') == '0'
    if z(f):
        out('ANS: f = 0 is both odd and even')
    elif z(fm + '-(' + f + ')'):
        out('f(-x) = f(x) for all x')
        out('ANS: f is even')
    elif z(fm + '+(' + f + ')'):
        out('f(-x) = -f(x) for all x')
        out('ANS: f is odd')
    else:
        out('f(-x) != f(x), f(-x) != -f(x)')
        out('e.g. f(1) = ' + pp(S('subst(' + f + ',x=1)')) + ', f(-1) = ' +
            pp(S('subst(' + f + ',x=-1)')))
        out('ANS: neither odd nor even')
    wait()


ITEMS = [('Lines', lines), ('Composite/inverse', compinv),
         ('Rational function', ratfn), ('Odd/even test', oddeven)]
