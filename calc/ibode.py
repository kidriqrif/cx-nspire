# ibode.py - first-order differential equations (AA 5.18)
from ibcore import *

TITLE = 'ODEs'


def _f(e, xv, yv):
    v = F('subst(' + e + ',[x,y],[' + str(xv) + ',' + str(yv) + '])')
    return v if v is not None and abs(v) < 1e300 else None


def _g(v, n=6):
    # compact number for display
    return (('%.' + str(n) + 'g') % v) if abs(v) > 1e-12 else '0'


def _sb(f, xv, yv):
    # f(x,y) with the numbers put in, for display
    o = ''
    i = 0
    n = len(f)
    while i < n:
        j = i
        while j < n and f[j] in LET:
            j += 1
        if j == i:
            o += f[i]
            i += 1
            continue
        w = f[i:j]
        if w == 'x' or w == 'y':
            w = _g(xv if w == 'x' else yv, 5)
            if o[-1:] == '*':
                o = o[:-1]
                w = '(' + w + ')'
            elif w[0] == '-':
                w = '(' + w + ')'
        o += w
        i = j
    r = ''
    for t in split_terms(o):
        neg, b = sign_body(t)
        r += (' - ' if neg else ' + ') + pp(b) if r else ('-' if neg else '') + pp(b)
    return r


def _x(e):
    # decimals -> exact so the working stays exact
    return (Gs('exact(' + e + ')') or e) if '.' in e else e


def _b(e):
    # bracket a sum for display
    return '(' + ps(e) + ')' if len(split_terms(e)) > 1 else pp(e)


def _br(e):
    # bracket a sum or a fraction
    return '(' + ps(e) + ')' if len(split_terms(e)) > 1 or len(split_top(e, '/')) > 1 else pp(e)


def _idx(e, v='x'):
    # integral of e dv
    return INT() + ('' if e == '1' else _b(e) + ' ') + 'd' + v


def _dd(e, v):
    # separated side: (1/y) dy, x dx, dx
    return 'd' + v if e == '1' else _br(e) + ' d' + v


def _pf(e, v):
    # integrand -> partial fractions (shown) when it splits
    p = Gs('partfrac(' + e + ',' + v + ')')
    if len(split_terms(p)) > 1 and len(split_terms(e)) < 2 and not bad(p):
        out(pp(e) + ' = ' + ps(_nice(p)))
        return p
    return e


def euler():
    hdr("Euler's method")
    f = norm(rhs(ask('dy/dx =', '', 0)))
    out('dy/dx = ' + ps(f))
    x0 = askn('x0', '0', 0)
    y0 = askn('y0', '1', 0)
    h = askn('h', '0.1', 0)
    t = ask('Steps n or x=end', '5', 0)
    out('x0 = %s, y0 = %s, h = %s' % (pp(x0), pp(y0), pp(h)))
    xv = F(x0)
    yv = F(y0)
    hv = F(h)
    n = 0
    if not hv:
        out('h cannot be 0')
        wait()
        return
    if '=' in t:
        xe = F(norm(rhs(t)))
        n = int(round((xe - xv) / hv))
        if abs(xv + n * hv - xe) > 1e-9:
            out('x = ' + _g(xe) + ' is not reached in whole steps of h')
            wait()
            return
    else:
        n = int(t)
    if n < 1 or n > 60:
        out('Use 1-60 steps')
        wait()
        return
    hs = pp(h)
    sg = ' + '
    if hs[0] == '-':
        sg = ' - '
        hs = hs[1:]
    if '/' in hs:
        hs = '(' + hs + ')'
    out('y(n+1) = y(n) + h f(x(n),y(n))')
    out('y(n+1) = y(n)' + sg + hs + (f + '(n)' if len(f) == 1 else '(' + ps(f) + ')'))
    out('x(n+1) = x(n)' + sg + hs)
    out('n  x(n)  y(n)  f(x(n),y(n))')
    for k in range(n + 1):
        x = xv + k * hv
        if k == n:
            out('%d  %s  %s' % (k, _g(x), sf3(yv)))
            break
        fv = _f(f, x, yv)
        if fv is None:
            raise GErr('f undefined at x=' + _g(x))
        out('%d  %s  %s  %s' % (k, _g(x), sf3(yv), sf3(fv)))
        y1 = yv + hv * fv
        if k < 2:
            out('y%d = %s%s%s(%s) = %s' % (k + 1, _g(yv, 5), sg, hs, _sb(f, x, yv), _g(y1, 5)))
        yv = y1
    ans('y(' + _g(x) + ')', sf3(yv), 0)
    wait()


def _ic():
    s = ask('y(x0)=y0 (blank=none)', '', 0)
    if not s:
        return None
    if '=' in s:
        k = s.find('=')
        l = s[:k]
        return [_x(norm(l[l.find('(') + 1:l.rfind(')')])), _x(norm(s[k + 1:]))]
    p = split_top(s.strip('()[] '), ',')
    return [_x(norm(p[0])), _x(norm(p[1]))]


