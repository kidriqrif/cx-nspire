# ibdiff.py - differentiation with rule-by-rule working (AA 5.3, 5.6, 5.12, 5.14, 5.15)
from ibcore import *

TITLE = 'Differentiation'
STDF = ('sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'exp', 'ln', 'log10',
        'asin', 'acos', 'atan')


def _fn(g):
    # 'name(arg)' -> [name, arg] when the call spans all of g
    k = g.find('(')
    if k <= 0 or g[-1] != ')':
        return None
    for c in g[:k]:
        if c not in LET and c not in DIG:
            return None
    d = 0
    for j in range(k, len(g)):
        if g[j] in OPN:
            d += 1
        elif g[j] in CLS:
            d -= 1
            if d == 0 and j < len(g) - 1:
                return None
    return [g[:k], g[k + 1:-1]]


def _pow(g):
    # 'base^p' at top level -> [base, p]
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


def _al(s):
    # plain name or whole number: needs no brackets as a base/exponent
    for c in s:
        if c not in LET and c not in DIG:
            return False
    return s != ''


def kind(g, v):
    # classify a single factor: const/power/std/chain + chain parts
    g = unwrap(g)
    if not has(g, v):
        return ['const']
    if len(split_terms(g)) > 1:
        return ['other']
    if g == v:
        return ['power', '1']
    f = _fn(g)
    if f:
        if f[0] == 'sqrt':
            if unwrap(f[1]) == v:
                return ['power', '1/2']
            return ['chain', f[1], 'sqrt(U)']
        if unwrap(f[1]) == v and f[0] in STDF:
            return ['std']
        return ['chain', f[1], f[0] + '(U)']
    p = _pow(g)
    if p:
        b, e = p
        if has(b, v) and not has(e, v):
            if b == v:
                return ['power', e]
            return ['chain', b, 'U^' + (e if _al(e) else '(' + e + ')')]
        if not has(b, v) and has(e, v):
            if e == v:
                return ['std']
            return ['chain', e, (b if _al(b) else '(' + b + ')') + '^U']
    return ['other']


def rule_of(t, v):
    neg, fs = split_factors(t)
    xs = [f for f in fs if has(f[1], v)]
    if not xs:
        return 'const'
    num = [f[1] for f in xs if f[0] == '*']
    den = [f[1] for f in xs if f[0] == '/']
    if den and num:
        return 'quotient'
    if len(num) > 1:
        return 'product'
    if den:
        k = kind(den[0], v)
        return 'power' if k[0] == 'power' else 'chain'
    k = kind(num[0], v)
    return k[0]


def _prod(lst):
    if not lst:
        return '1'
    return '*'.join(['(' + a + ')' for a in lst])


# textbook derivative forms (formula booklet); SEC* are display-only
SEC = {'tan': 'sec(U)^2', 'sec': 'sec(U)tan(U)', 'csc': '-cosec(U)cot(U)',
       'cot': '-cosec(U)^2'}
INV = {'sqrt': '1/(2*sqrt(U))', 'asin': '1/sqrt(1-U^2)',
       'acos': '-1/sqrt(1-U^2)', 'atan': '1/(1+U^2)'}


def _fname(outer):
    k = outer.find('(')
    return outer[:k] if k > 0 else ''


def _cy(c, s):
    # coefficient c times s (Giac syntax): 3*sin(u), -sin(u)
    return s if c == '1' else ('-' + s if c == '-1' else c + '*' + s)


def _dr(g, v):
    # derivative, re-evaluated so that 3*2*x shows as 6x
    r = S('diff(' + g + ',' + v + ')')
    q = Gs('(' + r + ')')
    return q if q and len(q) <= len(r) else r


def _ch(b, d):
    # dy/du in x times du/dx as written: 3(x^2-1)^2(2x), (-3/(x^2+1)^2)(2x)
    if len(split_terms(b)) > 1 or len(split_top(b, '/')) > 1:
        b = '(' + b + ')'
    return b + '(' + d + ')'


def _chain(g, v, U, L, c='1'):
    # chain-rule working for factor g (coefficient c) into L;
    # -> [du, fn, inner, dy/dx]
    k = kind(g, v)
    inner = k[1]
    outer = k[2].replace('U', U)
    fn = _fname(k[2])
    du = _dr(inner, v)
    L.append(' ' + U + ' = ' + pp(inner) + ', y = ' + pp(_cy(c, outer)))
    d1 = ' d' + U + '/d' + v + ' = ' + ps(du) + ', dy/d' + U + ' = '
    if fn in SEC:
        L.append(d1 + _secd(c, '1', fn, U))
        L.append(' dy/d' + v + ' = ' + _ch(_secd(c, '1', fn, inner), ps(du)))
        return [du, fn, inner, '']
    dy = S('(' + c + ')*(' + INV[fn].replace('U', U) + ')') if fn in INV else _dr(_cy(c, outer), U)
    L.append(d1 + ps(dy))
    back = G('subst(' + dy + ',' + U + '=(' + inner + '))')
    if fn in INV:
        back = G('expand(' + back + ')')
    L.append(' dy/d' + v + ' = ' + _ch(pp(back), ps(du)))
    return [du, fn, inner, S('(' + back + ')*(' + du + ')')]


