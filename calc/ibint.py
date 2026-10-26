# ibint.py - integration with working (AA 5.5, 5.10, 5.15, 5.16)
from ibcore import *

TITLE = 'Integration'
MAXIBP = 4


def _prod(lst):
    return '*'.join(['(' + a + ')' for a in lst]) or '1'


def _sq(s):
    return s.replace(' ', '')


def _int(s, v):
    # 'int x^2 dx' in ASCII mode (s already pretty; a sum is bracketed)
    return INT().strip() + ' ' + _tp('(' + s + ')' if len(split_terms(s)) > 1 else s) + ' d' + v


def _d(s):
    # display of a Giac expression: sec^2(x), spaced signs
    return _tp(ps(_sec(s)))


def _fl(L):
    for s in L:
        out(s)


def _cf(c):
    # coefficient in front: 1 -> '', -1 -> '-', 3 -> '3', 1/2 -> '(1/2)'
    if c in ('1', '-1'):
        return c[:-1]
    return '(' + pp(c) + ')' if '/' in c or len(split_terms(c)) > 1 else pp(c)


def _pr(s, z=''):
    # bracket a sum (or a term starting with a char in z)
    return '(' + ps(s) + ')' if len(split_terms(s)) > 1 or s[:1] in z else pp(s)


def _br(t):
    # bracket a pretty factor unless it is a plain token
    return t if t.isalpha() or t.isdigit() else '(' + t + ')'


def _split(t, v):
    # signed term -> [constant, v-factors on top, v-factors below]
    neg, fs = split_factors(t)
    g = lambda o, b: [f[1] for f in fs if f[0] == o and has(f[1], v) == b]
    return [S(('-' if neg else '') + _prod(g('*', 0)) + '/' + _prod(g('/', 0))), g('*', 1), g('/', 1)]


def _kc(e, v):
    # u^3/2 -> (1/2)u^3: constant factor in front
    c, num, den = _split(e, v)
    if c == '1':
        return pp(e)
    return _cf(c) + _pr(S(_prod(num) + '/' + _prod(den)))


def _inner(h, v):
    # chain inner of one factor: f(u), u^n, a^u -> u (or None)
    h = unwrap(h)
    k = h.find('(')
    if k > 0 and h[:k].isalpha() and _cl(h, k + 1) == len(h):
        return h[k + 1:-1]
    t = split_top(h, '^')
    if len(t) == 2:
        b = unwrap(t[0])
        e = unwrap(t[1])
        if has(b, v) != has(e, v):
            return b if has(b, v) else e


def _df(u, v='x'):
    return S('diff(' + u + ',' + v + ')')


def _linear(u, v):
    return not has(_df(u, v), v)


def _lp(t, v):
    # p when t = c v^p (c constant), else ''
    p = Gs('normal(' + v + '*diff(' + t + ',' + v + ')/(' + t + '))')
    return '' if has(p, v) else p


def _pf(t, v, F):
    # power rule on c v^p (p != -1): [t as c v^p if rewritten, working, antiderivative]
    p = _lp(t, v)
    c = S('(' + t + ')/' + v + '^(' + p + ')') if p else ''
    if p in ('', '-1') or has(c, v):
        return None
    n = S(p + '+1')
    e = n if n.isdigit() else '(' + pp(n) + ')'
    m = _cf(c)
    r = m + v + ('' if p == '1' else '^' + (p if p.isdigit() else '(' + pp(p) + ')'))
    w = v + '^' + e + '/' + e
    w = m + ('(' + w + ')' if m[:1] == '(' else w)
    if '/' in n and n.lstrip('-') != '1/2':
        # 3x^(5/3)/5, -2/(3x^(3/2)); not Giac's 3x(x^(1/3))^2/5
        F = S('(' + c + ')/(' + n + ')' + ('/' if n[0] == '-' else '*') + 'zzw').replace('zzw', v + '^(' + n.lstrip('-') + ')')
    return ['' if p.isdigit() or _sq(r) == _sq(pp(t)) else r, w, F]


