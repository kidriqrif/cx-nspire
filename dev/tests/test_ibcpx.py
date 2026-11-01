# Hand-checked cases for calc/ibcpx.py (complex numbers, conjugate roots, linear systems)
MODULE = 'ibcpx'
CASES = [
    # --- forms / operations
    ('cforms', ['1+i', ''],
     ['z = 1 + i', '|z| = sqrt(1^2 + 1^2) = sqrt(2)', 'ref angle = arctan(1) = pi/4', 'arg z = pi/4 (1st quadrant)',
      'z = sqrt(2)cis(pi/4)', 'z = sqrt(2)e^(i pi/4)', 'ANS: |z| = sqrt(2)', 'ANS: arg z = pi/4'],
     ['Quadrant', 'z = 1 + i\nz = 1 + i', '(1)^2']),
    # zw = -2 + i + 2sqrt3 i - sqrt3 i^2 = (sqrt3 - 2) + (1 + 2sqrt3)i ; z/w = ((-2-sqrt3) + (2sqrt3-1)i)/5
    ('cforms', ['-1+sqrt(3)i', '2-i'],
     ['|z| = sqrt((-1)^2 + (sqrt(3))^2) = 2', 'arg z = pi - pi/3 = 2pi/3 (2nd quadrant)', 'z = 2cis(2pi/3)',
      'z = 2e^(2i pi/3)', 'ANS: arg z = 2pi/3', 'w = 2 - i', 'ANS: z + w = 1 + (sqrt(3)-1)i',
      ' = -2 + i + 2sqrt(3)i - sqrt(3)i^2', 'ANS: zw = sqrt(3) - 2 + (1+2sqrt(3))i',
      'ANS: z/w = (-2-sqrt(3))/5 + ((2sqrt(3)-1)/5)i', 'ANS: z* = -1 - sqrt(3)i'], ['Quadrant']),
    # zw = 3 + 6i - 4i - 8i^2 = 11 + 2i ; z/w = (-5-10i)/5 = -1-2i
    ('cforms', ['3-4i', '1+2i'],
     ['|z| = sqrt(3^2 + (-4)^2) = 5', 'arg z = -arctan(4/3) (4th quadrant)', 'z = 5e^(-i arctan(4/3))',
      'ANS: arg z = -arctan(4/3)', '~ -0.927', 'w = 1 + 2i', 'ANS: zw = 11 + 2i', ' = (-5 - 10i)/5',
      'ANS: z/w = -1 - 2i', 'ANS: z* = 3 + 4i']),
    ('cforms', ['-sqrt(3)-i', ''],
     ['arg z = pi/6 - pi = -5pi/6 (3rd quadrant)', 'ANS: |z| = 2', 'ANS: arg z = -5pi/6']),
    ('cforms', ['2cis(pi/3)', ''],
     ['z = 2cis(pi/3)', 'z = 1 + sqrt(3)i', 'arg z = pi/3 (1st quadrant)', 'ANS: arg z = pi/3']),
    ('cforms', ['0'], ['|z| = 0', 'arg undefined'], ['ANS:']),
    # on an axis: modulus and argument straight away
    ('cforms', ['-3', ''], ['|z| = 3', 'arg z = pi', 'z = 3e^(i pi)', 'ANS: arg z = pi'], ['sqrt(']),
    ('cforms', ['-2i', ''], ['|z| = 2', 'arg z = -pi/2', 'z = 2cis(-pi/2)', 'ANS: arg z = -pi/2'], ['sqrt(']),
    # arg = pi - arctan(4/3) = 2.214
    ('cforms', ['-3+4i', ''],
     ['arg z = pi - arctan(4/3) (2nd quadrant)', 'z = 5cis(pi-arctan(4/3))', 'ANS: |z| = 5', '~ 2.21']),
    # --- De Moivre: (sqrt2)^8 cis(2pi) = 16
    ('demoivre', ['1+i', '8'],
     ['n = 8', 'z = sqrt(2)cis(pi/4)', 'z^8 = (sqrt(2))^8 cis(8pi/4) (De Moivre)', ' = 16cis(2pi)', 'ANS: z^8 = 16'],
     ['cis(0)', '16(1)', 'z^n = r^n']),
    ('demoivre', ['1-sqrt(3)i', '6'],
     ['z = 2cis(-pi/3)', 'z^6 = 2^6 cis(6(-pi/3)) (De Moivre)', ' = 64cis(-2pi)', 'ANS: z^6 = 64'], ['cis(0)']),
    # 2^-3 cis(-pi/2) = -i/8
    ('demoivre', ['sqrt(3)+i', '-3'],
     ['z^(-3) = 2^(-3) cis(-3pi/6) (De Moivre)', ' = (1/8)cis(-pi/2)', 'ANS: z^(-3) = -(1/8)i'], ['(-i)']),
    # (3+4i)^3 = -117 + 44i
    ('demoivre', ['3+4i', '3'],
     ['z = 5cis(arctan(4/3))', 'z^3 = 5^3 cis(3arctan(4/3)) (De Moivre)', ' = 125cis(3arctan(4/3))',
      'ANS: z^3 = -117 + 44i']),
    ('demoivre', ['-1+sqrt(3)i', '3'], [' = 8cis(2pi)', 'ANS: z^3 = 8'], ['cis(0)']),
    ('demoivre', ['1+i', '1/2'], ['n must be an integer'], ['ANS:']),
    # i^7 = -i ; the modulus 1 is not written as 1^7
    ('demoivre', ['i', '7'], ['z^7 = cis(7pi/2) (De Moivre)', ' = cis(-pi/2)', 'ANS: z^7 = -i'], ['1^7']),
    ('demoivre', ['-2', '3'], ['|z| = 2', 'ANS: z^3 = -8']),
    # (1+i)^5 = 4sqrt2 cis(5pi/4) = -4 - 4i
    ('demoivre', ['1+i', '5'], [' = 4sqrt(2)cis(5pi/4)', ' = 4sqrt(2)cis(-3pi/4)', 'ANS: z^5 = -4 - 4i']),
    # --- nth roots: w^3 = 8i -> 2cis(pi/6), 2cis(5pi/6), 2cis(-pi/2)
    # the k=2 line shows the formula angle and its principal value (must agree)
    ('nroots', ['8i', '3'],
     ['z = 8i', 'n = 3', 'z = 8cis(pi/2 + 2kpi)', 'w = 2cis((pi/2 + 2kpi)/3)', 'k = 0, 1, 2',
      'k=2: w = 2cis(3pi/2) = 2cis(-pi/2)', 'ANS: w0 = sqrt(3) + i', 'ANS: w1 = -sqrt(3) + i', 'ANS: w2 = -2i'],
     ['2(-i)']),
    ('nroots', ['16', '4'],
     ['z = 16cis(2kpi)', 'ANS: w0 = 2', 'ANS: w1 = 2i', 'ANS: w2 = -2', 'ANS: w3 = -2i'], ['2(1)', '0 + 2kpi']),
    ('nroots', ['-1+sqrt(3)i', '2'],
     ['w = sqrt(2)cis((2pi/3 + 2kpi)/2)', 'ANS: w0 = sqrt(2)/2 + (sqrt(6)/2)i', 'ANS: w1 = -sqrt(2)/2 - (sqrt(6)/2)i']),
    # (2+i)^2 = 3+4i ; second root arg reduced into (-pi, pi]
    ('nroots', ['3+4i', '2'], ['ANS: w0 = 2 + i', 'cis(-pi+arctan(4/3)/2)', 'ANS: w1 = -2 - i']),
    ('nroots', ['-8', '3'], ['k=2: w = 2cis(5pi/3) = 2cis(-pi/3)',
                             'ANS: w0 = 1 + sqrt(3)i', 'ANS: w1 = -2', 'ANS: w2 = 1 - sqrt(3)i']),
    ('nroots', ['1+i', '1'], ['Need integer n >= 2'], ['ANS:']),
    # (1+i)^4 = (2i)^2 = -4 ; modulus 4^(1/4) = sqrt(2)
    ('nroots', ['-4', '4'],
     ['w = sqrt(2)cis((pi + 2kpi)/4)', 'ANS: w0 = 1 + i', 'ANS: w1 = -1 + i', 'ANS: w2 = -1 - i', 'ANS: w3 = 1 - i'],
     ['4^(1/4)']),
    # cube roots of unity; w = cis(theta) is already the answer form
    ('nroots', ['1', '3'],
     ['ANS: w0 = 1', 'ANS: w1 = -1/2 + (sqrt(3)/2)i', 'ANS: w2 = -1/2 - (sqrt(3)/2)i'], ['\n = -1/2']),
    # --- conjugate roots: (x^2-2x+5)(x-3)
    ('conjroot', ['x^3-5x^2+11x-15', '1+2i'],
     ['p(x) = x^3 - 5x^2 + 11x - 15', 'z = 1 + 2i', 'p(1 + 2i) = 0', 'z* = 1 - 2i is also a root',
      '(x - (1 + 2i))(x - (1 - 2i)) = x^2 - 2x + 5', 'p(x) = (x^2 - 2x + 5)(x + c)',
      'constant: 5c = -15, c = -3', 'p(x) = (x^2 - 2x + 5)(x - 3)', 'ANS: roots = 1 + 2i, 1 - 2i, 3']),
    # Re: 3a+2b+12 = 0, Im: 4a+b+11 = 0 -> a = -2, b = -3 ; (x^2-4x+5)(x+2)
    ('conjroot', ['x^3+ax^2+bx+10', '2+i'],
     ['Re: 3a + 2b + 12 = 0', 'Im: 4a + b + 11 = 0', 'ANS: a = -2', 'ANS: b = -3', 'p(x) = x^3 - 2x^2 - 3x + 10',
      'p(x) = (x^2 - 4x + 5)(x + c)', 'constant: 5c = 10, c = 2', 'p(x) = (x^2 - 4x + 5)(x + 2)',
      'ANS: roots = 2 + i, 2 - i, -2']),
    # quartic: (x^2-2x+5)(x^2+bx+c): x^3: b-2 = -2 so b = 0 ; 5c = 5 so c = 1
    ('conjroot', ['x^4-2x^3+6x^2-2x+5', '1+2i'],
     ['p(x) = (x^2 - 2x + 5)(x^2 + bx + c)', 'x^3: b - 2 = -2, b = 0', 'constant: 5c = 5, c = 1',
      'p(x) = (x^2 - 2x + 5)(x^2 + 1)', 'ANS: roots = 1 + 2i, 1 - 2i, -i, i']),
    ('conjroot', ['x^4+4', '1+i'],
     ['x^3: b - 2 = 0, b = 2', 'constant: 2c = 4, c = 2', 'p(x) = (x^2 - 2x + 2)(x^2 + 2x + 2)',
      'ANS: roots = 1 + i, 1 - i, -1 - i, -1 + i']),
    ('conjroot', ['x^2+1', '2+i'], ['p(2 + i) = 4 + 4i', 'z is not a root'], ['ANS:']),
    ('conjroot', ['x^3+2x+3', '-1'], ['z is real'], ['ANS:']),
    # leading coefficient 2: 2(x-3)(x^2+4)
    ('conjroot', ['2x^3-6x^2+8x-24', '2i'],
     ['(x - (2i))(x - (-2i)) = x^2 + 4', 'p(x) = (x^2 + 4)(2x + c)', 'constant: 4c = -24, c = -6',
      'p(x) = (x^2 + 4)(2x - 6)', 'ANS: roots = 2i, -2i, 3']),
    ('conjroot', ['x^2-2x+5=0', '1+2i'], ['p(x) = x^2 - 2x + 5', 'ANS: roots = 1 + 2i, 1 - 2i'], ['(1)']),
    # p(i) = 0 but the coefficients are not real
    ('conjroot', ['x^2-(2+i)x+2i', 'i'], ['p(i) = 0', 'Coefficients are not real'], ['ANS:']),
    # --- linear systems: (1, 2, 3)
    ('linsys', ['x+y+z=6', '2x-y+z=3', 'x+2y-z=2'],
     ['x+y+z=6', 'Augmented matrix:', 'R2 -> R2 - 2R1', 'R3 -> R3 + 3R2', 'Unique solution', 'R2: y - 2(3) = -4',
      'R1: x + 2 + 3 = 6', 'ANS: x = 1', 'ANS: y = 2', 'ANS: z = 3'], ['Row echelon', ' => x = 1\nANS']),
    ('linsys', ['2x+3y=7', 'x-y=1', ''], ['R1 <-> R2', 'R1: x - 1 = 1', 'ANS: x = 2', 'ANS: y = 1']),
    ('linsys', ['0.5x+y=2', 'x-y=1', ''], ['[1  2 | 4]', 'ANS: x = 2', 'ANS: y = 1']),
    ('linsys', ['x+y+z=1', '2x+2y+2z=3', 'x-y=0'],
     ['R3: 0 = 1 (inconsistent)', 'ANS: no solution'], ['ANS: x', 'Row echelon']),
    # z = l, y = (1+l)/2, x = (5-3l)/2
    ('linsys', ['x+y+z=3', 'x-y+2z=2', '2x+3z=5'],
     ['Infinitely many solutions', 'z = lambda', 'R2: -2y + lambda = -1', ' => y = (lambda+1)/2',
      'R1: x + (lambda+1)/2 + lambda = 3', ' => x = -3lambda/2 + 5/2',
      'ANS: (x,y,z) = (-3lambda/2+5/2,(lambda+1)/2,lambda)'], ['(lambda)']),
    ('linsys', ['x+y+z=3', '2x+2y+2z=6', '3x+3y+3z=9'],
     ['y = lambda', 'z = mu', 'R1: x + lambda + mu = 3', 'ANS: (x,y,z) = (3-lambda-mu,lambda,mu)']),
    # two planes: z = l, y = (l-2)/2, x = (4-3l)/2
    ('linsys', ['x+y+z=1', 'x-y+2z=3', ''], ['Infinitely many solutions', 'ANS: (x,y,z) = (-3lambda/2+2,lambda/2-1,lambda)']),
    # parameter: last row [0 0 k-7 | -10] ; det = k - 7
    ('linsys', ['x+2y+z=3', '2x-y+kz=1', 'x+y+2z=4'],
     ['[0  0 k-7 | -10]', 'ANS: unique solution if k != 7', 'ANS: x = (5k-5)/(k-7)',
      'ANS: z = -10/(k-7)', 'k = 7:', 'R3: 0 = -10 (inconsistent)', 'ANS: no solution'], ['Unique iff', '-- k']),
    # det = -(k-1)^2(k+2): k = 1 infinite, k = -2 none, else x = y = z = 1/(k+2)
    ('linsys', ['x+y+kz=1', 'x+ky+z=1', 'kx+y+z=1'],
     ['R3 -> R3 - kR1', 'Unique iff k-1 != 0, -k^2-k+2 != 0', 'ANS: unique solution if k != 1, k != -2',
      'ANS: x = 1/(k+2)', 'k = 1:', 'ANS: (x,y,z) = (1-lambda-mu,lambda,mu)', 'k = -2:', 'R3: 0 = 3 (inconsistent)',
      'ANS: no solution'], ['(k)R1', '-- k']),
    # [0 0 a-7 | b-7]: a = 7, b = 7 -> (l-1, 2-2l, l)
    ('linsys', ['x+y+z=1', 'x+2y+3z=3', 'x+4y+az=b'],
     ['[0 0 a-7 | b-7]', 'ANS: unique solution if a != 7', 'a = 7:', 'Consistent iff b-7 = 0',
      'ANS: b != 7: no solution', 'ANS: (x,y,z) = (lambda-1,2-2lambda,lambda)']),
    ('linsys', ['xy=1', 'x+y=2', ''], ['Not linear'], ['ANS:']),
    # negative symbolic multiplier: R3 -> R3 + kR1 ; det = k + 1
    ('linsys', ['x+y+z=1', 'x+2y+z=2', '-kx+y+z=0'],
     ['R3 -> R3 + kR1', 'R3 -> R3 - (k + 1)R2', 'ANS: unique solution if k != -1', 'ANS: x = 1/(k+1)',
      'ANS: y = 1', 'ANS: z = -1/(k+1)', 'k = -1:', 'R3: 0 = -1 (inconsistent)', 'ANS: no solution'],
     ['(-k)R1']),
    ('linsys', ['x+y=2', '2x+2y=4', ''], ['Infinitely many solutions', 'y = lambda', 'ANS: (x,y) = (2-lambda,lambda)']),
    # 0^n is undefined for n <= 0, 0 only for n > 0
    ('demoivre', ['0', '0'], ['undefined for z = 0, n <= 0'], ['ANS:']),
    ('demoivre', ['0', '-2'], ['undefined for z = 0, n <= 0'], ['ANS:']),
    ('demoivre', ['0', '3'], ['ANS: z^3 = 0'], ['undefined']),
]
