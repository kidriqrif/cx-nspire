"""Run every example in make_keying_pdf.py through the solver its code names.

    python keychk.py
"""
import sys
import harness  # noqa: F401  (sets sys.path, fake cas)
from harness import run_solver
from make_keying_pdf import EXAMPLES

# jump code -> (module, solver, inputs after the example text)
SOLVER = {'511': ('ibdiff', 'diff_steps', ['', '']), '121': ('ibalg2', 'explog', []),
          '331': ('ibtrig3', 'trig_eq', ['r', '', '', 'y']), '232': ('ibfun3', 'modeq', []),
          '514': ('ibdiff', 'implicit', ['(1,1)']), '573': ('ibode', 'homog', ['y(1)=2']),
          '132': ('ibcpx', 'demoivre', ['5'])}
bad = 0
for ty, s, hint, code in EXAMPLES:
    m, f, more = SOLVER[code]
    text, left, _ = run_solver(m, f, [s] + more)
    ok = 'ANS' in text and 'rror' not in text and not left
    bad += not ok
    ans = [ln for ln in text.split('\n') if ln.startswith('ANS')]
    print('%-4s %-15s %-30s %s' % ('OK' if ok else 'FAIL', ty, s, (ans[0] if ans else text[-200:])[:60]))
print('failures', bad)
sys.exit(1 if bad else 0)
