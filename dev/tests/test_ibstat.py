# Tests for calc/ibstat.py (AA 4.1-4.4, 4.10). Expected values hand-checked.
MODULE = 'ibstat'
CASES = [
    # raw 2,4,4,5,7,9,10: Sx=41, mean 41/7; Sx^2=291, var=291/7-(41/7)^2=356/49,
    # sd=2sqrt(89)/7=2.695; Q1=4 (2nd), Q3=9 (6th), fences 4-7.5, 9+7.5
    ('data_summary', ['1', '2,4,4,5,7,9,10', '0'],
     ['n = 7', 'Sorted: 2,4,4,5,7,9,10', 'Sum x = 41', 'mean = 41/7 (5.86)',
      'median = 4th value = 5', 'Q1 = 2nd value = 4', 'Q3 = 6th value = 9',
      'IQR = Q3 - Q1 = 9 - 4 = 5', 'Q1 - 1.5(IQR) = 4 - 1.5(5) = -3.5',
      'Q3 + 1.5(IQR) = 9 + 1.5(5) = 16.5',
      'Outliers: none', 'Box: min 2, Q1 4, med 5, Q3 9, max 10', 'mode = 4',
      'Sum x^2 = 291', 'var = 291/7 - (41/7)^2 = 356/49 (7.27)',
      'ANS: mean = 41/7 (5.86)', 'ANS: sd = 2sqrt(89)/7 (2.70)', 'ANS: median = 5'],
     ['Whiskers', 'median of lower half', 'sd = sqrt(var)', 'grouped:1', 'x1,x2,..:2']),
    # even n, outlier 30 > 8+7.5; P30: 0.3*6 = 1.8 -> 2nd value
    ('data_summary', ['', '1,3,5,6,8,30', '30'],
     ['median = (3rd+4th)/2 = (5+6)/2 = 5.5', 'IQR = Q3 - Q1 = 8 - 3 = 5',
      'Q3 + 1.5(IQR) = 8 + 1.5(5) = 15.5', 'Outliers: 30', 'Whiskers: 1 to 8', 'mode = none',
      'P30: 0.3(6) = 1.8 -> 2nd value = 3', 'Sum x^2 = 1035', '3401/36',
      'ANS: mean = 53/6 (8.83)', 'ANS: sd = sqrt(3401)/6 (9.72)', 'ANS: median = 5.5'],
     ['position', 'skip):30']),
    # freq table: n=20, Sfx=53, Sfx^2=159, var=159/20-2.65^2=0.9275, sd=sqrt(371)/20
    ('data_summary', ['2', '1,2,3,4', '3,5,8,4', '50'],
     ['x = 1,2,3,4', 'f = 3,5,8,4', 'n = 20', 'Sum fx = 53', 'mean = 53/20 = 2.65',
      'median = (10th+11th)/2 = (3+3)/2 = 3', 'Q1 = (5th+6th)/2 = (2+2)/2 = 2',
      'Q3 = (15th+16th)/2 = (3+3)/2 = 3', 'IQR = Q3 - Q1 = 3 - 2 = 1', 'mode = 3',
      'P50: 0.5(20) = 10 -> (10th+11th)/2 = (3+3)/2 = 3', 'Sum fx^2 = 159',
      'var = 159/20 - (2.65)^2 = 0.9275', 'ANS: sd = sqrt(371)/20 (0.963)',
      'ANS: mean = 2.65'], ['Values x:1,2,3,4']),
    # grouped: mids 5,15,25; Sfm=360; median 10+(10-4)/6*10=20; Q1 35/3; Q3 25;
    # P90: t=18 -> 20+(18-10)/10*10=28; Sfm^2=7700, var=385-324=61
    ('data_summary', ['3', '0,10,20,30', '4,6,10', '90'],
     ['bounds = 0,10,20,30', 'f = 4,6,10', 'n = 20', 'Mid-points: 5,15,25', 'Sum fm = 360',
      'mean ~ 360/20 = 18',
      'Cum freq: 4,10,20', 'Modal class: 20-30', 'median ~ 10 + (10 - 4)/6 * 10 = 20',
      'Q1 ~ 10 + (5 - 4)/6 * 10 = 35/3 (11.7)', 'Q3 ~ 20 + (15 - 10)/10 * 10 = 25',
      'P90 ~ 20 + (18 - 10)/10 * 10 = 28', 'IQR ~ 40/3 (13.3)', 'Sum fm^2 = 7700',
      'var = 7700/20 - 18^2 = 61',
      'ANS: mean = 18', 'ANS: sd = sqrt(61) (7.81)', 'ANS: median = 20'],
     ['L + (t - CF)', 'sd = sqrt(var)']),
    # decimals: mean 8.5/4=2.125; var 19.75/4-2.125^2=27/64, sd=3sqrt(3)/8=0.650
    ('data_summary', ['1', '2.5,1.5,3,1.5', ''],
     ['Sorted: 1.5,1.5,2.5,3', 'mean = 8.5/4 = 2.125', 'median = (2nd+3rd)/2 = (1.5+2.5)/2 = 2',
      'Q1 = (1st+2nd)/2 = (1.5+1.5)/2 = 1.5', 'Q3 = (3rd+4th)/2 = (2.5+3)/2 = 2.75',
      'IQR = Q3 - Q1 = 2.75 - 1.5 = 1.25', 'Q1 - 1.5(IQR) = 1.5 - 1.5(1.25) = -0.375',
      'mode = 1.5', 'Sum x^2 = 19.75',
      'var = 19.75/4 - (2.125)^2 = 27/64 (0.422)', 'ANS: sd = 3sqrt(3)/8 (0.650)'],
     ['0.421875']),
    ('data_summary', ['2', '1,2,3', '4,5'], ['Error: list lengths'], ['ANS']),
    ('data_summary', ['3', '0,10,20', '4,6,10'], ['Error: need k+1 bounds'], ['ANS']),

    # aX+b: 2(12)-5=19, sd |2|3=6, var 4*9=36, median 2(2)-5=-1, IQR 10
    ('mean_transform', ['1', '12', '3', '', '2,5', '2', '-5'],
     ['mean = 12', 'sd = 3', 'median, IQR = 2,5', 'Y = 2X - 5', 'new mean = 2(12) - 5 = 19',
      'new sd = 2(3) = 6', 'new var = 2^2(9) = 36', 'new median = 2(2) - 5 = -1',
      'new IQR = 2(5) = 10', 'ANS: mean = 19', 'ANS: sd = 6', 'ANS: var = 36'],
     ['a:2', 'b:-5', 'new mean = a(mean) + b', '|a| sd']),
    # var given: -2(2.5)+1=-4, sd=sqrt(0.25)=0.5 -> 1, var 4(0.25)=1
    ('mean_transform', ['', '2.5', '', '0.25', '', '-2', '1'],
     ['var = 0.25', 'Y = -2X + 1', 'new mean = -2(2.5) + 1 = -4', 'new sd = |-2|(0.5) = 1',
      'new var = (-2)^2(0.25) = 1', 'ANS: mean = -4', 'ANS: sd = 1', 'ANS: var = 1']),
    # (20+k)/4 = 6 -> k = 4
    ('mean_transform', ['2', '3,7,k,10', '', '6'],
     ['x = 3,7,k,10', 'mean = 6', 'Sum x = k + 20', 'n = 4', '(k + 20)/4 = 6',
      'k + 20 = 24', 'ANS: k = 4'], ['Sum fx/Sum f', 'Sum f']),
    # (14+2k)/(6+k) = 2.2 -> 0.2k = 0.8 -> k = 4
    ('mean_transform', ['2', '1,2,3', '2,k,4', '2.2'],
     ['f = 2,k,4', 'Sum fx = 2k + 14', 'Sum f = k + 6', '(2k + 14)/(k + 6) = 2.2',
      '2k + 14 = 2.2(k + 6)', 'ANS: k = 4']),
    # mean 5 impossible: 2k+14 = 5k+30 -> k = -16/3 (not a frequency)
    ('mean_transform', ['2', '1,2,3', '2,k,4', '5'],
     ['k = -16/3 rejected', 'No solution: check data'], ['ANS']),
    ('mean_transform', ['2', '1,2,3', 'p,q,4', '2'], ['Need exactly one unknown'], ['ANS']),
    # combined: 80 + 195 = 275, 275/25 = 11
    ('mean_transform', ['3', '10,8', '15,13'],
     ['Sum x = 10(8) + 15(13) = 275', 'mean = 275/25', 'ANS: mean = 11'],
     ['Sum = n1 m1', 'n1,mean1:10,8', 'mean = 275/25 = 11']),
    # remove 3: (120-3)/9 = 13; add 30: (180+30)/10 = 21
    ('mean_transform', ['4', '10,12', '-3'],
     ['Sum x = 10(12) = 120', 'mean = (120 - 3)/9', 'ANS: mean = 13'], ['mean = (120 - 3)/9 = 13']),
    ('mean_transform', ['4', '9,20', '30'], ['mean = (180 + 30)/10', 'ANS: mean = 21']),

    # sxx=10, syy=6, sxy=6, r=6/sqrt(60)=sqrt(15)/5=0.775; b=0.6, a=4-1.8=2.2; d=1, c=-1
    ('regression', ['1,2,3,4,5', '2,4,5,4,5', '3', '1', '3.5', ''],
     ['x = 1,2,3,4,5', 'y = 2,4,5,4,5', 'By GDC:', 'ANS: r = 0.775',
      'strong positive linear correlation', 'ANS: y = 0.6x + 2.2', 'ANS: x = y - 1',
      'x = 3.5', 'y = 0.6(3.5) + 2.2', 'ANS: y(3.5) = 4.3'],
     ['Sxx', 'xbar', 'extrapolation', 'y increases', 'skip:1']),
    # perfect fit; x on y: d=4/8=0.5, c=2-2.5=-0.5; x(9)=4 outside y range 3..7
    ('regression', ['1,2,3', '3,5,7', '3', '2', '9', 'n'],
     ['perfect positive', 'ANS: r = 1', 'ANS: y = 2x + 1', 'ANS: x = 0.5y - 0.5',
      'y = 9', 'x = 0.5(9) - 0.5', 'ANS: x(9) = 4', '(extrapolation - unreliable)']),
    # Sxx=5, Syy=26, Sxy=-11, r=-11/sqrt(130)=-0.965, b=-2.2, a=10.5
    ('regression', ['1,2,3,4', '8,6,5,1', '', '1', '10', 'y'],
     ['strong negative', 'ANS: r = -0.965', 'ANS: y = -2.2x + 10.5', 'x = 10',
      'y = -2.2(10) + 10.5', 'ANS: y(10) = -11.5', '(extrapolation',
      'y decreases 2.2 per unit of x', 'y = 10.5 when x = 0'], ['ANS: x =']),
    ('regression', ['1,1,1', '2,3,4', '1'], ['Error: no variation'], ['ANS']),
    # removing the only value leaves no data (no division by 0)
    ('mean_transform', ['4', '1,3', '-10'], ['Error: no values left'], ['ANS', 'infinity']),
    # a = 0: the new mean is 5, no 'new mean = 5 = 5'
    ('mean_transform', ['1', '3', '2', '', '', '0', '5'], ['new mean = 5', 'ANS: mean = 5'], ['5 = 5']),
    ('regression', ['1,2', '3,4'], ['Error: need equal lists'], ['ANS']),
    # review regressions
    # 9 values: Sx^2=5676, var=776/9, sd=sqrt(776)/3=2sqrt(194)/3 (simplest form, not 6sqrt(194)/9)
    ('data_summary', ['1', '12,15,17,20,21,24,26,30,45', '0'],
     ['Sorted: 12,15,17,20,21,24,26,30,', 'Q1 = (2nd+3rd)/2 = (15+17)/2 = 16',
      'Q3 = (7th+8th)/2 = (26+30)/2 = 28',
      'ANS: sd = 2sqrt(194)/3 (9.29)', 'ANS: mean = 70/3 (23.3)'], ['6sqrt(194)/9']),
    # negative Q1 shown in brackets: 1 - (-2) = 3; sd sqrt(91/12)=sqrt(273)/6
    ('data_summary', ['1', '-2,-5,0,4,1,-1', '0'],
     ['IQR = Q3 - Q1 = 1 - (-2) = 3', 'Q1 - 1.5(IQR) = -2 - 1.5(3) = -6.5',
      'var = 47/6 - (-0.5)^2 = 91/12 (7.58)', 'ANS: sd = sqrt(273)/6 (2.75)'], ['1 - -2']),
    # zero frequency value 10 is not data: min 20, n=10, Sfx=310, var=1010-961=49, sd=7
    ('data_summary', ['2', '10,20,30,40', '0,2,5,3', '0'],
     ['Box: min 20, Q1 30, med 30, Q3 40, max 40', 'Outliers: none', 'var = 10100/10 - 31^2 = 49',
      'ANS: mean = 31', 'ANS: sd = 7'],
     ['min 10', 'Outliers: 10']),
    # fractional sum shown bracketed: (25/12)/4 = 25/48
    ('data_summary', ['1', '1/2,1/3,1/4,1', '0'],
     ['mean = (25/12)/4 = 25/48', 'var = (205/144)/4 - (25/48)^2 = 65/768', 'ANS: sd = sqrt(195)/48'], []),
    # no nested approximations inside working
    ('mean_transform', ['1', '4', 'sqrt(2)', '', '', '3', '1'],
     ['Y = 3X + 1', 'new sd = 3(sqrt(2)) = 3sqrt(2) (4.24)', 'new var = 3^2(2) = 18', 'ANS: var = 18'], ['(1.41)']),
    # Sxx=10.772, Sxy=32.82, Syy=101.2: b=3.0468, a=3.4816, d=0.32431, c=-1.0787, r=0.994
    ('regression', ['2.1,3.4,4.0,5.5,6.2', '10,14,15,21,22', '3', '1', '5', 'n'],
     ['ANS: y = 3.05x + 3.48', 'ANS: x = 0.324y - 1.08', 'ANS: r = 0.994',
      'y = 3.05(5) + 3.48', 'ANS: y(5) = 18.7'],
     ['8205/2693x', '50401/2693']),
    # GDC presentation: x on y only (d=1, c=-1), prediction x(2) = 2-1 = 1 inside the y range
    ('regression', ['1,2,3,4,5', '2,4,5,4,5', '2', '2', '2', 'n'],
     ['By GDC:', 'ANS: r = 0.775', 'ANS: x = y - 1', 'y = 2', 'x = 2 - 1', 'ANS: x(2) = 1'],
     ['ANS: y =', 'extrapolation']),
    # no correlation: sxy = 0, r = 0, y = ybar = 4/3 (no 0x term)
    ('regression', ['1,2,3', '1,2,1', '1', '1', '5', 'y'],
     ['ANS: r = 0', 'no linear correlation', 'ANS: y = 1.33', 'y = 1.33', 'ANS: y(5) = 1.33',
      'y does not depend on x'], ['0x']),
    # a = 1: sd and var unchanged, no 1(..) or 1^2 steps
    ('mean_transform', ['1', '5', '2', '', '', '1', '3'],
     ['Y = X + 3', 'new mean = 5 + 3 = 8', 'ANS: mean = 8', 'ANS: sd = 2', 'ANS: var = 4'],
     ['1(2)', '1^2']),
    # fractional a keeps exact brackets: (1/3)6-2=0, sd (1/3)3=1, var (1/9)9=1, median -4/3, IQR 5/3
    ('mean_transform', ['1', '6', '3', '', '2,5', '1/3', '-2'],
     ['Y = (1/3)X - 2', 'new mean = (1/3)(6) - 2 = 0', 'new sd = (1/3)(3) = 1',
      'new var = (1/3)^2(9) = 1', 'new median = (1/3)(2) - 2 = -4/3', 'new IQR = (1/3)(5) = 5/3',
      'ANS: mean = 0', 'ANS: sd = 1', 'ANS: var = 1']),
]