def iterm(t, v, noparts=0, q=0):
    # integrate one signed term with working; returns antiderivative
    # noparts: 1 = never by parts; 2 = inside by parts (inner substitution uses w, u is taken)
    # q: caller shows the result next, so skip the final ' = F'
    c, num, den = _split(t, v)
    head = _int(pp(t), v)
    if not num and not den:
        r = S('(' + c + ')*' + v)
        if not q:
            out(head + ' = ' + pp(r))
        return r
    F = I(t, v)
    if bad(F):
        out(head + ': no elementary antiderivative')
        return None
    F = S(F)
    w = ''
    pf = _pf(t, v, F)
    if pf:
        r, w, F = pf
        if r:
            # index form: sqrt(x)/x^3 = x^(-5/2)
            out((' ' if q else pp(t) + ' ') + '= ' + r)
            head = _int(r, v)
    elif len(num) + len(den) > 1:
        rc = _revchain(num, den, v)
        if rc:
            u, ratio, outer, Fu = rc
            m = _cf(S('(' + c + ')*(' + ratio + ')'))
            L = 'w' if noparts > 1 else 'u'
            out(head + '  (reverse chain)')
            for z in (' u = ' + ps(u) + ', du = ' + _pr(_df(u, v)) + ' d' + v,
                      ' = ' + m + _int(pp(outer), 'u'), ' = ' + m + (_pr(Fu, DIG + '-') if m else ps(Fu))):
                out(z.replace('u', L))
            F = S('(' + c + ')*(' + ratio + ')*(' + G('subst(' + Fu + ',u=(' + u + '))') + ')')
            if not q:
                out(' = ' + ps(F))
            return F
        if not noparts and _pick(t, v) and len(t) < 40 and not den:
            out('I = ' + head + '  (by parts)')
            return ibp_core(t, v, 0, q)
    if w and _sq(w) == _sq(ps(F)):
        w = ''
    if not q:
        out(head + ' = ' + (w + ' = ' if w else '') + ps(F))
    elif w:
        out(head + ' = ' + w)
    return F


def _revchain(num, den, v):
    facs = [[x, 1] for x in num] + [[x, -1] for x in den]
    for j in range(len(facs)):
        h, sg = facs[j]
        u = _inner(h, v)
        if sg == -1 and (u is None or _linear(u, v)):
            u = unwrap(h)
        if u is None or _linear(u, v):
            continue
        rs = '*'.join([('(' if z[1] == 1 else '1/(') + z[0] + ')' for z in facs[:j] + facs[j + 1:]]) or '1'
        ratio = Gs('normal((' + rs + ')/(' + _df(u, v) + '))')
        if ratio == '' or has(ratio, v):
            continue
        hh = h if sg == 1 else '1/(' + h + ')'
        outer = ''
        for s in GL('solve(zzu=' + u + ',' + v + ')'):
            # shortest form: 1/sqrt(u), not sqrt(u)/u
            try:
                o = S('subst(' + hh + ',' + v + '=' + s + ')')
            except GErr:
                o = ''
            if o and not has(o, v):
                outer = o.replace('zzu', 'u')
                break
        if not outer:
            continue
        Fu = I(outer, 'u')
        if bad(Fu):
            continue
        return [u, ratio, outer, Fu]
    return None


def _rank(f, v):
    if not has(f, v):
        return 9
    w = f.lstrip('+-( ')
    j = 0
    while j < len(w) and w[j] in LET:
        j += 1
    nx = w[j:j + 1]
    w = w[:j]
    for r, z in ((1, 'ln log10'), (2, 'asin acos atan'), (4, 'sin cos tan sec csc cot')):
        if w in z.split():
            return r
    if w == 'exp' or w == 'e' and nx == '^':
        return 5
    k = f.find('^')
    return 5 if k > 0 and has(f[k + 1:], v) and not has(f[:k], v) else 3


