"""Robustness fuzz: run every solver with blunt input profiles and report
crashes (uncaught exceptions would quit the app on the calculator), caught
Python errors, leaked Giac internals and hangs.

    python fuzz.py            # all modules, prints problems + summary
    python fuzz.py ibint      # one module
"""
import os
import subprocess
import sys
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
PROFILES = [('defaults', ''), ('zero', '0'), ('one', '1'), ('neg', '-2'), ('num', '3'),
            ('poly', 'x^2-4'), ('list', '1,2,3'), ('junk', 'abc'), ('paren', '(x+1')]
LEAKS = ('GIAC_ERROR', 'Large_object', 'rootof', 'Traceback', 'None', 'order_size', '**')
RAWTXT = ('NoneType', 'invalid literal', 'unpack', 'out of range', 'iterable', 'object', 'attribute',
          'not supported', 'argument')
TIMEOUT = 25
N_INPUTS = 14


def worker(module, start):
    sys.path.insert(0, HERE)
    import harness
    mod = __import__(module)
    jobs = [(fn, p) for _, fn in mod.ITEMS for p in PROFILES]
    for k in range(start, len(jobs)):
        fn, (pname, val) = jobs[k]
        res = {}

        def go():
            try:
                res['out'] = harness.run_solver(module, fn.__name__, [val] * N_INPUTS)[0]
            except harness.OutOfInput:
                res['out'] = ''
            except BaseException as e:  # noqa: B902 - report everything
                res['crash'] = type(e).__name__ + ': ' + str(e)[:80]

        t = threading.Thread(target=go, daemon=True)
        t.start()
        t.join(TIMEOUT)
        tag = '%s|%s|%s' % (module, fn.__name__, pname)
        if t.is_alive():
            print('PROB|' + tag + '|HANG|>%ds' % TIMEOUT, flush=True)
            print('NEXT|%d' % (k + 1), flush=True)
            os._exit(3)
        if 'crash' in res:
            print('PROB|' + tag + '|CRASH|' + res['crash'], flush=True)
            continue
        out = res.get('out', '')
        for line in out.split('\n'):
            if line.startswith('Error:'):
                raw = [k for k in RAWTXT if k in line]
                print('PROB|' + tag + ('|PYERR|' if raw else '|INPUT|') + line[:90], flush=True)
            for lk in LEAKS:
                if lk in line and not line.startswith('Giac error'):
                    print('PROB|' + tag + '|LEAK ' + lk + '|' + line[:90], flush=True)
        print('DONE|' + tag, flush=True)
    print('NEXT|-1', flush=True)


def driver(names):
    py = sys.executable
    mods = names or sorted(f[:-3] for f in os.listdir(os.path.join(os.path.dirname(HERE), 'calc'))
                           if f.startswith('ib') and f != 'ibcore.py')
    total = 0
    probs = []
    for m in mods:
        start = 0
        while start >= 0:
            p = subprocess.run([py, __file__, '--worker', m, str(start)], capture_output=True, text=True,
                               encoding='utf-8', errors='replace', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
            start = -1
            for line in p.stdout.split('\n'):
                if line.startswith('PROB|'):
                    probs.append(line[5:])
                    print(line[5:], flush=True)
                elif line.startswith('DONE|'):
                    total += 1
                elif line.startswith('NEXT|'):
                    start = int(line[5:])
            if p.returncode not in (0, 3):
                probs.append('%s|worker exit %d|%s' % (m, p.returncode, p.stderr.strip()[-200:]))
                print(probs[-1], flush=True)
                start = -1
    print('SUMMARY runs=%d problems=%d' % (total, len(probs)))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--worker':
        worker(sys.argv[2], int(sys.argv[3]))
    else:
        driver(sys.argv[1:])
