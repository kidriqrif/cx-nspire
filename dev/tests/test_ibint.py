MODULE = 'ibint'
CASES = [
    # power rule shown as 3x^3/3 = x^3 (no (3)x^(3)/(3), no narration)
    ('integ', ['3x^2 + 4x - 5', '', ''], ['int 3x^2 dx = 3x^3/3 = x^3', 'int 4x dx = 4x^2/2 = 2x^2', 'ANS:',
                                           'x^3 + 2x^2 - 5x + C'], ['term by term', 'x^(3)', '(3)x', 'Variable: x']),
    ('integ', ['cos(2x) + e^(3x)', '', ''], ['int cos(2x) dx = sin(2x)/2', 'int e^(3x) dx = e^(3x)/3', '+ C'],
     ['divide by']),
    ('integ', ['1/x + 1/(2x+1)', '', ''], ['int 1/x dx = ln|x|', 'ln|2x+1|', '+ C'], ['ln|x|\n = ln|x|']),
    ('integ', ['x*e^(x^2)', '', ''], ['reverse chain', 'u = x^2, du = 2x dx', '= (1/2)int e^u du', '= (1/2)e^u',
                                      'ANS: int f dx = e^(x^2)/2 + C'], ['let u']),
    ('integ', ['x/(x^2+1)', '', ''], ['reverse chain', '(1/2)ln|u|', 'ln(x^2+1)/2']),
    ('integ', ['sin(x)*cos(x)^3', '', ''], ['reverse chain', '= -int u^3 du', '= -u^4/4', '-cos(x)^4/4 + C'], ['(-1)']),
    ('integ', ['x^2', '', '0', '3'], ['[x^3/3] from 0 to 3', '= 9 - 0', 'ANS: Integral = 9'], ['(9) - (0)']),
    ('integ', ['1/(1+x^2)', '', '0', '1'], ['arctan', 'ANS: Integral = pi/4']),
    ('integ', ['e^(x^2)', ''], ['no elementary antiderivative']),
    # substitution as a student writes it; back-substituted result once (ANS)
    ('subst_u', ['x*(x^2+1)^3', 'x^2+1', ''],
     ['u = x^2 + 1', 'du/dx = 2x so dx = du/(2x)', 'int x(x^2+1)^3 dx = int (1/2)u^3 du', '= u^4/8 + C',
      'ANS: int f dx = (x^2+1)^4/8 + C'], ['u = x^2+1:', 'Let u = x^2+1']),
    ('subst_u', ['x*sqrt(x^2+1)', 'x^2+1', '0', '1'],
     ['x = 0 -> u = 1, x = 1 -> u = 2', 'int (1/2)sqrt(u) du', 'ANS: Integral = 2sqrt(2)/3-1/3'], ['(2sqrt(2)/3) - (1/3)']),
    # by parts: student layout, no program narration
    ('parts', ['x*e^x', '', ''],
     ['u = x, dv/dx = e^x', 'du/dx = 1, v = e^x', 'int xe^x dx = xe^x - int e^x dx', 'ANS: int f dx = xe^x - e^x + C'],
     ['Apply Formula', 'LIATE', 'Parts 1', 'u*v is', 'Remaining', 'dv/dx (enter=accept): ']),
    ('parts', ['x^2*e^x', '', ''],
     ['int x^2 e^x dx = x^2 e^x - int 2xe^x dx', 'u = 2x, dv/dx = e^x', 'int 2xe^x dx = 2xe^x - int 2e^x dx',
      'I = x^2 e^x - 2xe^x + int 2e^x dx', 'ANS: int f dx = x^2 e^x - 2xe^x + 2e^x + C'], ['Parts 2']),
    ('parts', ['ln(x)', '', '1', 'e'], ['u = ln(x)', 'int ln(x) dx = x ln(x) - int 1 dx', '= 0 - (-1)', 'ANS: Integral = 1']),
    ('parts', ['e^x*sin(x)', '', ''],
     ['int e^x cos(x) dx = e^x cos(x) + I', 'I = e^x sin(x) - e^x cos(x) - I', '2I = e^x sin(x) - e^x cos(x)',
      'ANS: int f dx = (e^x sin(x)-e^x cos(x))/2 + C'], ['reappears', '(2)I', '(-1)I', '- int e^x sin(x) dx']),
    # sin^2(x) in the I lines as well (not sin(x)^2)
    ('parts', ['sin(x)*cos(x)', '', ''], ['int sin(x)cos(x) dx = sin^2(x) - I', 'I = sin^2(x) - I', '2I = sin^2(x)',
                                          'ANS: int f dx = sin(x)^2/2 + C'], ['I = sin(x)^2']),
    ('parts', ['x*sin(x)', '', '0', 'pi'], ['int x sin(x) dx = -x cos(x) + int cos(x) dx', 'ANS: Integral = pi'],
     ['- int -cos']),
    ('parts', ['x*cos(x)', 'cos(x)', ''], ['u = x', 'x sin(x) + cos(x) + C']),
    ('pfrac', ['(3x+5)/((x+1)(x+3))', ''],
     ['f(x) = (3x+5)/((x+1)(x+3))', '= A/(x+1) + B/(x+3)', '3x + 5 = A(x+3) + B(x+1)', 'x = -1: 2 = 2A, A = 1',
      'x = -3: -4 = -2B, B = 2', 'f(x) = 1/(x+1) + 2/(x+3)', 'ln|x+1| + 2ln|x+3| + C'],
     ['Decompose', 'Cover-up', 'cover-up', '(2)A', 'Denominator']),
    ('pfrac', ['1/(x^2-1)', '2', '3'], ['x^2-1 = (x-1)(x+1)', 'f(x) = A/(x-1) + B/(x+1)', '= -ln(2)/2 - (-ln(3)/2)',
                                        'ANS: Integral = ln(3/2)/2']),
    ('trigpow', ['sin(x)^2', ''], ['== Trig powers ==', 'sin^2(x) = 1/2 - cos(2x)/2', 'x/2 - sin(2x)/4 + C'],
     ['identities', 'divide by', 'u = 2x']),
    ('trigpow', ['cos(x)^2', '0', 'pi'], ['cos^2(x) = 1/2 + cos(2x)/2', 'ANS: Integral = pi/2']),
    # regression: exam-style cases (answers verified by differentiating back)
    ('trigpow', ['tan(x)^2', ''], ['tan^2(x) = sec^2(x) - 1', 'ANS:', 'tan(x) - x + C'], ['Use ']),
    ('trigpow', ['tan(2x)^2', '0', 'pi/8'], ['tan^2(2x) = sec^2(2x) - 1', 'ANS: Integral = 1/2-pi/8']),
    ('trigpow', ['cos(3x)^2', ''], ['cos^2(3x) = 1/2 + cos(6x)/2', 'x/2 + sin(6x)/12 + C']),
    # sin^3 x = 3sin(x)/4 - sin(3x)/4
    ('trigpow', ['sin(x)^3', ''], ['sin^3(x) = 3sin(x)/4 - sin(3x)/4', 'ANS: int f dx = -3cos(x)/4 + cos(3x)/12 + C']),
    # the default offered is the dv actually used (re-split before the prompt)
    ('parts', ['x^3*e^(x^2)', '', ''], ['dv/dx (enter=accept) [xe^(x^2)]', 'u = x^2, dv/dx = xe^(x^2)', 'v = e^(x^2)/2',
                                        '= e^(x^2)/2', 'x^2 e^(x^2)/2 - e^(x^2)/2 + C'], ['v not elementary']),
    # dv/dx override: same split, entered by hand
    ('parts', ['x^3*e^(x^2)', 'x*e^(x^2)', ''], ['u = x^2, dv/dx = xe^(x^2)', 'x^2 e^(x^2)/2 - e^(x^2)/2 + C']),
    ('parts', ['arctan(x)', '', '0', '1'], ['reverse chain', 'ANS: Integral = pi/4-ln(2)/2'], ['reappears']),
    ('parts', ['e^x*cos(x)', '', ''],
     ['int e^x cos(x) dx = e^x cos(x) + int e^x sin(x) dx', 'int e^x sin(x) dx = e^x sin(x) - I',
      'I = e^x cos(x) + e^x sin(x) - I', '2I = e^x cos(x) + e^x sin(x)',
      '(e^x cos(x)+e^x sin(x))/2 + C'], ['int -e^x', 'int cos(x)e^x dx\nI']),
    # [e^x(cos x + sin x)/2] from 0 to pi = -(e^pi + 1)/2
    ('parts', ['e^x*cos(x)', '', '0', 'pi'], ['ANS: Integral = -1/2-e^pi/2', '~ -12.1']),
    ('pfrac', ['(2x^2+3)/(x^2-1)', ''], ['f(x) = 2 + 5/(x^2-1)', '= 2 + A/(x-1) + B/(x+1)', 'A = 5/2', 'B = -5/2',
                                         '2x + 5ln|x-1|/2 - 5ln|x+1|/2 + C'], ['Divide:']),
    ('pfrac', ['(x+5)/(x^2+x-2)', ''], ['x = 1: 6 = 3A, A = 2', 'x = -2: 3 = -3B, B = -1', '2ln|x-1| - ln|x+2| + C']),
    # 3/(2(x-1)(x+1)): 3 = 2(A(x+1) + B(x-1)), A = 3/4, B = -3/4
    ('pfrac', ['3/(2x^2-2)', ''], ['2x^2-2 = 2(x-1)(x+1)', '3/2 = A(x+1) + B(x-1)', 'x = 1: 3/2 = 2A, A = 3/4',
                                   'ANS: int f dx = 3ln|x-1|/4 - 3ln|x+1|/4 + C'], ['3 = 2(A']),
    ('integ', ['sec(x)^2 + 1/sqrt(1-x^2) + 3/(4+x^2)', '', ''], ['tan(x) + arcsin(x) + 3arctan(x/2)/2 + C']),
    ('integ', ['e^-x + x^(-1/2) + sin(3x+1)', '', ''], ['x^(1/2)/(1/2) = 2sqrt(x)', '-e^(-x) + 2sqrt(x) - cos(3x+1)/3 + C']),
    ('integ', ['x*ln(x)', '', ''], ['I = int x ln(x) dx  (by parts)', 'int x ln(x) dx = x^2 ln(x)/2 - int x/2 dx',
                                    'x^2 ln(x)/2 - x^2/4 + C']),
    # I is defined in the integrate route too, and the cyclic step shows it
    ('integ', ['e^x*sin(x)', '', ''], ['I = int e^x sin(x) dx  (by parts)', 'int e^x cos(x) dx = e^x cos(x) + I',
                                       '2I = e^x sin(x) - e^x cos(x)', 'ANS: int f dx = (e^x sin(x)-e^x cos(x))/2 + C']),
    # x e^(2x) by parts + 3x^(-2) by power rule
    ('integ', ['x*e^(2x) + 3/x^2', '', ''], ['= xe^(2x)/2 - e^(2x)/4', '3/x^2 = 3x^(-2)',
                                             'int 3x^(-2) dx = 3x^(-1)/(-1) = -3/x',
                                             'ANS: int f dx = xe^(2x)/2 - e^(2x)/4 - 3/x + C']),
    ('subst_u', ['cos(x)*sin(x)^4', 'sin(x)', '0', 'pi/2'], ['dx = du/cos(x)', 'int u^4 du', 'ANS: Integral = 1/5']),
    # back-substituted without Giac's regrouping: (2/3)u^(3/2) - 2u^(1/2)
    ('subst_u', ['x/sqrt(x+1)', 'x+1', ''], ['so dx = du', '(u-1)/sqrt(u)', '= 2u^(3/2)/3 - 2sqrt(u) + C',
                                             'ANS: int f dx = 2(x+1)^(3/2)/3 - 2sqrt(x+1) + C'],
     ['4sqrt', 'sqrt(x+1)(x+1)', 'sqrt((x+1))']),
    ('subst_u', ['2x*sqrt(x^2-3)', 'x^2-3', ''], ['du/dx = 2x so dx = du/(2x)', 'int sqrt(u) du',
                                                  'ANS: int f dx = 2(x^2-3)^(3/2)/3 + C'], ['sqrt(x^2-3)(x^2-3)']),
    # du/dx = sec^2(x), not 1 + tan^2(x)
    ('subst_u', ['sec(x)^2*tan(x)', 'tan(x)', ''],
     ['du/dx = sec^2(x) so dx = du/sec^2(x)', 'int sec^2(x) tan(x) dx = int u du', 'ANS: int f dx = tan(x)^2/2 + C'],
     ['1+tan']),
    ('subst_u', ['e^x/(1+e^x)', '1+e^x', ''], ['du/dx = e^x so dx = du/e^x', 'int 1/u du', 'ANS: int f dx = ln|1+e^x| + C']),
    # regression: 1/(x^2+1) is not x^(-2) (old _vpow read x^2+1 as x^(2+1))
    ('integ', ['1/(x^2+1)', '', ''], ['ANS: int f dx = arctan(x) + C'], ['x^(-2)', 'power']),
    ('integ', ['2/(x^2+4)', '', ''], ['ANS: int f dx = arctan(x/2) + C'], ['x^(-5)']),
    # x sqrt(x) = x^(3/2): power rule, not cyclic by parts
    ('integ', ['x*sqrt(x)', '', ''], ['= x^(3/2)', 'int x^(3/2) dx = x^(5/2)/(5/2)', 'ANS: int f dx = 2x^(5/2)/5 + C'],
     ['by parts', 'xx', '2I']),
    ('integ', ['x*sqrt(x)', '', '0', '4'], ['[2x^(5/2)/5] from 0 to 4', 'ANS: Integral = 64/5']),
    ('integ', ['x^(2/3)', '', ''], ['ANS: int f dx = 3x^(5/3)/5 + C'], ['(x^(1/3))^2']),
    # the index rewrite is shown before the power rule
    ('integ', ['sqrt(x)/x^3', '', ''], ['f(x) = sqrt(x)/x^3', '= x^(-5/2)', 'int x^(-5/2) dx = x^(-3/2)/(-3/2)',
                                        'ANS: int f dx = -2/(3x^(3/2)) + C']),
    ('integ', ['1/sqrt(x)', '', ''], ['= x^(-1/2)', 'int x^(-1/2) dx = x^(1/2)/(1/2)', 'ANS: int f dx = 2sqrt(x) + C']),
    ('integ', ['sqrt(x)', '', '0', '9'], ['= x^(1/2)', 'int x^(1/2) dx = x^(3/2)/(3/2)', 'ANS: Integral = 18']),
    ('integ', ['1/x^2', '', ''], ['= x^(-2)', 'int x^(-2) dx = x^(-1)/(-1)', 'ANS: int f dx = -1/x + C']),
    # a product of polynomials is expanded, not done by parts
    ('integ', ['x^2*(x+1)', '', ''], ['f(x) = x^2 (x+1)', '= x^3 + x^2', 'int x^3 dx = x^4/4', 'int x^2 dx = x^3/3',
                                      'ANS: int f dx = x^4/4 + x^3/3 + C'], ['by parts', 'u = x^2', 'x^3+2x^2']),
    ('integ', ['x*(2x+1)^3', '', ''], ['= 8x^4 + 12x^3 + 6x^2 + x', 'ANS: int f dx = 8x^5/5 + 3x^4 + 2x^3 + x^2/2 + C'],
     ['by parts']),
    # a power of a linear factor stays as it is
    ('integ', ['(2x+1)^3', '', ''], ['ANS: int f dx = (2x+1)^4/8 + C'], ['by parts', '8x^3']),
    # single quotient over a monomial: split first, x^2/2 + ln|x|
    ('integ', ['(x^2+1)/x', '', ''], ['= x + 1/x', 'int 1/x dx = ln|x|', 'ANS: int f dx = x^2/2 + ln|x| + C'],
     ['ln(x^2)']),
    ('integ', ['t^2-t', 't', ''], ['f(t) = t^2 - t', 'ANS: int f dt = t^3/3 - t^2/2 + C'], ['f(x) = t']),
    # remaining integral in by parts is evaluated (it is not the answer)
    ('parts', ['ln(x)/x^2', '', ''], ['= -ln(x)/x + int 1/x^2 dx', '1/x^2 = x^(-2)', 'int x^(-2) dx = x^(-1)/(-1) = -1/x',
                                      'ANS: int f dx = -ln(x)/x - 1/x + C'], ['(xx)']),
    ('parts', ['x^2*ln(x)', '', ''], ['int x^2/3 dx = (1/3)(x^3/3) = x^3/9', 'ANS: int f dx = x^3 ln(x)/3 - x^3/9 + C']),
    # the inner substitution uses w: u is the parts u
    ('parts', ['arcsin(x)', '', ''], ['= x arcsin(x) - int x/sqrt(-x^2+1) dx', 'w = -x^2 + 1, dw = -2x dx',
                                      '= (-1/2)int 1/sqrt(w) dw', '= -sqrt(-x^2+1)',
                                      'ANS: int f dx = x arcsin(x) + sqrt(-x^2+1) + C'],
     ['/(x^2-1)', 'sqrt(u)/u', 'u = -x^2']),
    # dv/dx = x overridden: the working goes in circles, so it is dropped and LIATE is used
    ('parts', ['x*e^x', 'x', ''], ['dv/dx = x: no progress', 'u = x, dv/dx = e^x', 'ANS: int f dx = xe^x - e^x + C'],
     ['I = 0', 'x^2 e^x/2', 'u = e^x']),
    # sec^2 x: v = tan x, then int tan x dx = -ln|cos x|
    ('parts', ['x*sec(x)^2', '', ''],
     ['dv/dx (enter=accept) [sec^2(x)]', 'I = int x sec^2(x) dx', 'u = x, dv/dx = sec^2(x)', 'du/dx = 1, v = tan(x)',
      'int x sec^2(x) dx = x tan(x) - int tan(x) dx', 'int tan(x) dx = -ln|cos(x)|',
      'ANS: int f dx = x tan(x) + ln|cos(x)| + C'], ['does not simplify', 'check failed', '1/cos']),
    # dx = x du (not du/(1/x)); dx = -du/sin(x)
    ('subst_u', ['ln(x)/x', 'ln(x)', '1', 'e'], ['du/dx = 1/x so dx = x du', '[u^2/2] from 0 to 1', 'ANS: Integral = 1/2'],
     ['du/(1/x)']),
    ('subst_u', ['sin(x)*cos(x)^2', 'cos(x)', ''], ['dx = -du/sin(x)', 'int -u^2 du', 'ANS: int f dx = -cos(x)^3/3 + C'],
     ['(-sin(x))']),
    # typed denominator factored: 1-x^2 = -(x-1)(x+1), numerator -1
    ('pfrac', ['1/(1-x^2)', ''], ['1-x^2 = -(x-1)(x+1)', 'f(x) = -1/((x-1)(x+1))', '-1 = A(x+1) + B(x-1)',
                                  'ANS: int f dx = -ln|x-1|/2 + ln|x+1|/2 + C'], ['x^2-1 =']),
    # coefficient 1: 'x = -1: A = 1'
    ('pfrac', ['1/(x^2+3x+2)', '0', '1'], ['x = -1: A = 1', 'x = -2: 1 = -B, B = -1', 'ANS: Integral = ln(4/3)'],
     ['1 = A,']),
    # sec x tan x: sec(x) + C (was 'Parts does not simplify', no answer)
    ('trigpow', ['sec(x)*tan(x)', ''], ['ANS: int f dx = sec(x) + C'], ['1/cos', 'Parts']),
    ('trigpow', ['2sec(x)*tan(x)', '0', 'pi/3'], ['[2sec(x)] from 0 to pi/3', 'ANS: Integral = 2']),
    ('trigpow', ['3tan(x)^2', '0', 'pi/4'], ['3tan^2(x) = 3sec^2(x) - 3', 'ANS: Integral = 3-3pi/4'], ['1/cos']),
    ('trigpow', ['tan(x)^2+1', ''], ['tan^2(x) + 1 = sec^2(x)', 'ANS: int f dx = tan(x) + C'], ['1/cos']),
    # 1/cos^2 x = sec^2 x (not the double-angle form)
    ('trigpow', ['1/cos(x)^2', ''], ['1/cos^2(x) = sec^2(x)', 'ANS: int f dx = tan(x) + C'], ['cos(2x)', '*']),
    ('trigpow', ['sec(x)^2', '0', 'pi/4'], ['f(x) = sec^2(x)', '[tan(x)] from 0 to pi/4', 'ANS: Integral = 1']),
    # partial fractions: typed factors keep their order; no syllabus narration; no repeated lines
    ('pfrac', ['(4x+1)/((2x-1)(x+3))', ''],
     ['= A/(2x-1) + B/(x+3)', '4x + 1 = A(x+3) + B(2x-1)', 'x = 1/2: 3 = (7/2)A, A = 6/7', 'x = -3: -11 = -7B, B = 11/7',
      'f(x) = 6/(7(2x-1)) + 11/(7(x+3))', 'ANS: int f dx = 3ln|2x-1|/7 + 11ln|x+3|/7 + C'], ['(x+3)(2x-1)']),
    ('pfrac', ['x/((x-1)(x-2))', ''], ['= A/(x-1) + B/(x-2)', 'x = 1: 1 = -A, A = -1', 'x = 2: B = 2'], ['(x-2)(x-1)']),
    ('pfrac', ['(x^3+1)/(x^2-1)', ''],
     ['x^2-1 = (x-1)(x+1)', 'f(x) = (x^2 - x + 1)/(x-1)', '= x + 1/(x-1)', 'ANS: int f dx = x^2/2 + ln|x-1| + C'],
     ['AA 1.11', 'f(x) = x + 1/(x-1)']),
    ('pfrac', ['1/(x+1)^2', ''], ['ANS: int f dx = -1/(x+1) + C'], ['AA 1.11', 'distinct']),
    ('pfrac', ['1/(x^2+1)', ''], ['ANS: int f dx = arctan(x) + C'], ['AA 1.11', 'distinct']),
    ('pfrac', ['(x+1)/(x^2-1)', ''], ['f(x) = 1/(x-1)', 'ANS: int f dx = ln|x-1| + C'], ['AA 1.11', 'A/']),
]
