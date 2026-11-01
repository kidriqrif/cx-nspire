# tests for ibvec2 (plane equations, intersections, angles, distances); answers hand-checked
MODULE = 'ibvec2'
CASES = [
    # ---- plane_eq ----
    # AB = (-1,2,0), AC = (-1,0,3), n = (6,3,2), d = 6
    ('plane_eq', ['1', '(1,0,0)', '(0,2,0)', '(0,0,3)'],
     ['A = (1, 0, 0)', 'AB = (0 - 1, 2 - 0, 0 - 0) = (-1, 2, 0)', 'AC = (0 - 1, 0 - 0, 3 - 0) = (-1, 0, 3)',
      'n = AB x AC = (2(3) - 0(0), 0(-1) - (-1)(3), (-1)(0) - 2(-1))', '= (6, 3, 2)',
      'r.n = a.n = 1(6) + 0(3) + 0(2) = 6', 'r.(6, 3, 2) = 6', 'r = (1, 0, 0) + s(-1, 2, 0) + t(-1, 0, 3)',
      'ANS: 6x + 3y + 2z = 6'], ['(1)(6)']),
    # n = (-8,-4,8) -> (2,1,-2); d = 4 (all three points check)
    ('plane_eq', ['1', '(2,0,0)', '(0,4,0)', '(0,0,-2)'],
     ['= (-8, -4, 8)', 'n parallel to (2, 1, -2)', 'r.n = a.n = 2(2) + 0(1) + 0(-2) = 4', 'ANS: 2x + y - 2z = 4']),
    ('plane_eq', ['1', '(0,0,0)', '(1,1,1)', '(2,2,2)'], ['= (0, 0, 0)', 'ANS: no unique plane']),
    # d = 2 - 3 - 2 = -3
    ('plane_eq', ['2', '(1,-1,2)', '(2,3,-1)'],
     ['a = (1, -1, 2)', 'n = (2, 3, -1)', 'r.n = a.n = 1(2) + (-1)(3) + 2(-1) = -3', 'r.(2, 3, -1) = -3',
      'ANS: 2x + 3y - z = -3']),
    ('plane_eq', ['2', '(1,2)'], ['Error: Bad 3D vector']),
    # decimal normal is not reduced by gcd (used to give 'Error: enter a number')
    ('plane_eq', ['2', '(1,1,1)', '(1.5,0,0)'], ['r.n = a.n', 'ANS: 1.5x = 1.5'], ['Error', 'parallel']),
    ('plane_eq', ['2', '(1,1,1)', '(2.0,4,6)'], ['ANS: 2.0x + 4y + 6z = 12.0'], ['n parallel to']),
    # n = (1,0,2) x (0,1,-1) = (-2,1,1) -> (2,-1,-1); d = 0
    ('plane_eq', ['3', '(1,1,1)', '(1,0,2)', '(0,1,-1)'],
     ['b = (1, 0, 2)', 'c = (0, 1, -1)', 'n = b x c = (0(-1) - 2(1), 2(0) - 1(-1), 1(1) - 0(0))', '= (-2, 1, 1)',
      'n parallel to (2, -1, -1)', 'ANS: 2x - y - z = 0']),
    # AP = (-1,0,1), n = (0,1,0) x (-1,0,1) = (1,0,1), d = 1
    ('plane_eq', ['4', '', '(1,0,0)', '(0,1,0)', '(0,0,1)'],
     ['P = (0, 0, 1)', 'AP = P - a = (0 - 1, 0 - 0, 1 - 0) = (-1, 0, 1)', 'n = b x AP', '= (1, 0, 1)',
      'ANS: x + z = 1']),
    ('plane_eq', ['4', '', '(1,0,0)', '(0,1,0)', '(1,5,0)'], ['P on line: plane not unique', 'ANS: no unique plane']),
    # intersecting lines: n = (1,1,1) x (1,-1,2) = (3,-1,-2), d = 3 - 2 - 6 = -5
    ('plane_eq', ['5', '', '(1,2,3)', '(1,1,1)', '', '(1,4,2)', '(1,-1,2)'],
     ['n = b1 x b2', '(a2 - a1).n = 0(3) + 2(-1) + (-1)(-2) = 0', 'ANS: 3x - y - 2z = -5']),
    # parallel lines: n = (1,2,3) x (1,2,4) = (2,-1,0), d = 2
    ('plane_eq', ['5', '', '(1,0,0)', '(1,2,3)', '', '(2,2,4)', '(2,4,6)'],
     ['b1 x b2 = 0: lines parallel', 'n = b1 x (a2 - a1)', '= (2, -1, 0)', 'ANS: 2x - y = 2']),
    ('plane_eq', ['5', '', '(0,0,0)', '(1,0,0)', '', '(0,1,1)', '(0,1,0)'],
     ['(a2 - a1).n != 0 => skew', 'ANS: no unique plane']),
    # Cartesian -> vector form; n x i = (0,2,1), n x j = (-2,0,2); P: 2 - 0 + 2 = 4
    ('plane_eq', ['6', '2x-y+2z=4', '(1,0,1)'],
     ['n = (2, -1, 2)', 'a = (2, 0, 0)', 'b = n x i = (0, 2, 1), c = n x j = (-2, 0, 2)',
      'ANS: r = (2, 0, 0) + s(0, 2, 1) + t(-2, 0, 2)', 'P = (1, 0, 1)', 'n.P = 1(2) + 0(-1) + 1(2) = 4',
      'ANS: 4 = 4 => P on plane']),
    ('plane_eq', ['6', 'x+y+z=3', '(1,1,2)'], ['ANS: 4 != 3 => P not on plane']),
    # z = 2: n x i = (0,1,0), n x j = (-1,0,0)
    ('plane_eq', ['6', 'z=2', ''],
     ['n = (0, 0, 1)', 'a = (0, 0, 2)', 'b = n x i = (0, 1, 0), c = n x j = (-1, 0, 0)',
      'ANS: r = (0, 0, 2) + s(0, 1, 0) + t(-1, 0, 0)']),
    ('plane_eq', ['6', 'x^2+y=3'], ['Error: Bad plane']),

    # ---- plane_int ----
    # (1+t) + (2-t) + (3+2t) = 12 -> 6 + 2t = 12 -> t = 3, P = (4,-1,9)
    ('plane_int', ['1', '', '(1,2,3)', '(1,-1,2)', 'x+y+z=12'],
     ['a = (1, 2, 3)', 'b = (1, -1, 2)', 'x+y+z=12', '(1 + t) + (2 - t) + (3 + 2t) = 12', '2t + 6 = 12 => t = 3',
      'ANS: P = (4, -1, 9)'], ['(1)(1']),
    ('plane_int', ['1', '', '(1,0,0)', '(1,-1,0)', 'x+y+z=1'], ['(1 + t) - t = 1', '1 = 1', 'ANS: line lies in the plane']),
    ('plane_int', ['1', '', '(1,0,0)', '(1,-1,0)', 'x+y+z=5'], ['1 = 5', 'ANS: line parallel to plane: no intersection']),
    # Cartesian line: (1+2t) + (-3-t) + 4t = 10 -> 5t = 12, P = (29/5, -27/5, 48/5)
    ('plane_int', ['1', '3', '(x-1)/2=(y+3)/(-1)=z/4', 'x+y+z=10'],
     ['a = (1, -3, 0), b = (2, -1, 4)', '(1 + 2t) + (-3 - t) + 4t = 10', '5t - 2 = 10 => t = 12/5',
      'ANS: P = (29/5, -27/5, 48/5)']),
    # coefficients: (1/2)(2t) + t = 1 -> 2t = 1, t = 1/2, P = (1, 1/2, 0)
    ('plane_int', ['1', '', '(0,0,0)', '(2,1,0)', 'x/2+y=1'],
     ['(1/2)(2t) + t = 1', '2t = 1 => t = 1/2', 'ANS: P = (1, 1/2, 0)']),
    # sin theta = 2/3, arcsin(2/3) = 0.730 rad = 41.8 deg
    ('plane_int', ['2', '', '(0,0,0)', '(1,2,2)', 'z=0'],
     ['b.n = 1(0) + 2(0) + 2(1) = 2', '|b| = sqrt(1^2 + 2^2 + 2^2) = sqrt(9) = 3',
      '|n| = sqrt(0^2 + 0^2 + 1^2) = 1', 'sin theta = |b.n|/(|b||n|) = 2/(3 x 1) = 2/3', 'theta = arcsin(2/3)',
      'ANS: theta = 0.730 rad = 41.8 deg']),
    # line along (0,0,1), plane z = 5: sin = 1 -> pi/2
    ('plane_int', ['2', '', '(0,0,0)', '(0,0,2)', 'z=5'], ['= 1', 'ANS: theta = pi/2 = 1.57 rad = 90 deg']),
    # line parallel to the plane: b.n = 0, sin = 0, theta = 0
    ('plane_int', ['2', '', '(0,0,0)', '(1,0,0)', 'z=5'],
     ['b.n = 1(0) + 0(0) + 0(1) = 0', '= 0', 'theta = arcsin(0)', 'ANS: theta = 0 rad = 0 deg']),
    # cos = 2/(sqrt3 sqrt6) = sqrt2/3 -> 61.9 deg
    ('plane_int', ['3', 'x+y+z=6', 'x-y+2z=3'],
     ['n1.n2 = 1(1) + 1(-1) + 1(2) = 2', '|n2| = sqrt(1^2 + (-1)^2 + 2^2) = sqrt(6)',
      'cos theta = |n1.n2|/(|n1||n2|) = 2/(sqrt(3) x sqrt(6)) = sqrt(2)/3', 'ANS: theta = 1.08 rad = 61.9 deg']),
    ('plane_int', ['3', 'x=1', 'y=2'],
     ['n1.n2 = 1(0) + 0(1) + 0(0) = 0 => perpendicular', 'ANS: theta = pi/2 = 1.57 rad = 90 deg'], ['cos']),
    # obtuse normals: n1.n2 = -1, acute angle between the planes: cos = 1/sqrt2 -> pi/4
    ('plane_int', ['3', 'x=1', '-x+y=0'],
     ['n1.n2 = 1(-1) + 0(1) + 0(0) = -1', 'cos theta = |n1.n2|/(|n1||n2|) = 1/(1 x sqrt(2)) = sqrt(2)/2',
      'ANS: theta = pi/4 = 0.785 rad = 45 deg'], ['arccos']),
    # direction (3,-1,-2); z = 0: x + y = 6, x - y = 3 -> (9/2, 3/2)
    ('plane_int', ['4', 'x+y+z=6', 'x-y+2z=3'],
     ['direction = n1 x n2', '= (3, -1, -2)', 'let z = 0: x + y = 6, x - y = 3', 'x = 9/2, y = 3/2',
      'ANS: r = (9/2, 3/2, 0) + t(3, -1, -2)']),
    ('plane_int', ['4', 'x+y+z=6', '2x+2y+2z=5'], ['ANS: planes parallel: no intersection']),
    ('plane_int', ['4', 'x+y+z=6', '2x+2y+2z=12'], ['ANS: planes coincide']),
    # direction (0,0,2) has z component: let z = 0 -> x = 1, y = 1
    ('plane_int', ['4', 'x+y=2', 'x-y=0'], ['let z = 0', 'ANS: r = (1, 1, 0) + t(0, 0, -2)']),
    # three planes: det 7, unique (1,2,3)
    ('plane_int', ['5', 'x+y+z=6', '2x-y+z=3', 'x+2y-z=2'],
     ['x+y+z=6', 'det = 7 != 0 => unique point', '[1, 1, 1 | 6]', 'R2 -> R2 - 2R1', '[0, -3, -1 | -9]',
      'R3 -> R3 - R1', 'R3 -> R3 + (1/3)R2', '[0, 0, -7/3 | -7]', 'z = 3, y = 2, x = 1', 'ANS: point (1, 2, 3)'],
     ['(2)R1', '(1)R1']),
    # pivot swap needed
    ('plane_int', ['5', 'y+z=3', 'x+y=2', 'x+z=3'],
     ['det = -2', 'R1 <-> R2', 'R3 -> R3 + R2', 'ANS: point (1, 1, 2)']),
    # sheaf: R3 = R1 + R2 -> line x = 9/2 - 3t/2, y = 3/2 + t/2, z = t
    ('plane_int', ['5', 'x+y+z=6', 'x-y+2z=3', '2x+3z=9'],
     ['det = 0', '[0, 0, 0 | 0]', 'let z = t', 'x = 9/2 - 3t/2, y = 3/2 + t/2, z = t',
      'ANS: line r = (9/2, 3/2, 0) + t(-3/2, 1/2, 1)'], ['unique']),
    ('plane_int', ['5', 'x+y+z=6', 'x-y+2z=3', '2x+3z=10'],
     ['0 = 1: inconsistent', 'ANS: no common point (triangular prism)']),
    ('plane_int', ['5', 'x+y+z=1', 'x+y+z=2', 'x-y=0'], ['ANS: no common point (parallel planes)']),
    ('plane_int', ['5', 'x+y+z=1', '2x+2y+2z=2', '3x+3y+3z=3'], ['ANS: planes coincide (one plane)']),
    # det = -2k + 6 = 0 at k = 3
    ('plane_int', ['5', 'x+y+z=6', 'x-y+2z=3', '2x+kz=9'], ['det = -2k+6', 'det = 0 => k = 3', 'ANS: unique point if k != 3']),
    # point-plane: (1+t)+(2+t)+(3+t) = 0 -> t = -2; F = (-1,0,1); dist 2sqrt3; P' = (-3,-2,-1)
    ('plane_int', ['6', '(1,2,3)', 'x+y+z=0'],
     ['P = (1, 2, 3)', 'PF: r = (1, 2, 3) + t(1, 1, 1)', '(1 + t) + (2 + t) + (3 + t) = 0', '3t + 6 = 0 => t = -2',
      'ANS: foot F = (-1, 0, 1)', '|PF| = sqrt((-2)^2 + (-2)^2 + (-2)^2)', 'ANS: distance |PF| = 2sqrt(3)',
      "ANS: reflection P' = 2F - P = (-3, -2, -1)"]),
    # (3,0,4) to z = 0... use 2x - y + 2z = 1 from (1,1,1): t = (1-3)/9 = -2/9, distance 2/9*3 = 2/3
    ('plane_int', ['6', '(1,1,1)', '2x-y+2z=1'],
     ['2(1 + 2t) - (1 - t) + 2(1 + 2t) = 1', '9t + 3 = 1 => t = -2/9', 'ANS: foot F = (5/9, 11/9, 5/9)',
      'ANS: distance |PF| = 2/3']),
    ('plane_int', ['6', '(1,1,1)', 'x+y+z=3'],
     ['t = 0', '|PF| = sqrt(0^2 + 0^2 + 0^2)', 'ANS: distance |PF| = 0'], ['sqrt(0)']),
    # regression: det = -(a-1)^2(a+2) with parameter a was reported as '!= 0 => unique point'
    ('plane_int', ['5', 'x+y+az=1', 'x+ay+z=1', 'ax+y+z=1'],
     ['det = -a^3+3a-2', 'det = 0 => a = -2, 1', 'ANS: unique point if a != -2, 1'], ['unique point [']),
    # regression: spaces in r . n = d; (t)+(2t)+(3t) = 6 -> t = 1
    ('plane_int', ['1', '1', '0,0,0', '1,1,1', 'r . (1,2,3) = 6'], ['t + 2t + 3t = 6', '6t = 6 => t = 1', 'ANS: P = (1, 1, 1)']),
]
