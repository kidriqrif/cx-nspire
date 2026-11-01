# ibtrig3.py - trig equations in an interval, trig graphs (AA 3.7-3.10)
from ibcore import *
import math

TITLE = 'Trig eq/graphs'
TF = ('sin', 'cos', 'tan', 'sec', 'csc', 'cot')
BS = {'sec': 'cos', 'csc': 'sin', 'cot': 'tan'}
IV = {'sin': 'asin', 'cos': 'acos', 'tan': 'atan'}
TB = {'sin': ('A H-A', 'H+A P-A', '1,2', '3,4'), 'cos': ('A P-A', 'H-A H+A', '1,4', '2,3'),
      'tan': ('A H+A', 'H-A P-A', '1,3', '2,4')}
_C = [0, '0', '2*pi', 1]
_N = ['']  # note for the next 'T(a) = c' line


def _isx(r):
    for k in ('asin', 'acos', 'atan', 'sin(', 'cos(', 'tan(', '.'):
        if k in r:
            return False
    return True


def _S(e):
    r = S(e)
    if not has_var(r) and ('+' in r[1:] or '-' in r[1:]):
        # pi+pi/12 -> 13pi/12 (raw and normal tie in length)
        for f in ('normal(', 'factor('):
            t = Gs(f + r + ')')
            if t and len(t) < len(r) + (f[0] == 'n'):
                r = t
    return r


def _br(z):
    # a factor as written: bracketed if it is a sum
    t = ps(z)
    return '(' + t + ')' if ' ' in t else t


def _cl(g):
    # tidy a linear argument k x + b: x-1/4*pi -> x - pi/4
    for w in _calls(g)[::-1]:
        if not has(S('diff(' + w[1] + ',x)'), 'x'):
            t = join_signed([S('diff(' + w[1] + ',x)*x'), S('subst(' + w[1] + ',x=0)')])
            g = g[:w[2] + 4] + t + g[w[3] - 1:]
    return g


def _ar(g):
    return sorted([c[1] for c in _calls(g)])


def _q(r, x=0, a=1):
    # exact if short (arcsin etc. only in radians, x=0), else 3 s.f.
    # a: r is an angle (degrees as a decimal: 75/2 -> 37.5, 100/3 -> 33.3)
    if a and _C[0] and isnum(r) and '/' in r:
        v = F(r)
        t = ('%.3f' % v).rstrip('0').rstrip('.')
        return t if abs(float(t) - v) < 1e-9 else sf3(v)
    if (_isx(r) or not (_C[0] or x) and '.' not in r) and len(r) < 28:
        t = split_terms(r)
        if len(t) == 2 and t[0][0] == '-' and t[1][0] != '-':
            t.reverse()  # -sqrt(3)+2 -> 2 - sqrt(3)
        return join_signed([pp(z) for z in t])
    v = F(r)
    return pp(r) if v is None else sf3(v)


def _calls(s):
    r = []
    i = 0
    n = len(s)
    while i < n - 3:
        w = s[i:i + 3]
        if w in TF and s[i + 3] == '(' and (i == 0 or s[i - 1] not in LET):
            d = 0
            j = i + 3
            while j < n:
                if s[j] == '(':
                    d += 1
                elif s[j] == ')':
                    d -= 1
                    if d == 0:
                        break
                j += 1
            r.append([w, s[i + 4:j], i, j + 1])
            i = j + 1
        else:
            i += 1
    return r


def _one(g):
    # the single distinct trig call text in g, or ''
    cl = _calls(g)
    if not cl:
        return ''
    t = cl[0][0] + '(' + cl[0][1] + ')'
    for c in cl:
        if c[0] + '(' + c[1] + ')' != t:
            return ''
    return t