def _deabs(e, p):
    # drop |..| using the sign at the initial point
    for r in range(6):
        i = e.find('abs(')
        if i < 0:
            break
        d = 0
        j = i + 3
        while j < len(e):
            if e[j] == '(':
                d += 1
            elif e[j] == ')':
                d -= 1
                if d == 0:
                    break
            j += 1
        a = e[i + 4:j]
        v = _f(a, p[0], p[1])
        e = e[:i] + ('(' + a + ')' if v is None or v >= 0 else '(-(' + a + '))') + e[j + 1:]
    return e


def _ok(t, p):
    # does t pass through the point p?
    v = _f(t + '-(' + p[1] + ')', p[0], '0')
    return v is not None and abs(v) < 1e-9


def _pick(L, R, p, w='y'):
    # solve L = R for w; keep the branch through point p
    ss = [t for t in GL('solve(' + L + '=(' + R + '),' + w + ')') if not bad(t)]
    for t in ss:
        if p and _ok(t, p):
            return t
    return ss[0] if len(ss) == 1 and not p else ''


def _s(e):
    # simplify; e^a e^b -> e^(a+b); prefer normal on ties
    if 'exp(' in e and not ('sin' in e or 'cos' in e or 'tan' in e):
        e = 'lin(' + e + ')'
    r = S(e)
    n = Gs('normal(' + e + ')')
    return n if n and len(n) <= len(r) else r


def _best(e):
    # neatest of simplified / expanded / tan -> sin/cos
    best = _s(e)
    for f in ('expand(', 'normal(tan2sincos('):
        if f[7:] and 'tan' not in e:
            continue
        b = Gs(f + e + ')' * (1 + (f[7:] != '')))
        if b and len(b) + 3 * b.count('/') <= len(best) + 3 * best.count('/'):
            best = b
    return best


def _fr(s):
    # p/q*X -> pX/q wherever it starts a term (also inside brackets)
    o = ''
    i = 0
    n = len(s)
    while i < n:
        j = i
        if i == 0 or s[i - 1] in '(+-':
            while j < n and s[j] in DIG + '/':
                j += 1
        q = s[i:j].split('/')
        if j > i and s[j:j + 1] == '*' and len(q) == 2 and q[0] and q[1]:
            k = j + 1
            d = 0
            while k < n and (d or s[k] not in '+-)/'):
                d += (s[k] == '(') - (s[k] == ')')
                k += 1
            o += ('' if q[0] == '1' else q[0] + '*') + s[j + 1:k] + '/' + q[1]
            i = k
        else:
            o += s[i:j + 1]
            i = j + 1
    return o


def _nice(e):
    # 1/3*x^2 -> x^2/3; 1/2/x -> 1/(2x)
    o = []
    for t in split_terms(_fr(e)):
        neg, b = sign_body(t)
        q = split_top(b, '/')
        if len(q) == 3 and isnum(q[0]) and isnum(q[1]):
            b = q[0] + '/(' + q[1] + '*' + q[2] + ')'
        o.append(('-' if neg else '') + b)
    return join_signed(o)


def _pc(c):
    # ' + c' / ' - c' for display
    if c == '0':
        return ''
    if c[0] == '-' and len(split_terms(c)) == 1:
        return ' - ' + pp(c[1:])
    return ' + ' + pp(c)


def _sq(y):
    # y = +-sqrt(..): show y^2 first when it is free of roots
    if 'sqrt(' in y:
        a = Gs('normal((' + y + ')^2)')
        b = Gs('factor((' + y + ')^2)')
        if a and b and 'sqrt' not in a + b and 'abs' not in a + b:
            out('y^2 = ' + ps(b if b[0] != '-' and len(b) <= len(a) + 2 else a))


