"""Run solver test cases against real Giac.

Each dev/tests/test_<module>.py defines:
    MODULE = 'ibdiff'
    CASES = [
        # (function, inputs, must_contain, must_not_contain)
        ('diff_steps', ['3x^2+5x'], ['ANS:', "6x+5"], []),
    ]
Matching ignores spaces. A case fails if output has 'Giac error'/'Error:'
(unless expected), inputs are left over, or the solver asks for more input.
Each case runs twice: wide (for matching) and 32-col paged (smoke test).

    python run_tests.py              # all
    python run_tests.py ibdiff -v    # one module, print every output
"""
import importlib
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'tests'))
from harness import run_solver, OutOfInput  # noqa: E402


def squash(s):
    return s.replace(' ', '')


def run_module(tmod, verbose):
    m = importlib.import_module(tmod)
    npass = nfail = 0
    for case in m.CASES:
        fn, inputs, must, mustnot = (list(case) + [[]])[:4]
        label = '%s.%s %r' % (m.MODULE, fn, inputs)
        try:
            text, left, _ = run_solver(m.MODULE, fn, inputs)
            run_solver(m.MODULE, fn, inputs, width=32, pause=1, uni=1)
        except OutOfInput as e:
            text, left = 'OUT OF INPUT: %s' % e, []
        except Exception:
            text, left = traceback.format_exc(), []
        st = squash(text)
        probs = []
        for s in must:
            if squash(s) not in st:
                probs.append('missing %r' % s)
        for s in mustnot:
            if squash(s) in st:
                probs.append('unexpected %r' % s)
        if ('Giacerror' in st or 'Error:' in st or 'Traceback' in st) and \
                not any('rror' in s for s in must):
            probs.append('error in output')
        if 'OUTOFINPUT' in st:
            probs.append('ran out of input')
        if left:
            probs.append('unused inputs %r' % left)
        if probs:
            nfail += 1
            print('FAIL ' + label + ': ' + '; '.join(probs))
            print('    ' + text.replace('\n', '\n    '))
        else:
            npass += 1
            if verbose:
                print('PASS ' + label)
                print('    ' + text.replace('\n', '\n    '))
    return npass, nfail


def main(args):
    verbose = '-v' in args
    names = [a for a in args if not a.startswith('-')]
    tdir = os.path.join(HERE, 'tests')
    mods = sorted(f[:-3] for f in os.listdir(tdir) if f.startswith('test_') and f.endswith('.py'))
    if names:
        mods = [t for t in mods if t[5:] in names]
    tp = tf = 0
    for t in mods:
        p, f = run_module(t, verbose)
        print('%-14s %3d pass %3d fail' % (t[5:], p, f))
        tp += p
        tf += f
    print('TOTAL %d pass %d fail' % (tp, tf))
    return 1 if tf else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
