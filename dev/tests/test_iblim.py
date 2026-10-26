# Tests for calc/iblim.py (limits and Maclaurin series, AA 5.13, 5.19).
# Every expected answer below was checked by hand.
MODULE = 'iblim'
CASES = [
    # ---- l'Hopital ----
    # sin x / x: cos 0 / 1 = 1
    ('lhop', ['sin(x)/x', ''],
     ['lim_(x->0) sin(x)/x', 'x = 0 gives 0/0', "= lim cos(x)/1 (l'Hopital)", 'ANS: lim = 1'],
     ['Form', 'Substitute', "f'(x)", '= 1\nANS']),
    # (1-cos x)/x^2: sin x/2x -> cos x/2 -> 1/2 (twice)
    ('lhop', ['(1-cos(x))/x^2', '0'],
     ['lim_(x->0) (1-cos(x))/x^2', "= lim sin(x)/(2x) (l'Hopital)", "= lim cos(x)/2 (l'Hopital)",
      'ANS: lim = 1/2']),
    # (tan x - x)/x^3: f''' = 6tan^4+8tan^2+2 -> 2, g''' = 6 -> 1/3
    ('lhop', ['(tan(x)-x)/x^3', '0'],
     ["= lim tan(x)^2/(3x^2) (l'Hopital)", "= lim (2tan(x)^3 + 2tan(x))/(6x) (l'Hopital)",
      "= lim (6tan(x)^4 + 8tan(x)^2 + 2)/6 (l'Hopital)", '= 2/6', 'ANS: lim = 1/3']),
    # 0 x inf: x ln x = ln x/(1/x); (1/x)/(-1/x^2) = -x -> 0
    ('lhop', ['x*ln(x)', '0+'],
     ['lim_(x->0+) x ln(x)', '= lim ln(x)/(1/x)', 'x -> 0+ gives -inf/inf', "= lim (1/x)/(-1/x^2) (l'Hopital)",
      '= lim -x', 'ANS: lim = 0'], ['Rewrite', 'Form']),
    # x^2 ln x = ln x/(1/x^2); (1/x)/(-2/x^3) = -x^2/2 -> 0
    ('lhop', ['x^2*ln(x)', '0+'],
     ['= lim ln(x)/(1/x^2)', '= lim -x^2/2', 'ANS: lim = 0']),
    # x e^x, x -> -inf: x/e^(-x) -> 1/(-e^(-x)) -> 0
    ('lhop', ['x*e^x', '-inf'],
     ['lim_(x->-inf) xe^x', '= lim x/e^(-x)', 'x -> -inf gives -inf/inf', "= lim 1/(-e^(-x)) (l'Hopital)",
      'x -> -inf gives 1/(-inf)', 'ANS: lim = 0'], ['*']),
    # x sin(1/x), x -> inf: sin(1/x)/(1/x) -> cos(1/x) -> 1
    ('lhop', ['x*sin(1/x)', 'inf'],
     ['= lim sin(1/x)/(1/x)', 'x -> inf gives 0/0', '= lim cos(1/x)', 'ANS: lim = 1']),
    # inf/inf twice: 6x/(4x-1) -> 6/4 = 3/2
    ('lhop', ['(3x^2+1)/(2x^2-x)', 'inf'],
     ['x -> inf gives inf/inf', "= lim 6x/(4x - 1) (l'Hopital)", "= lim 6/4 (l'Hopital)", 'ANS: lim = 3/2'],
     ['\n= 6/4\n']),
    # ln x / sqrt x: (1/x)/(1/(2 sqrt x)) = 2/sqrt(x) -> 0
    ('lhop', ['ln(x)/sqrt(x)', 'inf'],
     ["= lim (1/x)/(sqrt(x)/(2x)) (l'Hopital)", '= lim 2/sqrt(x)', 'x -> inf gives 2/inf', 'ANS: lim = 0']),
    # combine 1/x - 1/sin x = (sin x - x)/(x sin x); f''(0)/g''(0) = 0/2
    ('lhop', ['1/x - 1/sin(x)', '0'],
     ['lim_(x->0) (1/x - 1/sin(x))', '= lim (-x + sin(x))/(x sin(x))',
      "= lim (cos(x) - 1)/(sin(x) + x cos(x)) (l'Hopital)",
      "= lim -sin(x)/(-x sin(x) + 2cos(x)) (l'Hopital)", '= 0/2', 'ANS: lim = 0'], ['Combine']),
    # x -> pi: cos(pi)/1 = -1
    ('lhop', ['sin(x)/(x-pi)', 'pi'],
     ['x = pi gives 0/0', "= lim cos(x)/1 (l'Hopital)", 'ANS: lim = -1']),
    # one-sided from the left: (e^x - 1)/x -> e^0/1 = 1
    ('lhop', ['y = (e^x-1)/x', '0-'],
     ['lim_(x->0-) (e^x-1)/x', 'x -> 0- gives 0/0', "= lim e^x/1 (l'Hopital)", 'ANS: lim = 1']),
    # x^2/(1-cos x): 2/cos 0 = 2
    ('lhop', ['x^2/(1-cos(x))', ''],
     ["= lim 2x/sin(x) (l'Hopital)", "= lim 2/cos(x) (l'Hopital)", 'ANS: lim = 2']),
    # irrational answer: (2^x ln 2)/1 at 0 = ln 2 ~ 0.693
    ('lhop', ['(2^x-1)/x', '0'],
     ["(l'Hopital)", 'ANS: lim = ln(2)', '~ 0.693']),
    ('limser', ['(2^x-1)/x'],
     ['2^x = 1 + ln(2)x + (ln(2)^2/2)x^2', '= lim (ln(2)x + (ln(2)^2/2)x^2 + (ln(2)^3/6)x^3 + ...)/x',
      '= lim (ln(2) + (ln(2)^2/2)x + (ln(2)^3/6)x^2 + ...)', 'ANS: lim = ln(2)'], ['Divide', '/(1)']),
    # not indeterminate: direct substitution
    ('lhop', ['(x+1)/(x+2)', '0'], ['lim_(x->0) (x+1)/(x+2)', 'ANS: lim = 1/2'], ['Form', "(l'Hopital)", 'gives']),
    # 0/inf is not indeterminate (no l'Hopital, no "still indeterminate")
    ('lhop', ['e^(-x)/x', 'inf'], ['x -> inf gives 0/inf', 'ANS: lim = 0'], ['Form', 'indeterminate', "(l'Hopital)"]),
    # k/0: two-sided limit does not exist
    ('lhop', ['(x+1)/(x-1)', '1'], ['x = 1 gives 2/0', 'Limit does not exist (+-inf)'], ['ANS', 'k/0']),
    ('lhop', ['sin(x)/x^2', ''],
     ["= lim cos(x)/(2x) (l'Hopital)", 'x = 0 gives 1/0', 'Limit does not exist (+-inf)'], ['ANS']),

    # ---- limit by Maclaurin series ----
    ('limser', ['sin(x)/x'],
     ['lim_(x->0) sin(x)/x', 'x = 0 gives 0/0', 'sin(x) = x - x^3/6 + ...', '= lim (x - x^3/6 + ...)/x',
      '= lim (1 - x^2/6 + ...)', 'ANS: lim = 1'], ['Divide', '/(1)', 'Form', 'Substitute']),
    # x - sin x = x^3/6 - x^5/120 + ...
    ('limser', ['(x-sin(x))/x^3'],
     ['x - sin(x) = x^3/6 - x^5/120 + ...', '= lim (x^3/6 - x^5/120 + ...)/x^3',
      '= lim (1/6 - x^2/120 + ...)', 'ANS: lim = 1/6'], ['g(x) = x^3']),
    # ln(1+x) - x = -x^2/2 + x^3/3 - ...
    ('limser', ['(ln(1+x)-x)/x^2'],
     ['ln(1+x) = x - x^2/2 + x^3/3 - x^4/4 + ...', '= lim (-1/2 + x/3 - x^2/4 + ...)', 'ANS: lim = -1/2']),
    # (e^2x - 1)/sin x = (2x + 2x^2 + ...)/(x - x^3/6 + ...) -> 2
    ('limser', ['(e^(2x)-1)/sin(x)'],
     ['e^(2x) = 1 + 2x + 2x^2 + 4x^3/3 + ...', 'sin(x) = x - x^3/6 + ...',
      '= lim (2 + 2x + 4x^2/3 + ...)/(1 - x^2/6 + ...)', 'ANS: lim = 2'], ['g(x) = x - x^3/6']),
    # 1 - cos 2x = 2x^2 - 2x^4/3; x ln(1+x) = x^2 - x^3/2 + x^4/3 -> 2
    ('limser', ['(1-cos(2x))/(x*ln(1+x))'],
     ['cos(2x) = 1 - 2x^2 + 2x^4/3 + ...', '1 - cos(2x) = 2x^2 - 2x^4/3 + ...',
      'x ln(1+x) = x^2 - x^3/2 + x^4/3 + ...', '= lim (2 - 2x^2/3 + ...)/(1 - x/2 + x^2/3 + ...)',
      'ANS: lim = 2']),
    # 1/x - 1/sin x -> 0 (combined first)
    ('limser', ['1/x-1/sin(x)'],
     ['= lim (-x + sin(x))/(x sin(x))', '-x + sin(x) = -x^3/6 + ...', 'x sin(x) = x^2 - x^4/6 + ...',
      '= lim (-x/6 + ...)/(1 - x^2/6 + ...)', 'ANS: lim = 0'], ['Combine']),
    # not 0/0
    ('limser', ['(x+1)/(x+2)'], ['ANS: lim = 1/2'], ['series', 'gives']),
    # lower power on top: x/(x^2/2 + ...) -> 1/0
    ('limser', ['x/(e^x-1-x)'],
     ['x = 0 gives 0/0', '= lim 1/(x/2 + x^2/6 + ...)', 'x = 0 gives 1/0', 'Limit does not exist'], ['ANS']),
    # out of scope: ln x has no Maclaurin series
    ('limser', ['ln(x)/x'], ['No Maclaurin series at 0'], ['ANS']),

    # ---- Maclaurin from derivatives ----
    ('mderiv', ['e^(2x)', '4'],
     ['f(x) = e^(2x)', "f'(x) = 2e^(2x)", 'f^(4)(x) = 16e^(2x)', 'f^(4)(0) = 16',
      "f(x) = f(0) + f'(0)x + f''(0)x^2/2! + ...",
      '= 1 + 2x + 4x^2/2! + 8x^3/3! + 16x^4/4! + ...',
      'ANS: f(x) = 1 + 2x + 2x^2 + 4x^3/3 + 2x^4/3 + ...'], ['f(4)']),
    ('mderiv', ['ln(1+x)', '3'],
     ["f'(x) = 1/(1+x)", "f''(x) = -1/(1+x)^2", "f'''(x) = 2/(x+1)^3", "f'''(0) = 2",
      '= x - x^2/2! + 2x^3/3! + ...', 'ANS: f(x) = x - x^2/2 + x^3/3 + ...']),
    # binomial check: c2 = (1/2)(-1/2)/2 = -1/8, c3 = (1/2)(-1/2)(-3/2)/6 = 1/16
    ('mderiv', ['sqrt(1+x)', '3'],
     ["f'(0) = 1/2", "f''(0) = -1/4", "f'''(0) = 3/8",
      'ANS: f(x) = 1 + x/2 - x^2/8 + x^3/16 + ...']),
    # sec: f''(0) = 1, f''''(0) = 5
    ('mderiv', ['sec(x)', '4'],
     ["f'(0) = 0", "f''(0) = 1", 'f^(4)(0) = 5', 'ANS: f(x) = 1 + x^2/2 + 5x^4/24 + ...']),
    ('mderiv', ['tan(x)', '5'],
     ["f'(x) = 1 + tan(x)^2", 'f^(5)(0) = 16', 'ANS: f(x) = x + x^3/3 + 2x^5/15 + ...']),
    ('mderiv', ['ln(cos(x))', '4'],
     ["f'(x) = -tan(x)", "f''(0) = -1", 'f^(4)(0) = -2', 'ANS: f(x) = -x^2/2 - x^4/12 + ...']),
    # out of scope: f(0) undefined
    ('mderiv', ['ln(x)', '3'], ['f(0) undefined: no series'], ['ANS']),
    # up to x^1 the raw line would repeat the answer
    ('mderiv', ['sin(x)', '1'], ['f(0) = 0', "f'(0) = 1", 'ANS: f(x) = x + ...'], ['\n = x']),

    # ---- Maclaurin by substitution ----
    ('msub', ['e^(-x^2)', '6'],
     ['f(x) = e^(-x^2)', 'e^u = 1 + u + u^2/2 + u^3/6 + ...', 'u = -x^2',
      'e^(-x^2) = 1 + (-x^2) + (-x^2)^2/2 + (-x^2)^3/6 + ...',
      'ANS: f(x) = 1 - x^2 + x^4/2 - x^6/6 + ...'], ['Standard']),
    # sin 2x = 2x - 8x^3/6 + 32x^5/120
    ('msub', ['sin(2x)', '5'],
     ['sin(u) = u - u^3/6 + u^5/120 + ...', 'u = 2x', 'sin(2x) = 2x - (2x)^3/6 + (2x)^5/120 + ...',
      'ANS: f(x) = 2x - 4x^3/3 + 4x^5/15 + ...']),
    ('msub', ['ln(2+x)', '3'],
     ['f(x) = ln(2+x) = ln(2) + ln(1+x/2)', 'ln(1+u) = u - u^2/2 + u^3/3 + ...', 'u = x/2',
      'ln(1+x/2) = x/2 - (x/2)^2/2 + (x/2)^3/3 + ...',
      'ANS: f(x) = ln(2) + x/2 - x^2/8 + x^3/24 + ...']),
    # (2-x)^-2 = (1/4)(1 - x/2)^-2 = (1/4)(1 + x + 3x^2/4 + x^3/2)
    ('msub', ['1/(2-x)^2', '3'],
     ['f(x) = 1/(2-x)^2 = (1/4)(1-x/2)^(-2)', '(1+u)^(-2) = 1 - 2u + 3u^2 - 4u^3 + ...',
      'f(x) = (1/4)(1 + x + 3x^2/4 + x^3/2 + ...)',
      'ANS: f(x) = 1/4 + x/4 + 3x^2/16 + x^3/8 + ...']),
    # sqrt(4+x) = 2(1 + x/8 - x^2/128)
    ('msub', ['sqrt(4+x)', '2'],
     ['f(x) = sqrt(4+x) = 2(1+x/4)^(1/2)', 'ANS: f(x) = 2 + x/4 - x^2/64 + ...']),
    ('msub', ['(1-2x)^(-1/2)', '3'], ['u = -2x', 'ANS: f(x) = 1 + x + 3x^2/2 + 5x^3/2 + ...']),
    # x^2 cos 3x: cos 3x = 1 - 9x^2/2 + 81x^4/24
    ('msub', ['x^2*cos(3x)', '6'],
     ['f(x) = x^2 cos(3x)', 'f(x) = x^2 (1 - 9x^2/2 + 27x^4/8 + ...)',
      'ANS: f(x) = x^2 - 9x^4/2 + 27x^6/8 + ...'], ['cos(3x) = x^2', '*']),
    ('msub', ['(1+x)/(1-x)', '3'],
     ['(1-x)^(-1) = 1 - (-x) + (-x)^2 - (-x)^3 + ...', 'f(x) = (1+x)(1 + x + x^2 + x^3 + ...)',
      'ANS: f(x) = 1 + 2x + 2x^2 + 2x^3 + ...']),
    # composite: ln(cos x) = ln(1 + (cos x - 1))
    ('msub', ['ln(cos(x))', '4'],
     ['u = cos(x)-1 = -x^2/2 + x^4/24 + ...', 'ln(1+(cos(x)-1)) = (cos(x)-1) - (cos(x)-1)^2/2 + ...',
      'ANS: f(x) = -x^2/2 - x^4/12 + ...']),
    # e^(sin x): x^3 terms cancel (-1/6 + 1/6)
    ('msub', ['e^(sin(x))', '3'],
     ['u = sin(x) = x - x^3/6 + ...', 'e^(sin(x)) = 1 + sin(x) + (sin(x))^2/2 + (sin(x))^3/6 + ...',
      'ANS: f(x) = 1 + x + x^2/2 + ...']),
    ('msub', ['cos(sqrt(x))', '2'], ['u = sqrt(x)', 'ANS: f(x) = 1 - x/2 + x^2/24 + ...']),
    ('msub', ['e^x*sin(x)', '3'], ['Not a standard substitution', 'use Series product'], ['ANS']),
    ('msub', ['ln(x)', '3'], ['Not a standard substitution'], ['ANS', 'product']),

    # ---- series product ----
    ('mprod', ['e^x', 'sin(x)', '3'],
     ['f(x) = e^x = 1 + x + x^2/2 + x^3/6 + ...', 'g(x) = sin(x) = x - x^3/6 + ...',
      'f(x)g(x) = (1 + x + x^2/2 + x^3/6)(x - x^3/6)', '= x + x^2 - x^3/6 + x^3/2 + ...',
      'ANS: f(x)g(x) = x + x^2 + x^3/3 + ...'], ['(1)(']),
    ('mprod', ['e^x', 'ln(1+x)', '3'],
     ['= x - x^2/2 + x^2 + x^3/3 - x^3/2 + x^3/2 + ...',
      'ANS: f(x)g(x) = x + x^2/2 + x^3/3 + ...']),
    # x^4: 1/24 + 1/16 - 5/128 = (16 + 24 - 15)/384
    ('mprod', ['(1+x)^(1/2)', 'cos(x)', '4'],
     ['= 1 + x/2 - x^2/2 - x^2/8 - x^3/4 + x^3/16 + x^4/24 + x^4/16 - 5x^4/128 + ...',
      'ANS: f(x)g(x) = 1 + x/2 - 5x^2/8 - 3x^3/16 + 25x^4/384 + ...']),
    ('mprod', ['ln(x)', 'e^x', '3'], ['No Maclaurin series'], ['ANS']),
    # nothing to collect: the expansion is already the answer
    ('mprod', ['x', 'e^x', '3'], ['f(x)g(x) = (x)(1 + x + x^2/2 + x^3/6)', 'ANS: f(x)g(x) = x + x^2 + x^3/2 + ...'],
     ['\n= x']),

    # ---- series from a differential equation ----
    # exact y = 2e^x - x - 1
    ('mode', ['x+y', '1', '3'],
     ["y' = x + y", "y'(0) = 1", "y'' = 1 + y'", "y''(0) = 1 + 1 = 2", "y'''(0) = 2",
      '= 1 + x + 2x^2/2! + 2x^3/3! + ...', 'ANS: y = 1 + x + x^2 + x^3/3 + ...'], ['dy/dx = x+y']),
    # y'' = 1 + 2yy' = 3, y''' = 2y'^2 + 2yy'' = 8, y'''' = 6y'y'' + 2yy''' = 34
    ('mode', ['y^2+x', '1', '4'],
     ["y'' = 1 + 2yy'", "y'''(0) = 2(1)(3) + 2(1)^2 = 8", "y^(4) = 2yy''' + 6y'y''",
      'y^(4)(0) = 2(1)(8) + 6(1)(3) = 34',
      'ANS: y = 1 + x + 3x^2/2 + 4x^3/3 + 17x^4/12 + ...'], ['*', 'y(4)']),
    # exact y = 2e^(x^2/2)
    ('mode', ['dy/dx = x*y', 'y(0)=2', '4'],
     ["y' = xy", "y'(0) = 0(2) = 0", 'ANS: y = 2 + x^2 + x^4/4 + ...'], ['*']),
    # exact y = -ln(1-x)
    ('mode', ['e^y', '0', '3'], ["y'(0) = e^0 = 1", 'ANS: y = x + x^2/2 + x^3/3 + ...']),
    # exact y = x - 1 + e^(-x)/2
    ('mode', ['x-y', '-1/2', '3'],
     ["y'(0) = -(-1/2) = 1/2", 'ANS: y = -1/2 + x/2 + x^2/4 - x^3/12 + ...']),
    ('mode', ['1/x+y', '1', '3'], ["y'(0) undefined"], ['ANS']),

    # ---- series by integration / differentiation ----
    ('mint', ['1/(1+x^2)', 'i', '5'],
     ['f(x) = 1/(1+x^2) = 1 - x^2 + x^4 + ...', 'int (1 - x^2 + x^4 + ...)dx', '= C + x - x^3/3 + x^5/5 + ...',
      'C = arctan(0) = 0', 'ANS: arctan(x) = x - x^3/3 + x^5/5 + ...'], ['x = 0: C', 'arctan(x) = C']),
    ('mint', ['1/(1+x)', '', '4'],
     ['f(x) = 1/(1+x) = 1 - x + x^2 - x^3 + ...', 'C = ln|0+1| = 0',
      'ANS: ln|x+1| = x - x^2/2 + x^3/3 - x^4/4 + ...']),
    # non-elementary integral: constant stays
    ('mint', ['e^(-x^2)', 'i', '5'], ['ANS: int f dx = C + x - x^3/3 + x^5/10 + ...'], ['C = ']),
    ('mint', ['1/(1-x)', 'd', '3'],
     ['f(x) = 1/(1-x) = 1 + x + x^2 + x^3 + x^4 + ...', "f'(x) = 1/(1-x)^2",
      '= d/dx(1 + x + x^2 + x^3 + x^4 + ...)', "ANS: f'(x) = 1 + 2x + 3x^2 + 4x^3 + ..."]),
    ('mint', ['sin(x)', 'd', '4'], ["f'(x) = cos(x)", "ANS: f'(x) = 1 - x^2/2 + x^4/24 + ..."]),
    ('mint', ['ln(x)', 'i', '3'], ['No Maclaurin series'], ['ANS']),

    # ---- review regressions (hand-checked) ----
    # numerator -> -inf is not 'k/0'; x e^(-x) -> -inf
    ('lhop', ['x/e^x', '-inf'], ['x -> -inf gives -inf/0', 'ANS: lim = -inf'], ['k/0']),
    # 'x->0' typed at the a prompt
    ('lhop', ['sin(x)/x', 'x->0'], ['lim_(x->0) sin(x)/x', 'x = 0 gives 0/0', 'ANS: lim = 1'], ['does not exist']),
    ('lhop', ['xln(x)', 'x->0+'], ['= lim ln(x)/(1/x)', 'ANS: lim = 0']),
    # 'x^4' typed for n
    ('msub', ['ln(1+x^2)', 'x^4'], ['ANS: f(x) = x^2 - x^4/2 + ...']),

    # ---- added with the exam-script rewrite (hand-checked) ----
    # (x^2-1)/(x-1) -> 2x/1 = 2 at x = 1
    ('lhop', ['(x^2-1)/(x-1)', '1'],
     ['lim_(x->1) (x^2-1)/(x-1)', 'x = 1 gives 0/0', "= lim 2x/1 (l'Hopital)", 'ANS: lim = 2']),
    # x^2 e^(-x) = x^2/e^x -> 2x/e^x -> 2/e^x -> 0
    ('lhop', ['x^2*e^(-x)', 'inf'],
     ['= lim x^2/e^x', "= lim 2x/e^x (l'Hopital)", "= lim 2/e^x (l'Hopital)", 'x -> inf gives 2/inf',
      'ANS: lim = 0']),
    # sin x - x = -x^3/6 + x^5/120: limit -1/6
    ('limser', ['(sin(x)-x)/x^3'],
     ['sin(x) - x = -x^3/6 + x^5/120 + ...', '= lim (-1/6 + x^2/120 + ...)', 'ANS: lim = -1/6']),
    # 1/(1+x^2) = 1 - x^2 + x^4
    ('msub', ['1/(1+x^2)', '4'],
     ['u = x^2', '(1+x^2)^(-1) = 1 - x^2 + (x^2)^2 + ...', 'ANS: f(x) = 1 - x^2 + x^4 + ...']),
    # cos x e^(-x): the x^2 terms cancel, x^3: -1/6 + 1/2 = 1/3
    ('mprod', ['cos(x)', 'e^(-x)', '3'],
     ['= 1 - x + x^2/2 - x^2/2 - x^3/6 + x^3/2 + ...', 'ANS: f(x)g(x) = 1 - x + x^3/3 + ...']),
    # integral of 1 - x^2/2 + x^4/24 is sin x
    ('mint', ['cos(x)', 'i', '4'], ['C = sin(0) = 0', 'ANS: sin(x) = x - x^3/6 + ...']),
    # y' = y, y(0) = 2: y = 2e^x
    ('mode', ['y', '2', '3'], ["y' = y", "y'(0) = 2", 'ANS: y = 2 + 2x + x^2 + x^3/3 + ...']),
    # 1/(1-x): f''(0) = 2, coefficient 2/2! = 1
    ('mderiv', ['1/(1-x)', '2'], ["f''(0) = 2", 'ANS: f(x) = 1 + x + x^2 + ...']),
]