def _fin(L, R, p, h=0):
    # L(y) = R(x) + C: initial condition p (or None), explicit y
    gl = ps(L) + ' = ' + ps(R) + ' + C'
    if p:
        out(gl)
        lv = G('subst(' + L + ',[x,y],[' + p[0] + ',' + p[1] + '])')
        rv = G('subst(' + R + ',x=' + p[0] + ')')
        c = _s('(' + lv + ')-(' + rv + ')')
        pre = 'x = ' + pp(p[0]) + ', y = ' + pp(p[1]) + ':'
        if bad(c) or 'inf' in c:
            out(pre)
            out('C undefined at this point')
            return
        out(pre + ' ' + ps(lv) + ' = ' + (ps(rv) + ' + C' if rv != '0' else 'C'))
        if rv != '0' or ps(c) != ps(lv):
            out('C = ' + pp(c))
        L2 = G(_deabs(L, p))
        R2 = G(_deabs(R, p))
        y = _pick(L2, R2 + '+(' + c + ')', p)
        if y:
            y0 = _nice(y)
            y = _nice(_best(y))
            if not _ok(y, p):
                y = y0
            if h and 'sqrt(' in y and p[0] != '0':
                # homogeneous: y = +-x sqrt(Q) when that is neater
                v0 = F('(' + p[1] + ')/(' + p[0] + ')')
                Q = Gs('normal((' + y + ')^2/x^2)')
                if v0 and Q and 'sqrt' not in Q:
                    b = ('' if v0 > 0 else '-') + 'x*sqrt(' + Q + ')'
                    if len(b) + 3 * b.count('/') < len(y) + 3 * y.count('/'):
                        y = b
            if L2 != 'y':
                out(ps(L2) + ' = ' + ps(R2) + _pc(c))
            _sq(y)
            ans('y', y)
        else:
            out('ANS: ' + ps(_nice(L2)) + ' = ' + ps(_nice(_s(R2 + '+(' + c + ')'))))
        return
    k = L.find('ln(abs(')
    if k >= 0 and L.count('ln(') == 1:
        j = L.find(')', k)
        a = L[k + 7:j]
        c = _s('(' + L + ')/ln(abs(' + a + '))')
        if '(' not in a and not has(c, 'x') and not has(c, 'y'):
            E = _s('(' + R + ')/(' + c + ')')
            out(gl)
            if c != '1':
                out('ln|' + pp(a) + '| = ' + ps(_s('((' + R + ')+C)/(' + c + ')')))
            out('|' + pp(a) + '| = e^(' + ps(E) + ' + C)')
            if a != 'y':
                out(pp(a) + ' = Ae^(' + ps(E) + ')')
            y = _pick(a, 'A*exp(' + E + ')', None)
            if y:
                ans('y', _nice(_s(y)))
                return
    y = '' if 'abs(' in L else _pick(L, R + '+C', None)
    if y:
        if L != 'y':
            out(gl)
        ans('y', _nice(_best(y)))
    else:
        out('ANS: ' + ps(_nice(L)) + ' = ' + ps(_nice(R)) + ' + C')


def _split(f):
    # f(x,y) -> [g(x), h(y)] or None
    for e in (f, 'factor(' + f + ')', 'factor(texpand(' + f + '))'):
        r = Gs(e)
        if not r:
            continue
        neg, fs = split_factors(r)
        gx = '-1' if neg else '1'
        hy = '1'
        ok = True
        for op, t in fs:
            if has(t, 'x') and has(t, 'y'):
                ok = False
                break
            if has(t, 'y'):
                hy += op + '(' + t + ')'
            else:
                gx += op + '(' + t + ')'
        if ok:
            return [_s(gx), G(hy)]
    return None


def sep():
    hdr('Separable dy/dx')
    f = _x(norm(rhs(ask('dy/dx =', '', 0))))
    out('dy/dx = ' + ps(f))
    gh = _split(f)
    if not gh:
        out('Not of form g(x)h(y)')
        wait()
        return
    g, h = gh
    ih = G('1/(' + h + ')')
    r = _s(ih)
    if len(r) < len(ih) and ('/' in h or len(split_factors(h)[1]) < 2):
        ih = r
    p = _ic()
    if ih == '1':
        out('y = ' + _idx(g))
        L = 'y'
    else:
        out(_dd(ih, 'y') + ' = ' + _dd(g, 'x'))
        out(_idx(ih, 'y') + ' = ' + _idx(g))
        L = _s(I(_pf(ih, 'y'), 'y'))
    R = _s(I(g, 'x'))
    if bad(L) or bad(R):
        out('Integral not elementary')
        wait()
        return
    _fin(L, R, p)
    wait()


def homog():
    hdr('Homogeneous y=vx')
    f = _x(norm(rhs(ask('dy/dx =', '', 0))))
    out('dy/dx = ' + ps(f))
    Fv = _s('subst(' + f + ',y=v*x)')
    if has(Fv, 'x'):
        out('Not of form f(y/x)')
        wait()
        return
    out('y = vx, dy/dx = v + x dv/dx')
    out('v + x dv/dx = ' + ps(Fv))
    R = N('(' + Fv + ')-v')
    r = Gs('factor(' + R + ')')
    if r and len(r) <= len(R):
        R = r
    out('x dv/dx = ' + ps(R))
    p = _ic()
    if R == '0':
        out('v = A, y = Ax')
        if p:
            if p[0] == '0':
                out('A undefined at this point')
                wait()
                return
            A = _s('(' + p[1] + ')/(' + p[0] + ')')
            out('x = ' + pp(p[0]) + ', y = ' + pp(p[1]) + ': A = ' + pp(A))
        ans('y', _s('(' + A + ')*x') if p else 'A*x')
        wait()
        return
    iv = _s('1/(' + R + ')')
    if 'tan' in iv:
        iv = _s('tan2sincos(' + iv + ')')
    out(_idx(iv, 'v') + ' = ' + _idx('1/x'))
    Lv = _s(I(_pf(iv, 'v'), 'v'))
    if bad(Lv):
        out('Integral not elementary')
        wait()
        return
    out(ps(Lv) + ' = ln|x| + C')
    _fin(_s('subst(' + Lv + ',v=y/x)'), 'ln(abs(x))', p, 1)
    wait()


