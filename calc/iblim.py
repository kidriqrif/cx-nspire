# iblim.py - limits and Maclaurin series (AA 5.13, 5.19)
from ibcore import *

TITLE = 'Limits/series'


def _mk(k):
    return ["", "'", "''", "'''"][k] if k < 4 else '^(' + str(k) + ')'


def _ip(e):
    return Gs('is_polynomial(' + e + ',x)') == 'true'


def _dt(e):
    return '' if _ip(e) else ' + ...'


def _cf(e, n, v='x'):
    # Maclaurin coefficients [c0..cn]; None if no Maclaurin series
    r = Gs('series(' + e + ',' + v + '=0,' + str(n + 1) + ')')
    p = '+'.join(['(' + t + ')' for t in split_terms(r)
                  if 'order_size' not in t]) or '0'
    if bad(r) or 'inf' in r or \
            Gs('is_polynomial(' + p + ',' + v + ')') != 'true':
        return None
    return GL('[' + ','.join(['normal(coeff(' + p + ',' + v + ',' + str(k) + '))'
                              for k in range(n + 1)]) + ']')


def _tm(c, k, X='x'):
    # term c*X^k in IB style, e.g. 3x^2/2
    if k == 0:
        return c
    m = X if k == 1 else X + '^' + str(k)
    neg, b = sign_body(c)
    if isnum(b):
        q = ''
        if '/' in b:
            q = b[b.find('/'):]
            b = b[:b.find('/')]
        t = ('' if b == '1' else b) + m + q
    else:
        b = pp(b)
        t = (b if len(split_terms(b)) < 2 and '/' not in b else '(' + b + ')') + m
    return ('-' if neg else '') + t


def _poly(cs, X='x', lo=0):
    return ps(join_signed([_tm(cs[k], k - lo, X)
                           for k in range(lo, len(cs)) if cs[k] != '0']))


def _A(lbl, s):
    out('ANS: ' + lbl + ' = ' + s)


def _val(cs):
    for k in range(len(cs)):
        if cs[k] != '0':
            return k
    return -1


def _n(p, d='4'):
    n = int(ask(p, d, 0).split('^')[-1])
    return n if 0 < n < 11 else int(d)


def _prod(lst):
    if len(lst) == 1:
        return lst[0]
    return '*'.join(['(' + a + ')' for a in lst]) if lst else '1'


def _t(e):
    # tidy a derivative: shortest of S / factor / trigsimplify
    b = S(e)
    for f in ('factor(', 'trigsimplify('):
        if not has(b) or f[0] == 't' and not ('sin' in b or 'cos' in b):
            continue
        r = Gs(f + b + ')')
        if r and not has(r, 'i') and \
                len(r) + 9 * r.count('^-') < len(b) + 9 * b.count('^-'):
            b = r
    return b


def _rk(g):
    # keep-in-numerator rank for 0 x inf: e^.. < x^n < other < ln
    if 'ln(' in g:
        return 3
    if 'exp(' in g or g[:2] == 'e^':
        return 0
    return 1 if g == 'x' or (g[:2] == 'x^' and isnum(g[2:])) else 2


def _fr(n, d):
    # quotient as written, brackets only where needed
    p = ps(n)
    q = ps(d)
    if len(split_terms(n)) > 1 or len(split_top(n, '/')) > 1:
        p = '(' + p + ')'
    if len(split_terms(d)) > 1 or len(split_top(d, '/')) > 1 or len(split_top(d, '*')) > 1 or d[:1] == '-':
        q = '(' + q + ')'
    return (p + '/' + q).replace(')*', ') ')


def _wp(s, k=1):
    # a displayed series in brackets if it is a sum (k: or a quotient)
    return '(' + s + ')' if len(split_terms(s)) > 1 or (k and len(split_top(s, '/')) > 1) else s


def _ev(w, ln, ld):
    # the quotient's value: 'x = 0 gives 0/0', or a plain '= 2/6' step
    # when both are finite (nothing if the answer line says it all)
    t = _q(ln, ld)
    if _k(ln) in '0k' and _k(ld) == 'k':
        if ld == '1' or t.replace(' ', '') == pp(S('(' + ln + ')/(' + ld + ')')).replace(' ', ''):
            return
        out('= ' + t)
    else:
        out(w + ' gives ' + t)


