# Tests for calc/ibrv.py (AA 4.7, AHL 4.14). Values hand-checked.
MODULE = 'ibrv'
CASES = [
    # 10k = 1; E = (1+4+9+16)/10 = 3; E(X^2) = (1+8+27+64)/10 = 10; Var = 1
    ('discrete_rv', ['1', '1,2,3,4', 'k,2k,3k,4k', '0', 'X>=2', '2,1'],
     ['k + 2k + 3k + 4k = 1', '10k = 1', 'ANS: k = 1/10',
      'P : 1/10  1/5  3/10  2/5', 'E(X) = 1(1/10) + 2(1/5) + 3(3/10) + 4(2/5)', '= 3',
      'E(X^2) = 1(1/10) + 4(1/5) + 9(3/10) + 16(2/5)', 'Var(X) = 10 - 3^2 = 1',
      'P(X>=2) = P(X=2) + P(X=3) + P(X=4)', '= 1/5 + 3/10 + 2/5', 'ANS: P(X>=2) = 9/10',
      'E(aX+b) = aE(X) + b = 2(3) + 1', 'ANS: E(aX+b) = 7',
      'Var(aX+b) = a^2 Var(X) = 2^2(1)', 'ANS: Var(aX+b) = 4',
      'ANS: E(X) = 3', 'ANS: Var(X) = 1'],
     ['Sum P', 'Sum x', '(3)^2', '(2)^2']),
    # k^2 + k - 3/4 = 0 -> k = 1/2 (k = -3/2 gives P < 0); E = 1, E(X^2) = 3/2
    ('discrete_rv', ['1', '0,1,2', 'k^2,k,1/4', '0', '', ''],
     ['k^2 + k + 1/4 = 1', 'k = -3/2 rejected', 'ANS: k = 1/2', 'Var(X) = 3/2 - 1^2 = 1/2',
      'sd = sqrt(1/2) = 0.707', 'ANS: E(X) = 1', 'ANS: Var(X) = 1/2'], ['(1)^2']),
    # fair game: w/6 - 10/6 = 0 -> w = 10; E(X^2) = 100/6 + 20/6 = 20
    ('discrete_rv', ['1', 'w,-2', '1/6,5/6', '2', '', ''],
     ['E(X) = 0', 'w(1/6) + (-2)(5/6) = 0', 'ANS: w = 10', 'ANS: E(X) = 0',
      'ANS: Var(X) = 20'], ['Sum x']),
    # p + q = 0.8, p + 2q = 1.3 -> q = 0.5, p = 0.3; Var = 4.1 - 3.61 = 0.49
    ('discrete_rv', ['1', '1,2,3', 'p,q,0.2', '1', '1.9', 'X<3', ''],
     ['p + q + 0.2 = 1', '1(p) + 2(q) + 3(0.2) = 1.9', 'ANS: p = 0.3', 'ANS: q = 0.5',
      'E(X^2) = 1(0.3) + 4(0.5) + 9(0.2)', 'Var(X) = 4.1 - (1.9)^2 = 0.49', 'sd = sqrt(0.49) = 0.7',
      'ANS: P(X<3) = 0.8', 'ANS: Var(X) = 0.49']),
    # P(X=x) = x/6: E = 14/6 = 7/3, E(X^2) = 36/6 = 6, Var = 6 - 49/9 = 5/9
    ('discrete_rv', ['2', '1,2,3', 'x/6', '0', 'X=2', ''],
     ['P(X=1) = 1/6', 'P(X=2) = 1/3', 'P(X=3) = 1/2', 'ANS: P(X=2) = 1/3 (0.333)',
      'ANS: E(X) = 7/3 (2.33)', 'ANS: Var(X) = 5/9 (0.556)']),
    ('discrete_rv', ['1', '1,2,3', 'p,q,0.2', '0'], ['Need another condition'], ['ANS']),
    ('discrete_rv', ['1', '1,2', '1/2,1/3', '0', '', ''], ['Warning: sum of P is not 1', 'ANS: E(X) = 7/6']),
    ('discrete_rv', ['1', '1,2', 'k,k,k'], ['Error: list lengths'], ['ANS']),
    # k^2 = 1 with P = k, k: k=-1 rejected... (2k = 1 -> k = 1/2 only)
    ('discrete_rv', ['1', '0,1,2', 'k,k,k', '0', '', ''],
     ['3k = 1', 'ANS: k = 1/3', 'ANS: E(X) = 1', 'ANS: Var(X) = 2/3']),

    # k x^2 on [0,3]: 9k = 1; P(1<X<2) = 7/27; E = 9/4; E(X^2) = 27/5; Var = 27/80;
    # median m^3 = 27/2; mode 3; E(2X+1) = 11/2; Var(2X+1) = 27/20
    ('continuous_rv', ['1', 'k*x^2', '0,3', '0', '1,2', '2,1'],
     ['f(x) = kx^2, 0<=x<=3', 'int _0^3 kx^2 dx = 1', '[kx^3/3]_0^3 = 1', 'k(3^3/3) = 1',
      '9k = 1', 'ANS: k = 1/9', 'f(x) = x^2/9, 0<=x<=3', '= [x^3/27]_1^2', '= 2^3/27 - 1^3/27',
      'ANS: P(1<X<2) = 7/27 (0.259)', '= [x^4/36]_0^3', '= 3^4/36', 'ANS: E(X) = 9/4',
      '= [x^5/45]_0^3', 'Var(X) = 27/5 - (9/4)^2 = 27/80',
      'ANS: Var(X) = 27/80', 'm^3/27 = 1/2', 'ANS: median = (27/2)^(1/3) (2.38)',
      "f'(x) = 2x/9", 'ANS: mode = 3', 'ANS: E(aX+b) = 11/2', 'ANS: Var(aX+b) = 27/20'],
     ['Int', 'k*x', '(by parts)']),
    # k(4-x^2) on [0,2]: 16k/3 = 1; E = 3/4; E(X^2) = 4/5; Var = 19/80;
    # median: m^3 - 12m + 8 = 0 -> 0.695 (GDC); mode 0 (f decreasing)
    ('continuous_rv', ['1', 'k*(4-x^2)', '0,2', '345'],
     ['k(-2^3/3 + 4(2)) = 1', '16k/3 = 1', 'ANS: k = 3/16', '= -3(2)^4/64 + 3(2)^2/8',
      'ANS: E(X) = 3/4', 'ANS: Var(X) = 19/80', '(-m^3+12m)/16 = 1/2', 'By GDC:',
      'ANS: median = 0.695', 'ANS: mode = 0'], ['*']),
    # piecewise kx, k(2-x): k/2 + k/2 = 1; P(0.5<X<1.5) = 0.375 + 0.375; E = 1, Var = 1/6
    ('continuous_rv', ['2', 'k*x', '0,1', 'k*(2-x)', '1,2', '0', '0.5,1.5', ''],
     ['int _0^1 kx dx + int _1^2 k(2-x) dx = 1', '[kx^2/2]_0^1 + [-kx^2/2 + 2kx]_1^2 = 1',
      'k/2 + k/2 = 1', 'ANS: k = 1',
      'f(x) = x, 0<=x<=1', 'f(x) = 2 - x, 1<=x<=2', '= 0.375 + 0.375',
      'ANS: P(0.5<X<1.5) = 0.75', 'ANS: E(X) = 1', 'ANS: Var(X) = 1/6 (0.167)',
      'int _0^1 f dx = 0.5 >= 0.5', 'int _0^m x dx = 0.5', 'ANS: median = 1', 'ANS: mode = 1']),
    # two unknowns: 2a + 2b = 1, 8a/3 + 2b = 7/6 -> a = b = 1/4; E(X^2) = 5/3;
    # Var = 5/3 - 49/36 = 11/36; median m^2 + 2m - 4 = 0 -> sqrt(5) - 1
    ('continuous_rv', ['1', 'a*x+b', '0,2', 'E=7/6', '34'],
     ['2a+2b = 1', 'E(X) = int _0^2 x(ax+b) dx = 7/6', '[ax^3/3 + bx^2/2]_0^2 = 7/6',
      '8a/3+2b = 7/6', 'ANS: a = 1/4', 'ANS: b = 1/4', 'f(x) = (x+1)/4',
      'ANS: Var(X) = 11/36 (0.306)', 'ANS: median = sqrt(5)-1 (1.24)']),
    # f(2) = 0: 2a + b = 0, 2a + 2b = 1 -> a = -1/2, b = 1; E = 2/3, Var = 2/9
    ('continuous_rv', ['1', 'a*x+b', '0,2', 'f(2)=0', '35'],
     ['f(2) = 2a+b = 0', 'ANS: a = -1/2', 'ANS: b = 1', 'ANS: E(X) = 2/3 (0.667)',
      'ANS: Var(X) = 2/9 (0.222)', 'ANS: mode = 0']),
    # exponential on [0,inf): k = 1, E = 1 (by parts), Var = 1, median ln 2
    ('continuous_rv', ['1', 'k*e^(-x)', '0,inf', '1345'],
     ['[-ke^(-x)]_0^inf = 1', '0 - (-k) = 1', 'ANS: k = 1', 'E(X) = int _0^inf xe^(-x) dx (by parts)',
      'E(X^2) = int _0^inf x^2 e^(-x) dx (by parts)', '[(-x^2-2x-2)e^(-x)]_0^inf',
      'ANS: E(X) = 1', 'ANS: Var(X) = 1',
      '-e^(-m)+1 = 1/2', 'ANS: median = ln(2) (0.693)', 'ANS: mode = 0']),
    # uniform on [2,6]: k = 1/4, E = 4, Var = 16/12 = 4/3, median 4, no unique mode
    ('continuous_rv', ['1', 'k', '2,6', '345'],
     ['k(6 - 2) = 1', '4k = 1', 'ANS: k = 1/4', 'ANS: E(X) = 4', 'ANS: Var(X) = 4/3 (1.33)', 'm/4-1/2 = 1/2',
      'ANS: median = 4', 'mode: any x in 2<=x<=6, f = 1/4'], ['ANS: mode', 'mode: not unique']),
    # k sin x on [0,pi]: 2k = 1; E = pi/2; Var = pi^2/4 - 2; median, mode pi/2
    ('continuous_rv', ['1', 'k*sin(x)', '0,pi', '345'],
     ['k(-cos(pi) - (-cos(0))) = 1', '2k = 1', 'ANS: k = 1/2', 'ANS: E(X) = pi/2 (1.57)', 'ANS: Var(X) = pi^2/4-2 (0.467)',
      'ANS: median = pi/2 (1.57)', "f''(pi/2) = -1/2 < 0 max", 'ANS: mode = pi/2 (1.57)']),
    # k x(3-x) on [0,3]: 9k/2 = 1; f' = 0 at 3/2, f'' = -4/9 < 0
    ('continuous_rv', ['1', 'k*x*(3-x)', '0,3', '5'],
     ['ANS: k = 2/9', "f'(x) = 0 => x = 3/2, f''(3/2) = -4/9 < 0 max", 'max f(3/2) = 1/2',
      'ANS: mode = 3/2']),
    ('continuous_rv', ['1', 'a*x^2+b*x+c', '0,1'], ['Too many unknowns'], ['ANS']),
    ('continuous_rv', ['1', 'a*x+b', '0,2', '7'], ['Need a condition with ='], ['ANS']),
    # x e^(-x^2) is a substitution (not parts); E(X) has no elementary form -> GDC
    ('continuous_rv', ['1', 'k*x*e^(-x^2)', '0,inf', '3'],
     ['(substitution)', 'ANS: k = 2', 'f(x) = 2xe^(-x^2), x>=0', '= 0.886 (GDC)',
      'ANS: E(X) = 0.886', 'ANS: Var(X) = 0.215'], ['(by parts)', 'xx']),
    # f = 1/x^2 on [1,inf): k = 1, E(X) diverges; median 2
    ('continuous_rv', ['1', 'k/x^2', '1,inf', '1346', '2,1'],
     ['ANS: k = 1', 'E(X) does not exist', 'ANS: median = 2'], ['ANS: E(X)', 'Error']),
    # k x^2 on [-1,1]: 2k/3 = 1; bounds substituted with brackets; E = 0, Var = 3/5
    ('continuous_rv', ['1', 'k*x^2', '-1,1', '3'],
     ['k(1^3/3 - (-1)^3/3) = 1', 'ANS: k = 3/2', '3(1)^4/8 - 3(-1)^4/8', 'ANS: E(X) = 0',
      'ANS: Var(X) = 3/5']),
    # infinite bound in a discrete query is +-1e300: everything is selected, P = 1
    ('discrete_rv', ['1', '1,2,3', '1/6,1/3,1/2', '0', 'X<inf', ''],
     ['P(X<INF) = P(X=1) + P(X=2) + P(X=3)', 'ANS: P(X<INF) = 1'], ['Error']),
    ('discrete_rv', ['1', '1,2,3', '1/6,1/3,1/2', '0', 'X>-inf', ''],
     ['ANS: P(X>-INF) = 1'], ['Error']),
    # lower end -inf with an unknown k: ok() needs a finite sampling window; P with an inf bound
    ('continuous_rv', ['1', 'k*e^x', '-inf,0', '2', '-inf,-1'],
     ['[ke^x]_-inf^0 = 1', 'ANS: k = 1', 'f(x) = e^x, -inf<=x<=0',
      'ANS: P(-inf<X<-1) = 1/e (0.368)'], ['No valid solution', 'Error']),
    # constant pieces: mode is the whole interval of the larger one (f = 1/2 on [0,1])
    ('continuous_rv', ['2', 'k', '0,1', 'k/2', '1,3', '5'],
     ['ANS: k = 1/2', 'mode: any x in 0<=x<=1, f = 1/2'], ['mode: not unique', 'ANS: mode']),
]