def _t(P, v):
    # signed term P v for display: ' + 2y', ' - y/x', ' + (x + 1)y'
    if P == '0':
        return ''
    if len(split_terms(P)) > 1:
        return ' + (' + ps(P) + ')' + v
    neg, b = sign_body(P)
    t = v if b == '1' else pp(b + '*' + v) if '(' not in b else pp(b) + ' ' + v if len(split_top(b, '*')) + len(split_top(b, '/')) < 3 else '(' + pp(b) + ')' + v
    return (' - ' if neg else ' + ') + t


def _ex(u):
    # e^u for display
    return 'e^(' + ps(u) + ')' if len(split_terms(u)) > 1 else pp('exp(' + u + ')')


def _my(m):
    # m y for display: 2y, e^(2x) y, y/x, (x + 1)y
    if len(split_terms(m)) > 1:
        return '(' + ps(m) + ')y'
    if len(split_top(m, '/')) > 1:
        return pp(m + '*y')
    t = pp(m)
    return t + ('y' if len(t) < 2 else ' y')


def _gs(R, m):
    # general solution y = (R + C)/m: expanded, C term last
    k = _s('1/(' + m + ')')
    return ps(join_signed(split_terms(_nice(_best('(' + R + ')*(' + k + ')'))) + [_nice(_s('C*(' + k + ')'))]))


def intf():
    hdr('Integrating factor')
    a = _x(askx("a(x) of a(x)y'+b(x)y=c(x)", '1', 0))
    b = _x(askx('b(x) =', '0', 0))
    c = _x(askx('c(x) =', '0', 0))
    if has(a, 'y') or has(b, 'y') or has(c, 'y'):
        out('Not linear in y')
        wait()
        return
    out(('' if a == '1' else '-' if a == '-1' else _br(a) + ' ') + 'dy/dx' + _t(b, 'y') + ' = ' + ps(c))
    P = _s('(' + b + ')/(' + a + ')')
    Q = _s('(' + c + ')/(' + a + ')')
    if a != '1':
        out('dy/dx' + _t(P, 'y') + ' = ' + ps(Q))
    p = _ic()
    ip = I(P)
    if 'sin(' in P and 'cos(' in P:
        t = Gs('integrate(' + _s('subst(' + P + ',sin(x)=tan(x)*cos(x))') + ',x)')
        if t and not bad(t) and len(t) < len(ip):
            ip = t
    ip = _s(ip.replace('abs(', '('))
    out('IF = e^(' + INT() + _b(P) + ' dx) = ' + _ex(ip))
    mu = _s('exp(' + ip + ')')
    if pp(mu) != _ex(ip):
        out('IF = ' + ps(mu))
    qm = _s('(' + Q + ')*(' + mu + ')')
    out(_my(mu) + ' = ' + _idx(qm))
    R = _s(I(qm))
    if bad(R):
        out('Integral not elementary')
        wait()
        return
    out(' = ' + (ps(_nice(R)) + ' + C' if R != '0' else 'C'))
    if p:
        out('y = ' + _gs(R, mu))
        m0 = G('subst(' + mu + ',x=' + p[0] + ')')
        r0 = G('subst(' + R + ',x=' + p[0] + ')')
        l0 = _s('(' + m0 + ')*(' + p[1] + ')')
        C = _s('(' + l0 + ')-(' + r0 + ')')
        if bad(C) or 'inf' in C:
            out('C undefined at this point')
            wait()
            return
        out('x = ' + pp(p[0]) + ', y = ' + pp(p[1]) + ': ' + ps(l0) + ' = ' + (ps(r0) + ' + C' if r0 != '0' else 'C'))
        if r0 != '0' or ps(C) != ps(l0):
            out('C = ' + pp(C))
    else:
        C = 'C'
    y = _best('(' + R + '+(' + C + '))/(' + mu + ')')
    v = F('subst(' + y + '-(' + p[1] + '),x=' + p[0] + ')') if p else 0
    if v is None or abs(v) > 1e-9:
        out('No solution through this point')
    else:
        ans('y', _nice(y))
    wait()


ITEMS = [("Euler's method", euler), ('Separable', sep),
         ('Homogeneous y=vx', homog), ('Integrating factor', intf)]
