# tests for ibtrig (triangles, arcs/sectors, 3D solids); answers hand-checked
# (the wide run is ASCII: no degree sign must leak into it)
MODULE = 'ibtrig'
CASES = [
    # SAS: a^2 = 25+49-35 = 39; cosB = 63/(14sqrt39) = 3sqrt39/26; Area = 35sqrt3/4
    ('tri_solve', ['', '', '5', '7', '60', '', ''],
     ['b = 5, c = 7, A = 60', 'a^2 = 5^2 + 7^2 - 2(5)(7)cos(60) = 39  (cosine rule)', 'a = sqrt(39) = 6.24',
      'cosB = (39 + 7^2 - 5^2)/(2(sqrt(39))(7)) = 3sqrt(39)/26', 'B = arccos(3sqrt(39)/26) = 43.9',
      'C = 180 - 60 - 43.9 = 76.1', 'Area = (1/2)(5)(7)sin(60) = 35sqrt(3)/4',
      'ANS: a=sqrt(39), b=5, c=7', 'Area=35sqrt(3)/4', '~ a=6.24, Area=15.2'],
     ['°', 'Blank', 'SAS', 'a^2 = b^2']),
    # SSA ambiguous: sinB = 4/5; c = 10 sin(A+B) = 4sqrt3 +- 3
    ('tri_solve', ['d', '5', '8', '', '30', '', ''],
     ['sinB = 8sin(30)/5 = 4/5  (sine rule)', 'B = arcsin(4/5) = 53.1', 'or B = 180 - 53.1 = 127',
      '30 + 127 = 157 < 180', 'Two triangles', 'Triangle 1: B = 53.1', 'C = 180 - 30 - 53.1 = 96.9',
      'c = 5sin(96.9)/sin(30) = 4sqrt(3)+3 = 9.93', 'c=4sqrt(3)+3', 'C=96.9',
      'c=4sqrt(3)-3', 'C=23.1', 'B=53.1', '~ c=9.93, Area=19.9']),
    # SSS: cosC = (9+25-49)/30 = -1/2; cosA = 65/70 = 13/14
    ('tri_solve', ['', '3', '5', '7', '', '', ''],
     ['cosC = (3^2 + 5^2 - 7^2)/(2(3)(5)) = -1/2  (cosine rule)', 'C = arccos(-1/2) = 120',
      'cosA = (5^2 + 7^2 - 3^2)/(2(5)(7)) = 13/14', 'A = arccos(13/14) = 21.8',
      'B = 180 - 21.8 - 120 = 38.2', 'Area=15sqrt(3)/4', '~ Area=6.50']),
    # AAS: b = 10(sqrt3/2)/(sqrt2/2) = 5sqrt6; c = 10 sin75/sin45 = 5sqrt3+5
    ('tri_solve', ['', '10', '', '', '45', '60', ''],
     ['a = 10, A = 45, B = 60', 'C = 180 - 45 - 60 = 75', 'b = 10sin(60)/sin(45) = 5sqrt(6) = 12.2  (sine rule)',
      'c = 10sin(75)/sin(45) = 5sqrt(3)+5', 'b=5sqrt(6)', 'c=5sqrt(3)+5', 'Area=25(sqrt(3)+3)/2'],
     ['a/sinA']),
    # SSA right angle: sinB = 10(1/2)/5 = 1; c = 5sqrt3; Area = 25sqrt3/2
    ('tri_solve', ['', '5', '10', '', '30', '', ''],
     ['B = 90 (right angle)', '30 + 90 = 120 < 180', 'c=5sqrt(3)', 'Area=25sqrt(3)/2'], ['Two triangles']),
    # SSA obtuse A: sinB = 3sqrt3/14, B2 rejected, c = 5 (check c^2+3c-40=0)
    ('tri_solve', ['', '7', '3', '', '120', '', ''],
     ['sinB = 3sin(120)/7 = 3sqrt(3)/14', '120 + 158 = 278 >= 180: reject', 'c = 7sin(38.2)/sin(120) = 5',
      'Area=15sqrt(3)/4'], ['Two triangles']),
    ('tri_solve', ['', '2', '5', '', '60', '', ''], ['sinB = 5sin(60)/2 = 5sqrt(3)/4', 'sinB > 1: no triangle'], ['=>']),
    ('tri_solve', ['', '', '', '', '50', '60', '70'], ['A = 50, B = 60, C = 70', 'Not enough data']),
    ('tri_solve', ['', '1', '2', '5', '', '', ''], ['No triangle: 1 + 2 < 5']),
    # degenerate: 3 + 4 = 7
    ('tri_solve', ['', '3', '4', '7', '', '', ''], ['No triangle: 3 + 4 = 7'], ['ANS']),
    ('tri_solve', ['', '4', '', '', '100', '90', ''], ['Bad angle sum']),
    # two sides + area (new): sinC = 24/30 = 4/5; cosC = +-3/5: c^2 = 61 -+ 36 -> c = 5 or sqrt(97)
    ('tri_solve', ['d', '5', '6', '', '', '', '', '12'],
     ['(1/2)(5)(6)sinC = 12', 'sinC = 4/5', 'Two triangles', 'c^2 = 5^2 + 6^2 - 2(5)(6)cos(53.1) = 25',
      'c=5', 'C=53.1', 'c^2 = 5^2 + 6^2 - 2(5)(6)cos(127) = 97', 'c=sqrt(97)', 'C=127']),
    # area 6sqrt3, sides 4, 6: sinC = sqrt3/2, C = 60 or 120, c = 2sqrt7 or 2sqrt19
    ('tri_solve', ['d', '4', '6', '', '', '', '', '6sqrt3'],
     ['C = arcsin(sqrt(3)/2) = 60', 'c=2sqrt(7)', 'c=2sqrt(19)', 'C=120']),
    # sinA = 2(6)/12 = 1 -> right angle, a = 5 (was shown as 180/2)
    ('tri_solve', ['d', '', '3', '4', '', '', '', '6'], ['A = 90 (right angle)', 'a=5', 'A=90'], ['180/2']),
    ('tri_solve', ['d', '2', '3', '', '', '', '', '10'], ['sinC = 10/3', 'sinC > 1: no triangle'], ['=>']),
    ('tri_solve', ['d', '3', '4', '', '', '', '', ''], ['Not enough data']),
    # SSA A = 90, a = b: sinB = 1, B = 90, A + B = 180 -> no triangle (was accepted)
    ('tri_solve', ['d', '5', '5', '', '90', '', ''], ['reject', 'No triangle'], ['ANS']),
    # radians, equilateral
    ('tri_solve', ['r', '', '2', '2', 'pi/3', '', ''],
     ['a = 2', 'B = arccos(1/2) = pi/3', 'C = pi - pi/3 - pi/3 = pi/3', 'Area=sqrt(3)']),
    # SAS 150: c^2 = 74 + 35sqrt3, c = 11.6 (the decimal c is squared in cosA, not mixed with the exact c^2);
    # the ANS line keeps the exact nested root, with its 3 s.f. value on the ~ line
    ('tri_solve', ['d', '5', '7', '', '', '', '150'],
     ['c^2 = 5^2 + 7^2 - 2(5)(7)cos(150) = 35sqrt(3) + 74 = 135', 'c = 11.6',
      'cosA = (7^2 + 11.6^2 - 5^2)/(2(7)(11.6)) = 0.977', 'A = arccos(0.977) = 12.4', 'B = 180 - 12.4 - 150 = 17.6',
      'ANS: a=5, b=7, c=sqrt(35sqrt(3)+74)', 'A=12.4, B=17.6, C=150, Area=35/4', '~ c=11.6'], ['35sqrt(3) + 74 - 5^2']),
    # radians: Area = 3 - sqrt(3), written like that (not -sqrt(3) + 3)
    ('tri_solve', ['r', '', '', '2', 'pi/4', 'pi/3', ''],
     ['C = pi - pi/4 - pi/3 = 5pi/12', 'a = 2sin(pi/4)/sin(5pi/12) = 2sqrt(3) - 2', 'ANS: a=2sqrt(3) - 2, b=3sqrt(2) - sqrt(6), c=2',
      'Area=3 - sqrt(3)', '~ a=1.46, b=1.79'], ['-sqrt(3) + 3']),
    # decimal data: c^2 = 28.09 + 37.21 - 64.66cos47 = 21.2, c = 4.60
    ('tri_solve', ['', '5.3', '6.1', '', '', '', '47'],
     ['c^2 = 5.3^2 + 6.1^2 - 2(5.3)(6.1)cos(47) = 21.2', 'c = 4.60', 'A = arccos(0.540) = 57.3',
      'B = 180 - 57.3 - 47 = 75.7', 'ANS: a=5.3, b=6.1, c=4.60']),
    # three angles + a side: b = 4 sin60/sin50 = 4.52, c = 4 sin70/sin50 = 4.91
    ('tri_solve', ['', '4', '', '', '50', '60', '70'],
     ['a = 4, A = 50, B = 60, C = 70', 'b = 4sin(60)/sin(50) = 4.52', 'c = 4sin(70)/sin(50) = 4.91', 'Area=8.50']),
    # radians AAS: C = 7pi/12; b = 3 sin(pi/4)/sin(7pi/12) = 3sqrt3 - 3
    ('tri_solve', ['r', '', '', '3', 'pi/6', 'pi/4', ''],
     ['C = pi - pi/6 - pi/4 = 7pi/12', 'b = 3sin(pi/4)/sin(7pi/12) = 3sqrt(3)-3', 'b=3sqrt(3)-3', 'C=7pi/12']),

    # sector r=6, 2pi/3: l=4pi, A=12pi, P=12+4pi, chord 12 sin(pi/3), seg 18(2pi/3 - sqrt3/2)
    ('arc_sector', ['1', 'r', '6', '2pi/3'],
     ['r = 6, theta = 2pi/3', 'l = 6(2pi/3) = 4pi', 'A = (1/2)(6)^2(2pi/3) = 12pi', 'P = 2(6) + 4pi = 12 + 4pi',
      'ANS: l = 4pi, A = 12pi, P = 12 + 4pi', '~ l = 12.6, A = 37.7, P = 24.6',
      'chord = 2(6)sin(pi/3) = 6sqrt(3)', '12pi - 9sqrt(3)'], ['r theta', '(6)(2pi/3)']),
    # nested root in the chord (20 sin36 = 11.8): decimal only
    ('arc_sector', ['1', 'd', '10', '72'],
     ['theta = 72 x pi/180 = 2pi/5', 'ANS: l = 4pi, A = 20pi, P = 20+4pi', 'chord = 2(10)sin(pi/5) = 11.8'],
     ['sqrt(-2', 'theta = 72.0']),
    # l=5, A=10: theta=5/r, 5r/2=10 -> r=4, theta=5/4
    ('arc_sector', ['2', 'r', 'l=5,A=10'],
     ['l = 5, A = 10', 'r theta = 5', 'r^2 theta/2 = 10', 'theta = 5/r', '5r/2 = 10', 'r = 4, theta = 5/4',
      'ANS: l = 5, A = 10, P = 13']),
    ('arc_sector', ['2', 'r', 'P=20,r=5'],
     ['2r + r theta = 20', '10+5theta = 20', 'r = 5, theta = 2', 'ANS: l = 10, A = 25, P = 20']),
    # P=20, A=24: 10r - r^2 = 24 -> r = 4 (theta 3) or 6 (theta 4/3)
    ('arc_sector', ['2', 'r', 'P=20,A=24'],
     ['r = 4, theta = 3', 'r = 6, theta = 4/3', 'ANS: l = 12, A = 24', 'ANS: l = 8, A = 24']),
    # theta=90deg, A=4pi: r^2 = 16, r = 4 (r=-4 rejected), l = 2pi
    ('arc_sector', ['2', 'd', 'theta=90,A=4pi'],
     ['theta = 90 x pi/180 = pi/2', '(rejected)', 'r = 4, theta = pi/2', 'ANS: l = 2pi, A = 4pi, P = 8+2pi']),
    ('arc_sector', ['2', 'r', 'l=10,r=1'], ['(rejected)', 'No valid sector']),
    ('arc_sector', ['2', 'r', 'l=5'], ['Give exactly two values']),
    # regression: negative radius was accepted
    ('arc_sector', ['1', 'r', '-3', '1'], ['Need r > 0, 0 < theta <= 2pi'], ['ANS']),
    # theta = 400 deg is not a sector (the chord was negative)
    ('arc_sector', ['1', 'd', '5', '400'], ['theta = 400 x pi/180 = 20pi/9', 'Need r > 0, 0 < theta <= 2pi'],
     ['ANS', 'chord']),
    # decimals: 2.5(1.2) = 3; no 3.0 inside the working
    ('arc_sector', ['1', 'r', '2.5', '1.2'],
     ['l = 2.5(1.2) = 3.00', 'P = 2(2.5) + 3 = 8.00', 'ANS: l = 3.00, A = 3.75, P = 8.00'], ['+ 3.0 =']),
    # degrees chosen: theta = 5/4 rad also shown as 71.6 deg
    ('arc_sector', ['2', 'd', 'l=5,A=10'], ['r = 4, theta = 5/4', 'theta = 71.6 deg']),
    # regression: the t of sqrt was turned into theta (sqrtheta); r = sqrt3, theta = 2/sqrt3, A = sqrt3
    ('arc_sector', ['2', 'r', 'r=sqrt(3),l=2'],
     ['sqrt(3)theta = 2', 'ANS: l = 2, A = sqrt(3), P = 2sqrt(3)+2', '~ A = 1.73, P = 5.46'], ['sqrtheta']),
    # decimals: theta = 135 deg = 3pi/4; l = 12.5(3pi/4) = 29.5, A = 184, P = 25 + 29.5
    ('arc_sector', ['1', 'd', '12.5', '135'],
     ['l = 12.5(3pi/4) = 29.5', 'P = 2(12.5) + 29.5 = 54.5', 'ANS: l = 29.5, A = 184, P = 54.5'], ['29.4524']),
    # theta = 60 deg, l = 2pi: r = 6, A = 6pi
    ('arc_sector', ['2', 'd', 'theta=60,l=2pi'],
     ['theta = 60, l = 2pi', 'theta = 60 x pi/180 = pi/3', 'r theta = 2pi', 'ANS: l = 2pi, A = 6pi, P = 12+2pi']),

    ('solid_3d', ['1', '(1,2,3)', '(4,6,15)'],
     ['A(1, 2, 3), B(4, 6, 15)', 'd = sqrt((4 - 1)^2 + (6 - 2)^2 + (15 - 3)^2)', '= sqrt(9 + 16 + 144)',
      'ANS: d = 13', 'M = ((1 + 4)/2, (2 + 6)/2, (3 + 15)/2)', 'ANS: M = (5/2, 4, 9)'], ['x2-x1']),
    # negative coordinates: d^2 = 9 + 16 + 25 = 50
    ('solid_3d', ['1', '(-1,2,0)', '(2,-2,5)'],
     ['d = sqrt((2 - (-1))^2 + (-2 - 2)^2 + 5^2)', '= sqrt(9 + 16 + 25)', 'ANS: d = 5sqrt(2)', '~ 7.07',
      'ANS: M = (1/2, 0, 5/2)']),
    # cone r=3 h=4: l=5, V=12pi, SA=9pi+15pi
    ('solid_3d', ['2', '3', '3', '4'],
     ['Cone: r = 3, h = 4', 'l = sqrt(3^2+4^2) = 5', 'V = (1/3)pi(3)^2(4)', 'ANS: V = 12pi', 'SA = pi(3)^2 + pi(3)(5)',
      'ANS: SA = 24pi'], ['V = (1/3)pi r^2 h']),
    ('solid_3d', ['2', '3', '3', '', '5'],
     ['Cone: r = 3, l = 5', 'h = sqrt(5^2-3^2) = 4', 'ANS: V = 12pi']),
    # pyramid 6x6x4: slants 5, 5; V = 48; SA = 36+30+30
    ('solid_3d', ['2', '6', '6', '6', '4'],
     ['Pyramid: l = 6, w = 6, h = 4', 's = sqrt(4^2+(6/2)^2) = 5', 't = sqrt(4^2+(6/2)^2) = 5',
      'edge = sqrt(4^2+(6/2)^2+(6/2)^2) = sqrt(34)', 'V = (1/3)*6*6*4', 'ANS: V = 48',
      'SA = 6*6 + 6*5 + 6*5', 'ANS: SA = 96'], ['(6)(6)']),
    # 4 x 5 x 3 base-edge slants sqrt(61)/2 and sqrt(13): SA = 20 + 2sqrt61 + 5sqrt13 = 53.6
    ('solid_3d', ['2', '6', '4', '5', '3'],
     ['s = sqrt(3^2+(5/2)^2) = sqrt(61)/2', 't = sqrt(3^2+(4/2)^2) = sqrt(13)', 'V = (1/3)*4*5*3', 'ANS: V = 20',
      'SA = 4*5 + 4(sqrt(61)/2) + 5(sqrt(13))', 'ANS: SA = 5sqrt(13) + 2sqrt(61) + 20', '~ 53.6']),
    # open-top cylinder r=3 h=10: V = 90pi, SA = 9pi + 60pi
    ('solid_3d', ['2', '2', '3', '10', '1'],
     ['Cylinder (1 end): r = 3, h = 10', 'SA = pi(3)^2 + 2pi(3)(10)', 'ANS: V = 90pi', 'ANS: SA = 69pi']),
    ('solid_3d', ['2', '5', '2'], ['V = (2/3)pi(2)^3', 'ANS: V = 16pi/3', 'ANS: SA = 12pi']),
    ('solid_3d', ['2', '1', '2', '3', '4'],
     ['Cuboid: l = 2, w = 3, h = 4', 'V = 2*3*4', 'ANS: V = 24', 'SA = 2(2*3+2*4+3*4)', 'ANS: SA = 52'],
     ['(2)(3)']),
    ('solid_3d', ['2', '4', '-2'], ['Bad input']),
    # slant shorter than the radius: h would be imaginary
    ('solid_3d', ['2', '3', '5', '', '3'], ['Cone: r = 5, l = 3', 'Need l > r'], ['ANS', 'h =']),
    # decimals: d^2 = 4 + 9 + 1 (not 4.0)
    ('solid_3d', ['1', '(1/2,2,3)', '(2.5,-1,4)'],
     ['d = sqrt((2.5 - 1/2)^2 + (-1 - 2)^2 + (4 - 3)^2)', '= sqrt(4 + 9 + 1)', 'ANS: d = 3.74'], ['4.0']),
    # regression: solid 7 crashed with 'tuple index out of range'
    ('solid_3d', ['2', '7'], ['Choose 1-6']),
    # closed cylinder: V = 250pi, SA = 50pi + 100pi
    ('solid_3d', ['2', '2', '5', '10', '2'],
     ['Cylinder: r = 5, h = 10', 'V = pi(5)^2(10)', 'ANS: V = 250pi', 'SA = 2pi(5)^2 + 2pi(5)(10)', 'ANS: SA = 150pi']),
    # angle PQ with base: tan = 12/5
    ('solid_3d', ['3', '(0,0,0)', '(3,4,12)'],
     ['P(0, 0, 0), Q(3, 4, 12)', 'F = (3, 4, 0)', 'QF = |12 - 0| = 12', 'PF = sqrt(3^2 + 4^2) = 5', 'tan theta = 12/5',
      'arctan(12/5)', '1.18 rad = 67.4 deg']),
    # P not at the origin: F = (4, 6, 3), PF = sqrt(9 + 16)
    ('solid_3d', ['3', '(1,2,3)', '(4,6,15)'],
     ['F = (4, 6, 3)', 'QF = |15 - 3| = 12', 'PF = sqrt(3^2 + 4^2) = 5', 'arctan(12/5)', '67.4 deg']),
    ('solid_3d', ['3', '(1,1,0)', '(1,1,5)'], ['PF = sqrt(0) = 0', 'theta = 90']),
    # cos PQR = (4+3-3)/(4sqrt3) = sqrt3/3
    ('solid_3d', ['4', '(2,0,0)', '(0,0,0)', '(1,1,1)'],
     ['P(2, 0, 0), Q(0, 0, 0), R(1, 1, 1)', 'PQ = sqrt((-2)^2) = 2', 'cosPQR = (2^2 + 3 - 3)/(2(2)(sqrt(3))) = sqrt(3)/3',
      'cosine rule', 'arccos(sqrt(3)/3)', '54.7 deg']),
]