def _sq(s):
    # sloppy sin^2x, sin^2(2x) -> sin(x)^2
    for it in range(6):
        k = -1
        for f in TF:
            j = s.find(f + '^')
            if j >= 0:
                k = j + 3
        if k < 0:
            break
        m = k + 1
        while m < len(s) and s[m] in DIG:
            m += 1
        n = m
        while n < len(s) and s[n] == ' ':
            n += 1
        p = n
        if s[n:n + 1] == '(':
            d = 0
            while p < len(s):
                d += (s[p] == '(') - (s[p] == ')')
                p += 1
                if d == 0:
                    break
            a = s[n + 1:p - 1]
        else:
            while p < len(s) and (s[p] in DIG or s[p] in LET or s[p] == '.'):
                p += 1
            a = s[n:p]
        if m == k + 1 or not a:
            break
        s = s[:k] + '(' + a + ')' + s[k:m] + s[p:]
    return s


# ---------- basic equation T(A) = c in [lo, hi] ----------
def _tb(T, A, c, fin=0):
    # fin: the x line is the final answer, left to ANS
    dg, lo, hi, inc = _C
    if '.' in c and len(c) < 6:
        c = G('exact(' + c + ')')
    k = S('diff(' + A + ',x)')
    b0 = S('subst(' + A + ',x=0)')
    if has(k, 'x') or F(k) == 0:
        return None
    a = join_signed([pp(S(k + '*x')), pp(b0)])
    if T in BS:
        if F(c) == 0:
            if T != 'cot':
                out(T + '(' + a + ') = 0: no solution')
                return []
            T = 'cos'  # cot = 0  <=>  cos = 0
        else:
            T = BS[T]
            c = _S('1/(' + c + ')')
    out(T + '(' + a + ') = ' + _q(c, 0, 0) + _N[0])
    _N[0] = ''
    cv = F(c)
    if T != 'tan' and abs(cv) > 1 + 1e-12:
        out('|' + T + '| > 1: no solution')
        return []
    L = S('(' + k + ')*(' + lo + ')+' + b0)
    U = S('(' + k + ')*(' + hi + ')+' + b0)
    if F(k) < 0:
        L, U = U, L
    if A != 'x':
        out(pp(L) + ' <= ' + a + ' <= ' + pp(U))
    P, H = ('360', '180') if dg else ('2*pi', 'pi')
    ac = _S('abs(' + c + ')')
    al = G(IV[T] + '(' + ac + ')')
    if not _isx(al):
        al = IV[T] + '(' + ac + ')'
    if dg:
        al = _S(al + '*180/pi')
    out('ref angle = ' + (_q(al) if _isx(al) else 'arc' + T + '(' + pp(ac) + ') = ' + sf3(F(al))))
    t = TB[T]
    p = cv >= 0
    if 0 < abs(cv) < 1 or (T == 'tan' and cv != 0):
        out(T + (' > 0: Q' if p else ' < 0: Q') + (t[2] if p else t[3]).replace(',', ', Q'))
    Lf = F(L)
    Uf = F(U)
    Pf = F(P)
    vs = []
    for z in (t[0] if p else t[1]).split(' '):
        th = _S(z.replace('H', H).replace('P', P).replace('A', '(' + al + ')'))
        tf = F(th)
        n0 = int(math.floor((Lf - tf) / Pf))
        n1 = min(int(math.ceil((Uf - tf) / Pf)), n0 + 50)
        for n in range(n0, n1 + 1):
            v = tf + n * Pf
            e = 1e-9 if inc else -1e-9
            if Lf - e < v < Uf + e:
                vs.append([v, _S('(' + th + ')+(' + str(n) + ')*' + P) if n else th])
    vs = _srt(vs)
    if not (fin and A == 'x'):
        out(a + ' = ' + (', '.join([_q(v[1]) for v in vs]) if vs else 'none in range'))
    if A == 'x' or not vs:
        return vs
    kf = F(k)
    bf = F(b0)
    xs = [[(v[0] - bf) / kf, _S('normal(((' + v[1] + ')-(' + b0 + '))/(' + k + '))')] for v in vs]
    xs = _srt(xs)
    if not fin:
        out('x = ' + ', '.join([_q(v[1]) for v in xs]))
    return xs