def _pick(g, v):
    # LIATE order -> [u, dv] or None (integrate directly); constants stay in u
    neg, facs = split_factors(g)
    best = -1
    br = 9
    for k in range(len(facs)):
        if facs[k][0] == '*':
            r = _rank(facs[k][1], v)
            if r < br or (r == br and r < 9 and len(facs[k][1]) < len(facs[best][1])):
                br = r
                best = k
    nx = len([q for q in facs if has(q[1], v)])
    if best < 0 or br == 9 or (nx == 1 and br >= 3):
        return None
    u = ('-' if neg else '') + '(' + facs[best][1] + ')'
    dv = '1'
    for k in range(len(facs)):
        if k == best:
            continue
        if has(facs[k][1], v):
            dv += facs[k][0] + '(' + facs[k][1] + ')'
        else:
            u += facs[k][0] + '(' + facs[k][1] + ')'
    return [S(u), N(dv)]


def _ro(h, f):
    # two factors in the order of f: e^x cos(x), not cos(x)e^x
    n, b = sign_body(h)
    a = split_top(b, '*')
    if len(a) == 2 and pp(a[1]) in pp(f) and pp(a[0]) not in pp(f):
        return ('-' if n else '') + a[1] + '*' + a[0]
    return h


def ibp_core(f, v, ia, q=0):
    # repeated / cyclic by parts: I = acc + sg*INT g; returns antiderivative
    # (0: the dv override went round in circles; ask again without it)
    L = []
    acc = '0'
    sg = 1
    g = f
    step = 0
    o = ''
    while step < MAXIBP and has(g, v):
        p = _pick(g, v)
        if p is None or step and [z for z in split_factors(g)[1] if z[0] == '/' and has(z[1], v)]:
            break
        u, dv = p
        vv = S(I(dv, v))
        if bad(vv) and has(u, v) and _lp(u, v) not in ('', '1'):
            # e.g. x^3*e^(x^2): u = x^2, dv = x*e^(x^2)
            u = S('(' + u + ')/' + v)
            dv = S('(' + dv + ')*' + v)
            vv = S(I(dv, v))
        if ia and not step:
            z = _d(dv)
            t = ask('dv/d' + v + ' (enter=accept)', z, 0)
            if t != z:
                dv = o = norm(t)
                u = S('(' + g + ')/(' + dv + ')')
                vv = S(I(dv, v))
        if bad(vv):
            if not step:
                L.append('v not elementary: try substitution')
            break
        du = _df(u, v)
        h = '(' + vv + ')*(' + du + ')'
        w = N(h)
        h = S(h)
        if len(w) <= len(h):
            h = w
        h = _ro(h, f)
        if len(h) > 3 * len(f) + 20:
            _fl(L)
            out('Parts does not simplify: try substitution')
            return None
        step += 1
        L.append('u = ' + _d(u) + ', dv/d' + v + ' = ' + _d(dv))
        L.append('du/d' + v + ' = ' + _d(du) + ', v = ' + _d(vv))
        uv = S('(' + vv + ')*(' + u + ')')
        acc = S('(' + acc + ')+(' + str(sg) + ')*(' + uv + ')')
        # INT g = uv - INT h; keep the new integrand positive
        s2 = -1
        if h[0] == '-':
            h = S('-(' + h + ')')
            s2 = 1
        sg *= s2
        r = Gs('normal((' + h + ')/(' + f + '))')
        c = r and not has(r, v)
        n = s2 < 0
        w = _int(_d(h), v)
        if c:
            n, w = sign_body(S(str(s2) + '*(' + r + ')'))
            w = _cf(w) + 'I'
        L.append(_int(_d(g), v) + ' = ' + _d(uv) + (' - ' if n else ' + ') + w)
        if c:
            k = S(str(sg) + '*(' + r + ')')
            if k != '1':
                _fl(L)
                n, w = sign_body(k)
                out('I = ' + _d(acc) + (' - ' if n else ' + ') + _cf(w) + 'I')
                out(_cf(S('1-(' + k + ')')) + 'I = ' + _d(acc))
                return S('(' + acc + ')/(1-(' + k + '))')
            if o:
                out('dv/d' + v + ' = ' + pp(o) + ': no progress')
                return 0
        g = h
        if step > 1:
            L.append('I = ' + _d(acc) + (' + ' if sg > 0 else ' - ') + _int(_d(g), v))
    _fl(L)
    if g != '0':
        # remaining integral: its value is working, not the answer
        Ig = iterm(g, v, 2)
        if Ig is None:
            return None
        acc = S('(' + acc + ')+(' + str(sg) + ')*(' + Ig + ')')
    if not q:
        out(' = ' + _d(acc))
    return acc