def _dd(g, v):
    # derivative of one factor -> [value, display (textbook form)]
    r = _dr(g, v)
    k = kind(g, v)
    fn = _fname(unwrap(g)) if k[0] == 'std' else (_fname(k[2]) if k[0] == 'chain' else '')
    if fn in SEC:
        i = k[1] if k[0] == 'chain' else v
        return [r, _secd('1', _dr(i, v), fn, i)]
    if k == ['power', '1/2'] and unwrap(g)[:5] == 'sqrt(':
        return [r, '1/(2' + pp(g) + ')']
    return [r, ps(r)]


def _br(a):
    # bracket a displayed factor that is a sum
    return '(' + a + ')' if len(split_terms(a)) > 1 else a


def _bp(a):
    # bracket unless a symbol, number or function call: (x^3)^2, (2x)^2, sin(x)^2
    return a if a.isdigit() or len(a) == 1 and a in LET or a[0] in LET and _fn(a) else '(' + a + ')'


def _mul(a, b):
    # displayed product as written: 2x sin(x), 2x(x^3), x^3(1/x), e^(2x)(-sin(x))
    if a == '1':
        return b
    if b == '1':
        return a
    a = _br(a)
    b = _br(b)
    if '(' in a and '(' not in b:
        a, b = b, a
    if '/' in a:
        a = '(' + a + ')'
    if '/' in b or b[0] == '-' or b[0] in DIG or (
            not isnum(a) and a[-1] in LET + DIG and b[1:2] in ('', '^') and b[0] in LET and b[0] != 'e'):
        b = '(' + b + ')'
    return a + (' ' if a[-1] not in '()' and b[0] in LET and not isnum(a) else '') + b


def _secd(c, du, fn, inner):
    # display of c*du*sec-family derivative
    m = S('(' + c + ')*(' + du + ')')
    t = SEC[fn].replace('U', pp(inner))
    if t[0] == '-':
        m = S('-(' + m + ')')
        t = t[1:]
    if m == '1':
        return t
    if m == '-1':
        return '-' + t
    if len(split_terms(m)) > 1:
        return '(' + ps(m) + ')' + t
    return pp(m) + t


def _cf(c):
    # coefficient as a factor: '' / '-' / 3 / (1/2)
    if c in ('1', '-1'):
        return c[:-1]
    return pp(c) if isnum(c) and '/' not in c else '(' + pp(c) + ')'


def _xp(v, e):
    # v^e as written: x^0 -> '', x^1 -> x
    if e == '0':
        return ''
    if e == '1':
        return v
    return v + '^' + (e if _al(e) else '(' + pp(e) + ')')