def _srt(vs):
    vs.sort()
    o = []
    for v in vs:
        if not o or abs(v[0] - o[-1][0]) > 1e-9:
            o.append(v)
    return o


# ---------- trig equation ----------
def _r1(f):
    # double angle where A and 2A both occur
    for it in range(6):
        cl = _calls(f)
        ar = [S(c[1]) for c in cl]
        hit = None
        for c in cl:
            A = S('(' + c[1] + ')/2')
            if c[0] in IV and A in ar and has(A, 'x'):
                hit = c
                break
        if not hit:
            return f
        n = hit[0]
        sA = 0
        for i in range(len(cl)):
            if cl[i][0] == 'sin' and ar[i] == A:
                sA = 1
        r = {'sin': '2*sin(A)*cos(A)', 'tan': '2*tan(A)/(1-tan(A)^2)',
             'cos': '1-2*sin(A)^2' if sA else '2*cos(A)^2-1'}[n].replace('A', A)
        out(pp(n + '(' + hit[1] + ')') + ' = ' + ps(r) + '  (double angle)')
        f = f[:hit[2]] + '(' + r + ')' + f[hit[3]:]
    return f


def _r2(f):
    # Pythagorean identities with a single argument
    cl = _calls(f)
    if not cl:
        return f
    a = cl[0][1]
    for c in cl:
        if S(c[1]) != S(a):
            return f
    for x, y, r in (('cos', 'sin', '1-'), ('sin', 'cos', '1-'), ('sec', 'tan', '1+'),
                    ('csc', 'cot', '1+')):
        X = x + '(' + a + ')'
        Y = y + '(' + a + ')'
        t = f.replace(X + '^2', '#')
        if '#' in t and X not in t and Y in t:
            out(pp(X + '^2') + ' = ' + r.replace('-', ' - ').replace('+', ' + ') + pp(Y + '^2'))
            return t.replace('#', '(' + r + Y + '^2)')
    return f


def _r3(g):
    # a sinA + b cosA = 0 -> tanA = -b/a ; tan with sin/cos -> sin/cos
    cl = _calls(g)
    nm = [c[0] for c in cl]
    if not cl:
        return g
    a = cl[0][1]
    s = 'sin(' + a + ')'
    c = 'cos(' + a + ')'
    if s in g and c in g and 'tan(' not in g:
        h = g.replace(s, 'p').replace(c, 'q')
        A = Gs('diff(' + h + ',p)')
        B = Gs('diff(' + h + ',q)')
        if A and B and not (has(A, 'p') or has(A, 'q') or has(B, 'p') or has(B, 'q') or has(h, 'x')) \
                and S(h + '-(' + A + ')*p-(' + B + ')*q') == '0' and F(A) != 0:
            k = _S('-(' + B + ')/(' + A + ')')
            _N[0] = '  (divide by ' + pp(c) + ')'
            return 'tan(' + a + ')-(' + k + ')'
    if 'tan' in nm and ('sin' in nm or 'cos' in nm):
        t = cl[nm.index('tan')][1]
        out(pp('tan(' + t + ')') + ' = ' + pp('sin(' + t + ')/cos(' + t + ')'))
        for i in range(8):
            cl = _calls(g)
            z = [w for w in cl if w[0] == 'tan']
            if not z:
                break
            w = z[0]
            g = g[:w[2]] + '(sin(' + w[1] + ')/cos(' + w[1] + '))' + g[w[3]:]
        g = G('numer(normal(' + g + '))')
        out(ps(g) + ' = 0')
    return g


