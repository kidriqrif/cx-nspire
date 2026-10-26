"""Run calculator solvers on the desktop with scripted input().

    from harness import run_solver
    text = run_solver('ibdiff', 'diff_steps', ['3x^2+5x'])
"""
import builtins
import importlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.environ.get('IB_CALC') or os.path.join(os.path.dirname(HERE), 'calc')  # IB_CALC: test another build
for p in (HERE, CALC):
    if p not in sys.path:
        sys.path.insert(0, p)

import ibcore  # noqa: E402

AUTO = ('-- more', '[enter]')


class OutOfInput(Exception):
    pass


def run_solver(module, fn, inputs, width=200, pause=0, uni=0):
    """Return (output_text, leftover_inputs, prompts)."""
    ibcore.CFG.update({'w': width, 'pg': 10, 'uni': uni, 'pause': pause})
    ibcore.init()
    mod = importlib.import_module(module)
    func = getattr(mod, fn)
    queue = list(inputs)
    prompts = []
    buf = io.StringIO()

    def fake_input(p=''):
        buf.write(p + '\n')
        if p.startswith(AUTO):
            return ''
        prompts.append(p)
        if not queue:
            raise OutOfInput('no input left for prompt: ' + p)
        return str(queue.pop(0))

    old_in, old_out = builtins.input, sys.stdout
    builtins.input, sys.stdout = fake_input, buf
    try:
        ibcore.run(func)
    finally:
        builtins.input, sys.stdout = old_in, old_out
    return buf.getvalue(), queue, prompts


if __name__ == '__main__':
    # python harness.py ibdiff diff_steps "3x^2+5x" ...
    text, left, _ = run_solver(sys.argv[1], sys.argv[2], sys.argv[3:], width=32, uni=0)
    sys.stdout.write(text)
    if left:
        print('UNUSED INPUTS:', left)
