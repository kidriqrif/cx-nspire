# tests for ibtrig2 (exact values, inverse, given ratio, compound angles, identities)
# every expected answer hand-checked
MODULE = 'ibtrig2'
CASES = [
    # ---- trig_values option 1: f(angle) ----
    # 7pi/6 in Q3, cos negative: -cos(pi/6) = -sqrt3/2
    ('trig_values', ['1', 'r', 'cos(7pi/6)'],
     ['cos(7pi/6)', '7pi/6 in Q3, ref angle pi/6', 'cos < 0 in Q3', 'cos(7pi/6) = -cos(pi/6)',
      'ANS: cos(7pi/6) = -sqrt(3)/2'], ['(d/r): ', 'cos(7pi/6) = -cos(pi/6) = -sqrt(3)/2']),
    # sin(300) = -sqrt3/2 -> cosec = -2/sqrt3 = -2sqrt3/3
    ('trig_values', ['1', 'd', 'cosec(300)'],
     ['300 in Q4, ref angle 60', 'sin < 0 in Q4', 'cosec(300) = -cosec(60)', 'ANS: cosec(300) = -2sqrt(3)/3'],
     ['csc(']),
    # 17pi/6 - 2pi = 5pi/6 (Q2): sin = 1/2
    ('trig_values', ['1', 'r', 'sin(17pi/6)'],
     ['sin(17pi/6) = sin(5pi/6)  (period)', '5pi/6 in Q2', 'sin(5pi/6) = sin(pi/6)', 'ANS: sin(17pi/6) = 1/2']),
    # -pi/3 -> 5pi/3, cos(pi/3) = 1/2
    ('trig_values', ['1', 'r', 'cos(-pi/3)'], ['5pi/3 in Q4', 'ANS: cos(-pi/3) = 1/2']),
    # 5pi/3 in Q4: sec = 1/cos(pi/3) = 2
    ('trig_values', ['1', 'r', 'sec(5pi/3)'], ['cos > 0 in Q4', 'ANS: sec(5pi/3) = 2']),
    # axis angles: (0,1) -> tan undefined, cot 0
    ('trig_values', ['1', 'r', 'tan(pi/2)'], ['pi/2: (cos, sin) = (0, 1)', 'ANS: tan(pi/2) = undefined']),
    ('trig_values', ['1', 'd', 'cot(270)'], ['270: (cos, sin) = (0, -1)', 'ANS: cot(270) = 0']),
    # Q1: no sign step; tan(75) = 2 + sqrt3
    ('trig_values', ['1', 'r', 'tan(5pi/12)'],
     ['tan(5pi/12)', 'ANS: tan(5pi/12) = 2 + sqrt(3)', '~ 3.73'], ['in Q1', 'ref angle', 'tan(5pi/12) = tan(5pi/12)']),
    # tan 105 = -tan 75 = -(2 + sqrt3)
    ('trig_values', ['1', 'd', 'tan(105)'],
     ['105 in Q2, ref angle 75', 'tan < 0 in Q2', 'tan(105) = -tan(75)', 'ANS: tan(105) = -2 - sqrt(3)', '~ -3.73']),
    # not an exact value: 3 s.f. only (sin 37 = 0.602), no sin(37pi/180)
    ('trig_values', ['1', 'd', 'sin(37)'], ['ANS: sin(37) = 0.602'], ['pi/180', '~']),
    ('trig_values', ['1', 'd', 'cos(3600)'], ['cos(3600) = cos(0)  (period)', 'ANS: cos(3600) = 1']),
    ('trig_values', ['1', 'r', 'sec(pi/2)'], ['pi/2: (cos, sin) = (0, 1)', 'ANS: sec(pi/2) = undefined']),
    ('trig_values', ['1', 'r', 'sin(x)'], ['Bad angle'], ['ANS']),
    ('trig_values', ['1', 'r', 'x^2'], ['Use f(angle)'], ['ANS']),
    # cos(arcsin(4/5)): sin x = 4/5 in Q1 -> cos x = 3/5
    ('trig_values', ['1', 'r', 'cos(arcsin(4/5))'],
     ['sin x = 4/5, Q1', 'cos^2x = 1 - sin^2x = 1 - (4/5)^2 = 9/25', 'cos x = sqrt(9/25) = 3/5  (Q1: cos > 0)',
      'ANS: cos(arcsin(4/5)) = 3/5'], ['sec x', 'tan x', '=>']),
    # tan(arccos(-1/3)): Q2, sin = 2sqrt2/3, tan = -2sqrt2
    ('trig_values', ['1', 'r', 'tan(arccos(-1/3))'],
     ['cos x = -1/3, Q2', 'sin x = sqrt(8/9) = 2sqrt(2)/3  (Q2: sin > 0)', 'tan x = sin x/cos x = -2sqrt(2)',
      'ANS: tan(arccos(-1/3)) = -2sqrt(2)'], ['sec x']),
    # nested with a double angle: only sin 2x is worked out (cos x = 3/5, sin x = 4/5)
    ('trig_values', ['1', 'r', 'sin(2*arccos(3/5))'],
     ['cos x = 3/5, Q1', 'sin x = sqrt(16/25) = 4/5', 'sin 2x = 2 sin x cos x = 2(4/5)(3/5) = 24/25',
      'ANS: sin(2arccos(3/5)) = 24/25'], ['cos 2x', 'tan 2x', 'sec x']),
    # tan(arctan(-3/4)): sec^2 = 25/16, sec = 5/4 (Q4), cos = 4/5, sin = -3/5
    ('trig_values', ['1', 'r', 'sec(arctan(-3/4))'],
     ['sec^2x = 1 + tan^2x = 1 + (-3/4)^2 = 25/16', 'sec x = sqrt(25/16) = 5/4  (Q4: cos > 0)',
      'ANS: sec(arctan(-3/4)) = 5/4']),
    # ---- option 2: inverse ----
    ('trig_values', ['2', 'r', 'arccos(-1/2)'],
     ['y = arccos(-1/2): cos y = -1/2, 0 <= y <= pi', 'ref angle = arccos(1/2) = pi/3', 'y = pi - pi/3',
      'ANS: arccos(-1/2) = 2pi/3'], ['(v < 0)', 'e.g. arccos(-1/2): arccos']),
    ('trig_values', ['2', 'd', 'arcsin(-sqrt(2)/2)'],
     ['-90 <= y <= 90', 'ref angle = arcsin(sqrt(2)/2) = 45', 'y = -45', 'ANS: arcsin(-sqrt(2)/2) = -45']),
    ('trig_values', ['2', 'r', 'arctan(-sqrt(3))'], ['-pi/2 < y < pi/2', 'ANS: arctan(-sqrt(3)) = -pi/3']),
    # non-standard value: arccos(1/3) = 1.23 (no 'arccos(1/3) = arccos(1/3)', no ref angle line)
    ('trig_values', ['2', 'r', 'arccos(1/3)'], ['y = arccos(1/3): cos y = 1/3, 0 <= y <= pi', 'ANS: arccos(1/3) = 1.23'], ['ANS: arccos(1/3) = arccos', 'ref angle', '~']),
    # negative non-standard value: pi - arccos(1/3) = 1.91
    ('trig_values', ['2', 'r', 'arccos(-1/3)'],
     ['ref angle = arccos(1/3) = 1.23', 'y = pi - 1.23', 'ANS: arccos(-1/3) = pi - arccos(1/3)', '~ 1.91']),
    ('trig_values', ['2', 'd', 'arcsin(1/3)'], ['-90 <= y <= 90', 'ANS: arcsin(1/3) = 19.5']),
    ('trig_values', ['2', 'r', 'arcsin(2)'], ['|v| > 1: undefined'], ['ANS']),
    ('trig_values', ['2', 'r', 'arcsin(t)'], ['Bad value'], ['ANS']),
    # ---- option 3: given one ratio + quadrant ----
    # sin x = 3/5, Q2: cos -4/5, tan -3/4, sin2x = -24/25, cos2x = 1 - 18/25 = 7/25, tan2x = -24/7
    # half angle: x/2 in Q1, sin(x/2) = sqrt(9/10) = 3sqrt10/10, cos(x/2) = sqrt(1/10) = sqrt10/10
    ('trig_values', ['3', 'sin(x)=3/5', '2', 'y'],
     ['sin(x) = 3/5, x in Q2', 'cos^2x = 1 - sin^2x = 1 - (3/5)^2 = 16/25',
      'cos x = -sqrt(16/25) = -4/5  (Q2: cos < 0)', 'sec x = -5/4, cosec x = 5/3, cot x = -4/3',
      'sin 2x = 2 sin x cos x = 2(3/5)(-4/5) = -24/25', 'cos 2x = 1 - 2sin^2x = 1 - 2(3/5)^2 = 7/25',
      'tan 2x = sin 2x/cos 2x = (-24/25)/(7/25) = -24/7',
      'ANS: sin x = 3/5, cos x = -4/5, tan x = -3/4', 'sin 2x = -24/25, cos 2x = 7/25, tan 2x = -24/7',
      'x/2 in Q1', 'sin(x/2) = sqrt((1 - (-4/5))/2) = 3sqrt(10)/10',
      'cos(x/2) = sqrt((1 + (-4/5))/2) = sqrt(10)/10'], ['=>', 'Quadrant of x (1-4): ']),
    # tan x = 2, Q3: sec^2 = 5, sec = -sqrt5, cos = -sqrt5/5, sin = -2sqrt5/5
    # sin2x = 4/5, cos2x = 1/5 - 4/5 = -3/5, tan2x = 4/(1-4) = -4/3
    ('trig_values', ['3', 'tan(x)=2', '3', 'n'],
     ['tan(x) = 2, x in Q3', 'sec^2x = 1 + tan^2x = 1 + 2^2 = 5', 'sec x = -sqrt(5)  (Q3: cos < 0)',
      'cos x = 1/sec x = -sqrt(5)/5', 'sin x = tan x cos x = 2(-sqrt(5)/5) = -2sqrt(5)/5',
      'cos 2x = cos^2x - sin^2x = (-sqrt(5)/5)^2 - (-2sqrt(5)/5)^2 = -3/5',
      'ANS: sin x = -2sqrt(5)/5, cos x = -sqrt(5)/5, tan x = 2', 'sin 2x = 4/5, cos 2x = -3/5, tan 2x = -4/3']),
    # sec x = 2, Q4: cos 1/2, sin -sqrt3/2, sin2x = -sqrt3/2, cos2x = -1/2, tan2x = sqrt3
    ('trig_values', ['3', 'sec(x)=2', '4', 'n'],
     ['cos x = 1/sec x = 1/2', 'sin x = -sqrt(3/4) = -sqrt(3)/2  (Q4: sin < 0)',
      'ANS: sin x = -sqrt(3)/2, cos x = 1/2, tan x = -sqrt(3)',
      'sin 2x = -sqrt(3)/2, cos 2x = -1/2, tan 2x = sqrt(3)'], ['1/(2)']),
    # cos x = -1/3, Q3: sin -2sqrt2/3, tan 2sqrt2, sin2x 4sqrt2/9, cos2x -7/9, tan2x -4sqrt2/7
    # half: x/2 in Q2, sin(x/2) = sqrt(2/3) = sqrt6/3, cos(x/2) = -sqrt(1/3) = -sqrt3/3
    ('trig_values', ['3', 'cos(x)=-1/3', '3', 'y'],
     ['2(-2sqrt(2)/3)(-1/3) = 4sqrt(2)/9', 'cos 2x = 2cos^2x - 1 = 2(-1/3)^2 - 1 = -7/9', '= -4sqrt(2)/7',
      'x/2 in Q2', '= sqrt(6)/3', 'cos(x/2) = -sqrt((1 + (-1/3))/2) = -sqrt(3)/3']),
    # tan x = 1 in Q1: cos2x = 0 so tan2x undefined
    # tan x = 1: sin x = tan x cos x needs no factor 1
    ('trig_values', ['3', 'tan(x)=1', '1', 'n'],
     ['sin x = tan x cos x = sqrt(2)/2', 'tan 2x = sin 2x/cos 2x = (1)/(0) = undefined',
      'sin 2x = 1, cos 2x = 0, tan 2x = undefined'], ['1(sqrt']),
    # tan x = 0: no 0(1) step; (1)^2 - (0)^2 written 1^2 - 0^2
    ('trig_values', ['3', 'tan(x)=0', '1', 'n'],
     ['sin x = tan x cos x = 0', 'cos 2x = cos^2 x - sin^2 x = 1^2 - 0^2 = 1',
      'ANS: sin x = 0, cos x = 1, tan x = 0'], ['0(1)', '(1)^2']),
    # cosec x = -2, Q4: sin x = 1/cosec x = -1/2, cos = sqrt(3)/2, tan = -sqrt(3)/3, cos2x = 1 - 2/4 = 1/2
    ('trig_values', ['3', 'cosec(x)=-2', '4', 'n'],
     ['cosec(x) = -2, x in Q4', 'sin x = 1/cosec x = -1/2', 'cos x = sqrt(3/4) = sqrt(3)/2  (Q4: cos > 0)',
      'cos 2x = 1 - 2sin^2 x = 1 - 2(-1/2)^2 = 1/2', 'ANS: sin x = -1/2, cos x = sqrt(3)/2, tan x = -sqrt(3)/3',
      'sin 2x = -sqrt(3)/2, cos 2x = 1/2, tan 2x = -sqrt(3)']),
    ('trig_values', ['3', 'sin(x)=3/5', '3'], ['Wrong sign for Q3'], ['ANS']),
    ('trig_values', ['3', 'cos(x)=2', '1'], ['|cos x| > 1: impossible'], ['ANS']),
    ('trig_values', ['3', 'sin(x)=3/5', '5'], ['Bad input'], ['ANS']),
    # ---- option 4: A +- B ----
    # sinA=3/5 (Q1) cosA=4/5; cosB=5/13 (Q1) sinB=12/13
    # sin(A+B) = 15/65 + 48/65 = 63/65; cos(A+B) = 20/65 - 36/65 = -16/65; tan = -63/16
    ('trig_values', ['4', 'sin(A)=3/5', '1', 'cos(B)=5/13', '1', '+'],
     ['sin(A) = 3/5, A in Q1', 'cos A = sqrt(16/25) = 4/5', 'sin B = sqrt(144/169) = 12/13',
      'sin(A+B) = sin A cos B + cos A sin B', '= (3/5)(5/13) + (4/5)(12/13)',
      'tan(A+B) = (tan A + tan B)/(1 - tan A tan B)',
      'ANS: sin(A+B) = 63/65, cos(A+B) = -16/65, tan(A+B) = -63/16']),
    # sinA=3/5 Q2 (cosA=-4/5), cosB=-5/13 Q3 (sinB=-12/13)
    # sin(A-B) = -15/65 - 48/65 = -63/65; cos(A-B) = 20/65 - 36/65 = -16/65; tan = 63/16
    ('trig_values', ['4', 'sin(A)=3/5', '2', 'cos(B)=-5/13', '3', '-'],
     ['sin(A-B) = sin A cos B - cos A sin B', 'cos(A-B) = cos A cos B + sin A sin B',
      'ANS: sin(A-B) = -63/65, cos(A-B) = -16/65, tan(A-B) = 63/16']),
    # A = 90 deg (cos 0), B = 30 deg: A+B = 120 deg, tan via sin/cos
    ('trig_values', ['4', 'cos(A)=0', '1', 'sin(B)=1/2', '1', '+'],
     ['tan A = sin A/cos A = undefined', 'tan(A+B) = sin(A+B)/cos(A+B) = -sqrt(3)',
      'ANS: sin(A+B) = sqrt(3)/2, cos(A+B) = -1/2, tan(A+B) = -sqrt(3)']),

    # ---- trig_ident option 1: expand ----
    ('trig_ident', ['1', '', 'sin(x+pi/3)', ''],
     ['sin(x+pi/3)', 'sin(x + pi/3) = sin(x)cos(pi/3) + cos(x)sin(pi/3)  (compound angle)',
      '= (1/2)sin(x) + (sqrt(3)/2)cos(x)', 'ANS: sin(x+pi/3) = sin(x)/2 + sqrt(3)cos(x)/2'],
     ['(sin(x))', 'A = x', '*']),
    # numbers first, factor 1 dropped, no duplicate of the answer
    ('trig_ident', ['1', '', 'sin(x-pi/6)', ''],
     ['sin(x - pi/6) = sin(x)cos(pi/6) - cos(x)sin(pi/6)', '= (sqrt(3)/2)sin(x) - (1/2)cos(x)',
      'ANS: sin(x-pi/6) = sqrt(3)sin(x)/2 - cos(x)/2'], ['(sin(x))', '(cos(x))']),
    ('trig_ident', ['1', '', 'cos(x+pi)', ''], ['= (-1)cos(x) - (0)sin(x)', 'ANS: cos(x+pi) = -cos(x)']),
    # cos15 = cos45cos30 + sin45sin30 = (sqrt6+sqrt2)/4
    ('trig_ident', ['1', '', 'cos(pi/4-pi/6)', ''],
     ['cos(pi/4 - pi/6) = cos(pi/4)cos(pi/6) + sin(pi/4)sin(pi/6)', '= (sqrt(2)/2)(sqrt(3)/2) + (sqrt(2)/2)(1/2)',
      'ANS: cos(pi/4-pi/6) = (sqrt(6)+sqrt(2))/4', '~ 0.966']),
    ('trig_ident', ['1', '3', 'cos(2x)', ''], ['cos(2x)', 'ANS: cos(2x) = 1 - 2sin(x)^2'], ['cos(2x) = 1 - 2sin(x)^2  (double']),
    # sin3x = 3sinx - 4sin^3x
    ('trig_ident', ['1', '', 'sin(3x)', '1'],
     ['sin(2x + x) = sin(2x)cos(x) + cos(2x)sin(x)  (compound angle)',
      '= (2sin(x)cos(x))cos(x) + (2cos(x)^2 - 1)sin(x)  (double angle)', '= 4cos(x)^2 sin(x) - sin(x)',
      'ANS: sin(3x) = 3sin(x) - 4sin(x)^3'], ['(A = 2x, B = x)']),
    # cos3x = 4cos^3x - 3cosx
    ('trig_ident', ['1', '', 'cos(3x)', '2'],
     ['cos(2x + x) = cos(2x)cos(x) - sin(2x)sin(x)  (compound angle)', 'ANS: cos(3x) = 4cos(x)^3 - 3cos(x)']),
    # cos4x = 2cos^2(2x) - 1 = 2(2c^2-1)^2 - 1 = 8c^4 - 8c^2 + 1
    ('trig_ident', ['1', '2', 'cos(4x)', ''],
     ['cos(4x) = 2(2cos(x)^2-1)^2 - 1  (double angle)', 'ANS: cos(4x) = 8cos(x)^4 - 8cos(x)^2 + 1']),
    ('trig_ident', ['1', '', 'tan(x+pi/4)', ''],
     ['tan(x + pi/4) = (tan(x) + tan(pi/4))/(1 - tan(x)tan(pi/4))  (compound angle)',
      'ANS: tan(x+pi/4) = (tan(x)+1)/(1-tan(x))'], ['(1)']),
    ('trig_ident', ['1', '', 'tan(x-pi/4)', ''], ['ANS: tan(x-pi/4) = (tan(x)-1)/(1+tan(x))'], ['(1)']),
    # numbers only: tan 15 = (1 - sqrt3/3)/(1 + sqrt3/3) = 2 - sqrt3, written 2 - sqrt(3) not -sqrt(3) + 2
    ('trig_ident', ['1', '', 'tan(pi/4-pi/6)', ''],
     ['= ((1) - (sqrt(3)/3))/(1 + (1)(sqrt(3)/3))', 'ANS: tan(pi/4-pi/6) = 2 - sqrt(3)', '~ 0.268'], ['-sqrt(3) + 2']),
    ('trig_ident', ['1', '', 'tan(2x)', ''], ['ANS: tan(2x) = 2tan(x)/(1-tan(x)^2)']),
    ('trig_ident', ['1', '', 'sin(5x)'], ['Use kx (k=2,3,4) or A+B'], ['ANS']),
    ('trig_ident', ['1', '', 'x^2'], ['Use sin/cos/tan(..)'], ['ANS']),
    # ---- option 2: simplify ----
    ('trig_ident', ['2', '', 'sin(2x)/(1+cos(2x))'],
     ['E = sin(2x)/(1+cos(2x))', '(double angle)', '= sin(x)/cos(x)', 'ANS: tan(x)  (tan = sin/cos)'],
     ['= tan(x)']),
    ('trig_ident', ['2', '', 'cos(x)^2*(1+tan(x)^2)'],
     ['(tan = sin/cos)', '= cos(x)^2 (1+(sin(x)/cos(x))^2)', 'ANS: 1  (sin^2 x + cos^2 x = 1)'],
     ['etc', '= 1  (']),
    # symmetry: sin(pi - x) = sin x, tan(pi + x) = tan x
    ('trig_ident', ['2', '', 'sin(pi-x)'], ['E = sin(pi-x)', 'ANS: sin(x)  (compound angle)']),
    # brackets round a whole term are dropped: sin(pi+x)/cos(pi+x), not (sin(pi+x)/cos(pi+x))
    ('trig_ident', ['2', '', 'tan(pi+x)'],
     ['= sin(pi+x)/cos(pi+x)  (tan = sin/cos)', '= sin(x)/cos(x)  (compound angle)', 'ANS: tan(x)  (tan = sin/cos)'],
     ['(sin(pi+x)/cos(pi+x))']),
    ('trig_ident', ['2', '', 'sec(x)-cos(x)'],
     ['= 1/cos(x) - cos(x)  (sec = 1/cos)', 'ANS: sin(x)^2/cos(x)  (sin^2 x + cos^2 x = 1)']),
    ('trig_ident', ['2', '', '2sin(x)cos(x)'], ['ANS: sin(2x)  (double angle)']),
    # ---- option 3: verify ----
    ('trig_ident', ['3', '', '(1-cos(2x))/sin(2x)', 'tan(x)'],
     ['LHS = (1-cos(2x))/sin(2x)', '(double angle)', '= sin(x)/cos(x)', '= tan(x)', 'ANS: LHS = RHS'],
     ['\n= RHS']),
    ('trig_ident', ['3', '', 'sec(x)^2-1', 'tan(x)^2'],
     ['(1/cos(x))^2 - 1  (sec = 1/cos)', '= sin(x)^2/cos(x)^2', '= tan(x)^2', 'ANS: LHS = RHS'], ['\n= RHS']),
    # auto cos2A form picks cos^2 - sin^2 so (c-s)(c+s)/(c+s) cancels
    ('trig_ident', ['3', '', 'cos(2x)/(cos(x)+sin(x))', 'cos(x)-sin(x)'],
     ['(cos(x)^2-sin(x)^2)/(cos(x)+sin(x))', '= cos(x) - sin(x)', 'ANS: LHS = RHS']),
    ('trig_ident', ['3', '', 'tan(x)+cot(x)', '2/sin(2x)'],
     ['= sin(x)/cos(x) + cos(x)/sin(x)  (cot = cos/sin, tan = sin/cos)', '= 1/(cos(x)sin(x))',
      '= 2/(2sin(x)cos(x))', '= 2/sin(2x)', 'ANS: LHS = RHS']),
    ('trig_ident', ['3', '', 'cos(x)^4-sin(x)^4', 'cos(2x)'], ['(factorise)', 'ANS: LHS = RHS']),
    # counterexample at pi/6: sin(pi/3) = sqrt3/2, 2 sin(pi/6) = 1
    ('trig_ident', ['3', '', 'sin(2x)', '2sin(x)'],
     ['RHS = 2sin(x)', 'x = pi/6: LHS = sqrt(3)/2, RHS = 1', 'ANS: not an identity'], ['verified']),
    ('trig_ident', ['3', '', 'sin(x)^2', 'cos(x)^2'],
     ['x = pi/6: LHS = 1/4, RHS = 3/4', 'ANS: not an identity']),
    # two sides over a common denominator: 1/(1-s) + 1/(1+s) = 2/(1-s^2) = 2/c^2 = 2 sec^2
    ('trig_ident', ['3', '', '1/(1-sin(x))+1/(1+sin(x))', '2sec(x)^2'], ['= 2sec(x)^2', 'ANS: LHS = RHS']),
]
