"""Build calculator files: calc/*.py -> dist/*.py.tns (comments and
docstrings stripped, 1-space indents) so each module needs less heap
when KhiCAS compiles it. Each output is re-checked with mpy-cross 1.12.

    python build.py
"""
import ast
import io
import os
import tokenize
import subprocess
import sys
import tempfile

from check_mpy import MPY

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CALC = os.path.join(ROOT, 'calc')
DIST = os.path.join(ROOT, 'dist')


def strip_docstrings(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)):
            b = node.body
            if b and isinstance(b[0], ast.Expr) and isinstance(getattr(b[0], 'value', None), ast.Constant) \
                    and isinstance(b[0].value.value, str):
                node.body = b[1:] or [ast.Pass()]
    return tree


def _tight(line):
    # drop spaces between tokens unless both sides are word characters,
    # a NAME/NUMBER meets a string, or a number meets '.'; strings intact
    o = ''
    prev = None
    for t in tokenize.generate_tokens(io.StringIO(line).readline):
        if t.type in (tokenize.NEWLINE, tokenize.NL, tokenize.ENDMARKER,
                      tokenize.INDENT, tokenize.DEDENT):
            continue
        s = t.string
        if prev is not None:
            a, b = o[-1], s[0]
            word = (a.isalnum() or a == '_') and (b.isalnum() or b == '_')
            strj = t.type == tokenize.STRING and prev.type in (tokenize.NAME, tokenize.NUMBER)
            numdot = prev.type == tokenize.NUMBER and b == '.'
            if word or strj or numdot:
                o += ' '
        o += s
        prev = t
    return o


def minify(src):
    code = ast.unparse(strip_docstrings(ast.parse(src)))
    out = []
    for line in code.split('\n'):
        n = len(line) - len(line.lstrip(' '))
        if line.strip():
            out.append(' ' * (n // 4) + _tight(line.strip()))
    return '\n'.join(out) + '\n'


def main():
    os.makedirs(DIST, exist_ok=True)
    total = 0
    ok_all = True
    for f in sorted(os.listdir(CALC)):
        if not f.endswith('.py'):
            continue
        src = open(os.path.join(CALC, f), encoding='utf-8').read()
        small = minify(src)
        dst = os.path.join(DIST, f + '.tns')
        with open(dst, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(small)
        with tempfile.TemporaryDirectory() as td:
            p = subprocess.run([MPY, '-o', os.path.join(td, 'x.mpy'), dst], capture_output=True, text=True)
        ok = p.returncode == 0
        ok_all = ok_all and ok
        total += len(small.encode('utf-8'))
        print('%s %-14s %6d -> %6d bytes' % ('OK ' if ok else 'BAD', f + '.tns', len(src.encode('utf-8')),
                                             len(small.encode('utf-8'))))
        if not ok:
            print('   ' + (p.stdout + p.stderr).strip())
    print('total %d bytes in %s' % (total, DIST))
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main())