# degree mode shows the degree sign in unicode mode only (the wide runs above are ASCII)
from harness import run_solver  # noqa: E402
_t = run_solver('ibtrig', 'tri_solve', ['', '', '5', '7', '60', '', ''], uni=1)[0].replace(' ', '')
for _s in ('A=60\u00b0', 'cos(60\u00b0)', 'B=arccos(3\u221a(39)/26)=43.9\u00b0', 'C=180\u00b0-60\u00b0-43.9\u00b0=76.1\u00b0',
           'A=60\u00b0,B=43.9\u00b0,C=76.1\u00b0'):
    if _s not in _t:
        CASES.append(('tri_solve', ['', '', '5', '7', '60', '', ''], ['DEGREE SIGN MISSING: ' + _s]))
_t = run_solver('ibtrig', 'tri_solve', ['d', '5', '8', '', '30', '', ''], uni=1)[0].replace(' ', '')
for _s in ('B=arcsin(4/5)=53.1\u00b0', 'orB=180\u00b0-53.1\u00b0=127\u00b0', '30\u00b0+127\u00b0=157\u00b0<180\u00b0',
           'sin(96.9\u00b0)/sin(30\u00b0)'):
    if _s not in _t:
        CASES.append(('tri_solve', ['d', '5', '8', '', '30', '', ''], ['DEGREE SIGN MISSING: ' + _s]))
_t = run_solver('ibtrig', 'tri_solve', ['r', '', '2', '2', 'pi/3', '', ''], uni=1)[0]
if '\u00b0' in _t:
    CASES.append(('tri_solve', ['r', '', '2', '2', 'pi/3', '', ''], ['DEGREE SIGN IN RADIAN MODE']))