def _sum(parts):
    # keep each antiderivative's form (no log merging); '' if any failed
    for q in parts:
        if q is None:
            return ''
    s = G('+'.join(['(' + q + ')' for q in parts]))
    # Giac's sum unless it only reforms them (3x^(5/3)/5 -> 3x(x^(1/3))^2/5)
    q = join_signed(parts)
    return q if len(_sq(q)) <= len(s) else s


def _defn(F, v, a, b):
    # [F] from a to b = F(b) - F(a)
    sb = lambda z: S('subst(' + F + ',' + v + '=(' + z + '))')
    Fb = sb(b)
    Fa = sb(a)
    R = S('(' + Fb + ')-(' + Fa + ')')
    out('[' + ps(F) + '] from ' + pp(a) + ' to ' + pp(b))
    t = ps(Fb) + ' - ' + (pp(Fa) if Fa[0] != '-' and len(split_terms(Fa)) < 2 else '(' + ps(Fa) + ')')
    if _sq(t) != _sq(pp(R)):
        out(' = ' + t)
    ans('Integral', join_signed(split_terms(R)))


def _end(F, v='x'):
    # limits or + C for the antiderivative F (if it was found), then wait
    if F:
        a = ask('Lower limit (blank=indef.)', '', 0)
        if a:
            _defn(F, v, norm(a), askn('Upper limit', '', 0))
        else:
            ans(_int('f', v), F + ' + C', 0)
    wait()


def _af(p):
    return norm(rhs(ask(p, '', 0)).replace('dx', ''))


def integ():
    hdr('Integrate')
    f = _af('f(x) =')
    v = ask('Variable', 'x', 0)
    out('f(' + v + ') = ' + _tp(ps(f)))
    t = split_terms(f)
    if len(t) < 2:
        n = G('numer(' + f + ')')
        d = G('denom(' + f + ')')
        # (x^2+1)/x = x + 1/x, x^2(x+1) = x^3 + x^2
        if len(split_terms(d)) < 2 and (has(d, v) or len(_split(f, v)[1]) > 1) and \
                Gs('is_polynomial(' + n + ',' + v + ')') == 'true':
            t = split_terms(G('expand(' + f + ')'))
            if len(t) > 1:
                out(' = ' + join_signed([pp(z) for z in t]))
    _end(_sum([iterm(z, v, 0, len(t) < 2) for z in t]), v)


