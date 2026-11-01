# Hand-checked cases for calc/ibalg2.py (exp/log equations, binomial, partial fractions)
MODULE = 'ibalg2'
CASES = [
    # --- exp/log equations
    # 2^(x+1) = 2^(3x) -> x+1 = 3x -> x = 1/2
    ('explog', ['2^(x+1)=8^x'], ['2^(x+1)=8^x', '2^(x+1) = 2^(3x)', 'x + 1 = 3x', 'ANS: x = 1/2'],
     ['Same base', 'Equation in x: 2^']),
    # x ln3 = ln10 -> x = 2.096
    ('explog', ['3^x=10'], ['ln(3)x = ln(10)  (take ln)', 'ANS: x = ln(10)/ln(3)', '~ 2.10'], ['Take ln of both sides']),
    # u^2-5u+6 = 0 -> u = 2, 3
    ('explog', ['e^(2x)-5e^x+6=0'], ['Let u = e^x', 'u^2 - 5u + 6 = 0', 'e^x = 2', 'ANS: x = ln(2)', 'ANS: x = ln(3)'],
     ['=> x = ln']),
    # u^2-6u+8 = 0 -> 2^x = 2, 4
    ('explog', ['4^x-3*2^(x+1)+8=0'], ['Let u = 2^x', 'u^2 - 6u + 8 = 0', '2^x = 4', 'ANS: x = 1', 'ANS: x = 2']),
    # 2u^2-5u+2 = 0 -> u = 1/2, 2 -> x = -1, 1
    ('explog', ['2^(2x+1)-5*2^x+2=0'], ['2u^2 - 5u + 2 = 0', '2^x = 1/2', 'ANS: x = -1', 'ANS: x = 1']),
    # u - 6/u = 1 -> u^2-u-6 = 0 -> u = 3 (u = -2 rejected)
    ('explog', ['e^x-6e^(-x)=1'], ['u^2 - u - 6 = 0', 'u = -2 rejected', 'ANS: x = ln(3)']),
    # x(x-2) = 8 -> x = 4 (x = -2 rejected)
    ('explog', ['log_2(x)+log_2(x-2)=3'],
     ['log_2(x(x-2)) = 3  (log laws)', 'x(x-2) = 2^3 = 8', 'x^2 - 2x - 8 = 0', 'x = -2 rejected', 'ANS: x = 4']),
    ('explog', ['ln(x)+ln(x+2)=ln(8)'], ['ln(x(x+2)) = ln(8)', 'x(x+2) = 8', 'ANS: x = 2'], ['ANS: x = -4']),
    # log_9(x+6) = log_3(x+6)/2 -> x^2 = x+6 -> x = 3 (x = -2 rejected)
    ('explog', ['log_3(x)=log_9(x+6)'],
     ['log_9(x+6) = log_3(x+6)/2', '(change of base)', '2log_3(x) - log_3(x+6) = 0', 'log_3(x^2) - log_3(x+6) = 0  (power law)',
      'x^2 - x - 6 = 0', 'ANS: x = 3'], ['ANS: x = -2', 'Multiply by', 'log_3(9)']),
    # (2x-1)ln5 = x ln3 -> x = ln5/ln(25/3) = 0.759
    ('explog', ['5^(2x-1)=3^x'], ['ln(5)(2x-1) = ln(3)x', 'ln(25/3)x = ln(5)', 'ANS: x = ln(5)/ln(25/3)', '~ 0.759']),
    # x/(x-1) = 10 -> x = 10/9
    ('explog', ['log(x)-log(x-1)=1'], ['log(x/(x-1)) = 1', 'x/(x-1) = 10', 'ANS: x = 10/9']),
    # (x-1)(x+1) = x^2 -> -1 = 0
    ('explog', ['ln(x-1)+ln(x+1)=2ln(x)'], ['(power law)', 'No valid solution'], ['ANS:']),
    # 3 log_2(x) = 3 -> x = 4
    ('explog', ['log_2(x)+log_4(x)=3'], ['log_2(x^3) = 6', 'x^3 = 2^6 = 64', 'ANS: x = 4'], ['x^3 - 64 = 0']),
    # 2x ln3 = ln5 -> x = ln5/(2ln3) = 0.732 (denominator must stay bracketed)
    ('explog', ['3^(2x)=5'], ['2ln(3)x = ln(5)', 'ANS: x = ln(5)/(2ln(3))', '~ 0.732'], ['ln(5)/2ln(3)']),
    # ln((2x+1)/x) = 1 -> 2x+1 = ex -> x = 1/(e-2)
    ('explog', ['ln(2x+1)=ln(x)+1'], ['(2x+1)/x = e', 'ANS: x = 1/(e-2)', '~ 1.39']),
    # given line not repeated, x = e^2 only once (ANS)
    ('explog', ['ln(x)=2'], ['ANS: x = e^2', '~ 7.39'], ['ln(x)=2\nln(x)=2', 'x=e^2\nANS']),
    ('explog', ['ln(x)+3=5'], ['ln(x) = 2', 'ANS: x = e^2'], ['x=e^2\nANS']),
    # 2ln x = 4 -> x^2 = e^4 -> x = e^2 (x = -e^2 rejected)
    ('explog', ['2ln(x)=4'], ['ln(x^2) = 4  (power law)', 'x^2 = e^4', 'ANS: x = e^2'],
     ['ANS: x = -e^2', '(power law)\nln(x^2)', 'x^2 - e^4 = 0']),
    ('explog', ['e^x=-2'], ['No solution: a^x > 0'], ['ANS:']),
    # equate the log arguments: x = 2x - 1
    ('explog', ['ln(x)=ln(2x-1)'], ['x = 2x-1', 'ANS: x = 1']),
    ('explog', ['log(x)=log(2x-1)'], ['x = 2x-1', 'ANS: x = 1']),
    # exponential form before its value
    ('explog', ['log(x)=2'], ['x = 10^2', 'ANS: x = 100']),
    ('explog', ['log_2(x)=5'], ['x = 2^5', 'ANS: x = 32']),
    # a = 1: no 'x = ln(3)' line before the ANS; e^x = 1: x = ln(1) = 0
    ('explog', ['e^(2x)=3e^x'], ['2x = ln(3) + x  (take ln)', 'ANS: x = ln(3)'], ['x=ln(3)\nANS']),
    ('explog', ['e^(x+1)=e^(2x)'], ['x + 1 = 2x', 'ANS: x = 1'], ['-x = -1']),
    ('explog', ['e^x=1'], ['x = ln(1)', 'ANS: x = 0'], ['x=0(takeln)']),
    ('explog', ['e^x=2'], ['ANS: x = ln(2)'], ['x=ln(2)(takeln)']),
    # same base: 3^(x+2) = 3^3 (no brackets on a plain number)
    ('explog', ['3^(x+2)=27'], ['3^(x+2) = 3^3', 'x + 2 = 3', 'ANS: x = 1'], ['3^(3)']),
    ('explog', ['4^x=8'], ['2^(2x) = 2^3', 'ANS: x = 3/2']),
    # log on the right: swap sides, x = e^3
    ('explog', ['3=ln(x)'], ['ANS: x = e^3'], ['ln(1/x)', '1/x']),
    # divide by 3 first, as a student does (no ln(3) + ln(2)x)
    ('explog', ['3*2^x=48'], ['3*2^x = 48', '2^x = 16', 'ANS: x = 4'], ['3*2^x=48\n3*2^x', 'ln(3)', 'x = 4\nANS']),
    ('explog', ['2e^x=10'], ['e^x = 5', 'ANS: x = ln(5)', '~ 1.61'], ['ln(2)', 'take ln']),
    ('explog', ['5*3^x=20'], ['3^x = 4', 'ln(3)x = ln(4)  (take ln)', 'ANS: x = ln(4)/ln(3)']),
    # was complex garbage (-i pi + ln 3)/ln 3
    ('explog', ['-2*3^x=6'], ['3^x = -3', 'No solution: a^x > 0'], ['ANS:', 'pi']),
    # 2^x = x+3: GDC roots -2.86, 2.44
    ('explog', ['2^x=x+3'], ['ANS: x = -2.86 (GDC)', 'ANS: x = 2.44 (GDC)'], ['Solve (GDC):']),
    # --- binomial, natural n: 16x^4+96x^3+216x^2+216x+81
    # powers 0 and 1 are not written
    ('binom', ['(2x+3)^4', ''], ['T(r+1) = 4Cr (2x)^(4-r) 3^r', 'Power of x: 4 - r', '4C0 (2x)^4 = 16x^4',
                                 '4C1 (2x)^3 3 = 96x^3', '4C2 (2x)^2 3^2 = 216x^2', '4C3 (2x) 3^3 = 216x',
                                 '4C4 3^4 = 81', 'ANS: 16x^4 + 96x^3 + 216x^2 + 216x + 81'],
     ['nCr a^(n-r)', '-r + 4', '3^0', '3^1', '(2x)^1', '(2x)^0']),
    # 6-2r = 0 -> r = 3: 20 x^3 (-2/x)^3 = -160
    ('binom', ['(x-2/x)^6', '0'], ['T(r+1) = 6Cr x^(6-r) (-2/x)^r', 'Power of x: 6 - 2r', '6 - 2r = 0 => r = 3',
                                   'T4 = 6C3 x^3 (-2/x)^3', 'ANS: constant term = -160'],
     ['= -160\nANS', '-2r + 6', '(x)^', 'coeff of x^0']),
    # 18-3r = 6 -> r = 4: 9C4 = 126
    ('binom', ['(x^2+1/x)^9', '6'], ['18 - 3r = 6 => r = 4', '= 126x^6', 'ANS: coeff of x^6 = 126']),
    # 10-3r = 7 -> r = 1: 5(x^8)(-3/x) = -15x^7
    ('binom', ['(x^2-3/x)^5', '7'], ['10 - 3r = 7 => r = 1', 'T2 = 5C1 (x^2)^4 (-3/x)', ' = -15x^7',
                                     'ANS: coeff of x^7 = -15'], ['(-3/x)^1']),
    # 5C2 (2x)^3 (-1)^2 = 80x^3
    ('binom', ['(2x-1)^5', '3'], ['5 - r = 3 => r = 2', 'T3 = 5C2(2x)^3(-1)^2', 'ANS: coeff of x^3 = 80']),
    # 3-r = 5 -> r = -2: no term
    ('binom', ['(x+2)^3', '5'], ['3 - r = 5', 'no x^5 term', 'ANS: coeff = 0']),
    # a = 1: no 1^(7-r) factor; 7C3 2^3 = 280
    ('binom', ['(1+2x)^7', '3'], ['T(r+1) = 7Cr (2x)^r', 'T4 = 7C3 (2x)^3', 'ANS: coeff of x^3 = 280'], ['(1)^', '1^']),
    # --- binomial, rational n
    ('binom', ['(1+x)^(-1)', '4'], ['(-1)x = -x', '(-1)(-2)/2! x^2 = x^2', '(-1)(-2)(-3)/3! x^3 = -x^3',
                                    'ANS: 1 - x + x^2 - x^3 + ...', '-1 < x < 1'],
     ['(1+y)^n', 'Terms: 4', '(x)']),
    # 2(1-x/4)^(1/2) = 2 - x/4 - x^2/64
    ('binom', ['(4-x)^(1/2)', '3'],
     ['= 2(1 - x/4)^(1/2)', '(1/2)(-1/2)/2! (-x/4)^2 = -x^2/128', '= 2(1 - x/8 - x^2/128 + ...)',
      'ANS: 2 - x/4 - x^2/64 + ...', 'Valid for |x/4| < 1', '-4 < x < 4'], ['Multiply by']),
    # (1/4)(1+3x/2)^(-2) = 1/4 - 3x/4 + 27x^2/16
    ('binom', ['(2+3x)^(-2)', '3'], ['= (1/4)(1 + 3x/2)^(-2)', '= (1/4)(1 - 3x + 27x^2/4 + ...)',
                                     'ANS: 1/4 - 3x/4 + 27x^2/16 + ...', '-2/3 < x < 2/3'], ['3*x']),
    # (1/3)(-2/3)(-5/3)/6 (-2x)^3 = -40x^3/81
    ('binom', ['(1-2x)^(1/3)', '4'], ['ANS: 1 - 2x/3 - 4x^2/9 - 40x^3/81 + ...', '-1/2 < x < 1/2']),
    # 1/(x-2) = -1/2 (1-x/2)^(-1) = -1/2 - x/4 - x^2/8
    ('binom', ['(x-2)^(-1)', '3'], ['= (-1/2)(1 - x/2)^(-1)', '= (-1/2)(1 + x/2 + x^2/4 + ...)',
                                    'ANS: -1/2 - x/4 - x^2/8 + ...', '-2 < x < 2']),
    ('binom', ['(1+x+x^2)^3'], ['Enter as (a+b)^n'], ['ANS:']),
    ('binom', ['(x+y)^(1/2)'], ['Need (a + bx)^n'], ['ANS:']),
    # sqrt(2)(1 + x/2)^(1/2) = sqrt(2) + sqrt(2)x/4 - sqrt(2)x^2/32
    ('binom', ['(2+x)^(1/2)', '3'], ['= sqrt(2)(1 + x/2)^(1/2)', 'ANS: sqrt(2) + sqrt(2)x/4 - sqrt(2)x^2/32 + ...',
                                     '-2 < x < 2'], ['(sqrt(2))']),
    # --- partial fractions (cover-up): 3x+5 = A(x+3) + B(x+1)
    ('parfrac', ['(3x+5)/((x+1)(x+3))'],
     ['f(x) = (3x+5)/((x+1)(x+3))\n = A/(x+1) + B/(x+3)', '3x + 5 = A(x+3) + B(x+1)', 'x = -1: 2 = 2A, A = 1',
      'x = -3: -4 = -2B, B = 2', 'ANS: f(x) = 1/(x+1) + 2/(x+3)'],
     ['Decompose', 'cover-up', 'Cover-up', 'Denominator', '(3x + 5)/((x+1)(x+3)) =']),
    ('parfrac', ['1/(x^2-1)'],
     ['x^2-1 = (x-1)(x+1)', 'f(x) = A/(x-1) + B/(x+1)', 'A = 1/2', 'B = -1/2',
      'ANS: f(x) = 1/(2(x-1)) - 1/(2(x+1))']),
    # 5x-1 = A(2x-1) + B(x+1): A = 2, B = 1
    ('parfrac', ['(5x-1)/(2x^2+x-1)'],
     ['2x^2+x-1 = (x+1)(2x-1)', 'x = 1/2: 3/2 = (3/2)B, B = 1', 'ANS: f(x) = 2/(x+1) + 1/(2x-1)']),
    # improper: 1 + 2/(x^2-1) = 1 + 1/(x-1) - 1/(x+1)
    ('parfrac', ['(x^2+1)/(x^2-1)'],
     ['f(x) = 1 + 2/(x^2-1)', '= 1 + A/(x-1) + B/(x+1)', '2 = A(x+1) + B(x-1)',
      'ANS: f(x) = 1 + 1/(x-1) - 1/(x+1)'], ['Improper: divide']),
    # A = 4/(-7/2) = -8/7, B = 4/(7/3) = 12/7
    ('parfrac', ['4/(6x^2-x-2)'],
     ['6x^2-x-2 = (2x+1)(3x-2)', 'x = -1/2: 4 = (-7/2)A, A = -8/7', 'B = 12/7',
      'ANS: f(x) = -8/(7(2x+1)) + 12/(7(3x-2))']),
    # 3/(2(x-1)(x+1)): A = 3/4, B = -3/4
    ('parfrac', ['3/(2x^2-2)'], ['2x^2-2 = 2(x-1)(x+1)', '3/2 = A(x+1) + B(x-1)',
                                 'ANS: f(x) = 3/(4(x-1)) - 3/(4(x+1))']),
    # typed denominator factored: 1-x^2 = -(x-1)(x+1), so the numerator becomes -1
    ('parfrac', ['1/(1-x^2)'], ['1-x^2 = -(x-1)(x+1)', 'f(x) = -1/((x-1)(x+1))', '-1 = A(x+1) + B(x-1)',
                                'ANS: f(x) = -1/(2(x-1)) + 1/(2(x+1))'], ['x^2-1 = (x-1)(x+1)']),
    ('parfrac', ['2x/(4-x^2)'], ['4-x^2 = -(x-2)(x+2)', '-2x = A(x+2) + B(x-2)', 'ANS: f(x) = -1/(x-2) - 1/(x+2)'],
     ['x^2-4 =']),
    # coefficient 1 after substituting: x = -1: A = 2 (not '2 = A, A = 2')
    ('parfrac', ['(1-x)/(x^2+3x+2)'], ['1 - x = A(x+2) + B(x+1)', 'x = -1: A = 2', 'x = -2: 3 = -B, B = -3',
                                       'ANS: f(x) = 2/(x+1) - 3/(x+2)'], ['2 = A,']),
    ('parfrac', ['(2x+1)/(x(x-2))'], ['= A/x + B/(x-2)', '2x + 1 = A(x-2) + Bx', 'ANS: f(x) = -1/(2x) + 5/(2(x-2))']),
    # typed factors keep their order: no '(2x-1)(x+3) = (x+3)(2x-1)' line
    ('parfrac', ['(4x+1)/((2x-1)(x+3))'],
     ['= A/(2x-1) + B/(x+3)', '4x + 1 = A(x+3) + B(2x-1)', 'x = 1/2: 3 = (7/2)A, A = 6/7', 'x = -3: -11 = -7B, B = 11/7',
      'ANS: f(x) = 6/(7(2x-1)) + 11/(7(x+3))'], ['(x+3)(2x-1)']),
    ('parfrac', ['x/((x-1)(x-2))'], ['= A/(x-1) + B/(x-2)', 'x = 1: 1 = -A, A = -1', 'x = 2: B = 2',
                                     'ANS: f(x) = -1/(x-1) + 2/(x-2)'], ['(x-2)(x-1)']),
    # cancels down: a single answer, no 'out of scope'
    ('parfrac', ['(x+1)/(x^2-1)'], ['x^2-1 = (x-1)(x+1)', 'ANS: f(x) = 1/(x-1)'], ['Out of scope', 'Not 2', 'f(x) = 1/(x-1)\nANS']),
    ('parfrac', ['(x^3+1)/(x^2-1)'], ['ANS: f(x) = x + 1/(x-1)'], ['Out of scope', 'Not 2']),
    ('parfrac', ['(2x+3)/(x(x+1)(x+2))'], ['ANS: f(x) = 3/(2x) - 1/(x+1) - 1/(2(x+2))'], ['Out of scope']),
    # not two distinct linear factors: one short note, no ANS that only repeats the input
    ('parfrac', ['1/(x+1)^2'], ['Not 2 distinct linear factors'], ['Out of scope', 'cover-up', 'A/', 'ANS:']),
    ('parfrac', ['1/(x^2+1)'], ['Not 2 distinct linear factors'], ['Out of scope', 'cover-up', 'A/', 'ANS:']),
    # space before the log argument / unbracketed argument must still parse as logb
    ('explog', ['log_2 (x)+log_2 (x-2)=3'], ['log_2(x(x-2)) = 3  (log laws)', 'x(x-2) = 2^3 = 8', 'ANS: x = 4']),
    ('explog', ['log_2 x+log_2 (x-2)=3'], ['log_2(x(x-2)) = 3  (log laws)', 'ANS: x = 4']),
    # a^x = 0 has no solution (RHS exactly 0 must be caught, not only negative)
    ('explog', ['2^x=0'], ['No solution: a^x > 0'], ['ANS:']),
]