def _nd(f):
    # f -> [numerator, denominator] as a quotient (shows the rewrite)
    neg, fs = split_factors(f)
    nu = [g[1] for g in fs if g[0] == '*']
    de = [g[1] for g in fs if g[0] == '/']
    xs = [g for g in nu if has(g, 'x')]
    if not de and len(split_terms(f)) > 1:
        n = G('numer(' + f + ')')
        d = G('denom(' + f + ')')
        if d != '1':
            out('= lim ' + _fr(n, d))
        return [n, d]
    if not de and len(xs) == 2:
        mv = xs[0] if _rk(xs[0]) < _rk(xs[1]) else xs[1]
        nu = [g for g in nu if g != mv]
        de = [G('exp(-ln(' + mv + '))')]
        out('= lim ' + _fr(unwrap(_prod(nu)), de[0]))
    n = _prod(nu)
    if neg:
        n = G('-(' + n + ')')
    return [unwrap(n), unwrap(_prod(de))]


def _pt(a):
    a = a.split('>')[-1].strip()
    s = ''
    if 'inf' in a:
        return ['-inf' if a[0] == '-' else 'inf', '']
    if len(a) > 1 and a[-1] in '+-':
        s = ',1' if a[-1] == '+' else ',-1'
        a = a[:-1]
    return [norm(a), s]


def _q(a, b):
    # values of the quotient at the limit: n/d
    r = []
    for t in (a, b):
        t = pp(t.replace('+infinity', 'inf').replace('infinity', 'inf'))
        if 'bounded' in t:
            t = 'bounded'
        r.append('(' + t + ')' if '/' in t or len(split_terms(t)) > 1 or (r and t[:1] == '-') else t)
    return r[0] + '/' + r[1]


def _k(r):
    if 'infinity' in r:
        return 'i'
    if 'undef' in r or 'bounded' in r or 'limit' in r:
        return 'u'
    return '0' if r == '0' else 'k'


def _ind(a, b):
    return _k(a) == _k(b) and _k(a) in '0i'


def lhop():
    hdr("Limit / l'Hopital")
    f = norm(rhs(ask('f(x)/g(x) =', '', 0)))
    a, s = _pt(ask('x -> a, a =', '0', 0))
    A = a + s
    L = lambda e: G('limit(' + e + ',x,' + A + ')')
    pa = pp(a) + {',1': '+', ',-1': '-'}.get(s, '')
    w = 'x -> ' + pa if s or 'inf' in a else 'x = ' + pa
    out('lim_(x->' + pa + ') ' + _wp(ps(f), 0))
    n, d = _nd(f)
    ln = L(n)
    ld = L(d)
    _ev(w, ln, ld)
    for it in range(6):
        if not _ind(ln, ld):
            break
        if it == 5:
            out('Still indeterminate (GDC)')
            break
        n = _t('diff(' + n + ',x)')
        d = _t('diff(' + d + ',x)')
        out('= lim ' + _fr(n, d) + " (l'Hopital)")
        ln = L(n)
        ld = L(d)
        if _ind(ln, ld) and '/' in n + d:
            q = S('(' + n + ')/(' + d + ')')
            out('= lim ' + ps(q))
            n = G('numer(' + q + ')')
            d = G('denom(' + q + ')')
            ln = L(n)
            ld = L(d)
        if not (isnum(n) and isnum(d)):
            _ev(w, ln, ld)
    _res(f, A)
    wait()


def _res(f, a):
    r = G('limit(' + f + ',x,' + a + ')')
    if r == 'infinity':
        out('Limit does not exist (+-inf)')
    elif _k(r) == 'u' or bad(r):
        out('Limit does not exist')
    else:
        ans('lim', r.replace('+infinity', 'inf').replace('infinity', 'inf'))


def limser():
    hdr('Limit by Maclaurin')
    f = norm(rhs(ask('f(x)/g(x) =', '', 0)))
    out('lim_(x->0) ' + _wp(ps(f), 0))
    n, d = _nd(f)
    an = _cf(n, 8)
    ad = _cf(d, 8)
    if an is None or ad is None:
        out('No Maclaurin series at 0')
        wait()
        return
    k = _val(ad)
    kn = _val(an)
    _ev('x = 0', an[0], ad[0])
    if k < 1 or kn == 0:
        _res(f, '0')
        wait()
        return
    j = k if kn < 0 or kn > k else kn
    m = min(8, max(j + 2, k))
    seen = []
    for e, cs in ((n, an), (d, ad)):
        for t in split_terms(e):
            for g in split_factors(t)[1]:
                g = unwrap(g[1])
                c = None if g in seen or _ip(g) else _cf(g, m)
                if c:
                    seen.append(g)
                    out(pp(g) + ' = ' + _poly(c) + ' + ...')
        if not _ip(e) and unwrap(e) not in seen:
            out(ps(e) + ' = ' + _poly(cs[:m + 1]) + ' + ...')
    N = _poly(an[:m + 1]) + _dt(n)
    D = _poly(ad[:m + 1]) + _dt(d)
    out('= lim ' + _wp(N) + '/' + _wp(D))
    N = _poly(an[:m + 1], 'x', j) + _dt(n)
    D = _poly(ad[:m + 1], 'x', j) + _dt(d)
    out('= lim ' + _wp(N) + ('' if D == '1' else '/' + _wp(D)))
    _ev('x = 0', an[j], ad[j])
    if ad[j] == '0':
        _res(f, '0')
    else:
        ans('lim', S('(' + an[j] + ')/(' + ad[j] + ')'))
    wait()