def subst_u():
    hdr('Substitution')
    f = _af('Integrand f(x) =')
    u = norm(ask('Let u =', '', 0))
    out('u = ' + ps(u))
    d = _df(u)
    e = _sec(G('trigcos(' + d + ')')) if 'tan(' in d else d
    if has(G('denom(' + d + ')'), 'x'):
        # du/dx = 1/x: dx = x du
        z = _cf(S('1/(' + d + ')')) + ' du'
    else:
        neg, b = sign_body(e) if len(split_terms(e)) < 2 else (0, e)
        z = pp(b) if len(split_factors(b)[1]) < 2 and len(split_terms(b)) < 2 else '(' + pp(b) + ')'
        z = ('-' if neg else '') + 'du' + ('' if b == '1' else '/' + z)
    out('du/dx = ' + _tp(ps(e)) + ' so dx = ' + _tp(z))
    r = S('(' + f + ')/(' + d + ')')
    gu = ''
    for s in GL('solve(zzu=' + u + ',x)'):
        y = S('subst(' + r + ',x=' + s + ')')
        if not has(y, 'x'):
            gu = y.replace('zzu', 'u')
            break
    if not gu:
        out('Cannot write integrand in u: try another u')
        wait()
        return
    A = []
    for z in split_terms(G('expand(' + gu + ')')):
        y = S(I(z, 'u'))
        if bad(y):
            raise GErr('not integrable in scope')
        z = _pf(z, 'u', y)
        A.append(z[2] if z else y)
    Fu = _sum(A)
    a = ask('Lower limit (blank=indef.)', '', 0)
    if a:
        b = askn('Upper limit', '', 0)
        a = norm(a)
        ua = S('subst(' + u + ',x=(' + a + '))')
        ub = S('subst(' + u + ',x=(' + b + '))')
        out('x = ' + pp(a) + ' -> u = ' + pp(ua) + ', x = ' + pp(b) + ' -> u = ' + pp(ub))
    out(_int(pp(f), 'x') + ' = ' + _int(_kc(gu, 'u'), 'u'))
    if a:
        _defn(Fu, 'u', ua, ub)
    else:
        out(' = ' + ps(Fu) + ' + C')
        k = u.find('(')
        w = u if _br(u) == u or 0 < k and _cl(u, k + 1) == len(u) else '(' + u + ')'
        ans(_int('f', 'x'), Fu.replace('(u)', '(' + u + ')').replace('u', w) + ' + C', 0)
    wait()


def parts():
    hdr('By parts')
    f = _af('Integrand f(x) =')
    out('I = ' + _int(pp(f), 'x'))
    if _pick(f, 'x') is None:
        out('Not a parts case: use Integrate')
        wait()
        return
    F = ibp_core(f, 'x', 1, 1)
    if F == 0:
        F = ibp_core(f, 'x', 0, 1)
    if F is None:
        wait()
        return
    chk = Gs('simplify(' + D(F) + '-(' + f + '))')
    if chk != '0':
        out('check failed: ' + chk)
    _end(F)


def _dg(p):
    return int(G('degree(' + p + ',x)'))


def pfrac():
    hdr('Partial fractions')
    f = _af('Rational f(x) =')
    dn = G('denom(' + f + ')')
    nm = G('numer(' + f + ')')
    if Gs('is_polynomial((' + nm + ')*(' + dn + '),x)') != 'true' or not has(dn, 'x'):
        out('Not a rational function of x')
        wait()
        return
    lp = pp(f)
    out('f(x) = ' + lp)
    h = ' = '
    d = split_top(f, '/')
    # factor the denominator as typed: 1-x^2 = -(x-1)(x+1)
    td = unwrap(d[-1]) if len(d) == 2 else dn
    tl = [unwrap(z[1]) for z in split_factors(td)[1] if has(z[1], 'x')]
    lin = not [z for z in tl if _dg(z) != 1]
    tf = pp(G('factor(' + td + ')'))
    if not lin and _sq(tf) != _sq(pp(td)):
        out(pp(td) + ' = ' + tf)
        h = 'f(x) = '
    if S('(' + td + ')/(' + dn + ')') != '1':
        lp = _pr(nm) + '/' + _br(pp(G('factor(' + dn + ')')))
        out('f(x) = ' + lp)
        h = ' = '
    T = []
    pre = ''
    if _dg(nm) >= _dg(dn):
        q = G('quo(' + nm + ',' + dn + ',x)')
        nm = G('rem(' + nm + ',' + dn + ',x)')
        pre = ps(q) + ' + '
        lp = pre + _br(pp(nm)) + '/' + _br(pp(dn))
        out(h + lp)
        h = ' = '
        T = split_terms(q)
    fs = GL('factors(' + dn + ')')
    L = [fs[j] for j in range(0, len(fs) - 1, 2) if has(fs[j], 'x')]
    P = []
    if nm != '0' and len(L) == 2 and _dg(dn) == 2:
        if lin and len(tl) == 2:
            L = tl
        a, b = L
        out(h + pre + 'A/' + _br(pp(a)) + ' + B/' + _br(pp(b)))
        # divide by the constant factor of the denominator
        nm = S('(' + nm + ')*(' + a + ')*(' + b + ')/(' + dn + ')')
        tn = unwrap(d[0])
        out(ps(tn if len(d) == 2 and S(tn + '-(' + nm + ')') == '0' else nm) + ' = A' +
            _br(pp(b)) + ' + B' + _br(pp(a)))
        for w in ((a, b, 'A'), (b, a, 'B')):
            r = GL('solve(' + w[0] + '=0,x)')[0]
            lh = S('subst(' + nm + ',x=(' + r + '))')
            co = S('subst(' + w[1] + ',x=(' + r + '))')
            C = S('(' + lh + ')/(' + co + ')')
            out('x = ' + pp(r) + ': ' + ('' if co == '1' else pp(lh) + ' = ' + _cf(co) + w[2] + ', ') +
                w[2] + ' = ' + pp(C))
            P.append(G('factor(' + S('(' + C + ')/(' + w[0] + ')') + ')'))
    elif nm != '0':
        P = split_terms(G('partfrac((' + nm + ')/(' + dn + '),x)'))
    r = join_signed([pp(z) for z in T + P])
    if _sq(r) != _sq(lp):
        out('f(x) = ' + r)
    _end(_sum([iterm(t, 'x', 0, 1) for t in T + P]))


