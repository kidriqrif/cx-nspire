# Tests for calc/ibode.py (first-order ODEs, AA 5.18). Answers hand-checked.
MODULE = 'ibode'
CASES = [
    # Euler: y1=1.1, y2=1.22, y3=1.362, y4=1.5282, y5=1.72102
    ('euler', ['x+y', '0', '1', '0.1', '5'],
     ['dy/dx = x + y', 'x0 = 0, y0 = 1, h = 0.1', 'y(n+1) = y(n) + 0.1(x + y)',
      'y1 = 1 + 0.1(0 + 1) = 1.1', 'y2 = 1.1 + 0.1(0.1 + 1.1) = 1.22', '4  0.4  1.53  1.93',
      'ANS: y(0.5) = 1.72'], ['1.72102']),
    ('euler', ['dy/dx = x+y', '', '', '', 'x=0.5'],
     ['dy/dx = x + y', '5  0.5  1.72', 'ANS: y(0.5) = 1.72'], ['dy/dx = dy/dx']),
    # y1=1.75, y2=1.703125, y3=1.83984375, y4=2.1455078
    ('euler', ['x^2-y', '1', '2', '0.25', '4'],
     ['y1 = 2 + 0.25(1^2 - 2) = 1.75', 'y2 = 1.75 + 0.25(1.25^2 - 1.75) = 1.7031', 'ANS: y(2) = 2.15'],
     ['2.14551']),
    ('euler', ['x+y', '0', '1', '0.1', '100'], ['Use 1-60 steps'], ['ANS']),
    ('euler', ['1/x', '0', '1', '0.1', '3'], ['Giac error', 'f undefined at x=0'], ['ANS']),
    # f with a function: y1 = 1.1, y2 = 1.1 + 0.1(sin 0.1 + 1.1) = 1.21998
    ('euler', ['sin(x)+y', '0', '1', '0.1', '2'],
     ['y(n+1) = y(n) + 0.1(sin(x) + y)', 'y1 = 1 + 0.1(sin(0) + 1) = 1.1', 'ANS: y(0.2) = 1.22']),

    # Separation of variables
    ('sep', ['x*y', 'y(0)=2'],
     ['dy/dx = xy', '(1/y) dy = x dx', 'int 1/y dy = int x dx', 'ln|y| = x^2/2 + C', 'x = 0, y = 2: ln(2) = C',
      'ANS: y = 2e^(x^2/2)'], ['dy/dx = (x)(y)', '0 + C']),
    # y dy = x dx, y^2 = x^2 + 9, y(0) = -3 so negative root
    ('sep', ['x/y', 'y(0)=-3'],
     ['y dy = x dx', 'int y dy = int x dx', 'x = 0, y = -3: 9/2 = C', 'y^2 = x^2 + 9', 'ANS: y = -sqrt(x^2+9)'],
     ['ANS: y = sqrt']),
    ('sep', ['y^2*cos(x)', 'y(0)=1'],
     ['(1/y^2) dy = cos(x) dx', '-1/y = sin(x) + C', '-1 = C', '-1/y = sin(x) - 1', 'ANS: y = 1/(-sin(x)+1)']),
    ('sep', ['2x(y-1)', 'y(0)=3'],
     ['(1/(y-1)) dy = 2x dx', 'int 1/(y-1) dy = int 2x dx', 'ln|y-1| = x^2 + C', 'ln(2) = C',
      'ANS: y = 2e^(x^2) + 1']),
    ('sep', ['(1+y^2)/x', '(1,0)'],
     ['(1/(1+y^2)) dy = (1/x) dx', 'arctan(y) = ln|x| + C', 'x = 1, y = 0: 0 = C', 'ANS: y = tan(ln(x))']),
    ('sep', ['3x^2*y', ''], ['|y| = e^(x^3 + C)', 'ANS: y = Ae^(x^3)'], ['Ae^(x^3)\nANS']),
    ('sep', ['x/y', ''], ['ANS: y^2/2 = x^2/2 + C'], ['+ C\nANS']),
    ('sep', ['x^2', 'y(0)=1'], ['y = int x^2 dx', 'y = x^3/3 + C', '1 = C', 'ANS: y = x^3/3 + 1'], ['int 1 dy']),
    ('sep', ['x+y'], ['Not of form g(x)h(y)'], ['ANS']),
    # general solutions: the working line is not repeated by ANS
    ('sep', ['x^2', ''], ['y = int x^2 dx', 'ANS: y = x^3/3 + C'], ['+ C\nANS']),
    ('sep', ['y', ''], ['(1/y) dy = dx', 'int dx', '|y| = e^(x + C)', 'ANS: y = Ae^x'], ['Ae^x\nANS']),
    ('sep', ['2x(y-1)', ''], ['y-1 = Ae^(x^2)', 'ANS: y = Ae^(x^2) + 1']),
    # y dy = cos x dx: y^2 = 2 sin x + 1, y(0) = -1
    ('sep', ['cos(x)/y', 'y(0)=-1'], ['x = 0, y = -1: 1/2 = C', 'y^2 = 2sin(x) + 1', 'ANS: y = -sqrt(2sin(x)+1)']),
    ('sep', ['-2xy', 'y(0)=1'], ['(1/y) dy = -2x dx', 'ln|y| = -x^2 + C', 'ANS: y = e^(-x^2)']),

    # Homogeneous y = vx
    # v^2/2 = ln|x| + 2, so y^2 = 2x^2(ln x + 2) = x^2(2 ln x + 4), y > 0
    ('homog', ['(x^2+y^2)/(x*y)', 'y(1)=2'],
     ['dy/dx = (x^2+y^2)/(xy)', 'y = vx, dy/dx = v + x dv/dx', 'v + x dv/dx = (v^2+1)/v', 'x dv/dx = 1/v',
      'int v dv = int 1/x dx', 'v^2/2 = ln|x| + C', 'x = 1, y = 2: 2 = C',
      'y^2 = 2x^2(ln(x)+2)', 'ANS: y = x sqrt(2ln(x)+4)'], ['sqrt(2)*x', 'sqrt(2)x', 'v = y/x:']),
    ('homog', ['(x+y)/x', 'y(1)=3'],
     ['x dv/dx = 1', 'int dv = int 1/x dx', 'v = ln|x| + C', 'y/x = ln|x| + C', 'x = 1, y = 3: 3 = C',
      'ANS: y = x ln(x) + 3x'], ['int 1 dv']),
    # ln(v^2+1) = ln x + ln 2, v^2 = 2x - 1
    ('homog', ['(x^2+3y^2)/(2x*y)', 'y(1)=1'],
     ['x dv/dx = (v^2+1)/(2v)', 'ln(v^2+1) = ln|x| + C', 'x = 1, y = 1: ln(2) = C', 'y^2 = x^2(2x-1)',
      'ANS: y = x sqrt(2x-1)']),
    # -ln(v^2+1) = ln x - ln 2, y^2 = 2x - x^2
    ('homog', ['(y^2-x^2)/(2x*y)', 'y(1)=1'],
     ['-ln(v^2+1) = ln|x| + C', 'x = 1, y = 1: -ln(2) = C', 'y^2 = -x^2 + 2x', 'ANS: y = sqrt(-x^2+2x)']),
    ('homog', ['y/x', 'y(2)=6'], ['x dv/dx = 0', 'v = A, y = Ax', 'x = 2, y = 6: A = 3', 'ANS: y = 3x']),
    ('homog', ['(x+y)/(x-y)', ''],
     ['arctan(v)', 'ANS: arctan(y/x) - ln((y/x)^2+1)/2 = ln|x| + C'], ['\narctan(y/x)']),
    ('homog', ['x+y^2'], ['Not of form f(y/x)'], ['ANS']),

    # negative branch: y(1) = -2 gives y = -x sqrt(2 ln x + 4) (was the positive root)
    ('homog', ['(x^2+y^2)/(x*y)', 'y(1)=-2'],
     ['x = 1, y = -2: 2 = C', 'y^2 = 2x^2(ln(x)+2)', 'ANS: y = -x sqrt(2ln(x)+4)'], ['ANS: y = x sqrt']),
    # x0 < 0: y = -x sqrt(2 ln(-x) + 4) = 2 at x = -1
    ('homog', ['(x^2+y^2)/(x*y)', 'y(-1)=2'], ['x = -1, y = 2: 2 = C', 'ANS: y = -x sqrt(2ln(-x)+4)']),
    # y' = (x^2+y^2)/(2xy), y(2) = -1: v^2 = 1 - 3/(2x), y = -x sqrt((2x-3)/(2x))
    ('homog', ['(x^2+y^2)/(2x*y)', 'y(2)=-1'], ['ANS: y = -x sqrt((2x-3)/(2x))']),
    # x0 = 0 cannot be used with y = vx
    ('homog', ['(x^2+y^2)/(x*y)', 'y(0)=2'], ['C undefined at this point'], ['ANS']),

    # Integrating factor
    ('intf', ['1', '2', 'e^x', 'y(0)=1'],
     ['dy/dx + 2y = e^x', 'IF = e^(int 2 dx) = e^(2x)', 'e^(2x)y = int e^(3x) dx', ' = e^(3x)/3 + C',
      'y = e^x/3 + Ce^(-2x)', 'x = 0, y = 1: 1 = 1/3 + C', 'C = 2/3', 'ANS: y = (2e^(-2x)+e^x)/3'],
     ['(1)(1)', 'd/dx[', 'IF = e^(2x)\n']),
    ('intf', ['x', '-1', 'x^2', 'y(1)=3'],
     ['x dy/dx - y = x^2', 'dy/dx - y/x = x', 'IF = e^(int -1/x dx) = e^(-ln(x))', 'IF = 1/x',
      'y/x = int dx', ' = x + C', 'y = x^2 + Cx', 'x = 1, y = 3: 3 = 1 + C', 'C = 2', 'ANS: y = x^2 + 2x'],
     ['Divide by']),
    ('intf', ['cos(x)', 'sin(x)', '1', 'y(0)=0'],
     ['cos(x) dy/dx + sin(x)y = 1', 'dy/dx + (sin(x)/cos(x))y = 1/cos(x)',
      'IF = e^(int sin(x)/cos(x) dx) = e^(-ln(cos(x)))', 'IF = 1/cos(x)',
      'y/cos(x) = int 1/cos(x)^2 dx', ' = tan(x) + C', 'y = sin(x) + Ccos(x)', 'ANS: y = sin(x)']),
    ('intf', ['1', '1/x', 'x', ''],
     ['dy/dx + y/x = x', 'IF = x', 'xy = int x^2 dx', ' = x^3/3 + C', 'ANS: y = x^2/3 + C/x'],
     ['C/x\nANS']),
    ('intf', ['x', '3', '1/x', 'y(1)=1'],
     ['dy/dx + 3y/x = 1/x^2', 'IF = x^3', 'x^3y = int x dx', ' = x^2/2 + C', 'y = 1/(2x) + C/x^3',
      'x = 1, y = 1: 1 = 1/2 + C', 'C = 1/2', 'ANS: y = (x^2+1)/(2x^3)']),
    ('intf', ['1', '-2x', 'x*e^(x^2)', 'y(0)=1'],
     ['dy/dx - 2xy = xe^(x^2)', 'IF = e^(int -2x dx) = e^(-x^2)', 'e^(-x^2)y = int x dx', 'x = 0, y = 1: 1 = C',
      'ANS: y = (x^2+2)e^(x^2)/2']),
    ('intf', ['1', 'y', 'x'], ['Not linear in y'], ['ANS']),

    # ---- review regressions (hand-checked) ----
    # |y-1| with y<1 is 1-y (was (-y-1)); logistic y = e^x/(e^x+1), y(0) = 1/2
    ('sep', ['y(1-y)', 'y(0)=1/2'],
     ['(1/(y(1-y))) dy = dx', 'int 1/(y(1-y)) dy = int dx', '1/(y(1-y)) = 1/y - 1/(y-1)', 'x = 0, y = 1/2: 0 = C',
      'ANS: y = e^x/(e^x+1)'],
     ['(-y-1)', 'ln(-y']),
    # y/(y-1) = 2e^x -> y = 2e^x/(2e^x-1)
    ('sep', ['y(1-y)', 'y(0)=2'], ['x = 0, y = 2: ln(2) = C', 'ANS: y = 2e^x/(2e^x-1)']),
    # (1-y)/(1+y) = e^(2x) -> y = (1-e^(2x))/(1+e^(2x))
    ('sep', ['y^2-1', 'y(0)=0'],
     ['(1/(y^2-1)) dy = dx', '1/(y^2-1) = 1/(2(y-1)) - 1/(2(y+1))', 'ANS: y = (-e^(2x)+1)/(e^(2x)+1)']),
    # decimals exact: y = 100e^(-x/2)
    ('sep', ['-0.5y', 'y(0)=100'], ['dy/dx = -y/2', 'ln(100) = C', 'ANS: y = 100e^(-x/2)'], ['4.605']),
    ('sep', ['(x+1)/(y+2)', 'y(0)=0'],
     ['(y + 2) dy = (x + 1) dx', 'int (y + 2) dy = int (x + 1) dx', 'ANS: y = sqrt(x^2+2x+4) - 2']),
    ('sep', ['xe^-y', 'y(0)=0'], ['e^y dy = x dx', 'e^y = x^2/2 + C', 'x = 0, y = 0: 1 = C', 'e^y = x^2/2 + 1',
                                 'ANS: y = ln(x^2/2+1)'], ['1/2*']),
    ('sep', ['y/x', 'y(0)=1'], ['C undefined at this point'], ['ANS']),
    # cot v integrated as ln|sin v|; y = x arcsin x satisfies y' = y/x + tan(y/x), y(1) = pi/2
    ('homog', ['y/x+tan(y/x)', 'y(1)=pi/2'],
     ['int cos(v)/sin(v) dv = int 1/x dx', 'ln|sin(v)| = ln|x| + C', 'x = 1, y = pi/2: 0 = C',
      'ANS: y = x arcsin(x)'],
     ['undef']),
    ('homog', ['(x^2+y^2)/(2x^2)', 'y(1)=0'],
     ['x dv/dx = (v-1)^2/2', 'x = 1, y = 0: 2 = C', 'ANS: y = x ln(x)/(ln(x)+2)']),
    # y = (sin x - cos x)/2 + e^(-x)/2
    ('intf', ['', '1', 'sin(x)', 'y(0)=0'],
     ['dy/dx + y = sin(x)', 'IF = e^(int 1 dx) = e^x', 'e^x y = int e^x sin(x) dx',
      ' = e^x (-cos(x)/2+sin(x)/2) + C', 'x = 0, y = 0: 0 = -1/2 + C', 'C = 1/2',
      'ANS: y = sin(x)/2 - cos(x)/2 + 1/(2e^x)'], ['1/2/']),
    # y = x/2 + C/x cannot pass through (0,1)
    ('intf', ['', '1/x', '1', 'y(0)=1'], ['No solution through this point'], ['ANS']),
    # y = 4 + Ce^(-x/2), C = -4
    ('intf', ['', '0.5', '2', 'y(0)=0'],
     ['dy/dx + y/2 = 2', 'IF = e^(int 1/2 dx) = e^(x/2)', 'x = 0, y = 0: 0 = 4 + C', 'C = -4',
      'ANS: y = 4 - 4e^(-x/2)'], ['4.0']),
    ('intf', ['x^2', '-x', '1', ''],
     ['x^2 dy/dx - xy = 1', 'dy/dx - y/x = 1/x^2', 'y/x = int 1/x^3 dx', ' = -1/(2x^2) + C',
      'ANS: y = Cx - 1/(2x)'], ['/(1/x)']),
    ('intf', ['', '-2/x', 'x^3e^x', 'y(1)=e'],
     ['dy/dx - 2y/x = x^3 e^x', 'IF = 1/x^2', 'y/x^2 = int xe^x dx', ' = (x-1)e^x + C',
      'y = x^2 (x-1)e^x + Cx^2', 'x = 1, y = e: e = C', 'ANS: y = x^2 (x-1)e^x + ex^2']),
    # -y' + y = x: y = x + 1 + Ce^x, y(0) = 1 gives C = 0
    ('intf', ['-1', '1', 'x', 'y(0)=1'],
     ['-dy/dx + y = x', 'dy/dx - y = -x', 'IF = e^(int -1 dx) = e^(-x)', 'y = x + 1 + Ce^x', 'C = 0', 'ANS: y = x + 1']),
    # ((x+1)y)' = 1, y = (x + C)/(x+1)
    ('intf', ['x+1', '1', '1', ''],
     ['(x + 1) dy/dx + y = 1', 'dy/dx + (1/(x+1))y = 1/(x+1)', 'IF = x + 1', '(x + 1)y = int dx',
      'ANS: y = (C+x)/(x+1)']),
    # y' - y = 0: y = Ce^x
    ('intf', ['', '-1', '0', ''], ['dy/dx - y = 0', 'IF = e^(int -1 dx) = e^(-x)', ' = C', 'ANS: y = Ce^x']),
    ('euler', ['y', '0', '1', '0', '3'], ['h cannot be 0'], ['ANS']),
    # h = 0.3 does not reach x = 1 (was silently y(0.9))
    ('euler', ['x+y', '0', '1', '0.3', 'x=1'], ['not reached in whole steps'], ['ANS']),
    # y1 = 1.8, y2 = 1.638, y3 = 1.50696
    ('euler', ['xy', '1', '2', '-0.1', '3'],
     ['y(n+1) = y(n) - 0.1(xy)', 'y1 = 2 - 0.1(1(2)) = 1.8', 'y2 = 1.8 - 0.1(0.9(1.8)) = 1.638',
      'ANS: y(0.7) = 1.51'], ['+ -0.1']),
    ('euler', ['y', '0', '1', '1/2', '2'],
     ['y(n+1) = y(n) + (1/2)y(n)', 'y1 = 1 + (1/2)(1) = 1.5', 'ANS: y(1) = 2.25']),
]
