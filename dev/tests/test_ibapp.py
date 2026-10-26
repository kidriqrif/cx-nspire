MODULE = 'ibapp'
# Expected answers hand-checked:
#  x^3-2x at 2: y1=4, m=3(4)-2=10 -> y=10x-16; normal m=-1/10 -> y=-x/10+2/10+4=-x/10+21/5
#  ln x at e: y1=1, m=1/e -> y=x/e; normal m=-e -> y=-ex+e^2+1
#  sin x at pi/6: y1=1/2, m=sqrt3/2, c=1/2-sqrt3*pi/12
#  x^3-3x^2 on [-1,4]: f(-1)=-4, f(0)=0, f(2)=-4, f(4)=16; f''=6x-6: f''(0)=-6, f''(2)=6
#  x(10-2x)^2: f'=(10-2x)(10-6x), f(5/3)=(5/3)(20/3)^2=2000/27; f''=24x-80, f''(5/3)=-40
#  A=2x^2+2000/x: x^3=500, A=6x^2=150*4^(2/3)=378.0; A''=4+4000/x^3=4+8=12
#  cylinder A=2pi r^2+660/r: r^3=165/pi, A=6pi r^2=264.4; A''=4pi+1320/r^3=12pi
#  sphere: dV/dt=4pi(9)(2)=72pi; dr/dt=10/(4pi*9)=5/(18pi)
#  ladder x^2+y^2=25: y=4, dy/dt=-x(dx/dt)/y=-3/2
#  cone h=2r: V=2pi r^3/3, dV/dt=2pi r^2(1/2)=16pi at r=4
#  x^3-12x on [0,3]: f'=3x^2-12=0 at x=2, f(2)=-16 (min); f(0)=0, f(3)=-9 -> max 0 at x=0
#  square side x: A=x^2, dx/dt=3 at x=5: dA/dt=2(5)(3)=30
CASES = [
    # tangent & normal
    ('tangent', ['x^3-2x', '2'],
     ['f(x) = x^3 - 2x', "y1 = f(2) = 2^3 - 2(2) = 4", "f'(x) = 3x^2 - 2",
      "m = f'(2) = 3(2)^2 - 2 = 10", 'y - 4 = 10(x - 2)', 'ANS: tangent: y = 10x - 16',
      'normal gradient = -1/m = -1/10', 'ANS: normal: y = -x/10 + 21/5'],
     ['2*2', 'y - y1 = m(x - x1)', 'At x = 2']),
    ('tangent', ['x^2', '0'], ["m = f'(0) = 2(0) = 0", 'ANS: tangent: y = 0', 'normal is vertical',
                               'ANS: normal: x = 0']),
    ('tangent', ['sqrt(x)', '0'], ["m = f'(0) = 1/(2sqrt(0)) undefined", 'vertical tangent',
                                   'ANS: tangent: x = 0', 'ANS: normal: y = 0'], ['infinity']),
    ('tangent', ['ln(x)', 'e'], ['y1 = f(e) = ln(e) = 1', 'y - 1 = (1/e)(x - e)',
                                 'ANS: tangent: y = x/e', 'ANS: normal: y = -ex + e^2 + 1'], ['e^1']),
    ('tangent', ['y = e^(2x)', '0'], ['f(x) = e^(2x)', 'y1 = f(0) = e^(2(0)) = 1', 'y - 1 = 2x',
                                      'ANS: tangent: y = 2x + 1', 'ANS: normal: y = -x/2 + 1']),
    ('tangent', ['sin(x)', 'pi/6'], ['m = f\'(pi/6) = cos(pi/6) = sqrt(3)/2',
                                     'ANS: tangent: y = sqrt(3)x/2 - sqrt(3)pi/12 + 1/2']),
    ('tangent', ['ln(x)', '-1'], ['y1 = f(-1) = ln(-1) undefined'], ['ANS:']),
    # f'(x) = k
    ('gradk', ['x^3-2x', '10', ''], ['3x^2 - 2 = 10', '3x^2 - 12 = 0', '3(x-2)(x+2) = 0',
                                     'x = -2, 2', 'f(-2) = (-2)^3 - 2(-2) = -4', 'f(2) = 2^3 - 2(2) = 4',
                                     'ANS: point (-2, -4)', 'ANS: point (2, 4)']),
    ('gradk', ['x^2+3x', 'y=5x-1', ''], ['line gradient = 5', '2x + 3 = 5', 'f(1) = 1^2 + 3(1) = 4',
                                         'ANS: point (1, 4)']),
    ('gradk', ['x^2+1', '-1/2', ''], ['x = -1/4', 'ANS: point (-1/4, 17/16)']),
    ('gradk', ['sin(x)', '1/2', '0,2pi'], ['0 <= x <= 2pi', 'cos(x) = 1/2', 'x = pi/3, 5pi/3',
                                           'ANS: point (pi/3, sqrt(3)/2)',
                                           'ANS: point (5pi/3, -sqrt(3)/2)']),
    ('gradk', ['x^3', '-3', ''], ['3x^2 + 3 = 0', 'no real solution'], ['ANS:']),
    # optimisation
    ('optim', ['x^3-3x^2', '', '-1,4'], ['-1 <= x <= 4', 'x = 0, 2', "f''(x) = 6x - 6",
                                         "f''(0) = 6(0) - 6 = -6 < 0, so max",
                                         "f''(2) = 6(2) - 6 = 6 > 0, so min",
                                         'f(-1) = (-1)^3 - 3(-1)^2 = -4', 'f(4) = 4^3 - 3(4)^2 = 16',
                                         'ANS: max f = 16', 'at x = 4', 'ANS: min f = -4',
                                         'at x = 2, -1'], ['(max)', '(min)']),
    ('optim', ['x(10-2x)^2', '', '0,5'], ['4(x-5)(3x-5) = 0', 'f(5/3) = (5/3)(10-2(5/3))^2 = 2000/27',
                                          "f''(x) = 24x - 80",
                                          "f''(5/3) = 24(5/3) - 80 = -40 < 0, so max",
                                          'f(5) = 5(10-2(5))^2 = 0',
                                          'ANS: max f = 2000/27', 'at x = 5/3',
                                          'ANS: min f = 0', 'at x = 0, 5']),
    ('optim', ['2x^2+4xh', 'x^2h=500', 'h', '0,inf'],
     ['f = 2x^2 + 4xh', 'x^2 h = 500', 'h = 500/x^2', 'f(x) = 2x^2 + 2000/x', 'x > 0',
      'f = 2x^2 + 4x(500/x^2)', '4x^3 - 2000 = 0', "f''(x) = 4 + 4000/x^3", "= 12 > 0, so min",
      'max: none (not attained)', 'ANS: min f = 150*4^(2/3)', '~ 378'],
     ['numerator = 0', '4^(1/3)*4^(1/3)']),
    ('optim', ['2pi r^2+2pi r h', 'pi r^2 h=330', 'h', '0,inf'],
     ['h = 330/(pi r^2)', 'f = 2pi r^2 + 2pi r(330/(pi r^2))', 'f(r) = 2pi r^2 + 660/r',
      'r = (165/pi)^(1/3)', '= 12pi > 0, so min',
      'ANS: min f = 6*165^(2/3)pi^(1/3)', '~ 264'], ['((165pi^2)^(1/3))^2']),
    ('optim', ['x e^(-x)', '', ''], ['x = 1', "f''(1) = e^(-1) - 2e^(-1) = -1/e < 0, so max",
                                     'x -> inf: f -> 0', 'ANS: max f = 1/e', 'min: none (not attained)'],
     ['(1)e^(-1)']),
    ('optim', ['4xy', 'x^2+y^2=100', 'y', '0,10'], ['y = sqrt(-x^2+100)', '0 <= x <= 10',
                                                    "f''(5sqrt(2)) = -16 < 0, so max",
                                                    'ANS: max f = 200',
                                                    'at x = 5sqrt(2)', 'ANS: min f = 0']),
    ('optim', ['x^3-12x', '', '0,3'], ['x = 2', "f''(2) = 6(2) = 12 > 0, so min", 'f(3) = 3^3 - 12(3) = -9',
                                       'ANS: max f = 0', 'at x = 0', 'ANS: min f = -16', 'at x = 2']),
    # related rates
    ('rates', ['V=4/3pi r^3', 'r', '2', 'r=3'],
     ['V = 4pi r^3/3', 'dr/dt = 2', 'r = 3', 'dV/dr = 4pi r^2',
      'dV/dt = dV/dr x dr/dt = 4pi r^2(2) = 8pi r^2', 'dV/dt = 8pi (3)^2', 'ANS: dV/dt = 72pi'],
     ['(chain rule)', 'Known rate d?/dt for: r']),
    ('rates', ['V=4/3pi r^3', 'V', '10', 'V=36pi'],
     ['dV/dt = dV/dr x dr/dt', '10 = 4pi r^2 dr/dt', 'dr/dt = 5/(2pi r^2)', '36pi = 4pi r^3/3',
      'r = 3', 'ANS: dr/dt = 5/(18pi)']),
    ('rates', ['x^2+y^2=25', 'x', '2', 'x=3'],
     ['2x dx/dt + 2y dy/dt = 0', '2x(2) + 2y dy/dt = 0', 'dy/dt = -2x/y', '3^2 + y^2 = 25',
      'y = 4', 'dy/dt = -2(3)/4', 'ANS: dy/dt = -3/2']),
    ('rates', ['V=1/3pi r^2h', 'h=2r', 'r', '0.5', '4'],
     ['V = pi r^2 h/3', 'h = 2r', 'V = 2pi r^3/3', 'dV/dr = 2pi r^2',
      'dV/dt = dV/dr x dr/dt = 2pi r^2(0.5) = pi r^2', 'ANS: dV/dt = 16pi']),
    ('rates', ['A=pi r^2', 'A', '6', 'r=2'], ['dA/dr = 2pi r', '6 = 2pi r dr/dt',
                                              'ANS: dr/dt = 3/(2pi)']),
    ('rates', ['x^2+y^2=100', 'y', '-3', 'y=6'], ['2y(-3) + 2x dx/dt = 0', 'x = 8',
                                                  'ANS: dx/dt = 9/4']),
    ('rates', ['A=x^2', 'x', '3', '5'], ['dA/dt = (dA/dx)(dx/dt) = 2x(3) = 6x', 'dA/dt = 6(5)',
                                         'ANS: dA/dt = 30'], [' * ']),
    # y = x^3, dx/dt = 2 at x = 1: dy/dt = 3(1)^2(2) = 6
    ('rates', ['y=x^3', 'x', '2', 'x=1'], ['dy/dx = 3x^2', 'dy/dt = (dy/dx)(dx/dt) = 3x^2(2) = 6x^2',
                                           'dy/dt = 6(1)^2', 'ANS: dy/dt = 6'], [' * ']),
    # the only root x = 1 is outside [3, 5]: not "no real solution"; endpoints decide
    ('optim', ['x^2-2x', '', '3,5'], ['3 <= x <= 5', 'x = 1 not in domain', 'f(3) = 3^2 - 2(3) = 3',
                                      'f(5) = 5^2 - 2(5) = 15', 'ANS: max f = 15', 'at x = 5',
                                      'ANS: min f = 3', 'at x = 3'], ['no real solution']),
    # f' is a non-zero constant: f'(x) = 3 != 0, not "3 = 0" then "no real solution"
    ('optim', ['3x+1', '', '0,2'], ["f'(x) = 3 != 0", 'f(0) = 3(0) + 1 = 1', 'ANS: max f = 7', 'at x = 2',
                                    'ANS: min f = 1', 'at x = 0'], ['3 = 0', 'no real solution']),
    ('gradk', ['x^3-3x', '0', ''], ["f'(x) = 3x^2 - 3", '3(x-1)(x+1) = 0', 'x = -1, 1',
                                    'ANS: point (-1, 2)', 'ANS: point (1, -2)'],
     ["3x^2-3=0\n3x^2-3=0"]),
    ('gradk', ['3x+1', '5', ''], ["f'(x) = 3", '3 != 5, no solution'], ['ANS:', 'Error']),
    # x = 6 is outside the circle: no real y
    ('rates', ['x^2+y^2=25', 'x', '2', 'x=6'], ['6^2 + y^2 = 25', 'no real y when x = 6'],
     ['Error', 'ANS:']),
    ('rates', ['x*y=12', 'x', '2', 'x=4'], ['y dx/dt + x dy/dt = 0', 'y(2) + x dy/dt = 0', '4y = 12', 'y = 3',
                                            'ANS: dy/dt = -3/2'], ['(2)y', '(4)y']),
]
