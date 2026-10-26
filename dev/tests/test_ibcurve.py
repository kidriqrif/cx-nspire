MODULE = 'ibcurve'
# Expected answers hand-checked:
#  x^3-3x^2: f'=3x(x-2), f''=6x-6: max (0,0) f''=-6, min (2,-4) f''=6, inflexion (1,-2)
#  x^4: f''(0)=0, f' - then + -> min; f''=12x^2 no sign change -> no inflexion
#  x^3: f' + + -> stationary inflexion (0,0); f''=6x changes sign -> inflexion (0,0)
#  x e^(-x): f'=(1-x)e^-x, f''=(x-2)e^-x: max (1,1/e), inflexion (2,2/e^2)
#  sin x+cos x on [0,2pi]: f'=0 at pi/4, 5pi/4 -> max (pi/4,sqrt2), min (5pi/4,-sqrt2);
#     f''=0 at 3pi/4, 7pi/4 (f=0 there)
#  x^4-4x^3: f'=4x^2(x-3): (0,0) stationary inflexion, min (3,81-108=-27);
#     f''=12x(x-2): inflexions (0,0), (2,16-32=-16)
#  (x^2+1)/x: f'=1-1/x^2: max (-1,-2), min (1,2); f''=2/x^3 never 0
#  ln(x^2-1): f'=2x/(x^2-1), domain |x|>1: dec x<-1, inc x>1
#  s=t^3-6t^2+9t: v=3(t-1)(t-3), a=6t-12; s(2)=2, v(2)=-3, a(2)=0;
#     speeding up 1<t<2 (v<0,a<0) and t>3; slowing 0<t<1, 2<t<3
#  s=2sin t: v=2cos t, a=-2sin t; at t=pi: s=0, v=-2, a=0
#  s=e^-t+t: v=1-e^-t>0 for t>0, a=e^-t>0; speed at 1 = 1-1/e = 0.632
#  -x^2+4x on [0,5]: f'=4-2x=0 at x=2, f''=-2 -> max (2,4); concave down on 0<x<5
CASES = [
    # stationary points / inflexion / concavity
    ('stat', ['x^3-3x^2', ''],
     ['f(x) = x^3 - 3x^2', "f'(x) = 3x^2 - 6x", "f''(x) = 6x - 6", '3x(x-2) = 0', 'x = 0, 2',
      'f(0) = 0^3 - 3(0)^2 = 0', "f''(0) = 6(0) - 6 = -6 < 0, so max", 'ANS: max at (0, 0)',
      "f''(2) = 6(2) - 6 = 6 > 0, so min", 'ANS: min at (2, -4)',
      "x < 1: f''(0) = -6 < 0, concave down", "x > 1: f''(2) = 6 > 0, concave up",
      'ANS: inflexion at (1, -2)', 'ANS: concave up: x > 1', 'ANS: concave down: x < 1'],
     ['-> max', '6*0', '\nx = 0:']),
    ('stat', ['x^4', ''],
     ["f''(0) = 12(0)^2 = 0, inconclusive", "f'(-1) = -4 < 0", "f'(1) = 4 > 0", 'so min',
      'ANS: min at (0, 0)', "x = 0: f'' has no sign change, so not an inflexion",
      'ANS: concave down: none'],
     ['inflexion at']),
    ('stat', ['x^3', ''], ["f'(-1) = 3 > 0", "f'(1) = 3 > 0", 'so stationary inflexion',
                           'ANS: stationary inflexion at (0, 0)', 'ANS: inflexion at (0, 0)']),
    ('stat', ['x e^(-x)', ''], ['(-x+1)e^(-x) = 0',
                                "f''(1) = e^(-1) - 2e^(-1) = -1/e < 0, so max",
                                'ANS: max at (1, 1/e)', '~ (1, 0.368)',
                                'ANS: inflexion at (2, 2/e^2)', 'ANS: concave up: x > 2']),
    ('stat', ['sin(x)+cos(x)', '0,2pi'],
     ['0 <= x <= 2pi', 'x = pi/4, 5pi/4', 'f(pi/4) = sin(pi/4) + cos(pi/4) = sqrt(2)',
      'ANS: max at (pi/4, sqrt(2))', 'ANS: min at (5pi/4, -sqrt(2))',
      'x = 3pi/4, 7pi/4', 'ANS: inflexion at (3pi/4, 0)', 'ANS: inflexion at (7pi/4, 0)',
      'ANS: concave up: 3pi/4 < x < 7pi/4',
      'ANS: concave down: 0 < x < 3pi/4, 7pi/4 < x < 2pi']),
    ('stat', ['x^4-4x^3', ''], ['4x^2 (x-3) = 0', 'ANS: stationary inflexion at (0, 0)',
                                'ANS: min at (3, -27)', 'ANS: inflexion at (2, -16)',
                                'ANS: concave down: 0 < x < 2']),
    ('stat', ['(x^2+1)/x', ''], ['x^2 - 1 = 0', "f''(-1) = 2/(-1)^3 = -2 < 0, so max",
                                 'ANS: max at (-1, -2)', 'ANS: min at (1, 2)',
                                 "f''(x) != 0", 'ANS: concave up: x > 0', 'ANS: concave down: x < 0'],
     ['inflexion at', 'numerator = 0', '2 = 0', 'no real solution']),
    ('stat', ['x^3+x+1', ''], ['3x^2 + 1 = 0', 'No stationary points', 'ANS: inflexion at (0, 1)']),
    ('stat', ['sin(x)', ''], ['(periodic: give a domain)']),
    ('stat', ['-x^2+4x', '0,5'], ['0 <= x <= 5', "f''(2) = -2 < 0, so max", 'ANS: max at (2, 4)',
                                  "0 < x < 5: f''(2) = -2 < 0, concave down", 'ANS: concave up: none',
                                  'ANS: concave down: 0 < x < 5']),
    # increasing / decreasing
    ('incdec', ['x^3-3x^2', ''], ["x < 0: f'(-1) = 9 > 0, increasing",
                                  "0 < x < 2: f'(1) = -3 < 0, decreasing",
                                  'ANS: increasing: x < 0, x > 2', 'ANS: decreasing: 0 < x < 2']),
    ('incdec', ['ln(x^2-1)', ''], ["f' undefined: x = -1, 1", 'x = 0 not in domain',
                                   '-1 < x < 1: not in domain',
                                   'ANS: increasing: x > 1', 'ANS: decreasing: x < -1']),
    ('incdec', ['1/(x-1)', ''], ["f'(x) = -1/(x-1)^2", "f'(x) != 0", "f' undefined: x = 1",
                                 'ANS: increasing: none', 'ANS: decreasing: x < 1, x > 1'],
     ['-1 = 0', 'no real solution', 'numerator = 0']),
    ('incdec', ['x/(x^2+1)', ''], ["f'(x) = (-x^2+1)/(x^2+1)^2", '-(x-1)(x+1) = 0',
                                   'ANS: increasing: -1 < x < 1', 'ANS: decreasing: x < -1, x > 1'],
     ['x^4+2x^2+1']),
    ('incdec', ['sin(x)+cos(x)', '0,2pi'], ['ANS: increasing: 0 < x < pi/4, 5pi/4 < x < 2pi',
                                            'ANS: decreasing: pi/4 < x < 5pi/4']),
    ('incdec', ['5', ''], ['true for all x', "f'(0) = 0, constant", 'ANS: increasing: none',
                           'ANS: decreasing: none'], ["f'(0)=0=0", 'no real solution']),
    # kinematics
    ('kin', ['t^3-6t^2+9t', '', '2'],
     ['s(t) = t^3 - 6t^2 + 9t', 't >= 0', 'v(t) = ds/dt = 3t^2 - 12t + 9', 'a(t) = dv/dt = 6t - 12',
      '3(t-3)(t-1) = 0', 's(2) = 2^3 - 6(2)^2 + 9(2) = 2', 'v(2) = 3(2)^2 - 12(2) + 9 = -3',
      'a(2) = 6(2) - 12 = 0', 'ANS: speed |v(2)| = 3', 'ANS: at rest: t = 1, 3',
      'ANS: changes direction: t = 1, 3', '1 < t < 2: v(1.5) = -2.25 < 0, a(1.5) = -3 < 0, speeding up',
      'ANS: speeding up: 1 < t < 2, t > 3', 'ANS: slowing down: 0 < t < 1, 2 < t < 3'],
     ['At t = (blank=skip): 2']),
    ('kin', ['5t-t^2', '', ''], ['ANS: at rest: t = 5/2', 'ANS: speeding up: t > 5/2',
                                 'ANS: slowing down: 0 < t < 5/2']),
    ('kin', ['2sin(t)', '0,2pi', 'pi'],
     ['0 <= t <= 2pi', 's(pi) = 2sin(pi) = 0', 'v(pi) = 2cos(pi) = -2', 'ANS: speed |v(pi)| = 2',
      'ANS: at rest: t = pi/2, 3pi/2', 'ANS: speeding up: pi/2 < t < pi, 3pi/2 < t < 2pi',
      'ANS: slowing down: 0 < t < pi/2, pi < t < 3pi/2']),
    ('kin', ['e^(-t)+t', '', '1'], ['v(t) = ds/dt = -e^(-t) + 1', 's(1) = e^(-1) + 1 = 1/e + 1',
                                    'v(1) = -e^(-1) + 1 = 1 - 1/e', 'ANS: speed |v(1)| = 1 - 1/e',
                                    '~ 0.632',
                                    'ANS: changes direction: never', 'ANS: speeding up: t > 0',
                                    'ANS: slowing down: none']),
    # linear f: f'' = 0 for all x, so NO inflexion and no concavity (was "concave down")
    ('stat', ['3x+1', ''], ["f'(x) = 3 != 0", 'No stationary points', 'true for all x',
                            'no point of inflexion', 'ANS: concave up: none',
                            'ANS: concave down: none'],
     ["f''(0) = 0, concave", 'all x:', 'inflexion at', '3 = 0', 'no real solution']),
    # f'' a non-zero constant: concave up everywhere
    ('stat', ['x^2', ''], ["f''(x) = 2 != 0", "f''(0) = 2 > 0, so min", 'ANS: min at (0, 0)',
                           'ANS: concave up: all x', 'ANS: concave down: none'], ["\n2=0\n"]),
    # irrational x, rational y: both coordinates to 3 s.f. in the approximation
    ('stat', ['x^4-x^2', ''], ['ANS: min at (-sqrt(2)/2, -1/4)', '~ (-0.707, -0.250)',
                               'ANS: max at (0, 0)', 'ANS: min at (sqrt(2)/2, -1/4)', '~ (0.707, -0.250)']),
    # constant velocity: no dangling comma, no empty tag
    ('kin', ['5t+2', '', '1'], ['v(t) = ds/dt = 5', 'a(t) = dv/dt = 0', 'v(t) = 5 != 0',
                                't > 0: v(1) = 5 > 0, a(1) = 0, constant velocity',
                                'ANS: at rest: never', 'ANS: speeding up: none',
                                'ANS: slowing down: none'], ['a(1) = 0,\n', 'no real solution', '5 = 0']),
    ('kin', ['t^2-4t', '', '2'], ['v(t) = ds/dt = 2t - 4', 'a(t) = dv/dt = 2', 'v(2) = 2(2) - 4 = 0',
                                  'ANS: speed |v(2)| = 0', 'ANS: at rest: t = 2',
                                  'ANS: changes direction: t = 2', 'ANS: speeding up: t > 2',
                                  'ANS: slowing down: 0 < t < 2']),
    # roots outside the domain are reported, not "no real solution"
    ('incdec', ['x^2-2x', '3,5'], ["f'(x) = 2x - 2", 'x = 1 not in domain', '3 < x < 5: f\'(4) = 6 > 0, increasing',
                                   'ANS: increasing: 3 < x < 5', 'ANS: decreasing: none'],
     ['no real solution']),
]