def term_work(t, v, U):
    # working lines for one signed term -> [derivative, display, lines, raw]
    neg, fs = split_factors(t)
    k = [f[1] for f in fs if not has(f[1], v) and f[0] == '*']
    kd = [f[1] for f in fs if not has(f[1], v) and f[0] == '/']
    num = [f[1] for f in fs if has(f[1], v) and f[0] == '*']
    den = [f[1] for f in fs if has(f[1], v) and f[0] == '/']
    r = rule_of(t, v)
    res = _dr(t, v)
    disp = raw = ''
    L = []
    hd = 'd/d' + v + '[' + pp(t) + ']'
    tag = {'chain': 'chain rule', 'product': 'product rule',
           'quotient': 'quotient rule'}
    if r in tag:
        L.append(hd + '  (' + tag[r] + ')')
    c = S(('-' if neg else '') + _prod(k) + '/' + _prod(kd))
    cs = _cf(c)
    if r == 'power':
        g = num[0] if num else den[0]
        n = S(kind(g, v)[1] if num else '-(' + kind(g, v)[1] + ')')
        if den or g != v and not g.startswith(v + '^'):
            # rewrite as a power first: 4/x^2 = 4x^(-2)
            w = cs + _xp(v, n)
            L.append(pp(t) + ' = ' + w)
            hd = 'd/d' + v + '[' + w + ']'
        e = S(n + '-1')
        m = _xp(v, e)
        if c in ('1', '-1'):
            m = _cf(S(c + '*(' + n + ')')) + m
        else:
            m = cs + '(' + pp(n) + ')' + m
        if '/' in e:
            # rational power: keep c x^(n-1), as Giac would rationalise it
            cn = S('(' + c + ')*(' + n + ')')
            disp = _cf(cn) + _xp(v, e)
            raw = _cy(cn, v + '^(' + e + ')')
        else:
            disp = ps(res)
        L.append(hd + ' = ' + (m + ' = ' if n != '1' and _sq(m) != _sq(disp) else '') + disp)
    elif r == 'std':
        fn = _fname(unwrap(num[0])) if num else ''
        if fn in SEC:
            disp = _secd(c, '1', fn, v)
        elif fn in INV:
            res = S('(' + c + ')*(' + INV[fn].replace('U', v) + ')')
        disp = disp or ps(res)
        L.append(hd + ' = ' + disp)
    elif r == 'chain':
        if num:
            ch = _chain(num[0], v, U, L, c)
            if ch[1] in SEC:
                disp = _secd(c, ch[0], ch[1], ch[2])
            elif ch[1] in INV:
                res = ch[3]
        else:
            g = den[0]
            L.append(' ' + pp(t) + ' = ' + cs + '(' + pp(unwrap(g)) + ')^(-1)')
            _chain('(' + g + ')^(-1)', v, U, L, c)
    elif r == 'product':
        u = num[0]
        w = _prod(num[1:]) if len(num) > 2 else num[1]
        du, dud = _dd(u, v)
        dw, dwd = _dd(w, v)
        L.append(' u = ' + pp(u) + ', v = ' + pp(w))
        L.append(" u' = " + dud + _note(u, v))
        L.append(" v' = " + dwd + _note(w, v))
        d0 = join_signed([_mul(dud, pp(w)), _mul(pp(u), dwd)])
        if cs:
            d0 = cs + '(' + d0 + ')'
        L.append(' ' + cs + "(u'v + uv') = " + d0 if cs else " u'v + uv' = " + d0)
        if 'sec(' in dud + dwd or 'cot(' in dud + dwd:
            disp = d0
    elif r == 'quotient':
        u = _prod(num) if len(num) > 1 else unwrap(num[0])
        w = _prod(den) if len(den) > 1 else unwrap(den[0])
        du = _dr(u, v)
        dw = _dr(w, v)
        L.append(' u = ' + pp(u) + ', v = ' + pp(w))
        L.append(" u' = " + ps(du) + _note(u, v))
        L.append(" v' = " + ps(dw) + _note(w, v))
        d2 = _bp(pp(w)) + '^2'
        L.append(' ' + cs + "(u'v - uv')/v^2 = " + cs + '(' + _br(_mul(ps(du), pp(w))) + ' - ' +
                 _br(_mul(pp(u), ps(dw))) + ')/' + d2)
        q = S('(' + c + ')*((' + du + ')*(' + w + ')-(' + u + ')*(' + dw + '))')
        g = Gs('gcd(' + q + ',' + w + ')')
        if q != '0' and '/' not in q and g in ('', '1'):
            # keep v^2 unexpanded: -2/(x-1)^2
            b = len(split_terms(q)) > 1
            disp = ('(' + pp(q) + ')' if b else ps(q)) + '/' + d2
            if '(' not in q:
                raw = ('(' + q + ')' if b else q) + '/' + _bp(w) + '^2'
    elif r == 'const':
        L.append(hd + ' = 0')
    if not disp:
        disp = ps(res)
    if not L:
        L.append(hd)
    if _rs(L[-1]) != _sq(disp):
        L.append(' = ' + disp)
    return [res, disp, L, raw or res]


def _sq(s):
    return s.replace(' ', '')


def _ts(s):
    # the terms of a displayed sum, in a fixed order
    return sorted([t.lstrip('+') for t in split_terms(_sq(s))])


def _rs(s):
    # right-hand side of a working line (squashed)
    return _sq(s[s.rfind(' = ') + 3:])


def _note(g, v):
    k = kind(g, v)
    if k[0] == 'chain':
        return '  (chain rule)'
    return ''


def _uvar(v):
    return 'w' if v == 'u' else 'u'


def _tk(e):
    T = []
    i = 0
    n = len(e)
    while i < n:
        j = i + 1
        if e[i] in LET:
            while j < n and e[j] in LET:
                j += 1
        T.append(e[i:j])
        i = j
    return T


