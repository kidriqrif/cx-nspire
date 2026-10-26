# tests for ibvec (vector ops, lines, vector kinematics); every answer hand-checked
MODULE = 'ibvec'
CASES = [
    # ---- vec_ops 1: AB, magnitude, unit, midpoint ----
    # AB = (3,4,0), |AB| = 5, unit (3/5,4/5,0), M = (5/2,4,3), 10 x unit = (6,8,0)
    ('vec_ops', ['1', '(1,2,3)', '(4,6,3)', '10'],
     ['A = (1, 2, 3)', 'B = (4, 6, 3)', 'AB = OB - OA = (4 - 1, 6 - 2, 3 - 3)', 'ANS: AB = (3, 4, 0)',
      '|AB| = sqrt(3^2 + 4^2 + 0^2) = sqrt(25)', 'unit = (1/5)(3, 4, 0) = (3/5, 4/5, 0)',
      'M = ((1 + 4)/2, (2 + 6)/2, (3 + 3)/2) = (5/2, 4, 3)', 'L = 10', '10 x unit = 10(3/5, 4/5, 0)',
      'ANS: |AB| = 5', 'ANS: 10 x unit = (6, 8, 0)'], ['(3)^2', 'sqrt(25) = 5']),
    ('vec_ops', ['1', '[1,-2,2]', '', ''], ['v = (1, -2, 2)', '|v| = sqrt(1^2 + (-2)^2 + 2^2) = sqrt(9)',
                                          'unit = (1/3)(1, -2, 2) = (1/3, -2/3, 2/3)', 'ANS: |v| = 3'],
     ['ANS: v =']),
    # 1/sqrt14 = sqrt14/14, 2/sqrt14 = sqrt14/7, 3/sqrt14 = 3sqrt14/14
    ('vec_ops', ['1', '1,2,3', '', ''],
     ['|v| = sqrt(1^2 + 2^2 + 3^2)', '(sqrt(14)/14, sqrt(14)/7, 3sqrt(14)/14)',
      'ANS: |v| = sqrt(14)', '~ 3.74'], ['= 3.74']),
    # negative coordinates: B - A = (2-(-1), -1-3) = (3, -4)
    ('vec_ops', ['1', '(-1,3)', '(2,-1)', ''],
     ['AB = OB - OA = (2 - (-1), -1 - 3)', 'ANS: AB = (3, -4)', 'ANS: |AB| = 5',
      'M = ((-1 + 2)/2, (3 + (-1))/2) = (1/2, 1)']),
    # surd components: |v|^2 = 3 + 1 = 4, unit (sqrt3/2, 1/2), 2 x unit = (sqrt3, 1)
    ('vec_ops', ['1', '(sqrt(3),1)', '', '2'],
     ['|v| = sqrt((sqrt(3))^2 + 1^2) = sqrt(4)', 'ANS: |v| = 2', 'unit = (1/2)(sqrt(3), 1) = (sqrt(3)/2, 1/2)',
      '2 x unit = 2(sqrt(3)/2, 1/2)', 'ANS: 2 x unit = (sqrt(3), 1)']),
    ('vec_ops', ['1', '(1,2,3,4)'], ['Error: Bad vector']),
    # ---- 2: parallel ----
    ('vec_ops', ['2', '(2,-4,6)', '(-1,2,-3)'],
     ['u = (2, -4, 6)', 'v = (-1, 2, -3)', 'u = kv', '2 = -k => k = -2', '-4 = 2k => k = -2', '6 = -3k => k = -2',
      'ANS: u = -2v => parallel']),
    ('vec_ops', ['2', '(1,2,3)', '(2,4,5)'], ['3 = 5k => k = 3/5', 'ANS: not parallel'], ['=> parallel']),
    ('vec_ops', ['2', '(1,0,3)', '(2,0,6)'], ['0 = 0 true', 'ANS: u = (1/2)v => parallel']),
    ('vec_ops', ['2', '(2,1,4)', '(1,0,2)'], ['1 = 0 false', 'ANS: not parallel'], ['=> parallel']),
    ('vec_ops', ['2', '(3,-6)', '(3,-6)'], ['3 = 3k => k = 1', 'ANS: u = v => parallel']),
    ('vec_ops', ['2', '(3,-6)', '(-3,6)'], ['3 = -3k => k = -1', 'ANS: u = -v => parallel'], ['k = 1']),
    ('vec_ops', ['2', '(1,2,3)', '(1,2)'], ['Error: 2D/3D mix']),
    # ---- 3: scalar product, angle ----
    # u.v = 2 - 2 + 4 = 4, |u| = |v| = 3, cos = 4/9, arccos(4/9) = 1.110 rad = 63.6 deg
    ('vec_ops', ['3', '(1,2,2)', '(2,-1,2)', ''],
     ['u = (1, 2, 2)', 'v = (2, -1, 2)', 'u.v = 1(2) + 2(-1) + 2(2) = 4', '|u| = sqrt(1^2 + 2^2 + 2^2) = sqrt(9) = 3',
      '|v| = sqrt(2^2 + (-1)^2 + 2^2) = sqrt(9) = 3', 'cos theta = 4/(3 x 3) = 4/9', 'theta = arccos(4/9)',
      'ANS: theta = 1.11 rad = 63.6 deg']),
    ('vec_ops', ['3', '(1,0)', '(0,3)', ''], ['u.v = 1(0) + 0(3) = 0 => perpendicular', 'ANS: theta = pi/2 = 90 deg'],
     ['cos']),
    # cos = 1/sqrt2 = sqrt2/2 -> pi/4 (exact angle: no separate arccos line)
    ('vec_ops', ['3', '(1,0,0)', '(1,1,0)', ''],
     ['cos theta = 1/(1 x sqrt(2)) = sqrt(2)/2', 'ANS: theta = pi/4 = 0.785 rad = 45 deg'], ['arccos']),
    # angle ABC with B = origin: BA = (1,2,3), BC = (1,1,1): cos = 6/sqrt42 = sqrt42/7, 22.2 deg
    ('vec_ops', ['3', '(1,2,3)', '(0,0,0)', '(1,1,1)'],
     ['A = (1, 2, 3)', 'B = (0, 0, 0)', 'C = (1, 1, 1)', 'BA = (1 - 0, 2 - 0, 3 - 0) = (1, 2, 3)',
      'BC = (1 - 0, 1 - 0, 1 - 0) = (1, 1, 1)', 'BA.BC = 1(1) + 2(1) + 3(1) = 6', '|BA| = sqrt(1^2 + 2^2 + 3^2)',
      'cos theta = 6/(sqrt(14) x sqrt(3)) = sqrt(42)/7', 'ANS: theta = 0.388 rad = 22.2 deg']),
    # obtuse: cos = -1/sqrt2 -> 3pi/4 = 135 deg
    ('vec_ops', ['3', '(1,0,0)', '(-1,1,0)', ''],
     ['u.v = 1(-1) + 0(1) + 0(0) = -1', '|v| = sqrt((-1)^2 + 1^2 + 0^2) = sqrt(2)',
      'cos theta = -1/(1 x sqrt(2)) = -sqrt(2)/2', 'ANS: theta = 3pi/4 = 2.36 rad = 135 deg']),
    # same direction: cos = 1, theta = 0
    ('vec_ops', ['3', '(1,2,3)', '(2,4,6)', ''],
     ['u.v = 1(2) + 2(4) + 3(6) = 28', 'cos theta = 28/(sqrt(14) x 2sqrt(14)) = 1', 'theta = arccos(1)',
      'ANS: theta = 0 rad = 0 deg']),
    ('vec_ops', ['3', '(1,2,3)', '(1,2)', ''], ['Error: 2D/3D mix']),
    # ---- 4: vector product, areas ----
    ('vec_ops', ['4', '(1,2,3)', '(4,5,6)', ''],
     ['u x v = (2(6) - 3(5), 3(4) - 1(6), 1(5) - 2(4))', 'ANS: u x v = (-3, 6, -3)',
      '|u x v| = sqrt((-3)^2 + 6^2 + (-3)^2) = sqrt(54)',
      'ANS: parallelogram area = 3sqrt(6)', 'ANS: triangle area = |u x v|/2 = 3sqrt(6)/2']),
    # triangle (1,0,0),(0,2,0),(0,0,3): AB x AC = (6,3,2), |.| = 7, area 7/2
    ('vec_ops', ['4', '(1,0,0)', '(0,2,0)', '(0,0,3)'],
     ['AB = (0 - 1, 2 - 0, 0 - 0) = (-1, 2, 0)', 'AC = (0 - 1, 0 - 0, 3 - 0) = (-1, 0, 3)',
      'AB x AC = (2(3) - 0(0), 0(-1) - (-1)(3), (-1)(0) - 2(-1))', 'ANS: AB x AC = (6, 3, 2)',
      '|AB x AC| = sqrt(6^2 + 3^2 + 2^2) = sqrt(49)', 'ANS: parallelogram area = 7',
      'ANS: triangle area = |AB x AC|/2 = 7/2']),
    # 2D: (3,0) x (0,2) = (0,0,6)
    ('vec_ops', ['4', '(3,0)', '(0,2)', ''], ['ANS: u x v = (0, 0, 6)', 'ANS: parallelogram area = 6', 'triangle area = |u x v|/2 = 3']),
    # parallel vectors: zero cross product, area 0
    ('vec_ops', ['4', '(1,2,3)', '(2,4,6)', ''], ['ANS: u x v = (0, 0, 0)', 'ANS: parallelogram area = 0']),
    # ---- 5: find k ----
    # 2 + 3k - 4 = 0 -> k = 2/3
    ('vec_ops', ['5', '1', '(2,k,1)', '(1,3,-4)'],
     ['u = (2, k, 1)', 'v = (1, 3, -4)', 'u.v = 2(1) + k(3) + 1(-4) = 0', '3k - 2 = 0', 'ANS: k = 2/3']),
    # (2,k,6) = 2(1,3,3) -> k = 6
    ('vec_ops', ['5', '2', '(2,k,6)', '(1,3,3)'], ['u x v = 0', '2(3) - k(1) = 0 => -k + 6 = 0', 'k(3) - 6(3) = 0 => 3k - 18 = 0', 'ANS: k = 6']),
    ('vec_ops', ['5', '2', '(2,k,5)', '(1,3,3)'], ['2(3) - 5(1) = 0 => 1 = 0', 'ANS: no value of k']),
    # 4 + k^2 + 1 = 9 -> k = +-2
    ('vec_ops', ['5', '3', '(2,k,1)', '3'],
     ['|u| = 3', 'sqrt(2^2 + k^2 + 1^2) = 3', '2^2 + k^2 + 1^2 = 3^2', 'k^2 - 4 = 0', 'ANS: k = -2 or 2']),

    # ---- line_ops 1: forms ----
    ('line_ops', ['1', '2', '(1,2,3)', '(3,1,7)'],
     ['A = (1, 2, 3)', 'B = (3, 1, 7)', 'b = AB = (3 - 1, 1 - 2, 7 - 3) = (2, -1, 4)',
      'ANS: r = (1, 2, 3) + t(2, -1, 4)', 'x = 1 + 2t, y = 2 - t, z = 3 + 4t',
      '(x - 1)/2 = (y - 2)/(-1) = (z - 3)/4']),
    ('line_ops', ['1', '3', '(x-1)/2=(y+3)/(-1)=z/4'],
     ['L = (x-1)/2=(y+3)/(-1)=z/4', 'a = (1, -3, 0), b = (2, -1, 4)', 'ANS: r = (1, -3, 0) + t(2, -1, 4)',
      '(y + 3)/(-1) = z/4']),
    ('line_ops', ['1', '', '(0,5,-2)', '(1,0,3)'],
     ['a = (0, 5, -2)', 'b = (1, 0, 3)', 'x = t, y = 5, z = -2 + 3t', 'x = (z + 2)/3, y = 5']),
    ('line_ops', ['1', '3', '(x-1)/2=(y+3)/5, z=4'], ['ANS: r = (1, -3, 4) + t(2, 5, 0)', '(x - 1)/2 = (y + 3)/5, z = 4']),
    ('line_ops', ['1', '', '(1,2,3)', '(0,0,0)'], ['Error: Bad line']),
    # ---- 2: point on line ----
    ('line_ops', ['2', '', '(1,2,3)', '(2,-1,4)', '(5,0,11)'],
     ['P = (5, 0, 11)', '1 + 2t = 5 => t = 2', '2 - t = 0 => t = 2', '3 + 4t = 11 => t = 2', 'ANS: P on line (t = 2)']),
    ('line_ops', ['2', '', '(1,2,3)', '(2,0,4)', '(5,3,11)'], ['2 = 3 false', 'ANS: P not on line']),
    # ---- 3: angle between lines (acute, |b1.b2|) ----
    ('line_ops', ['3', '', '(0,0,0)', '(1,1,0)', '', '(1,2,3)', '(0,1,1)'],
     ['a1 = (0, 0, 0)', 'b1 = (1, 1, 0)', 'a2 = (1, 2, 3)', 'b2 = (0, 1, 1)', 'b1.b2 = 1(0) + 1(1) + 0(1) = 1',
      '|b1| = sqrt(1^2 + 1^2 + 0^2) = sqrt(2)', 'cos theta = |b1.b2|/(|b1||b2|) = 1/(sqrt(2) x sqrt(2)) = 1/2',
      'ANS: theta = pi/3 = 1.05 rad = 60 deg']),
    ('line_ops', ['3', '', '(0,0,0)', '(1,0,0)', '', '(0,0,0)', '(-1,1,0)'],
     ['b1.b2 = 1(-1) + 0(1) + 0(0) = -1', '|b2| = sqrt((-1)^2 + 1^2 + 0^2) = sqrt(2)',
      'cos theta = |b1.b2|/(|b1||b2|) = 1/(1 x sqrt(2)) = sqrt(2)/2', 'ANS: theta = pi/4']),
    # perpendicular lines
    ('line_ops', ['3', '', '(0,0,0)', '(1,0,0)', '', '(0,0,0)', '(0,2,0)'],
     ['b1.b2 = 1(0) + 0(2) + 0(0) = 0 => perpendicular', 'ANS: theta = pi/2 = 1.57 rad = 90 deg'], ['cos']),
    # ---- 4: relationship ----
    # 1+t = 1+s, 2+t = 4-s -> t = s = 1; (iii) 3+1 = 2+2 -> intersect (2,3,4)
    ('line_ops', ['4', '', '(1,2,3)', '(1,1,1)', '', '(1,4,2)', '(1,-1,2)'],
     ['1 + t = 1 + s  (i)', '2 + t = 4 - s  (ii)', 'from (i),(ii): t = 1, s = 1', '(iii): 4 = 4 true',
      'ANS: intersect at (2, 3, 4)'], ['b1 x b2']),
    ('line_ops', ['4', '', '(0,0,0)', '(1,0,0)', '', '(0,1,1)', '(0,1,0)'],
     ['from (i),(ii): t = 0, s = -1', '(iii): 0 = 1 false', 'ANS: skew lines']),
    ('line_ops', ['4', '', '(1,0,0)', '(1,2,3)', '', '(2,2,3)', '(-2,-4,-6)'],
     ['b2 = -2b1 => parallel', '1 + t = 2 => t = 1', 'ANS: coincident (a2 on L1)']),
    # (2,2,4): t = 1 from x, y but 3t = 4 gives t = 4/3
    ('line_ops', ['4', '', '(1,0,0)', '(1,2,3)', '', '(2,2,4)', '(2,4,6)'],
     ['b2 = 2b1 => parallel', '3t = 4 => t = 4/3', 'ANS: parallel, distinct']),
    ('line_ops', ['4', '', '(0,0)', '(1,2)', '', '(3,0)', '(1,-1)'],
     ['t = 3 + s  (i)', '2t = -s  (ii)', 't = 1, s = -2', 'ANS: intersect at (1, 2)'], ['(iii)']),
    # ---- 5: foot of perpendicular, shortest distance ----
    # PF = (t-2, t, -2), PF.b = 2t - 2 = 0, F = (2,1,0), |PF| = sqrt(1+1+4) = sqrt6
    ('line_ops', ['5', '', '(1,0,0)', '(1,1,0)', '(3,0,2)'],
     ['P = (3, 0, 2)', 'F = (1 + t, t, 0)', 'PF = F - P = (t - 2, t, -2)', 'PF.b1 = 0 => 2t - 2 = 0 => t = 1',
      'ANS: foot F = (2, 1, 0)', 'PF = (-1, 1, -2)', '|PF| = sqrt((-1)^2 + 1^2 + (-2)^2)',
      'ANS: distance |PF| = sqrt(6)']),
    ('line_ops', ['5', '', '(0,0,0)', '(1,0,0)', '', '', '(0,1,1)', '(0,1,0)'],
     ['P = (t, 0, 0), Q = (0, 1 + s, 1)', 'PQ = Q - P = (-t, s + 1, 1)', 'PQ.b1 = 0 => -t = 0',
      'PQ.b2 = 0 => s + 1 = 0', 't = 0, s = -1', 'P = (0, 0, 0), Q = (0, 0, 1)',
      '|PQ| = sqrt(0^2 + 0^2 + 1^2)', 'ANS: shortest distance |PQ| = 1'], ['b1 x b2']),
    # skew: |(a2-a1).(b1 x b2)|/|b1 x b2| = |-5|/sqrt14 = 5sqrt14/14
    ('line_ops', ['5', '', '(1,1,1)', '(2,1,-1)', '', '', '(0,2,1)', '(1,1,1)'],
     ['PQ = Q - P = (s - 2t - 1, s - t + 1, s + t)', 'PQ.b1 = 0 => 2s - 6t - 1 = 0', 'PQ.b2 = 0 => 3s - 2t = 0',
      't = -3/14, s = -1/7', '|PQ| = sqrt((-5/7)^2 + (15/14)^2 + (-5/14)^2) = sqrt(25/14)',
      'ANS: shortest distance |PQ| = 5sqrt(14)/14']),
    # parallel lines: distance from (2,1,0) to (1,2,3)+t(1,0,1): foot (0,2,2), distance 3
    ('line_ops', ['5', '', '(1,2,3)', '(1,0,1)', '', '', '(2,1,0)', '(2,0,2)'],
     ['b2 = 2b1 => parallel', 'P = a2 = (2, 1, 0)', 'PF = F - P = (t - 1, 1, t + 3)', 'ANS: foot F = (0, 2, 2)',
      '|PF| = sqrt((-2)^2 + 1^2 + 2^2) = sqrt(9)', 'ANS: distance |PF| = 3']),

    # ---- kinematics ----
    ('kinem', ['1', '(1,2)', '(3,4)', '2'],
     ['r = (1, 2) + t(3, 4)', 'speed = |v| = sqrt(3^2 + 4^2) = sqrt(25)', 'ANS: speed = 5', 't = 2',
      'r(2) = (1 + 2(3), 2 + 2(4))', 'ANS: r(2) = (7, 10)']),
    ('kinem', ['1', '(0,0,0)', '(1,1,1)', ''], ['ANS: speed = sqrt(3)', '~ 1.73'], ['r(']),
    # t = 1 needs no factor
    ('kinem', ['1', '(1,2)', '(3,-4)', '1'], ['r(1) = (1 + 3, 2 + (-4))', 'ANS: r(1) = (4, -2)'], ['1(3)']),
    ('kinem', ['5', '10', '(3,4)'],
     ['speed = 10', 'd = (3, 4)', '|d| = sqrt(3^2 + 4^2) = sqrt(25) = 5', 'v = (10/5)(3, 4)', 'ANS: v = (6, 8)']),
    ('kinem', ['5', '6', '(1,2,2)'], ['ANS: v = (2, 4, 4)']),
    ('kinem', ['2', '(1,2,3)', '(2,0,-1)', '(5,2,1)'],
     ['P = (5, 2, 1)', '1 + 2t = 5 => t = 2', '2 = 2 true', '3 - t = 1 => t = 2', 'ANS: at P when t = 2']),
    ('kinem', ['2', '(1,2,3)', '(2,0,-1)', '(5,3,1)'], ['2 = 3 false', 'ANS: never at P']),
    # D^2 = (2t)^2 + (10-t)^2 = 5t^2 - 20t + 100, t = 2, D^2 = 80 -> 4sqrt5
    ('kinem', ['3', '(0,0)', '(2,0)', '(0,10)', '(0,-1)'],
     ['rA = (0, 0) + t(2, 0)', 'rB = (0, 10) + t(0, -1)', 'rB - rA = (-2t, -t + 10)',
      'D^2 = (-2t)^2 + (-t + 10)^2 = 5t^2 - 20t + 100', 'd(D^2)/dt = 10t - 20 = 0 => t = 2',
      'A at (4, 0), B at (0, 8)', 'D = sqrt(80)', 'ANS: D_min = 4sqrt(5)']),
    ('kinem', ['3', '(0,0)', '(1,1)', '(5,0)', '(1,1)'], ['D^2 = 5^2 + 0^2 = 25', 'ANS: constant distance = 5']),
    # stationary B: minimum at t = -5 < 0, so t = 0: sqrt(25 + 9)
    ('kinem', ['3', '(0,0)', '(1,0)', '(-5,3)', '(0,0)'],
     ['=> t = -5', 't < 0: for t >= 0 min at t = 0', 'ANS: D_min = sqrt(34)'], ['D = sqrt(34)']),
    ('kinem', ['4', '(0,0)', '(1,2)', '(4,0)', '(-1,2)'],
     ['rA = rB', 't = 4 - t => t = 2', '2t = 2t true', 'ANS: collide at t = 2, (2, 4)']),
    ('kinem', ['4', '(0,0)', '(1,2)', '(4,1)', '(-1,2)'], ['2t = 1 + 2t false', 'ANS: no collision']),
    # regression: u.v shown as k*k - 2k + 3 (now k^2); k^2 - 2k + 3 has discriminant -8 < 0
    ('vec_ops', ['5', '1', 'k,k,1', 'k,-2,3'], ['k^2 - 2k + 3 = 0', 'ANS: no value of k'], ['k*k']),
    # regression: r_B - r_A shown as 10 - t - t; D^2 = (10-2t)^2 + 25, min at t = 5, D = 5
    ('kinem', ['3', '0,0', '1,0', '10,5', '-1,0'],
     ['rB - rA = (-2t + 10, 5)', 'D = sqrt(25)', 'ANS: D_min = 5'], ['t - t']),
    # regression: parallel with k in two components showed k*k; k^2 - 2 = 0
    ('vec_ops', ['5', '2', '(k,2)', '(1,k)'], ['k(k) - 2(1) = 0 => k^2 - 2 = 0', 'ANS: k = -sqrt(2) or sqrt(2)'], ['k*k', 'kk']),
    # 2D point with a 3D line: clear message instead of a raw index error
    ('line_ops', ['2', '', '(1,2,3)', '(3,4,5)', '(0,0)'], ['Error: 2D/3D mix']),
    ('line_ops', ['5', '', '(1,2,3)', '(3,4,5)', '(0,0)'], ['Error: 2D/3D mix']),
    # 2D foot of perpendicular: F = (1 + 3t, 2 + 4t), 25t + 11 = 0
    ('line_ops', ['5', '', '(1,2)', '(3,4)', '(0,0)'],
     ['F = (1 + 3t, 2 + 4t)', 'PF.b1 = 0 => 25t + 11 = 0 => t = -11/25', 'ANS: foot F = (-8/25, 6/25)',
      'ANS: distance |PF| = 2/5']),
    # zero vector: |v| = 0 and no unit vector
    ('vec_ops', ['1', '(0,0,0)', '', ''], ['|v| = sqrt(0^2 + 0^2 + 0^2)', 'ANS: |v| = 0'], ['unit', 'sqrt(0)']),
]
