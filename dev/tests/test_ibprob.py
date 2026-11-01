# Tests for calc/ibprob.py (AA 4.5, 4.6, 4.11, 4.13). Values hand-checked.
MODULE = 'ibprob'
CASES = [
    # P(AnB) = 1/2 + 2/5 - 7/10 = 1/5 = P(A)P(B) -> independent
    ('prob_rules', ['1', '1/2', '2/5', '', '7/10', '', '', '', '0', '0'],
     ['P(A) = 1/2', 'P(B) = 2/5', 'P(AuB) = 7/10',
      'P(AuB) = P(A) + P(B) - P(AnB)', '7/10 = 1/2 + 2/5 - P(AnB)', 'P(AnB) = 1/5',
      'P(A|B) = P(AnB)/P(B)', '= (1/5)/(2/5)', '= 1/2', '= (1/5)/(1/2)', '= 2/5',
      "P(A'nB') = 1 - P(AuB)", '= 1 - 7/10', '= 3/10',
      'A only = P(A) - P(AnB) = 3/10', 'B only = P(B) - P(AnB) = 1/5',
      'P(A)P(B) = (1/2)(2/5) = 1/5', 'P(AnB) = P(A)P(B) => independent',
      "ANS: P(AnB) = 1/5, P(A|B) = 1/2, P(B|A) = 2/5, P(A'nB') = 3/10"],
     ['=> P(A', 'neither', 'P(A|B) = (1/5)', 'mut.excl:0', 'P(A|B) (blank=?): 1/2']),
    # P(AnB) = 0.6(0.3) = 0.18; P(AuB) = 0.62; P(A|B) = 0.36; 0.15 != 0.18;
    # P(A|B') = (0.3-0.18)/(1-0.5) = 0.24
    ('prob_rules', ['1', '0.3', '0.5', '', '', '', '0.6', '', '0', '1'],
     ['P(A) = 0.3', 'P(B) = 0.5', 'P(B|A) = 0.6', 'P(B|A) = P(AnB)/P(A)', '0.6 = P(AnB)/0.3',
      'P(AnB) = 0.18', '= 0.3 + 0.5 - 0.18', '= 0.62', '= 0.18/0.5', '= 0.36',
      'P(A)P(B) = (0.3)(0.5) = 0.15', 'P(AnB) != P(A)P(B) => not independent',
      'not mut. exclusive', "P(A|B') = (P(A) - P(AnB))/(1 - P(B))",
      '= (0.3 - 0.18)/(1 - 0.5)', "ANS: P(A|B') = 0.24",
      "ANS: P(AnB) = 0.18, P(AuB) = 0.62, P(A|B) = 0.36, P(A'nB') = 0.38"],
     ['=> P(A', '(1 - 0.5) = 0.24', 'none:1']),
    # independent: 0.7 = a + 0.4 - 0.4a -> a = 0.5, P(AnB) = 0.2
    ('prob_rules', ['1', '', '0.4', '', '0.7', '', '', '', '1', '0'],
     ['(simultaneous equations)', '0.7 = P(A) + 0.4 - P(AnB)', 'P(AnB) = P(A)(0.4)',
      'P(A) = 0.5, P(AnB) = 0.2', '= 0.2/0.4', '= 0.5', '= 0.2/0.5', '= 0.4'],
     ['independent =>', 'Solve simultaneously', '=> P(A']),
    # mutually exclusive: P(AuB) = 0.3 + 0.4 = 0.7
    ('prob_rules', ['1', '0.3', '0.4', '', '', '', '', '', '2', '0'],
     ['P(AnB) = 0', 'P(AuB) = P(A) + P(B) - P(AnB)', '= 0.3 + 0.4', '= 0.7', '= 0/0.4',
      "P(A'nB') = 1 - P(AuB)", '= 1 - 0.7', '= 0.3'],
     ['0.4 - 0', 'P(AnB)=0\n=0', '=> P(A']),
    # P(AnB) = 0.8 > P(A): impossible
    ('prob_rules', ['1', '0.5', '0.6', '', '0.3', '', '', '', '0'], ['Inconsistent data'], ['ANS']),
    ('prob_rules', ['1', '', '', '', '0.3', '', '', '', '2'], ['Not enough information'], ['ANS']),
    # regions: 6x + 0.1 = 1 -> x = 0.15; P(2|{2,3}) = 0.3/0.75 = 0.4; P(1 or 2) = 0.45
    ('prob_rules', ['2', 'x,2x,3x,0.1', '1', '2', '2,3', '1,2', '', ''],
     ['x + 2x + 3x + 0.1 = 1', '6x + 0.1 = 1', 'ANS: x = 0.15', 'Regions: 0.15, 0.3, 0.45, 0.1',
      'P(2|2,3) = 0.3/0.75', 'ANS: P(2|2,3) = 0.4', 'P(1,2) = 0.15 + 0.3', 'ANS: P(1,2) = 0.45'],
     ['1/10', '0.45/1', 'W|G', '= 1\nx = 0.15', 'end):2']),
    # counts: 3x + 13 = 40 -> x = 9; n(2)/n(2,3) = 9/17; n(4)/40 = 18/40
    ('prob_rules', ['2', '5,x,8,2x', '40', '1,2', '2,3', '4', '', ''],
     ['5 + x + 8 + 2x = 40', '3x + 13 = 40', 'ANS: x = 9', 'Regions: 5, 9, 8, 18',
      'ANS: P(1,2|2,3) = 9/17 (0.529)', 'P(4) = 18/40', 'ANS: P(4) = 9/20'],
     ['18/40 = 9/20', '9/17 = 9/17', 'P(1,2|2,3) = 9/17\nANS']),
    # table [[10,20],[30,40]]: P(r1|c2) = 20/60; P(c2|r1) = 20/30; r1uc2 = 10+20+40
    ('prob_rules', ['3', '10,20', '30,40', '', 'r1|c2', 'c2|r1', 'r1uc2', 'r1nc2', ''],
     ['r1 = 10,20', 'r2 = 30,40', 'Row totals: 30, 70', 'Col totals: 40, 60', 'N = 100',
      'P(r1|c2) = n(r1nc2)/n(c2) = 20/60', 'P(c2|r1) = n(c2nr1)/n(r1) = 20/30',
      'ANS: P(c2|r1) = 2/3 (0.667)', 'P(r1uc2) = n(r1uc2)/N = 70/100',
      'ANS: P(r1uc2) = 7/10', 'ANS: P(r1nc2) = 1/5', 'ANS: P(r1|c2) = 1/3 (0.333)'],
     ['20/60 = 1/3', '70/100 = 7/10', 'end):r1|c2']),

    # P(B) = 0.006 + 0.035 = 0.041, P(A1|B) = 6/41
    ('tree_bayes', ['2', '0.3', '', '0.02', '0.05', '2', '1'],
     ['P(A1) = 0.3', 'P(B|A1) = 0.02', 'P(B|A2) = 0.05',
      'P(A2) = 1 - 0.3 = 0.7', 'P(A1nB) = P(A1)P(B|A1)', '= (0.3)(0.02) = 0.006',
      'P(A2nB) = (0.7)(0.05) = 0.035', 'P(B) = P(A1nB) + P(A2nB)', '= 0.006 + 0.035 = 0.041',
      'P(A1|B) = P(A1nB)/P(B)', '= 0.006/0.041', 'ANS: P(A1|B) = 6/41 (0.146)'],
     ['Bayes:', '0.041 = 6/41', 'events(2/3):2', 'P(A1):0.3']),
    # P(B) = 0.005 + 0.006 + 0.006 = 0.017, P(A3|B) = 6/17
    ('tree_bayes', ['3', '0.5', '0.3', '', '0.01', '0.02', '0.03', '2', '3'],
     ['P(A3) = 1 - 0.5 - 0.3 = 0.2', 'P(A3nB) = (0.2)(0.03) = 0.006',
      '= 0.005 + 0.006 + 0.006 = 0.017', 'ANS: P(A3|B) = 6/17 (0.353)']),
    # P(B) = 1/6 + 1/4 = 5/12; P(A1nB') = 1/12, P(B') = 7/12 -> 1/7
    ('tree_bayes', ['2', '1/4', '', '2/3', '1/3', '3', '1'],
     ['P(A2) = 1 - 1/4 = 3/4', '= 1/6 + 1/4 = 5/12 (0.417)', "P(B'|A1) = 1 - 2/3 = 1/3",
      "P(A1nB') = (1/4)(1/3) = 1/12", "P(B') = 1 - 5/12 = 7/12", "= (1/12)/(7/12)",
      "ANS: P(A1|B') = 1/7 (0.143)"], ['(7/12) = 1/7']),
    # unknown prior: 0.2x/(0.5 - 0.3x) = 0.4 -> 0.32x = 0.2 -> x = 0.625
    ('tree_bayes', ['2', 'x', '', '0.2', '0.5', '2', '1', '0.4'],
     ['P(A2) = 1 - x', 'P(A1|B) = 0.4', '= x(0.2) = 0.2x', '(1 - x)(0.5) = 0.5 - 0.5x',
      '= 0.2x + 0.5 - 0.5x = -0.3x + 0.5', '-2x/(3x-5) = 0.4', 'ANS: x = 0.625'],
     ['1 - x = 1-x', '+ -', '(x)(0.2)', '1/2']),
    ('tree_bayes', ['2', '1/3', '2/3', '1/2', '1/4', '1'],
     ['= 1/6 + 1/6', 'ANS: P(B) = 1/3 (0.333)'], ['1/6 + 1/6 = 1/3']),
    ('tree_bayes', ['2', '0.5', '0.6', '0.1', '0.2'], ['Priors must sum to 1'], ['ANS']),

    ('bag_draws', ['5,3', '', '2', 'n', '1', 'RR'],
     ['Bag: 5R, 3B (total 8)', '2 draws, without replacement', 'P(RR) = 5/8 x 4/7',
      'ANS: P(RR) = 5/14 (0.357)'], ['Total = 8', '4/7\n=5/14', 'counts e.g. 5,3: 5,3']),
    # exactly one B: 2 x (3/8)(5/7) = 15/28
    ('bag_draws', ['5,3', '', '2', 'n', '2', 'B', '1'],
     ['Arrangements: BR, RB', 'P(1 B) = 2 x 3/8 x 5/7', '= 2 x 15/56',
      'ANS: P(1 B) = 15/28 (0.536)'], ['15/56 = 15/28']),
    # with replacement: 1 - (5/8)^2 = 39/64
    ('bag_draws', ['5,3', '', '2', 'y', '3', 'B'],
     ['2 draws, with replacement', 'P(no B) = 5/8 x 5/8 = 25/64',
      'P(at least 1 B) = 1 - P(no B)', '= 1 - 25/64', 'ANS: P(at least 1 B) = 39/64'],
     ['25/64 = 39/64', 'P = 1 -']),
    # 3 x (4/6)(3/5)(2/4) = 3/5
    ('bag_draws', ['4,2', '', '3', 'n', '2', 'R', '2'],
     ['Arrangements: RRB, RBR, BRR', 'P(2 R) = 3 x 4/6 x 3/5 x 2/4', '= 3 x 1/5',
      'ANS: P(2 R) = 3/5'], ['1/5 = 3/5']),
    # all same: 60/720 + 6/720 + 0 = 11/120 (GGG impossible)
    ('bag_draws', ['5,3,2', '', '3', 'n', '4'],
     ['P(RRR) = 5/10 x 4/9 x 3/8', 'P(BBB) = 3/10 x 2/9 x 1/8', 'P(all same) = P(RRR) + P(BBB)',
      '= 1/12 + 1/120', 'ANS: P(all same) = 11/120 (0.0917)'], ['P(GGG)', '1/120 = 11/120']),
    # at least 2 R: 3(5*4*5)/720 + 60/720 = 5/12 + 1/12 = 1/2
    ('bag_draws', ['5,3,2', '', '3', 'n', '5', 'R', '2'],
     ['P(2 R) = 3 x 5/10 x 4/9 x 5/8', '= 3 x 5/36 = 5/12', 'P(3 R) = 5/10 x 4/9 x 3/8',
      'P(R>=2) = 5/12 + 1/12', 'ANS: P(R>=2) = 1/2'], ['1/12 = 1/2']),
    # three colours, exactly 1 G: 2 x (2/10)(8/9) = 16/45, other group labelled G'
    ('bag_draws', ['5,3,2', 'RBG', '2', 'n', '2', 'G', '1'],
     ["Arrangements: GG', G'G", '= 2 x 8/45', 'ANS: P(1 G) = 16/45 (0.356)'], ['8/45 = 16/45']),
    ('bag_draws', ['2,1', '', '4', 'n'], ['Error: check counts/labels/d'], ['ANS']),
    # review regressions
    # P(A)=x, P(B)=2x, P(AnB)=0.1, P(AuB)=0.5: 3x - 0.1 = 0.5 -> x = 0.2; P(A|B) = 0.1/0.4 = 0.25
    ('prob_rules', ['1', 'x', '2x', '0.1', '0.5', '', '', '', '0', '0'],
     ['P(A) = x', 'P(B) = 2x', '0.5 = x + 2x - 0.1', 'x = 0.2', '= 0.1/0.4', 'x = 0.2'],
     ['Inconsistent', '=> x']),
    # independent, P(A)=0.3, P(B)=x, P(AuB)=0.65: 0.3 + 0.7x = 0.65 -> x = 0.5, P(AnB) = 0.15
    ('prob_rules', ['1', '0.3', 'x', '', '0.65', '', '', '', '1', '0'],
     ['(simultaneous equations)', 'P(AnB) = 0.15, x = 0.5', 'B only = P(B) - P(AnB) = 0.35'],
     ['No valid solution']),
    # regions that do not add up to the total must not be printed as an equation
    ('prob_rules', ['2', '0.2,0.5,0.6', '1'], ['0.2 + 0.5 + 0.6 != 1'], ['ANS', '0.6 = 1']),
    # no colour can be drawn twice from 1,1: P(all same) = 0, no empty working line
    ('bag_draws', ['1,1', '', '2', 'n', '4'], ['ANS: P(all same) = 0'], ['=  = 0']),
    # tree with unknown prior x: x(0.8) = 0.8x; P(B) = 0.5x + 0.3 = 0.55 -> x = 0.5
    ('tree_bayes', ['2', 'x', '', '0.8', '0.3', '1', '0.55'],
     ['P(B) = 0.55', '= x(0.8) = 0.8x', '= 0.8x - 0.3x + 0.3 = 0.5x + 0.3', '0.5x + 0.3 = 0.55',
      'ANS: x = 0.5'], ['4/5*x', '(x)(0.8)', '4x/5']),
    # colour not among the labels: clear message instead of 'substring not found'
    ('bag_draws', ['7,3', '', '2', 'n', '2', 'X'], ['Error: use labels RB'], ['substring', 'ANS']),
    # regions with a total N: P(1 or 2) = (5 + 9)/40 = 7/20
    ('prob_rules', ['2', '5,9,8,18', '40', '1,2', '', ''],
     ['5 + 9 + 8 + 18 = 40', 'P(1,2) = (5 + 9)/40', 'ANS: P(1,2) = 7/20'], ['W|G']),
    # a single region of a total of 1: no repeated 'P(3) = 0.7' line, just the answer
    ('prob_rules', ['2', '0.1,0.2,0.7', '1', '3', '', ''],
     ['0.1 + 0.2 + 0.7 = 1', 'ANS: P(3) = 0.7'], ['P(3) = 0.7\nANS']),
    # exactly 0 or all d of a colour: one arrangement, no 'Arrangements' line, no repeated value
    ('bag_draws', ['5,3', '', '2', 'n', '2', 'B', '0'],
     ['P(0 B) = 5/8 x 4/7', 'ANS: P(0 B) = 5/14'], ['Arrangements', '= 5/14\nANS']),
    # only one colour can be drawn 3 times from 5R, 2B: P(RRR) = 60/210 = 2/7
    ('bag_draws', ['5,2', '', '3', 'n', '4'],
     ['P(RRR) = 5/7 x 4/6 x 3/5', 'ANS: P(all same) = 2/7'], ['P(all same) = P(RRR)']),
    # at least 3 R in 3 draws: single term 60/336 = 5/28
    ('bag_draws', ['5,3', '', '3', 'n', '5', 'R', '3'],
     ['P(3 R) = 5/8 x 4/7 x 3/6', 'ANS: P(R>=3) = 5/28 (0.179)'], ['= 5/28\nP(R>=3)', '= 5/28\nANS']),
    # 3x3 table: r3|c1 = 7/12, c2 = 15/45
    ('prob_rules', ['3', '1,2,3', '4,5,6', '7,8,9', 'r3|c1', 'c2', ''],
     ['r3 = 7,8,9', 'Row totals: 6, 15, 24', 'Col totals: 12, 15, 18', 'N = 45',
      'P(r3|c1) = n(r3nc1)/n(c1) = 7/12', 'ANS: P(r3|c1) = 7/12 (0.583)',
      'P(c2) = n(c2)/N = 15/45', 'ANS: P(c2) = 1/3 (0.333)'], ['7/12 = 7/12']),
    # P(A) = P(B) = 0.5, B entered with the ditto mark; independent -> P(AnB) = 0.25
    ('prob_rules', ['1', '0.5', '"', '', '', '', '', '', '1', '0'],
     ['P(A) = 0.5', 'P(B) = 0.5', 'P(AnB) = 0.25', 'P(AuB) = 0.75']),
    # repeating an answer without the ditto mark counts as blank (and says so)
    ('prob_rules', ['1', '0.5', '0.5', '', '', '', '', '', '0'],
     ['(same=blank; type " to repeat)'], ['P(B) = 0.5']),
]