def _rw(v, k):
    # raw term f(k)(0) x^k/k!
    if k == 0:
        return pp(v)
    c = v if isnum(v) and '/' not in v else '(' + pp(v) + ')'
    c = {'1': '', '-1': '-'}.get(c, c)
    return c + 'x' + ('^' + str(k) + '/' + str(k) + '!' if k > 1 else '')


def mderiv():
    hdr('Maclaurin (derivs)')
    f = norm(rhs(ask('f(x) =', '', 0)))
    n = _n('Up to x^n')
    out('f(x) = ' + ps(f))
    cur = f
    cs = []
    raw = []
    fk = 1
    for k in range(n + 1):
        if k:
            cur = _t('diff(' + cur + ',x)')
            fk *= k
            out('f' + _mk(k) + '(x) = ' + ps(cur))
        v = S('subst(' + cur + ',x=0)')
        if bad(v) or 'inf' in v:
            out('f' + _mk(k) + '(0) undefined: no series')
            wait()
            return
        out('f' + _mk(k) + '(0) = ' + pp(v))
        cs.append(S('(' + v + ')/' + str(fk)))
        if v != '0':
            raw.append(_rw(v, k))
    out("f(x) = f(0) + f'(0)x + f''(0)x^2/2! + ...")
    s = _poly(cs) + ' + ...'
    if join_signed(raw) + ' + ...' != s:
        out(' = ' + join_signed(raw) + ' + ...')
    _A('f(x)', s)
    wait()


def _pw(g):
    # top-level 'b^p' -> [b, p]
    if len(split_terms(g)) > 1:
        return None
    d = 0
    for j in range(len(g)):
        c = g[j]
        if c in OPN:
            d += 1
        elif c in CLS:
            d -= 1
        elif c == '^' and d == 0:
            return [unwrap(g[:j]), unwrap(g[j + 1:])]
    return None


def _call(g):
    # 'name(arg)' spanning g -> [name, arg]
    k = g.find('(')
    if k < 1 or g[-1] != ')' or unwrap(g[k:]) == g[k:]:
        return None
    for c in g[:k]:
        if c not in LET:
            return None
    return [g[:k], g[k + 1:-1]]


def _std(g):
    # g -> [std form in u, u, '' / '*' / '+', value at 0]
    g = unwrap(g)
    c = _call(g)
    if c:
        nm, u = c
        if nm in ('exp', 'sin', 'cos', 'atan'):
            return [nm + '(u)', u, '', '']
        if nm == 'ln':
            c = S('subst(' + u + ',x=0)')
            v = F(c)
            if v is None or v <= 0:
                return None
            return ['ln(1+u)', S('(' + u + ')/(' + c + ')-1'),
                    '' if c == '1' else '+', 'ln(' + c + ')']
        if nm != 'sqrt':
            return None
        g = '(' + u + ')^(1/2)'
    w = _pw(g)
    if not w:
        return None
    b, p = w
    if b == 'e':
        return ['exp(u)', p, '', '']
    w = _pw(b)
    if w and not has(w[1], 'x'):
        b = w[0]
        p = '(' + w[1] + ')*(' + p + ')'
    if has(p, 'x') or not has(b, 'x'):
        return None
    p = S(p)
    c = S('subst(' + b + ',x=0)')
    v = F(c)
    if v is None or v == 0 or (v < 0 and not (isnum(p) and '/' not in p)):
        return None
    return ['(1+u)^(' + p + ')', S('(' + b + ')/(' + c + ')-1'),
            '' if c == '1' else '*', S('(' + c + ')^(' + p + ')')]


