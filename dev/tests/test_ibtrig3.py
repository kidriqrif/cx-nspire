# tests for ibtrig3 (trig equations in an interval, trig graphs); answers hand-checked
MODULE = 'ibtrig3'
CASES = [
    # ---- trig_eq ----
    # cos2x = -1/2, 0 <= 2x <= 4pi: 2x = 2pi/3, 4pi/3, 8pi/3, 10pi/3
    ('trig_eq', ['2cos(2x)=-1', 'r', '', '', 'y'],
     ['2cos(2x)=-1', '0 <= x <= 2pi', 'cos(2x) = -1/2', '0 <= 2x <= 4pi', 'ref angle = pi/3',
      'cos < 0: Q2, Q3', '2x = 2pi/3, 4pi/3, 8pi/3, 10pi/3', 'ANS: x = pi/3, 2pi/3, 4pi/3, 5pi/3'],
     ['(d/r): ', 'Lower bound: ', 'endpoints (y/n): ', 'x = pi/3, 2pi/3, 4pi/3, 5pi/3\nANS']),
    # two u values: both x lines are working, the ANS line collects them
    ('trig_eq', ['sin(x)^2=1/4', 'r', '-pi', 'pi', ''],
     ['x = -5pi/6, -pi/6\n', 'x = pi/6, 5pi/6\n', 'ANS: x = -5pi/6, -pi/6, pi/6, 5pi/6']),
    # 2(1 - s^2) = 1 + s -> 2s^2 + s - 1 = (2s-1)(s+1) = 0
    ('trig_eq', ['2cos(x)^2=1+sin(x)', '', '', '', ''],
     ['cos(x)^2 = 1 - sin(x)^2', 'Let u = sin(x)', '2u^2 + u - 1 = 0', '(u+1)(2u-1) = 0',
      'ANS: x = pi/6, 5pi/6, 3pi/2']),
    # 2 sinx cosx - cosx = cosx(2sinx - 1) = 0 on [0, pi]
    ('trig_eq', ['sin(2x)=cos(x)', 'r', '', 'pi', ''],
     ['(double angle)', 'cos(x)(2sin(x) - 1) = 0', 'ANS: x = pi/6, pi/2, 5pi/6'], ['((', '(cos(x))']),
    # 1 - 2s^2 = s, degrees
    ('trig_eq', ['cos(2x)=sin(x)', 'd', '', '', ''],
     ['cos(2x) = 1 - 2sin(x)^2  (double angle)', 'u = -1 or u = 1/2', 'ANS: x = 30, 150, 270']),
    # a sinx + b cosx = 0 -> tan x = 4/3: arctan(4/3) = 0.927, pi + arctan(4/3) = 4.07
    ('trig_eq', ['3sin(x)=4cos(x)', '', '', '', ''],
     ['3sin(x)=4cos(x)', 'tan(x) = 4/3  (divide by cos(x))', 'ref angle = arctan(4/3) = 0.927',
      'ANS: x = arctan(4/3), pi + arctan(4/3)', '~ 0.927, 4.07']),
    ('trig_eq', ['sin(x)=2', '', '', '', ''], ['|sin| > 1: no solution', 'ANS: no solution in interval']),
    # x - pi/3 in [-pi/3, 5pi/3]: -pi/3, pi/3, 5pi/3
    ('trig_eq', ['cos(x-pi/3)=1/2', '', '0', '2pi', ''],
     ['cos(x - pi/3) = 1/2', '-pi/3 <= x - pi/3 <= 5pi/3', 'x - pi/3 = -pi/3, pi/3, 5pi/3',
      'ANS: x = 0, 2pi/3, 2pi']),
    # endpoints excluded: only pi
    ('trig_eq', ['sin(x)=0', '', '0', '2pi', 'n'], ['0 < x < 2pi', 'ANS: x = pi'], ['x = 0', '2pi,']),
    # sec^2 = 1 + tan^2: tan^2 = 3
    ('trig_eq', ['2tan(x)^2=sec(x)^2+2', 'd', '0', '360', ''],
     ['sec(x)^2 = 1 + tan(x)^2', 'u^2 - 3 = 0', 'ANS: x = 60, 120, 240, 300'], ['Pythagorean']),
    ('trig_eq', ['sec(x)=2', '', '', '', ''], ['cos(x) = 1/2', 'ANS: x = pi/3, 5pi/3']),
    ('trig_eq', ['sin(x)^2=1/4', 'r', '-pi', 'pi', ''],
     ['(2u-1)(2u+1) = 0', 'ANS: x = -5pi/6, -pi/6, pi/6, 5pi/6']),
    # 2x - 30 in [-30, 330]: 45, 225 -> x = 37.5, 127.5
    ('trig_eq', ['tan(2x-30)=1', 'd', '0', '180', ''],
     ['-30 <= 2x - 30 <= 330', '2x - 30 = 45, 225', 'ANS: x = 37.5, 127.5'], ['75/2']),
    # 3x - 20 in [-20, 340]: 45, 225 -> x = 65/3 = 21.7, 245/3 = 81.7 (degrees as decimals)
    ('trig_eq', ['tan(3x-20)=1', 'd', '0', '120', ''],
     ['3x - 20 = 45, 225', 'ANS: x = 21.7, 81.7'], ['65/3']),
    # 3x in [0, 3pi]: pi/4, 3pi/4, 9pi/4, 11pi/4
    ('trig_eq', ['sin(3x)=sqrt(2)/2', 'r', '0', 'pi', ''],
     ['3x = pi/4, 3pi/4, 9pi/4, 11pi/4', 'ANS: x = pi/12, pi/4, 3pi/4, 11pi/12']),
    # 2c^2 + 3c + 1 = (2c+1)(c+1) = 0
    ('trig_eq', ['cos(2x)+3cos(x)+2=0', '', '', '', ''],
     ['2u^2 + 3u + 1 = 0', 'ANS: x = 2pi/3, pi, 4pi/3']),
    # tan = sin/cos: sin x (cos x - 1) = 0
    ('trig_eq', ['sin(x)=tan(x)', '', '', '', ''],
     ['tan(x) = sin(x)/cos(x)', '(cos(x) - 1)sin(x) = 0', 'ANS: x = 0, pi, 2pi'], ['cos != 0']),
    # sinx + cosx = sqrt2 cos(x - pi/4) = 1: x - pi/4 = -pi/4, pi/4, 7pi/4 -> x = 0, pi/2, 2pi
    ('trig_eq', ['sin(x)+cos(x)=1', '', '', '', ''],
     ['sqrt(2)cos(x - pi/4) - 1 = 0  (compound angle)', 'ANS: x = 0, pi/2, 2pi'], ['GDC', '1/4*pi']),
    # regression: sinx cosx = 1/4 -> sin2x = 1/2, 2x in [0,4pi]: pi/6, 5pi/6, 13pi/6, 17pi/6 (was GDC 'none')
    ('trig_eq', ['sin(x)cos(x)=1/4', '', '', '', ''],
     ['sin(2x)/2 - 1/4 = 0  (double angle)', 'ANS: x = pi/12, 5pi/12, 13pi/12, 17pi/12'], ['none']),
    # regression: GDC roots exactly on the sampling grid (x sinx = 0 at 0, pi, 2pi)
    ('trig_eq', ['x*sin(x)=0', '', '', '', ''], ['ANS: x = 0, 3.14, 6.28  (GDC)'], ['Using GDC', 'AA']),
    # regression: sloppy tan^2x; tan x = +-sqrt3 on [0, pi]: pi/3, 2pi/3
    ('trig_eq', ['tan^2x=3', '', '0', 'pi', ''], ['Let u = tan(x)', 'ANS: x = pi/3, 2pi/3']),
    # regression: decimal 0.5 -> exact 1/2
    ('trig_eq', ['cos(x)=0.5', '', '', '', ''], ['cos(x) = 1/2', 'ANS: x = pi/3, 5pi/3'], ['1.05']),
    # regression: sin(x+pi/3) = cos x -> tan x = 2 - sqrt3 -> pi/12, 13pi/12 (pi+pi/12 not simplified before)
    ('trig_eq', ['sin(x+pi/3)=cos(x)', '', '', '', ''],
     ['tan(x) = 2 - sqrt(3)  (divide by cos(x))', 'ref angle = pi/12', 'ANS: x = pi/12, 13pi/12'],
     ['pi+pi', '-sqrt(3) + 2']),
    # a degree ratio stays a fraction (sin x = 1/2, not 0.5); only angles are decimals
    ('trig_eq', ['sin(x)=-1/2', 'd', '0', '720', ''],
     ['0 <= x <= 720', 'sin(x) = -1/2', 'ref angle = 30', 'ANS: x = 210, 330, 570, 690'], ['0.5']),
    # sin x = 0.8 -> exact 4/5, 3 s.f. angles
    ('trig_eq', ['sin(x)=0.8', 'd', '', '', ''],
     ['sin(x) = 4/5', 'ref angle = arcsin(4/5) = 53.1', 'ANS: x = 53.1, 127']),
    # not an AA analytic form -> GDC: x sinx = 1 at 1.11, 2.77
    ('trig_eq', ['x*sin(x)=1', '', '', '', ''], ['ANS: x = 1.11, 2.77  (GDC)'], ['Using GDC', 'AA']),

    # ---- trig_graph option 1: features ----
    ('trig_graph', ['1', 'r', '3sin(2(x-pi/4))+1'],
     ['f(x) = 3sin(2(x-pi/4))+1', 'a = 3, b = 2, c = pi/4, d = 1', 'amplitude = 3', 'period = 2pi/2 = pi',
      'shift pi/4 right', 'principal axis y = 1', 'max = 1 + 3 = 4', 'min = 1 - 3 = -2',
      'ANS: range -2 <= f(x) <= 4'], ['|a|', '|b|']),
    ('trig_graph', ['1', 'r', '-2cos(x/2)+5'],
     ['amplitude = 2', 'period = 2pi/(1/2) = 4pi', 'no horizontal shift', 'max = 5 + 2 = 7',
      'ANS: range 3 <= f(x) <= 7']),
    # degrees: 3x + 60 = 3(x + 20), period 360/3
    ('trig_graph', ['1', 'd', '4cos(3x+60)-1'],
     ['3x + 60 = 3(x + 20)', 'period = 360/3 = 120', 'shift 20 left', 'max = -1 + 4 = 3', 'min = -1 - 4 = -5',
      'ANS: range -5 <= f(x) <= 3'], ['2180']),
    # tan(3x): period pi/3, asymptotes 3x = pi/2 + n pi
    ('trig_graph', ['1', 'r', '2tan(3x)'],
     ['period = pi/3', 'asymptotes: x = pi/6 + n(pi/3)', 'ANS: range all real y'], ['amplitude', 'pi/3 = pi/3']),
    # no vertical shift: max/min on one line; period 2pi with b = 1 is not 2pi/1
    ('trig_graph', ['1', 'r', '2sin(x)'],
     ['period = 2pi', 'max = 2, min = -2', 'ANS: range -2 <= f(x) <= 2'], ['2pi/1', '+ 0']),
    ('trig_graph', ['1', 'r', 'sec(x)+1'], ['asymptotes: x = pi/2 + n(pi)', 'ANS: range y <= 0 or y >= 2']),
    # no '0 + n(...)' when the first asymptote is at 0
    ('trig_graph', ['1', 'r', 'csc(2x)'], ['period = 2pi/2 = pi', 'asymptotes: x = n(pi/2)', 'ANS: range y <= -1 or y >= 1'],
     ['0 + n']),
    ('trig_graph', ['1', 'r', '-tan(x/2)+1'], ['a = -1, b = 1/2, c = 0, d = 1', 'period = pi/(1/2) = 2pi',
                                                'asymptotes: x = pi + n(2pi)', 'ANS: range all real y']),
    # a fractional b is written (1/2)(x - 60), not 1/2(x - 60)
    ('trig_graph', ['1', 'd', '(3/2)cos(x/2-30)'],
     ['a = 3/2, b = 1/2, c = 60, d = 0', 'x/2 - 30 = (1/2)(x - 60)', 'period = 360/(1/2) = 720',
      'max = 3/2, min = -3/2', 'ANS: range -3/2 <= f(x) <= 3/2'], ['1/2(x']),
    ('trig_graph', ['1', 'r', 'sin(x)+cos(x)'], ['Not a T(bx+c)+d: use GDC'], ['ANS']),
    # ---- option 2: model from max/min/period ----
    # a = 3, d = 4, b = 2pi/8 = pi/4, c = 2 - (pi/2)/(pi/4) = 0
    ('trig_graph', ['2', 'r', '7', '1', '8', 'sin', '2'],
     ['max = 7', 'max at x = 2', 'a = (7 - 1)/2 = 3', 'd = (7 + 1)/2 = 4', 'b = 2pi/8 = pi/4',
      '(pi/4)(2 - c) = pi/2', 'c = 0', 'ANS: f(x) = 3sin(pi x/4) + 4'], ['((pi/4)x)']),
    ('trig_graph', ['2', 'd', '10', '2', '360', 'cos', '90'],
     ['a = (10 - 2)/2 = 4', 'b = 360/360 = 1', 'c = 90  (max at x = c)', 'ANS: f(x) = 4cos(x - 90) + 6'],
     ['1(x', '((']),
    ('trig_graph', ['2', 'r', '5', '-1', 'pi', 'sin', ''],
     ['a = (5 - (-1))/2 = 3', 'd = (5 - 1)/2 = 2', 'b = 2pi/pi = 2', 'ANS: f(x) = 3sin(2x) + 2'], ['(pi)']),
    # a = 1 is not written; d = 0 is not written
    ('trig_graph', ['2', 'r', '2', '0', '2pi', 'sin', ''], ['ANS: f(x) = sin(x) + 1'], ['1sin']),
    # period 3pi: b = 2pi/(3pi), bracketed; c = pi/3 for a cosine max
    ('trig_graph', ['2', 'r', '4', '-2', '3pi', 'cos', 'pi/3'],
     ['max at x = pi/3', 'b = 2pi/(3pi) = 2/3', 'c = pi/3  (max at x = c)', 'ANS: f(x) = 3cos((2/3)(x - pi/3)) + 1']),
    # degrees: c = 15 - 90/4 = -7.5 (a decimal, not -15/2)
    ('trig_graph', ['2', 'd', '20', '10', '90', 'sin', '15'],
     ['b = 360/90 = 4', '4(15 - c) = 90', 'c = -7.5', 'ANS: f(x) = 5sin(4(x + 7.5)) + 15'], ['15/2', '180/2']),
    ('trig_graph', ['2', 'r', '3', '-3', '4', 'cos', '0'],
     ['d = (3 - 3)/2 = 0', 'ANS: f(x) = 3cos(pi x/2)'], ['+ 0']),
    # ---- option 3: max/min/zeros on an interval ----
    # sin(2x - pi/2) = 1 -> x = pi/2; = -1 -> x = 0, pi; = -1/3 -> x = 0.615, 2.53
    ('trig_graph', ['3', 'r', '3sin(2(x-pi/4))+1', '0', 'pi'],
     ['0 <= x <= pi', 'sin(2x - pi/2) = 1', 'ANS max: (pi/2, 4)', 'ANS min: (0, -2), (pi, -2)',
      '3sin(2(x-pi/4)) + 1 = 0', 'sin(2x - pi/2) = -1/3', 'ANS zeros: (0.615, 0), (2.53, 0)', 'f(0) = -2']),
    # degrees: 3x + 60 = 360 -> x = 100 (y 3); = 180 -> x = 40 (y -5); cos = 1/4 -> 5.17, 74.8; f(0) = 4cos60 - 1 = 1
    ('trig_graph', ['3', 'd', '4cos(3x+60)-1', '0', '120'],
     ['ANS max: (100, 3)', 'ANS min: (40, -5)', 'ref angle = arccos(1/4) = 75.5',
      'ANS zeros: (5.17, 0), (74.8, 0)', 'f(0) = 1']),
    ('trig_graph', ['3', 'r', 'sin(x)+3', '0', '2pi'],
     ['ANS max: (pi/2, 4)', 'ANS min: (3pi/2, 2)', '|sin| > 1: no solution', 'ANS zeros: none']),
    ('trig_graph', ['3', 'd', '2tan(x)-2', '0', '360'], ['ANS zeros: (45, 0), (225, 0)', 'f(0) = -2'], ['ANS max']),
]