def _rep(e, v, a):
    # e with v replaced by a, bracketed as a student does: 3(2)^2, 2^3, (x+h+1)^2
    pl = True
    for c in a:
        if c not in LET and c not in DIG and c != '.':
            pl = False
    T = _tk(e.replace(' ', ''))
    for k in range(len(T)):
        if T[k] == v:
            p = T[k - 1] if k else ''
            q = T[k + 1] if k + 1 < len(T) else ''
            n = T[k + 2] if k + 2 < len(T) else ''
            # bare in f(x), beside + - inside a bracket, or a plain value
            # that is not next to a number: 2^3, 5(10 - 2(5)); else (a)
            if not (p + q == '()' or p in ('(', '') and q in ('+', '-', ')', '') or
                    pl and not (p == '*' and a[:1].isdigit() or q == '*' and n.isdigit())):
                T[k] = '(' + a + ')'
            else:
                T[k] = a
    return ''.join(T)


def _lx(s):
    # ln(2)*2^x -> 2^x ln(2): the power is written first
    m = '×' if CFG['uni'] else '*'
    i = s.find('ln(')
    for _ in range(6):
        if i < 0:
            break
        j = s.find(')', i) + 1
        k = j + len(m)
        b = s[i + 3:j - 1] + '^'
        f = k + len(b)
        if b[0] in DIG and s[j:k] == m and s[k:f] == b:
            f = s.find(')', f) + 1 if s[f:f + 1] == '(' else f + 1
            w = s[k:f]
            if i and s[i - 1] in DIG:
                w = '(' + w + ')'
            s = s[:i] + w + ' ' + s[i:j] + s[f:]
        i = s.find('ln(', i + 1)
    return s


def _fin(L, A, lbl, r=''):
    # print working, dropping a last line that only repeats the answer;
    # A displayed as is (ans() would re-split its spaces), r exact value
    s = L[-1] if L else ''
    if _rs(s) == _sq(A):
        k = s.rfind(' = ')
        L[-1] = s[:k] if ' = ' in s[:k] else ''
    for s in L:
        if s.strip():
            out(_lx(s))
    if r:
        ans(lbl, join_signed(split_terms(r)))
    else:
        out(_lx('ANS: ' + lbl + ' = ' + A))


def _at(f, v, a, nm, sub=1, d=''):
    # nm(a) = substitution (of d, else f), then ANS
    a = norm(a)
    val = S('subst(' + f + ',' + v + '=(' + a + '))')
    w = ps(_rep(d or f, v, a))
    _fin([nm + '(' + pp(a) + ') = ' + w] if sub else [], ps(val), nm + '(' + pp(a) + ')', val)


def diff_steps():
    hdr('Differentiate')
    f = norm(rhs(ask('f(x) =', '', 0)))
    v = ask('Variable', 'x', 0)
    U = _uvar(v)
    terms = split_terms(f)
    out('f(' + v + ') = ' + ps(f))
    parts = []
    L = []
    for t in terms:
        p = term_work(t, v, U)
        parts.append(p)
        L += p[2]
    comb = join_signed([p[1] for p in parts])
    fin = S('+'.join(['(' + p[0] + ')' for p in parts]))
    sec = 0
    for p in parts:
        if 'sec(' in p[1] or 'cot(' in p[1]:
            sec = 1
    A = ps(fin)
    if len(terms) < 2 or sec or [p for p in parts if p[3] != p[0]] or _ts(A) == _ts(comb):
        A = comb
    if len(terms) > 1:
        L.append("f'(" + v + ') = ' + comb)
    _fin(L, A, "f'(" + v + ')')
    a = ask('Evaluate at ' + v + ' = (blank=skip)', '', 0)
    if a:
        _at(fin, v, a, "f'", not sec, join_signed([p[3] for p in parts]) if A == comb else '')
    wait()


def _fp(p):
    # x,h polynomial in student order: by degree, then falling power of x
    T = []
    for t in split_terms(G('expand(' + p + ')')):
        a = b = 0
        for f in split_factors(t)[1]:
            g = f[1]
            if g[0] in 'xh' and (len(g) == 1 or g[1] == '^'):
                n = int(g[2:]) if len(g) > 1 else 1
                if g[0] == 'x':
                    a += n
                else:
                    b += n
        m = '*'.join([q for q in (_xp('x', str(a)), _xp('h', str(b))) if q]) or '1'
        T.append([-100 * (a + b) - a, N('(' + t + ')/(' + m + ')'), m])
    T.sort(key=lambda q: q[0])
    s = ''
    for q in T:
        c = q[1]
        t = c if q[2] == '1' else (c[:-1] if c in ('1', '-1') else c + '*') + q[2]
        s += t if t[0] == '-' or not s else '+' + t
    return ps(s)