def _um(g, fin=0):
    # polynomial in one trig call -> solutions, or None
    t = _one(g)
    if not t:
        return None
    gu = g.replace(t, 'u')
    if has(gu, 'x'):
        return None
    gu = G('numer(normal(' + gu + '))')
    d = int(G('degree(' + gu + ',u)'))
    if d < 1 or d > 4:
        return None
    if F(G('coeff(' + gu + ',u,' + str(d) + ')')) < 0:
        gu = G('expand(-(' + gu + '))')
    rs = GL('solve(' + gu + '=0,u)')
    for r in rs:
        if bad(r) or 'i' in r:
            return None
    if d > 1:
        out('Let u = ' + pp(t))
        out(ps(gu) + ' = 0')
        fu = G('factor(' + gu + ')')
        if fu != gu:
            neg, fs = split_factors(fu)
            out(('-' if neg else '') + ''.join([_br(unwrap(z[1])) for z in fs]) + ' = 0')
        out(('u = ' + ' or u = '.join([pp(r) for r in rs])) if rs else 'no real u')
    T = t[:3]
    A = t[4:-1]
    o = []
    for r in rs:
        x = _tb(T, A, r, fin and len(rs) == 1)
        if x is None:
            return None
        o += x
    return o


def _cls(g):
    if _one(g):
        return _um(g, 1)
    neg, fs = split_factors(G('factor(' + g + ')'))
    ps_ = []
    for op, z in fs:
        if op == '*' and has(z, 'x'):
            k = z.rfind('^')
            if k > 0 and z[-1] in DIG and z[k - 1] == ')':
                z = unwrap(z[:k])
            ps_.append(z)
    if len(ps_) < 2:
        return None
    ps_ = [unwrap(z) for z in ps_]
    out(''.join([_br(z) for z in ps_]) + ' = 0')
    out(' or '.join([ps(z) + ' = 0' for z in ps_]))
    o = []
    for z in ps_:
        r = _um(G('expand(' + z + ')'))
        if r is None:
            return None
        o += r
    return o


def _gdc(f):
    dg, lo, hi, inc = _C
    if dg:
        f = G('subst(' + f + ',x=x*pi/180)')
    a = F(lo)
    b = F(hi)
    ys = []
    for y in GL('seq(evalf(subst(' + f + ',x=(' + lo + ')+j*((' + hi + ')-(' + lo + '))/120)),j,0,120)'):
        try:
            ys.append(float(y))
        except ValueError:
            ys.append(None)
    h = (b - a) / 120
    rs = []
    for i in range(len(ys)):
        y0 = ys[i]
        y1 = ys[i + 1] if i < len(ys) - 1 else None
        # roots on the grid (standard angles) give ~1e-15, not 0
        if y0 is not None and abs(y0) < 1e-9:
            if inc or 0 < i < 120:
                rs.append(a + i * h)
        elif y0 is not None and y1 is not None and abs(y1) >= 1e-9 and y0 * y1 < 0:
            r = parse_list(Gs('fsolve(' + f + '=0,x=' + str(a + i * h) + '..' + str(a + i * h + h) + ')'))
            v = F(r[0]) if r and r[0] else None
            w = F('subst(' + f + ',x=' + str(v) + ')') if v is not None else None
            if w is not None and abs(w) < 1e-6:  # a residual of exactly 0 is a valid root
                rs.append(v)
        if len(rs) > 20:
            break
    out('ANS: x = ' + (', '.join([sf3(v) for v in rs]) if rs else 'none') + '  (GDC)')