def _cl(s, k):
    # index just past the ')' that closes the '(' at s[k - 1]
    d = 1
    while k < len(s) and d:
        d += (s[k] == '(') - (s[k] == ')')
        k += 1
    return k


def _tan2(f):
    # tan(A)^2 -> (sec(A)^2-1); returns (new, changed)
    o = f
    i = o.find('tan(')
    n = 0
    while i >= 0 and n < 6:
        n += 1
        j = _cl(o, i + 4)
        if o[j:j + 2] == '^2':
            o = o[:i] + '(sec' + o[i + 3:j] + '^2-1)' + o[j + 2:]
        i = o.find('tan(', i + 4)
    return o, o != f


def _tp(s):
    # sin(x)^2 -> sin^2(x) (display)
    for nm in ('sin(', 'cos(', 'tan(', 'sec(', 'cot('):
        i = s.find(nm)
        while i >= 0:
            j = _cl(s, i + 4)
            k = j + 1
            while k < len(s) and s[k] in DIG:
                k += 1
            if s[j:j + 1] == '^' and k > j + 1 and (i == 0 or s[i - 1] not in LET):
                s = s[:i + 3] + s[j:k] + s[i + 3:j] + s[k:]
            i = s.find(nm, i + 1)
    return s


def trigpow():
    hdr('Trig powers')
    f = _af('f(x) =')
    s = _sec(f)
    g, ch = _tan2(s)
    if ch:
        g = unwrap(g) if len(split_terms(unwrap(g))) > 1 and unwrap(g) != g else G('expand(' + g + ')')
    elif 'sec(' in s or 'tan(' in s:
        g = s
    else:
        g = G('tlin(' + f + ')')
    out((_tp(ps(f)) if g != f else 'f(x)') + ' = ' + _tp(ps(_sec(g))))
    F = _sum([iterm(t, 'x', 1, 1) for t in split_terms(g)])
    _end(F and _sec(F))


def _sec(s):
    # Giac string: 1/cos(A) -> sec(A), 2/cos(A) -> 2*sec(A), (1/cos(A))^2 -> sec(A)^2
    i = s.find('/cos(')
    while i > 0:
        j = i
        while j and s[j - 1] in DIG:
            j -= 1
        if j < i and (j == 0 or s[j - 1] in '+-*('):
            k = _cl(s, i + 5)
            t = ('' if s[j:i] == '1' else s[j:i] + '*') + 'sec' + s[i + 4:k]
            if j and s[j - 1] == '(' and s[k:k + 2] == ')^':
                j -= 1
                k += 1
            s = s[:j] + t + s[k:]
        i = s.find('/cos(', i + 1)
    return s


ITEMS = [('Integrate', integ), ('Substitution', subst_u), ('By parts', parts),
         ('Partial fractions', pfrac), ('Trig powers', trigpow)]