def first_principles():
    hdr('First principles')
    f = norm(rhs(ask('Polynomial f(x) =', '', 0)))
    if G('is_polynomial(' + f + ',x)') != 'true':
        out('Polynomials only (AA 5.12)')
        wait()
        return
    u = CFG['uni']
    lim = "f'(x) = lim h" + ('→' if u else '->') + '0 '
    out('f(x) = ' + ps(f))
    out(lim + '(f(x+h) - f(x))/h')
    fh = 'subst(' + f + ',x=x+h)'
    w = ps(_rep(f, 'x', 'x+h'))
    e = _fp(fh)
    out('f(x+h) = ' + (w + ' = ' if _sq(unwrap(w)) != _sq(e) else '') + e)
    dif = fh + '-(' + f + ')'
    out('f(x+h) - f(x) = ' + _fp(dif))
    q = G('expand(normal((' + dif + ')/h))')
    out('(f(x+h) - f(x))/h = ' + _fp(q) + '  (h ' + ('≠' if u else '!=') + ' 0)')
    _fin([lim + '(' + _fp(q) + ')'], _fp(G('subst(' + q + ',h=0)')), "f'(x)")
    wait()


def higher():
    hdr('Higher derivatives')
    f = norm(rhs(ask('f(x) =', '', 0)))
    v = ask('Variable', 'x', 0)
    n = int(ask('Up to order n', '2', 0))
    if n < 1 or n > 6:
        n = 1 if n < 1 else 6
        out('order 1 to 6 only: n = ' + str(n))
    out('f(' + v + ') = ' + ps(f))
    cur = f
    marks = ["'", "''", "'''", '^(4)', '^(5)', '^(6)']
    L = []
    for k in range(n):
        cur = S('diff(' + cur + ',' + v + ')')
        L.append('f' + marks[k] + '(' + v + ') = ' + ps(cur))
    _fin(L, ps(cur), 'f' + marks[n - 1] + '(' + v + ')')
    a = ask('Evaluate at ' + v + ' = (blank=skip)', '', 0)
    if a:
        _at(cur, v, a, 'f' + marks[n - 1])
    wait()


def _dy(c):
    # c dy/dx as written: 2y dy/dx, (x^2 + 3y^2)dy/dx
    if c in ('1', '-1'):
        return c[:-1] + 'dy/dx'
    if len(split_terms(c)) > 1 or '/' in c:
        return '(' + ps(c) + ')dy/dx'
    return pp(c) + ' dy/dx'


def implicit():
    hdr('Implicit diff (x,y)')
    e = norm(ask('Equation in x,y', '', ''))
    k = e.find('=')
    L = e[:k] if k >= 0 else e
    R = e[k + 1:] if k >= 0 else '0'
    sx = []
    sy = []
    shown = []
    for side, sg in ((L, '1'), (R, '-1')):
        row = []
        for t in split_terms(side):
            fx = _dr(t, 'x')
            fy = _dr(t, 'y')
            sx.append('(' + sg + ')*(' + fx + ')')
            sy.append('(' + sg + ')*(' + fy + ')')
            if fy == '0':
                row.append(ps(fx))
            elif fx == '0':
                row.append(_dy(fy))
            else:
                row.append(join_signed([ps(fx), _dy(fy)]))
            out(' d/dx[' + pp(t) + '] = ' + row[-1])
        shown.append(join_signed(row))
    out(shown[0] + ' = ' + shown[1])
    A = S('+'.join(sy))
    B = S('-(' + '+'.join(sx) + ')')
    w = _dy(A) + ' = ' + ps(B)
    if A != '1' and _sq(w) != _sq(shown[0] + '=' + shown[1]):
        out(w)
    res = S('(' + B + ')/(' + A + ')')
    _fin([], ps(res), 'dy/dx')
    a = ask('At point (x,y) (blank=skip)', '', 0)
    if a:
        p = [norm(z) for z in split_top(a.strip('()[] '), ',')]
        val = S('subst(' + res + ',[x,y],[' + p[0] + ',' + p[1] + '])')
        w = ['dy/dx = ' + ps(_rep(_rep(res, 'x', p[0]), 'y', p[1]))]
        lb = 'dy/dx at (' + pp(p[0]) + ',' + pp(p[1]) + ')'
        if 'inf' in val or 'undef' in val:
            # zero denominator
            _fin(w, 'undefined' + (' (vertical tangent)' if 'inf' in val else ''), lb)
        else:
            _fin(w, ps(val), lb, val)
    wait()


ITEMS = [('Step differentiate', diff_steps), ('First principles', first_principles),
         ('Higher derivatives', higher), ('Implicit dy/dx', implicit)]