def trig_eq():
    hdr('Trig equation')
    e = norm(_sq(ask('Equation in x', '', '')))
    dg = ask('Deg or rad (d/r)', 'r', 0).lower()[:1] == 'd'
    lo = askn('Lower bound', '0', 0)
    hi = askn('Upper bound', '360' if dg else '2pi', 0)
    inc = yes('Include endpoints', 'y')
    out(pp(lo) + (' <= x <= ' if inc else ' < x < ') + pp(hi))
    _N[0] = ''
    _C[0] = dg
    _C[1] = lo
    _C[2] = hi
    _C[3] = inc
    f = lhs0(e) if '=' in e else e
    f0 = f
    f = _r2(_r1(f))
    g = G('expand(' + f + ')')
    g2 = _r3(g)
    if g2 != g:
        g = G('expand(' + g2 + ')')
    elif f != f0:
        out(ps(g) + ' = 0')
    r = _cls(g)
    for h in ('tcollect(', 'texpand('):
        # sinx cosx -> sin2x/2, a sinx + b cosx, sin(x+A) -> expand
        g3 = Gs(h + g + ')') if r is None else ''
        if g3 and _ar(g3) != _ar(g):
            out(ps(_cl(g3)) + ' = 0  (' + ('compound' if 'pi' in g3 or h[1] == 'e' else 'double') + ' angle)')
            r = _cls(G('expand(' + _r3(g3) + ')'))
    if r is None:
        _gdc(f0)
    else:
        r = _srt(r)
        out('ANS: ' + ('x = ' + ', '.join([_q(v[1]) for v in r]) if r else 'no solution in interval'))
        if not dg and [v for v in r if not _isx(v[1])]:
            out('     ~ ' + ', '.join([sf3(v[0]) for v in r]))
    wait()


# ---------- graphs ----------
def _sin(f):
    t = _one(f)
    if not t:
        return None
    g = f.replace(t, 'w')
    A = t[4:-1]
    b = S('diff(' + A + ',x)')
    if has(g, 'x') or S('diff(' + g + ',w,2)') != '0' or has(b, 'x'):
        return None
    return [t[:3], A, S('diff(' + g + ',w)'), S('subst(' + g + ',w=0)'), b, S('subst(' + A + ',x=0)')]


def _pb(b):
    # a factor/divisor: bare if a plain number or pi, else bracketed
    t = pp(b)
    return t if t in ('pi', '\u03c0') or isnum(t) and '/' not in t and '-' not in t else '(' + t + ')'


def _pa(a):
    # leading coefficient: bare if a plain number
    return pp(a) if isnum(a) and '/' not in a else '(' + pp(a) + ')'


def _bk(x):
    return '(' + pp(x) + ')' if x[:1] == '-' else pp(x)


