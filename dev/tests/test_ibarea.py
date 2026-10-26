MODULE = 'ibarea'
# Expected answers hand-checked (working in comments).
CASES = [
    # [x^3+x^2]_0^2 = 8+4 = 12
    ('defint', ['3x^2+2x', '0', '2'],
     ['int_0^2 (3x^2 + 2x) dx', '= [x^3 + x^2]_0^2', '= (2^3 + 2^2) - 0', 'ANS: I = 12'],
     ['Set I', 'F(x)', 'int 3x^2 dx', 'f(x) = 3x^2+2x', '= 12\nANS']),
    # [-cos x]_0^(pi/2) = 0 - (-1) = 1
    ('defint', ['sin(x)', '0', 'pi/2'],
     ['= [-cos(x)]_0^(pi/2)', '= -cos(pi/2) - (-cos(0))', '= 0 - (-1)', 'ANS: I = 1'], ['F(x)', '= 1\nANS']),
    # [ln|x|]_1^e = 1 - 0
    ('defint', ['1/x', '1', 'e'], ['= [ln|x|]_1^e', '= ln|e| - ln|1|', 'ANS: I = 1'], ['= 1\nANS']),
    # [e^(2x)/2]_0^ln3 = 9/2 - 1/2 = 4
    ('defint', ['e^(2x)', '0', 'ln(3)'], ['= [e^(2x)/2]_0^(ln(3))', '= 9/2 - 1/2', 'ANS: I = 4'], ['= 4\nANS']),
    # reversed limits: [x^4]_2^1 = 1 - 16 = -15
    ('defint', ['4x^3', '2', '1'], ['= [x^4]_2^1', '= 1^4 - 2^4', '= 1 - 16', 'ANS: I = -15']),
    # |x-1| on [0,3]: 1/2 + 2 = 5/2
    ('defint', ['|x-1|', '0', '3'],
     ['int_0^3 |x-1| dx', 'x - 1 = 0', 'x = 1', 'I1 = |int_0^1 (x - 1) dx|', '= |-1/2|', '= 1/2',
      'I2 = int_1^3 (x - 1) dx', 'I = 1/2 + 2', 'ANS: I = 5/2'], ['-int']),
    # reversed limits with |f|: -int_0^3 = -5/2
    ('defint', ['|x-1|', '3', '0'], ['int_3^0 |x-1| dx', '= -int_0^3 |x-1| dx', 'I = 1/2 + 2', 'ANS: I = -5/2']),
    # int_0^k 2x dx = k^2 = 9 -> k = +-3
    ('defint', ['2x', '0', 'k', '9'],
     ['int_0^k 2x dx', '= [x^2]_0^k', '= k^2 - 0', 'ANS: I = k^2', 'k^2 = 9', 'ANS: k = -3', 'ANS: k = 3'], ['Set I = (blank=skip): 9']),
    ('defint', ['1/x', '-1', '1'], ['int_(-1)^1 1/x dx', 'f undefined at x = 0', 'Improper integral: not in AA'], ['ANS']),
    ('defint', ['x', '0', 'inf'], ['Infinite limit: not in AA'], ['ANS']),
    # no elementary antiderivative -> GDC 0.746824...
    ('defint', ['e^(-x^2)', '0', '1'], ['No elementary antiderivative', '= 0.747 (GDC)', 'ANS: I = 0.747']),

    # by parts antiderivative: [(x-1)e^x]_0^1 = 0 - (-1) = 1
    ('defint', ['x*e^x', '0', '1'],
     ['int_0^1 xe^x dx', '= [(x-1)e^x]_0^1', '= (1-1)e - (0-1)e^0', '= 0 - (-1)', 'ANS: I = 1'], ['*']),
    # decimal limits made exact: [x^3/3]_(1/2)^(3/2) = 9/8 - 1/24 = 13/12
    ('defint', ['x^2', '0.5', '1.5'],
     ['int_(1/2)^(3/2) x^2 dx', '= (3/2)^3/3 - (1/2)^3/3', '= 9/8 - 1/24', 'ANS: I = 13/12']),
    # Si(2) - Si(1) = 0.6593
    ('defint', ['sin(x)/x', '1', '2'], ['No elementary antiderivative', 'ANS: I = 0.659']),
    ('defint', ['ln(x)', '0', '2'], ['f undefined on [0, 2]', 'Improper'], ['ANS']),
    ('defint', ['tan(x)', '0', '2'], ['f undefined at x = pi/2', 'Improper'], ['ANS']),

    # f = 2x^3 - 2x + C, f(1) = 0 + C = 5
    ('antider', ['6x^2-2', '1,5'],
     ["f'(x) = 6x^2-2", 'f(x) = int (6x^2 - 2) dx', '= 2x^3 - 2x + C', 'f(1) = 5', '2(1)^3 - 2(1) + C = 5',
      'C = 5', 'ANS: f(x) = 2x^3 - 2x + 5'], ['0 + C = 5', 'int 6x^2', 'C = 5\nANS: f(x) = 2x^3 - 2x + 5\nANS']),
    # f = sin(2x)/2 + C, sin(pi/2)/2 = 1/2 -> C = 5/2
    ('antider', ['cos(2x)', 'pi/4, 3'],
     ['f(x) = int cos(2x) dx', '= sin(2x)/2 + C', 'f(pi/4) = 3', 'sin(2(pi/4))/2 + C = 3', '1/2 + C = 3', 'C = 5/2',
      'ANS: f(x) = sin(2x)/2 + 5/2']),
    # f = ln|2x+1|/2 + C, f(0) = 0 + C = 1
    ('antider', ['1/(2x+1)', '0,1'],
     ['= ln|2x+1|/2 + C', 'f(0) = 1', 'ln|2(0)+1|/2 + C = 1', 'C = 1', 'ANS: f(x) = ln|2x + 1|/2 + 1'], ['0 + C = 1']),
    # f = 2x^(3/2) + C, f(4) = 16 + C = 20 -> C = 4
    ('antider', ['3sqrt(x)', '4,20'],
     ['= 2x^(3/2) + C', '2(4)^(3/2) + C = 20', '16 + C = 20', 'C = 4', 'ANS: f(x) = 2x^(3/2) + 4'], ['x sqrt(x)']),
    ('antider', ['e^(x^2)', '0,1'], ['No elementary antiderivative'], ['ANS']),
    ('antider', ['4x', '3'], ['Giac error: enter two values a,b'], ['ANS']),

    # x^2-4 on [0,3]: |[x^3/3-4x]_0^2| = 16/3, [..]_2^3 = 7/3, total 23/3
    ('area_x', ['x^2-4', '0,3'],
     ['x^2 - 4 = 0', 'x = 2', 'A1 = |int_0^2 (x^2 - 4) dx|', '= |[x^3/3 - 4x]_0^2|',
      '= |(2^3/3 - 4(2)) - 0|', '= |-16/3|', '= 16/3', 'A2 = int_2^3 (x^2 - 4) dx', '= [x^3/3 - 4x]_2^3',
      '= -3 - (-16/3)', '= 7/3', 'A = 16/3 + 7/3', 'ANS: A = 23/3'], ['-int', 'F(x)', '[-x^3/3']),
    # three arches of sin, area 2 each
    ('area_x', ['sin(x)', '0,3pi'],
     ['sin(x) = 0', 'x = pi, 2pi', 'A2 = |int_pi^(2pi) sin(x) dx|', '= |[-cos(x)]_pi^(2pi)|', 'A = 2 + 2 + 2',
      'ANS: A = 6']),
    # roots -1,0,1: 1/4 + 1/4 (roots listed once)
    ('area_x', ['x^3-x', ''],
     ['x^3 - x = 0', 'x = -1, 0, 1', 'A1 = int_(-1)^0 (x^3 - x) dx', '= 0 - ((-1)^4/4 - (-1)^2/2)',
      'A2 = |int_0^1 (x^3 - x) dx|', 'A = 1/4 + 1/4', 'ANS: A = 1/2'], ['\nx = 0\n']),
    # root ln2: (2ln2 - 1) + (e^2 - 6 + 2ln2) = e^2 + 4ln2 - 7 ~ 3.16
    ('area_x', ['e^x-2', '0,2'],
     ['e^x - 2 = 0', 'x = ln(2)', '= |1 - 2ln(2)|', '= 2ln(2) - 1', 'ANS: A = e^2+4ln(2)-7', '~ 3.16']),
    # irreducible cubic: root 1.3247 (GDC), pieces 1.43 + 1.43
    ('area_x', ['x^3-x-1', '0,2'], ['x = 1.32 (GDC)', '= |-1.43|', 'A = 1.43 + 1.43', 'ANS: A = 2.86']),
    # cos x = x at 0.739085 (GDC): 0.40049 + 0.05902 = 0.45951
    ('area_x', ['cos(x)-x', '0,1'], ['x = 0.739 (GDC)', 'A = 0.400 + 0.0590', 'ANS: A = 0.460']),
    # x e^x on [-1,1]: (1 - 2/e) + 1
    ('area_x', ['x*e^x', '-1,1'],
     ['xe^x = 0', 'x = 0', 'A1 = |int_(-1)^0 xe^x dx|', '= |2/e - 1|', 'A = (1 - 2/e) + 1', 'ANS: A = 2 - 2/e', '~ 1.26'],
     ['*']),
    # touching root (x-1)^2: 1/3 + 1/3
    ('area_x', ['(x-1)^2', '0,2'], ['A = 1/3 + 1/3', 'ANS: A = 2/3']),
    ('area_x', ['1/x', '-1,1'], ['f undefined at x = 0', 'Improper'], ['ANS']),
    ('area_x', ['x^2+1', '', ''], ['Fewer than 2 roots: give limits'], ['ANS']),
    ('area_x', ['x^2', '0,k'], ['Giac error: limits must be numbers'], ['ANS']),
    # no root inside: single piece, no sum line
    ('area_x', ['x^2+1', '0,3'], ['A1 = int_0^3 (x^2 + 1) dx', '= (3^3/3 + 3) - 0', 'ANS: A = 12'], ['\nA = ', '\nx = ']),

    # x - x^2 on [0,1]: 1/2 - 1/3 = 1/6
    ('area_2', ['x', 'x^2', ''],
     ['x = x^2', 'x = 0, 1', '0 < x < 1: x > x^2', 'A1 = int_0^1 (x - x^2) dx', '= (1^2/2 - 1^3/3) - 0', 'ANS: A = 1/6'],
     ['f - g', 'f on top']),
    # x^3 vs x on [-1,1]: 1/4 + 1/4
    ('area_2', ['x^3', 'x', ''],
     ['x^3 = x', 'x = -1, 0, 1', '-1 < x < 0: x^3 > x', 'A1 = int_(-1)^0 (x^3 - x) dx', '0 < x < 1: x > x^3',
      'A2 = int_0^1 (x - x^3) dx', 'A = 1/4 + 1/4', 'ANS: A = 1/2']),
    # 4 - x^2 = x + 2 at x = -2, 1: [2x - x^2/2 - x^3/3]_-2^1 = 7/6 + 10/3 = 9/2
    ('area_2', ['4-x^2', 'x+2', ''],
     ['4 - x^2 = x + 2', 'x = -2, 1', '-2 < x < 1: 4 - x^2 > x + 2', '= 7/6 - (-10/3)', 'ANS: A = 9/2']),
    # (sqrt2 - 1) + (1 + sqrt2) = 2sqrt2
    ('area_2', ['sin(x)', 'cos(x)', '0,pi'],
     ['sin(x) = cos(x)', 'x = pi/4', '0 < x < pi/4: cos(x) > sin(x)', 'pi/4 < x < pi: sin(x) > cos(x)',
      'ANS: A = 2sqrt(2)', '~ 2.83']),
    # e^x = x + 2 at -1.84, 1.15 (GDC); int (x+2-e^x) = 1.95
    ('area_2', ['e^x', 'x+2', '', ''],
     ['x = -1.84 (GDC), 1.15 (GDC)', 'x + 2 > e^x', 'A1 = int_(-1.84)^1.15 (x + 2 - e^x) dx', 'ANS: A = 1.95']),
    # 1/x = 5/2 - x at 1/2, 2: [5x/2 - x^2/2 - ln x] = 15/8 - 2ln2
    ('area_2', ['1/x', '5/2-x', ''], ['x = 1/2, 2', '5/2 - x > 1/x', 'ANS: A = 15/8-2ln(2)', '~ 0.489']),
    # x^2 = x + 1 at (1 -+ sqrt5)/2: area = 5sqrt5/6
    ('area_2', ['x^2', 'x+1', ''], ['x + 1 > x^2', 'ANS: A = 5sqrt(5)/6', '~ 1.86']),
    ('area_2', ['2x+1', '2x+3', '', ''], ['Fewer than 2 roots'], ['ANS']),

    # x = sqrt(y): int_1^4 = 2/3(8 - 1) = 14/3, F in power form
    ('area_y', ['y=x^2', '1', '4', ''],
     ['y=x^2', 'x = -sqrt(y) or sqrt(y)', 'x = sqrt(y)', 'A1 = int_1^4 sqrt(y) dy', '= [(2/3)y^(3/2)]_1^4',
      '= (2/3)(4)^(3/2) - (2/3)(1)^(3/2)', '= 16/3 - 2/3', 'ANS: A = 14/3'], ['y sqrt(y)', 'Which x (1-2): 2', 'Rearrange']),
    # |y^2 - 1| on [-1,1] = 4/3
    ('area_y', ['x=y^2-1', '-1', '1'],
     ['A1 = |int_(-1)^1 (y^2 - 1) dy|', '= |-2/3 - 2/3|', '= |-4/3|', 'ANS: A = 4/3'], ['-int']),
    # x = e^y on [0,1]: e - 1
    ('area_y', ['y=ln(x)', '0', '1'], ['x = e^y', '= [e^y]_0^1', 'ANS: A = e-1', '~ 1.72']),
    # x = y^2 + 1 on [0,2]: 8/3 + 2 = 14/3
    ('area_y', ['y=sqrt(x-1)', '0', '2'], ['x = y^2 + 1', 'ANS: A = 14/3']),
    # x = y^3 crosses y-axis at 0: 1/4 + 4
    ('area_y', ['x=y^3', '-1', '2'], ['y^3 = 0', 'y = 0', 'A1 = |int_(-1)^0 y^3 dy|', 'A = 1/4 + 4', 'ANS: A = 17/4']),
    ('area_y', ['y=x^2', '-4', '-1'], ['Cannot make x the subject'], ['ANS']),
    # cube root: (3/4)[y^(4/3)]_1^8 = (3/4)(16 - 1) = 45/4
    ('area_y', ['y=x^3', '1', '8'], ['x = y^(1/3)', '= [(3/4)y^(4/3)]_1^8', '= 12 - 3/4', 'ANS: A = 45/4'], ['y y^']),
    # fractional power kept as a power: (2/5)[x^(5/2)]_1^4 = (2/5)(32 - 1) = 62/5
    ('defint', ['x^(3/2)', '1', '4'], ['= [(2/5)x^(5/2)]_1^4', '= 64/5 - 2/5', 'ANS: I = 62/5']),
    # sqrt from 0: (2/3)(9)^(3/2) = 18, F(0) = 0
    ('area_y', ['y=x^2', '0', '9', ''], ['= [(2/3)y^(3/2)]_0^9', '= (2/3)(9)^(3/2) - 0', 'ANS: A = 18']),

    # pi int_0^4 x dx = 8pi
    ('volume', ['', 'sqrt(x)', '0', '4', ''],
     ['V = pi int_0^4 (sqrt(x))^2 dx', '= pi int_0^4 x dx', '= pi[x^2/2]_0^4', '= pi(4^2/2 - 0)', 'ANS: V = 8pi'],
     ['V = pi(8)', 'F(x)', 'y^2']),
    # x^2 = y: pi int_0^4 y dy = 8pi
    ('volume', ['y', 'y=x^2', '0', '4'],
     ['y=x^2', 'x = -sqrt(y) or sqrt(y)', 'V = pi int_0^4 x^2 dy', '= pi int_0^4 y dy', '= pi[y^2/2]_0^4', 'ANS: V = 8pi'],
     ['V = pi(8)']),
    # pi int_0^pi sin^2 = pi * pi/2
    ('volume', ['', 'sin(x)', '0', 'pi', ''],
     ['V = pi int_0^pi sin(x)^2 dx', '= pi[(2x-sin(2x))/4]_0^pi', '= pi(pi/2)', 'ANS: V = pi^2/2', '~ 4.93'],
     ['(sin(x))^2', '\n= pi int']),
    # washer: pi int_0^1 (x^2 - x^4) = pi(1/3 - 1/5) = 2pi/15
    ('volume', ['', 'x', '0', '1', 'x^2'],
     ['V = pi int_0^1 (x^2 - (x^2)^2) dx', '= pi int_0^1 (x^2 - x^4) dx', 'ANS: V = 2pi/15', '~ 0.419']),
    # pi int_0^1 e^(2x) = pi(e^2 - 1)/2 ~ 10.0
    ('volume', ['', 'e^x', '0', '1', ''],
     ['V = pi int_0^1 (e^x)^2 dx', '= pi int_0^1 e^(2x) dx', '= pi(e^2/2 - 1/2)', 'ANS: V = (pi e^2-pi)/2', '~ 10.0']),
    # x^2 = y - 1: pi[y^2/2 - y]_1^5 = pi(15/2 + 1/2) = 8pi
    ('volume', ['y', 'y=x^2+1', '1', '5'],
     ['x = -sqrt(y-1) or sqrt(y-1)', '= pi int_1^5 (y - 1) dy', '= pi(15/2 - (-1/2))', 'ANS: V = 8pi']),
    # non-elementary: pi * 0.59814 = 1.879
    ('volume', ['', 'e^(-x^2)', '0', '1', ''], ['No elementary antiderivative', '= 0.598 (GDC)', '= pi(0.598)', 'ANS: V = 1.88']),
    ('volume', ['', '1/x', '0', '1', ''], ['f undefined at x = 0', 'Improper'], ['ANS']),

    # s = [t^3/3 - 2t^2 + 3t]_0^4 = 4/3; v = 0 at t = 1, 3: 4/3 + 4/3 + 4/3 = 4
    ('kin_v', ['t^2-4t+3', '', '4'],
     ['Displacement = int_0^4 (t^2 - 4t + 3) dt', '= [t^3/3 - 2t^2 + 3t]_0^4', 'ANS: displacement = 4/3',
      'Distance = int_0^4 |t^2 - 4t + 3| dt', 't^2 - 4t + 3 = 0', 't = 1, 3', 'd1 = int_0^1 (t^2 - 4t + 3) dt',
      'd2 = |int_1^3 (t^2 - 4t + 3) dt|', '= |-4/3|', 'd = 4/3 + 4/3 + 4/3', 'ANS: distance = 4'],
     ['F(t)', '= 4/3\nANS', '-int']),
    # 2 sin t on [0,2pi]: displacement 0, distance 4 + 4
    ('kin_v', ['2sin(t)', '', '2pi'],
     ['ANS: displacement = 0', 'sin(t)', 't = pi', 'd2 = |int_pi^(2pi) 2sin(t) dt|', 'd = 4 + 4', 'ANS: distance = 8']),
    # 10 - 2t on [0,8]: 80 - 64 = 16; 25 + 9 = 34
    ('kin_v', ['10-2t', '', '8'], ['ANS: displacement = 16', 't = 5', 'd = 25 + 9', 'ANS: distance = 34']),
    # e^t - 2 on [0,1]: e - 3; (2ln2 - 1) + (e - 4 + 2ln2) = e + 4ln2 - 5 ~ 0.491
    ('kin_v', ['e^t-2', '', '1'], ['ANS: displacement = e-3', 't = ln(2)', '~ 0.491']),
    # sin(t^2) on [0,2]: Simpson 0.80478; |v| split at sqrt(pi): 0.89483 + 0.09005 = 0.98489
    ('kin_v', ['sin(t^2)', '', '2'],
     ['ANS: displacement = 0.805', 't = sqrt(pi)', 'd = 0.895 + 0.0901', 'ANS: distance = 0.985']),
    ('kin_v', ['t', '3', '1'], ['Need t1 < t2'], ['ANS']),
    # no sign change: distance = |displacement|
    ('kin_v', ['3t^2', '', '2'],
     ['= [t^3]_0^2', 'ANS: displacement = 8', 'v does not change sign', 'ANS: distance = 8'], ['d1']),
    ('kin_v', ['-3t^2', '', '2'], ['ANS: displacement = -8', 'v does not change sign', 'ANS: distance = 8']),

    # v = 3t^2 + C, C = 2; s = t^3 + 2t + C, C = 1
    ('kin_a', ['6t', '', '2', '1'],
     ['v(t) = int 6t dt', '= 3t^2 + C', 'v(0) = 2', 'C = 2', 'ANS: v(t) = 3t^2 + 2', 's(t) = int (3t^2 + 2) dt',
      '= t^3 + 2t + C', 's(0) = 1', 'ANS: s(t) = t^3 + 2t + 1'], ['0 + C = 2', 't0: 0']),
    # v = -e^(-t) + C, v(0) = -1 + C = 0
    ('kin_a', ['e^(-t)', '', '0', ''],
     ['= -e^(-t) + C', '-e^0 + C = 0', '-1 + C = 0', 'ANS: v(t) = -e^(-t) + 1'], ['s(t) =']),
    # v = sin t + C, v(pi/2) = 1 + C = 3 -> C = 2
    ('kin_a', ['cos(t)', 'pi/2', '3', ''], ['v(pi/2) = 3', '1 + C = 3', 'ANS: v(t) = sin(t) + 2']),
    ('kin_a', ['e^(t^2)', '', '0', ''], ['No elementary antiderivative'], ['ANS']),

    # ---- review regressions (hand-checked) ----
    # decimals -> exact: int_0^1.5 x^2/2 dx = (27/8)/6 = 9/16
    ('defint', ['0.5x^2', '0', '1.5'], ['= [x^3/6]_0^(3/2)', 'ANS: I = 9/16'], ['0.1666']),
    # exact root pi/3 (was 1.05 GDC); A = (sqrt3/2 - pi/6) + (pi/3 + sqrt3/2) = sqrt3 + pi/6
    ('area_x', ['cos(x)-0.5', '0,pi'], ['x = pi/3', 'A1 = int_0^(pi/3) (cos(x) - 1/2) dx', 'ANS: A = pi/6+sqrt(3)'],
     ['(GDC)', 'pi/3/2']),
    # partial fractions shown: [ln|x-1| - ln|x+1|]_2^3 = -ln2 + ln3 = ln(3/2)
    ('defint', ['2/(x^2-1)', '2', '3'],
     ['2/(x^2-1) = 1/(x-1) - 1/(x+1)', 'int 1/(x-1) dx = ln|x-1|', 'ANS: I = ln(3/2)'], ['Partial']),
    # (x^2+1)/(x+1) = x - 1 + 2/(x+1): [x^2/2 - x + 2ln|x+1|]_0^1 = 2ln2 - 1/2
    ('defint', ['(x^2+1)/(x+1)', '0', '1'],
     ['(x^2+1)/(x+1) = x - 1 + 2/(x+1)', 'ANS: I = 2ln(2)-1/2'], ['Divide']),
    # constant not merged into the log: f(3) = ln(1/5) + C = 0
    ('antider', ['4/(x^2-4)', '3,0'], ['C = ln(5)', 'ANS: f(x) = ln(|x-2|/|x+2|)+ln(5)'], ['ln(5*']),
    # -ln(cos(pi/4)) = ln(2)/2 in simplest form
    ('defint', ['tan(x)', '0', 'pi/4'], ['ANS: I = ln(2)/2'], ['sqrt(2)/2)']),
    # product expanded before integrating; u = x-1: int_0^2 u^2(u-2) du = -4/3 -> 4/3
    ('area_x', ['(x-1)^2(x-3)', ''],
     ['(x-1)^2(x-3) = x^3 - 5x^2 + 7x - 3', 'A1 = |int_1^3 (x-1)^2(x-3) dx|', '= |-4/3|', 'ANS: A = 4/3'], ['Expand']),
    # linear composite kept (reverse chain): [(1+2x)^4/8]_0^1 = 81/8 - 1/8 = 10
    ('defint', ['(1+2x)^3', '0', '1'], ['= [(1+2x)^4/8]_0^1', 'ANS: I = 10'], ['Expand']),
    # Giac's 1/2*(x^2+1)^4/4 tidied: 16/8 - 1/8 = 15/8
    ('defint', ['x(x^2+1)^3', '0', '1'], ['= [(x^2+1)^4/8]_0^1', 'ANS: I = 15/8'], ['/4/']),
    # a = -9.8 exact: v = -49t/5 + 20, s = -49t^2/10 + 20t
    ('kin_a', ['-9.8', '', '20', '0'], ['ANS: v(t) = -49t/5 + 20', 'ANS: s(t) = -49t^2/10 + 20t'],
     ['20.0', '-0.0']),
    ('kin_v', ['1/(t-2)', '', '4'], ['f undefined at t = 2', 'Improper'], ['Need t1', 'ANS']),
    # pi int_1^3 x^-2 dx = pi(1 - 1/3)
    ('volume', ['', '1/x', '1', '3', ''],
     ['V = pi int_1^3 (1/x)^2 dx', '= pi int_1^3 1/x^2 dx', 'ANS: V = 2pi/3']),
    # parameter k is not 'undefined': 9k = 18
    ('defint', ['kx^2', '0', '3', '18'], ['ANS: I = 9k', 'ANS: k = 2'], ['undefined']),
    ('area_2', ['x^2', 'x^2'], ['Same curve: no region'], ['ANS']),
]
