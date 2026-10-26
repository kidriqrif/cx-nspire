"""Drive calc/main.py end to end with scripted keypresses (32 cols, paged)."""
import builtins
import sys
import harness  # sets sys.path, imports fake cas
import ibcore

ibcore.CFG.update({'w': 32, 'pg': 10, 'uni': 1, 'pause': 1})
keys = sys.argv[1:] or ['5', '1', '1', 'x^2*sin(x)', '', '', '0', '0', '6', '', '', '', '', '0']


def fake(p=''):
    print('[' + p + ']')
    if not keys:
        raise SystemExit('script ended at prompt: ' + p)
    return keys.pop(0)


builtins.input = fake
import main  # noqa: E402,F401  (runs main())
print('-- quit cleanly, unused keys:', keys)