def trig_graph():
    hdr('Trig graphs')
    o = ask('1)features 2)find a,b,c,d 3)max/min/zeros', '1', 0)
    dg = ask('Deg or rad (d/r)', 'r', 0).lower()[:1] == 'd'
    H, P = ('180', '360') if dg else ('pi', '2*pi')
    _C[0] = dg
    if o == '2':
        mx = askn('max =')
        mn = askn('min =')
        pr = askn('period =')
        T = 'cos' if ask('Model sin/cos', 'sin', 0)[:1] == 'c' else 'sin'
        x1 = askn('x of a max (blank=none)', '', 'max at x')
        a = _S('((' + mx + ')-(' + mn + '))/2')
        out('a = (' + pp(mx) + ' - ' + _bk(mn) + ')/2 = ' + pp(a))
        d = _S('((' + mx + ')+(' + mn + '))/2')
        out('d = (' + pp(mx) + (' - ' + pp(mn[1:]) if mn[:1] == '-' else ' + ' + pp(mn)) + ')/2 = ' + pp(d))
        b = _S('2*' + H + '/(' + pr + ')')
        out('b = ' + pp(P) + '/' + _pb(pr) + ' = ' + pp(b))
        c = '0'
        if x1:
            if T == 'sin':
                c = _S('(' + x1 + ')-' + H + '/(2*(' + b + '))')
                out(('' if b == '1' else _pb(b)) + '(' + pp(x1) + ' - c) = ' + pp(_S(H + '/2')))
                if dg and isnum(c) and '/' in c:
                    c = _q(c)
                out('c = ' + pp(c))
            else:
                c = x1
                out('c = ' + pp(c) + '  (max at x = c)')
        if c == '0':
            arg = pp(_S(b + '*x'))
        else:
            arg = ps(S('x-(' + c + ')'))
            if b != '1':
                arg = _pb(b) + '(' + arg + ')'
        out('ANS: f(x) = ' + join_signed([('' if a == '1' else _pa(a)) + T + '(' + arg + ')', pp(d)]))
        wait()
        return
    f = norm(rhs(ask('f(x) e.g. 3sin(2(x-pi/4))+1', '', 'f(x)')))
    r = _sin(f)
    if not r:
        out('Not a T(bx+c)+d: use GDC')
        wait()
        return
    T, A, a, d, b, b0 = r
    c = _S('-(' + b0 + ')/(' + b + ')')
    am = _S('abs(' + a + ')')
    out('a = ' + pp(a) + ', b = ' + pp(b) + ', c = ' + pp(c) + ', d = ' + pp(d))
    z = _pb(b) + '(' + ps(S('x-(' + c + ')')) + ')'
    if c != '0' and b != '1' and z.replace(' ', '') != pp(A):
        out(ps(A) + ' = ' + z)
    sc = T in ('sin', 'cos')
    if o == '3':
        _C[1] = askn('Lower bound', '0', 0)
        _C[2] = askn('Upper bound', '360' if dg else '2pi', 0)
        _C[3] = 1
        out(pp(_C[1]) + ' <= x <= ' + pp(_C[2]))
        s = '1' if F(a) > 0 else '-1'
        for nm, v in (('max', s), ('min', S('-' + s)), ('zeros', _S('-(' + d + ')/(' + a + ')'))):
            if nm != 'zeros' and not sc:
                continue
            out(nm + ':' if sc and nm != 'zeros' else ps(f) + ' = 0')
            xs = _tb(T, A, v)
            y = _q(S('(' + a + ')*(' + v + ')+(' + d + ')'), 1, 0)
            out('ANS ' + nm + ': ' + (', '.join(['(' + _q(z[1], 1) + ', ' + y + ')' for z in xs]) if xs else 'none'))
        out('f(0) = ' + _q(S('(' + a + ')*' + T + '((' + b0 + ')' + ('*pi/180' if dg else '') + ')+(' + d + ')'), 1, 0))
        wait()
        return
    ab = _S('abs(' + b + ')')
    PP = H if T in ('tan', 'cot') else P
    pr = _S(PP + '/(' + ab + ')')
    if sc:
        out('amplitude = ' + pp(am))
    t = pp(PP) + '/' + _pb(ab)
    out('period = ' + ('' if ab == '1' or t == pp(pr) else t + ' = ') + pp(pr))
    cf = F(c)
    out('no horizontal shift' if cf == 0 else 'shift ' + pp(_S('abs(' + c + ')'))
        + (' right' if cf > 0 else ' left'))
    out('principal axis y = ' + pp(d))
    if sc:
        mx = _S(d + '+' + am)
        mn = _S(d + '-' + am)
        if F(d) == 0:
            out('max = ' + pp(mx) + ', min = ' + pp(mn))
        else:
            out('max = ' + pp(d) + ' + ' + pp(am) + ' = ' + pp(mx))
            out('min = ' + pp(d) + ' - ' + pp(am) + ' = ' + pp(mn))
        out('ANS: range ' + pp(mn) + ' <= f(x) <= ' + pp(mx))
    else:
        x1 = _S('(' + ('0' if T in ('cot', 'csc') else H + '/2') + '-(' + b0 + '))/(' + b + ')')
        out('asymptotes: x = ' + join_signed([pp(x1), 'n(' + pp(_S(H + '/abs(' + b + ')')) + ')']))
        if T in ('tan', 'cot'):
            out('ANS: range all real y')
        else:
            out('ANS: range y <= ' + pp(_S(d + '-' + am)) + ' or y >= ' + pp(_S(d + '+' + am)))
    wait()


ITEMS = [('Trig equation', trig_eq), ('Trig graphs', trig_graph)]
