# ibstat.py - descriptive statistics (AA 4.1-4.4, 4.10, 4.14 aX+b)
from ibcore import *

TITLE = 'Statistics'
_M = {'d': 1}


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
        o += t
        i = j
    return o


def _s3(v):
    # 3 s.f. without the 0.9996 -> 1.000 overflow of sf3
    return sf3(float('%.2e' % v))


def _f(r):
    # display value: exact, decimal if it terminates (dec mode), + 3 s.f.
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
        if q == 1 and _M['d']:
            d = G('evalf(' + r + ')')
            if len(d) < 8 and 'e' not in d:
                return d
    return s + ' (' + t + ')' if len(s) < 18 else t


def _e(s):
    return S(_q(s)) if s else ''


def _A(lbl, r):
    out('ANS: ' + lbl + ' = ' + _f(r))


def _fl(s):
    try:
        return float(s)
    except ValueError:
        v = F(_q(s))
        if v is None:
            raise GErr('bad value ' + s)
        return v


def _L(p, e=1):
    return [a for a in askv(p, '', e) if a]


def _S():
    return 'Σ' if CFG['uni'] else 'Sum '


def _X():
    return '×' if CFG['uni'] else '*'


def _sum(a):
    return S('+'.join(['(' + x + ')' for x in a]) if a else '0')