def _cw(c):
    # coefficient prefix: 2, x^2, (1/4), -
    ng, b = sign_body(c)
    for ch in b:
        if ch not in LET + DIG + '^':
            b = '(' + b + ')'
            break
    b = '' if b == '1' else b
    return ('-' if ng else '') + b + (' ' if b and (b[-1] in LET or '^' in b) else '')


def _se(e, cs):
    # ' = series' after a function (nothing if it is that polynomial already)
    s = _poly(cs) + _dt(e)
    return '' if s.replace(' ', '') == ps(e).replace(' ', '') else ' = ' + s


def msub():
    hdr('Maclaurin (subst)')
    f = norm(rhs(ask('f(x) =', '', 0)))
    n = _n('Up to x^n')
    neg, fs = split_factors(f)
    mul = []
    st = None
    nx = 0
    for op, g in fs:
        if not has(g, 'x') or (op == '*' and _ip(g)):
            mul.append(op + '(' + g + ')')
        else:
            nx += 1
            st = _std(g if op == '*' else '(' + g + ')^(-1)')
    if nx != 1 or not st or Gs('subst(' + st[1] + ',x=0)') != '0':
        out('f(x) = ' + ps(f))
        out('Not a standard substitution')
        if nx > 1:
            out('(product: use Series product)')
        wait()
        return
    u = st[1]
    pu = pp(u)
    ng, ub = sign_body(pu)
    if len(split_terms(ub)) > 1:
        ng, ub = 0, '(' + pu + ')'
    sg = st[0].replace('1+u', '1' + '+-'[ng] + ub).replace('(u)', '(' + u + ')')
    m = S(('-' if neg else '') + '1' + ''.join(mul))
    mc = S(m + '*(' + (st[3] if st[2] == '*' else '1') + ')')
    hd = pp(sg)
    if st[2] == '+':
        hd = pp(st[3]) + ' + ' + hd
        if mc != '1':
            hd = '(' + hd + ')'
    rs = _cw(pp(mc)) + hd if st[2] or mc != '1' else ps(f)
    out('f(x) = ' + ps(f) + ('' if rs.replace(' ', '') == ps(f).replace(' ', '') else ' = ' + rs))
    vm = _val(_cf(m, n)) if m != '1' else 0
    n = max(n, vm + 1)
    nn = n - vm
    cu = _cf(u, nn)
    vu = _val(cu) if cu else 0
    t = max(1, nn // vu) if vu > 0 else 2 * nn
    sc = _cf(st[0], t, 'u')
    g = st[0].replace('u', '(' + u + ')')
    gs = _cf(g, nn)
    if sc is None or gs is None:
        out('No Maclaurin series')
        wait()
        return
    out(pp(st[0]) + ' = ' + _poly(sc, 'u') + ' + ...')
    if u != 'x':
        if _ip(u) or not cu:
            out('u = ' + pu)
        else:
            out('u = ' + pu + ' = ' + _poly(cu) + ' + ...')
        w = '(' + pu + ')'
        x1 = w if ng or len(split_terms(pu)) > 1 else pu
        out(pp(sg) + ' = ' + join_signed([_tm(sc[k], k, x1 if k == 1 and sc[k] in ('1', '-1') else w)
                                          for k in range(t + 1) if sc[k] != '0']) + ' + ...')
        out(' = ' + _poly(gs) + ' + ...')
    hd = _poly(gs)
    if st[2] == '+':
        hd = pp(st[3]) + ' + ' + hd
    if mc != '1':
        out('f(x) = ' + _cw(pp(mc)) + '(' + hd + ' + ...)')
    _A('f(x)', _poly(_cf(f, n)) + ' + ...')
    wait()


def mprod():
    hdr('Series product')
    f = norm(rhs(ask('f(x) =', '', 0)))
    g = norm(rhs(ask('g(x) =', '', 0)))
    n = _n('Up to x^n')
    a = _cf(f, n)
    b = _cf(g, n)
    out('f(x) = ' + ps(f) + ('' if a is None else _se(f, a)))
    out('g(x) = ' + ps(g) + ('' if b is None else _se(g, b)))
    if a is None or b is None:
        out('No Maclaurin series')
        wait()
        return
    out('f(x)g(x) = (' + _poly(a) + ')(' + _poly(b) + ')')
    sums = []
    pr = []
    ks = []
    for k in range(n + 1):
        p = [i for i in range(k + 1) if a[i] != '0' and b[k - i] != '0']
        sums.append('+'.join(['(' + a[i] + ')*(' + b[k - i] + ')' for i in p]) or '0')
        pr += ['normal((' + a[i] + ')*(' + b[k - i] + '))' for i in p]
        ks += [k] * len(p)
    cs = GL('[' + ','.join(sums) + ']')
    vs = GL('[' + ','.join(pr) + ']') if pr else []
    ex = join_signed([_tm(vs[i], ks[i]) for i in range(len(vs))]) + ' + ...'
    s = _poly(cs) + ' + ...'
    if ex != s:
        out('= ' + ex)
    _A('f(x)g(x)', s)
    wait()


def _sub(e, d):
    # replace whole identifiers in e using dict d (a number after '*' in brackets)
    o = ''
    i = 0
    n = len(e)
    while i < n:
        if e[i] in LET:
            j = i
            while j < n and (e[j] in LET or e[j] in DIG):
                j += 1
            w = e[i:j]
            r = d.get(w, w)
            if o[-1:] == '*' and r != w and r[:1] in DIG:
                r = '(' + r + ')'
            o += r
            i = j
        else:
            o += e[i]
            i += 1
    return o


def mode():
    hdr('Series from ODE')
    f = norm(rhs(ask('dy/dx =', '', 0)))
    y0 = norm(rhs(ask('y(0) =', '1', 0)))
    n = _n('Up to x^n')
    nm = {}
    for k in range(1, 11):
        nm['y' + str(k)] = 'y' + _mk(k)
    vals = {'x': '0', 'y': _w(y0)}
    cs = [y0]
    raw = [pp(y0)]
    e = f
    fk = 1
    out('y(0) = ' + pp(y0))
    for k in range(1, n + 1):
        if k > 1:
            t = 'diff(' + e + ',x)+diff(' + e + ',y)*y1'
            for j in range(1, k - 1):
                t += '+diff(' + e + ',y' + str(j) + ')*y' + str(j + 1)
            e = S(t)
            fk *= k
        yk = nm['y' + str(k)]
        out(yk + ' = ' + ps(_sub(e, nm).replace("'*", "' ")))
        z = _sub(e, vals)
        v = S(z)
        if bad(v) or 'inf' in v:
            out(yk + '(0) undefined')
            wait()
            return
        z = ps(z)
        out(yk + '(0) = ' + (z + ' = ' if z != pp(v) else '') + pp(v))
        vals['y' + str(k)] = _w(v)
        cs.append(S('(' + v + ')/' + str(fk)))
        if v != '0':
            raw.append(_rw(v, k))
    out("y = y(0) + y'(0)x + y''(0)x^2/2! + ...")
    s = _poly(cs) + ' + ...'
    if join_signed(raw) + ' + ...' != s:
        out(' = ' + join_signed(raw) + ' + ...')
    _A('y', s)
    wait()


def _w(v):
    return v if isnum(v) and v[0] != '-' and '/' not in v else '(' + v + ')'


def mint():
    hdr('Series int/diff')
    g = norm(rhs(ask('f(x) =', '', 0)))
    d = ask('d=diff i=integrate', 'i', 0)[:1] == 'd'
    n = _n('Result up to x^n')
    a = _cf(g, n + (1 if d else -1))
    out('f(x) = ' + ps(g) + ('' if a is None else _se(g, a)))
    if a is None:
        out('No Maclaurin series')
        wait()
        return
    s = _poly(a) + _dt(g)
    if d:
        h = "f'(x)"
        out(h + ' = ' + ps(_t('diff(' + g + ',x)')))
        out(' = d/dx(' + s + ')')
        b = [S(str(k) + '*(' + a[k] + ')') for k in range(1, n + 2)]
    else:
        h = Gs('integrate(' + g + ',x)')
        b = ['C'] + [S('(' + a[k] + ')/' + str(k + 1)) for k in range(n)]
        out(INT() + '(' + s + ')dx')
        out(' = ' + _poly(b) + ' + ...')
        if bad(h):
            h = INT() + 'f dx'
        else:
            h = S(h)
            b[0] = S('subst(' + h + ',x=0)')
            c = pp(_sub(h, {'x': '0'}))
            out('C = ' + (c + ' = ' if c != pp(b[0]) else '') + pp(b[0]))
            h = pp(h)
    _A(h, _poly(b) + ' + ...')
    wait()


ITEMS = [("Limit l'Hopital", lhop), ('Limit Maclaurin', limser),
         ('Maclaurin derivs', mderiv), ('Maclaurin subst', msub),
         ('Series product', mprod), ('Series from ODE', mode),
         ('Series int/diff', mint)]