def _o(k):
    s = 'th'
    if k % 100 not in (11, 12, 13):
        s = {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')
    return str(k) + s


def _rows(h, a):
    for j in range(0, len(a), 8):
        out((h if j == 0 else '  ') + ','.join(a[j:j + 8]) + (',' if j + 8 < len(a) else ''))


# ---------- data summary ----------
def _kth(fs, k):
    c = 0
    for j in range(len(fs)):
        c += fs[j]
        if c >= k:
            return j
    return len(fs) - 1


def _mh(X, a, b):
    # median of ordered positions a..b -> [text, exact]
    xs, ex, fs = X
    m = b - a + 1
    p = a + (m - 1) // 2
    j = _kth(fs, p)
    if m % 2:
        return [_o(p) + ' value = ' + xs[j], ex[j]]
    k = _kth(fs, p + 1)
    v = S('(' + ex[j] + '+' + ex[k] + ')/2')
    return ['(' + _o(p) + '+' + _o(p + 1) + ')/2 = (' + xs[j] + '+' + xs[k] + ')/2 = ' + _f(v), v]


def data_summary():
    hdr('Data summary')
    _M['d'] = 1
    t = ask('Type 1=raw 2=freq 3=grouped', '1', 0)
    if t == '3':
        _grouped()
        return
    if t == '2':
        xs = _L('Values x', 'x')
        fs = [int(a) for a in _L('Freqs f', 'f')]
    else:
        xs = _L('Data x1,x2,..', 0)
        fs = [1] * len(xs)
    n = sum(fs)
    if len(xs) != len(fs) or n < 2 or min(fs) < 0:
        out('Error: list lengths')
        wait()
        return
    xs = [xs[j] for j in range(len(xs)) if fs[j]]
    fs = [f for f in fs if f]
    fv = [_fl(a) for a in xs]
    o = sorted(range(len(xs)), key=lambda j: fv[j])
    xs = [xs[j] for j in o]
    fs = [fs[j] for j in o]
    fv = [fv[j] for j in o]
    ex = [_q(a) for a in xs]
    X = [xs, ex, fs]
    out('n = ' + str(n))
    if t == '2':
        lb = 'fx'
    else:
        lb = 'x'
        _rows('Sorted: ', xs)
    pr = ['(' + ex[j] + ')*' + str(fs[j]) for j in range(len(xs))]
    Sx = _sum(pr)
    out(_S() + lb + ' = ' + _f(Sx))
    m = S('(' + Sx + ')/' + str(n))
    _mean(Sx, m, n, '=')
    md = _mh(X, 1, n)
    out('median = ' + md[0])
    h = n // 2
    q1 = _mh(X, 1, h)
    q3 = _mh(X, n - h + 1, n)
    out('Q1 = ' + q1[0])
    out('Q3 = ' + q3[0])
    iqr = S(q3[1] + '-(' + q1[1] + ')')
    out('IQR = Q3 - Q1 = ' + _g(q3[1]) + ' - ' + _b(q1[1], '-') + ' = ' + _f(iqr))
    lo = S(q1[1] + '-3/2*(' + iqr + ')')
    hi = S(q3[1] + '+3/2*(' + iqr + ')')
    out('Q1 - 1.5(IQR) = ' + _g(q1[1]) + ' - 1.5(' + _g(iqr) + ') = ' + _f(lo))
    out('Q3 + 1.5(IQR) = ' + _g(q3[1]) + ' + 1.5(' + _g(iqr) + ') = ' + _f(hi))
    a = F(lo)
    b = F(hi)
    ol = [xs[j] for j in range(len(xs)) if fv[j] < a or fv[j] > b]
    ok = [xs[j] for j in range(len(xs)) if a <= fv[j] <= b]
    out('Outliers: ' + (','.join(ol) if ol else 'none'))
    out('Box: min ' + xs[0] + ', Q1 ' + _f(q1[1]) + ', med ' + _f(md[1]) + ', Q3 ' + _f(q3[1]) + ', max ' + xs[-1])
    if ol and ok:
        out('Whiskers: ' + ok[0] + ' to ' + ok[-1])
    if t == '2':
        c = fs
    else:
        c = [fv.count(v) for v in fv]
    mx = max(c)
    mo = []
    for j in range(len(xs)):
        if c[j] == mx and xs[j] not in mo:
            mo.append(xs[j])
    out('mode = ' + (','.join(mo) if mx > 1 or len(mo) == 1 else 'none (all once)'))
    p = _fl(ask('Percentile p (0=skip)', '0', 0))
    if 0 < p < 100:
        r = p * n / 100
        k = int(r)
        if r == k:
            v = _mh(X, k, k + 1) if k < n else _mh(X, n, n)
        else:
            v = _mh(X, k + 1, k + 1)
        out('P' + _n(p) + ': ' + _n(p / 100) + '(' + str(n) + ') = ' + _n(r) + ' -> ' + v[0])
    sq = _sum(['(' + ex[j] + ')^2*' + str(fs[j]) for j in range(len(xs))])
    out(_S() + lb + '^2 = ' + _f(sq))
    sd = _var(sq, m, n)
    _A('mean', m)
    _A('sd', sd)
    _A('median', md[1])
    wait()


def _n(v):
    return str(int(v)) if v == int(v) else str(v)


def _p(s):
    return '(' + s + ')' if len(split_terms(s)) > 1 else s


def _g(r):
    return _f(r).split(' (')[0]


def _b(r, c):
    s = _g(r)
    return '(' + s + ')' if c in s else s


def _c(r):
    # coefficient / value as a student writes it: a plain number, else 3 s.f.
    s = _g(r)
    return s if isnum(s) and '/' not in s else _s3(F(r))


def _mean(Sx, m, n, c):
    a = _b(Sx, '/') + '/' + str(n)
    b = _f(m)
    out('mean ' + c + ' ' + (b if b.split(' (')[0] == a else a + ' = ' + b))


def _var(sq, m, n):
    v = S('(' + sq + ')/' + str(n) + '-(' + m + ')^2')
    out('var = ' + _b(sq, '/') + '/' + str(n) + ' - ' + _k(_g(m)) + '^2 = ' + _f(v))
    return S('normal(sqrt(' + v + '))')


def _grouped():
    b = _L('Class bounds b0,b1,..', 'bounds')
    fs = [int(a) for a in _L('Freqs f1..fk', 'f')]
    k = len(fs)
    if len(b) != k + 1 or k < 1:
        out('Error: need k+1 bounds')
        wait()
        return
    be = [_q(a) for a in b]
    ms = [S('(' + be[j] + '+' + be[j + 1] + ')/2') for j in range(k)]
    n = sum(fs)
    out('n = ' + str(n))
    _rows('Mid-points: ', [_f(x) for x in ms])
    Sm = _sum([str(fs[j]) + '*' + ms[j] for j in range(k)])
    out(_S() + 'fm = ' + _f(Sm))
    m = S('(' + Sm + ')/' + str(n))
    _mean(Sm, m, n, '~')
    cum = []
    c = 0
    for f in fs:
        c += f
        cum.append(c)
    _rows('Cum freq: ', [str(x) for x in cum])
    mx = max(fs)
    out('Modal class: ' + ', '.join([b[j] + '-' + b[j + 1] for j in range(k) if fs[j] == mx]))
    p = _fl(ask('Percentile p (0=skip)', '0', 0))
    rs = []
    for nm, t in (('median', '/2'), ('Q1', '/4'), ('Q3', '*3/4'), ('P' + _n(p), '*' + _n(p) + '/100')):
        if nm[0] == 'P' and not 0 < p < 100:
            continue
        t = S(str(n) + t)
        tv = _fl(t)
        j = _kth(fs, tv)
        cf = str(cum[j - 1]) if j else '0'
        w = S(be[j + 1] + '-(' + be[j] + ')')
        v = S(be[j] + '+(' + t + '-' + cf + ')/' + str(fs[j]) + '*(' + w + ')')
        out(nm + ' ~ ' + b[j] + ' + (' + _f(t) + ' - ' + cf + ')/' + str(fs[j]) + ' ' + _X() + ' ' + _f(w) + ' = ' + _f(v))
        rs.append(v)
    iqr = S(rs[2] + '-(' + rs[1] + ')')
    out('IQR ~ ' + _f(iqr))
    sq = _sum([str(fs[j]) + '*(' + ms[j] + ')^2' for j in range(k)])
    out(_S() + 'fm^2 = ' + _f(sq))
    sd = _var(sq, m, n)
    _A('mean', m)
    _A('sd', sd)
    _A('median', rs[0])
    wait()


# ---------- mean transform ----------
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
                if w not in ('pi', 'e', 'sqrt', 'ln', 'exp', 'abs') and w not in u:
                    u.append(w)
                i = j
            else:
                i += 1
    return u


def _k(s):
    return s if s.isdigit() else '(' + s + ')'


def _sub(c, v, a, f=_c):
    # c(v) + a with coefficients 1 and -1 simplified
    s = f(c)
    u = _g(v)
    if '/' in s:
        s = '(' + s + ')'
    t = u if s == '1' else ('-' + _k(u) if s == '-1' else s + '(' + u + ')')
    return join_signed(['' if s == '0' else t, f(a)])


def mean_transform():
    hdr('Mean/transform')
    _M['d'] = 1
    t = ask('1 aX+b 2 unknown 3 combine 4 add/remove', '1', 0)
    if t == '2':
        xs = _L('Values x (may use k)', 'x')
        fs = _L('Freqs f (blank=all 1)', 'f')
        raw = not fs
        fs = fs or ['1'] * len(xs)
        m = _e(askn('Given mean', '', 'mean'))
        if len(xs) != len(fs):
            out('Error: list lengths')
            wait()
            return
        u = _unk(xs + fs)
        if len(u) != 1:
            out('Need exactly one unknown')
            wait()
            return
        u = u[0]
        sfx = N('+'.join(['(' + _q(xs[j]) + ')*(' + _q(fs[j]) + ')' for j in range(len(xs))]))
        sf = N('+'.join(['(' + _q(a) + ')' for a in fs]))
        out(_S() + ('x' if raw else 'fx') + ' = ' + ps(sfx))
        out(('n' if raw else _S() + 'f') + ' = ' + ps(sf))
        out(_p(ps(sfx)) + '/' + _p(ps(sf)) + ' = ' + _g(m))
        out(ps(sfx) + ' = ' + (_g(S(m + '*' + sf)) if not has_var(sf) else _g(m) + '(' + ps(sf) + ')'))
        e = N(sfx + '-(' + m + ')*(' + sf + ')')
        rs = GL('solve(' + e + '=0,' + u + ')')
        inf = has(''.join(fs), u)
        ok = []
        for r in rs:
            v = F(r)
            if inf and (v is None or v < 0 or abs(v - round(v)) > 1e-9):
                out(u + ' = ' + pp(r) + ' rejected')
            else:
                ok.append(r)
        if not ok:
            out('No solution: check data')
        for r in ok:
            _A(u, r)
    elif t == '3':
        a = askv('n1, mean1', '', 0)
        b = askv('n2, mean2', '', 0)
        T = S('(' + _q(a[0]) + ')*(' + _q(a[1]) + ')+(' + _q(b[0]) + ')*(' + _q(b[1]) + ')')
        out(_S() + 'x = ' + a[0] + '(' + a[1] + ') + ' + b[0] + '(' + b[1] + ') = ' + _f(T))
        n = S(_q(a[0]) + '+' + _q(b[0]))
        M = S('(' + T + ')/(' + n + ')')
        out('mean = ' + _f(T) + '/' + _f(n))
        _A('mean', M)
    elif t == '4':
        a = askv('n, mean', '', 0)
        v = _e(askn('value (+add/-remove)', '', 0))
        Sm = S('(' + _q(a[0]) + ')*(' + _q(a[1]) + ')')
        out(_S() + 'x = ' + a[0] + '(' + a[1] + ') = ' + _f(Sm))
        n2 = S(_q(a[0]) + ('+1' if F(v) >= 0 else '-1'))
        if F(n2) < 1:
            out('Error: no values left')
            wait()
            return
        M = S('(' + Sm + '+(' + v + '))/' + n2)
        out('mean = (' + join_signed([_g(Sm), _g(v)]) + ')/' + _g(n2))
        _A('mean', M)
    else:
        m = _e(askn('mean (or E(X))', '', 'mean'))
        s = _e(askn('sd (blank=skip)', '', 'sd'))
        v = _e(askn('var (blank=skip)', '', 'var'))
        md = [_e(x) for x in _L('median, IQR (blank=skip)', 'median, IQR')]
        a = _e(askn('a', '1', 0))
        b = _e(askn('b', '0', 0))
        if s and not v:
            v = S('(' + s + ')^2')
        if v and not s:
            s = S('normal(sqrt(' + v + '))')
        m2 = S('(' + a + ')*(' + m + ')+(' + b + ')')
        if s:
            s2 = S('abs(' + a + ')*(' + s + ')')
            v2 = S('(' + a + ')^2*(' + v + ')')
        out(_lin(a, b, 'Y', 'X', _g))
        t = _sub(a, m, b, _g)
        out('new mean = ' + t + ('' if t == _f(m2) else ' = ' + _f(m2)))
        ab = '|' + _g(a) + '|' if F(a) < 0 else _k(_g(a))
        if s and ab != '1':
            out('new sd = ' + ab + '(' + _g(s) + ') = ' + _f(s2))
            out('new var = ' + _k(_g(a)) + '^2(' + _g(v) + ') = ' + _f(v2))
        if md:
            t = _sub(a, md[0], b, _g)
            v = _f(S('(' + a + ')*(' + md[0] + ')+(' + b + ')'))
            out('new median = ' + t + ('' if t == v else ' = ' + v))
        if len(md) > 1 and ab != '1':
            out('new IQR = ' + ab + '(' + _g(md[1]) + ') = ' + _f(S('abs(' + a + ')*(' + md[1] + ')')))
        _A('mean', m2)
        if s:
            _A('sd', s2)
            _A('var', v2)
    wait()


# ---------- regression (r and the lines by GDC) ----------
def _lin(b, a, y, x, f=_c):
    bs = f(b)
    if bs == '0':
        return y + ' = ' + f(a)
    if '/' in bs:
        bs = '(' + bs + ')'
    t = '' if bs == '1' else ('-' if bs == '-1' else bs)
    return y + ' = ' + join_signed([t + x, f(a)])


def regression():
    hdr('Regression/r')
    _M['d'] = 1
    xs = _L('x list', 'x')
    ys = _L('y list', 'y')
    n = len(xs)
    if n != len(ys) or n < 3:
        out('Error: need equal lists, n>=3')
        wait()
        return
    X = '[' + ','.join([_q(a) for a in xs]) + ']'
    Y = '[' + ','.join([_q(a) for a in ys]) + ']'
    ln = ask('Line 1=y on x 2=x on y 3=both', '1', 0)
    N_ = str(n)
    xb = S('sum(' + X + ')/' + N_)
    yb = S('sum(' + Y + ')/' + N_)
    sxx = S('dot(' + X + ',' + X + ')-' + N_ + '*(' + xb + ')^2')
    syy = S('dot(' + Y + ',' + Y + ')-' + N_ + '*(' + yb + ')^2')
    sxy = S('dot(' + X + ',' + Y + ')-' + N_ + '*(' + xb + ')*(' + yb + ')')
    if F(sxx) == 0 or F(syy) == 0:
        out('Error: no variation')
        wait()
        return
    r = S('(' + sxy + ')/sqrt((' + sxx + ')*(' + syy + '))')
    b = S('(' + sxy + ')/(' + sxx + ')')
    a = S(yb + '-(' + b + ')*(' + xb + ')')
    d = S('(' + sxy + ')/(' + syy + ')')
    c = S(xb + '-(' + d + ')*(' + yb + ')')
    out('By GDC:')
    out('ANS: r = ' + _c(r))
    rv = F(r)
    z = abs(rv)
    if z < 1e-12:
        out('no linear correlation')
    else:
        w = 'perfect' if z > 1 - 1e-9 else ('strong' if z >= 0.75 else ('moderate' if z >= 0.5 else ('weak' if z >= 0.25 else 'very weak')))
        out(w + (' positive' if rv > 0 else ' negative') + ' linear correlation')
    if ln != '2':
        out('ANS: ' + _lin(b, a, 'y', 'x'))
    if ln != '1':
        out('ANS: ' + _lin(d, c, 'x', 'y'))
    pr = ask('Predict 1=y from x 2=x from y 0=skip', '0', 0)
    if pr in ('1', '2'):
        k = pr == '1'
        v = _e(askn('value', '', 'x' if k else 'y'))
        p = S('(' + (b if k else d) + ')*(' + v + ')+(' + (a if k else c) + ')')
        vv = F(v)
        out(('y = ' if k else 'x = ') + _sub(b if k else d, v, a if k else c))
        out('ANS: ' + ('y' if k else 'x') + '(' + _f(v) + ') = ' + _c(p))
        fl = [_fl(z) for z in (xs if k else ys)]
        if vv < min(fl) or vv > max(fl):
            out('(extrapolation - unreliable)')
    if yes('Interpret a,b?', 'n'):
        bv = F(b)
        out('y does not depend on x' if bv == 0 else 'y ' + ('increases' if bv > 0 else 'decreases') + ' ' + _c(S('abs(' + b + ')')) + ' per unit of x')
        out('y = ' + _c(a) + ' when x = 0')
    wait()


ITEMS = [('Data summary', data_summary), ('Mean/transform', mean_transform),
         ('Regression/r', regression)]
