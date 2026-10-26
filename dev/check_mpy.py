"""Static checks that calc/*.py will load in KhiCAS MicroPython 1.12.

1. Compile with mpy-cross 1.12 (MicroPython's own parser/compiler).
2. AST lint: no f-strings, walrus, annotations, match, `re`, direct
   recursion, or str methods missing from MicroPython 1.12.
3. Report source size (each module is compiled on the calculator heap).

    python check_mpy.py            # all modules
    python check_mpy.py ibdiff     # one module
"""
import ast
import os
import subprocess
import sys
import tempfile

import mpy_cross

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.join(os.path.dirname(HERE), 'calc')
MPY = os.path.join(os.path.dirname(mpy_cross.__file__), 'mpy-cross.exe')
CORE_MAX = 14500  # ibcore is compiled once at start and stays resident
MAX_BYTES = 13000  # limit on the MINIFIED size (dev/build.py) per module; calculator heap may be ~40-64K
BAD_METHODS = {'partition', 'rpartition', 'center', 'ljust', 'rjust', 'zfill',
               'casefold', 'title', 'capitalize', 'swapcase', 'expandtabs',
               'format_map', 'isidentifier', 'isnumeric', 'isdecimal',
               'removeprefix', 'removesuffix', 'isascii'}
BAD_MATH = {'log10', 'log2', 'gcd', 'isclose', 'comb', 'perm', 'prod', 'dist',
            'factorial', 'erf', 'erfc', 'gamma', 'lgamma'}
BAD_MODULES = {'re', 'numpy', 'sympy', 'pandas', 'fractions', 'decimal',
               'itertools', 'functools', 'typing', 'dataclasses', 'string'}


def lint(path):
    src = open(path, encoding='utf-8').read()
    tree = ast.parse(src)
    errs = []
    for node in ast.walk(tree):
        ln = getattr(node, 'lineno', '?')
        if isinstance(node, ast.JoinedStr):
            errs.append('%s: f-string' % ln)
        elif isinstance(node, ast.NamedExpr):
            errs.append('%s: walrus :=' % ln)
        elif isinstance(node, ast.AnnAssign) or (isinstance(node, ast.arg) and node.annotation):
            errs.append('%s: type annotation' % ln)
        elif isinstance(node, (ast.FunctionDef,)) and node.returns is not None:
            errs.append('%s: return annotation' % ln)
        elif type(node).__name__ == 'Match':
            errs.append('%s: match statement' % ln)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module]
            for n in names:
                if n and n.split('.')[0] in BAD_MODULES:
                    errs.append('%s: import %s' % (ln, n))
        elif isinstance(node, ast.Attribute):
            if node.attr in BAD_METHODS:
                errs.append('%s: .%s() not in MicroPython 1.12' % (ln, node.attr))
            if isinstance(node.value, ast.Name) and node.value.id == 'math' and node.attr in BAD_MATH:
                errs.append('%s: math.%s may be missing' % (ln, node.attr))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ('print',):
            for kw in node.keywords:
                if kw.arg == 'end' or kw.arg == 'sep':
                    pass
    # direct recursion
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        for node in ast.walk(fn):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == fn.name:
                errs.append('%s: recursion in %s()' % (node.lineno, fn.name))
    return errs, len(src.encode('utf-8'))


def compile_mpy(path):
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, 'x.mpy')
        p = subprocess.run([MPY, '-o', out, path], capture_output=True, text=True)
        return p.returncode == 0, (p.stdout + p.stderr).strip()


def main(names):
    files = sorted(f for f in os.listdir(CALC) if f.endswith('.py'))
    if names:
        files = [f for f in files if f[:-3] in names]
    ok_all = True
    for f in files:
        path = os.path.join(CALC, f)
        ok, msg = compile_mpy(path)
        errs, size = lint(path)
        from build import minify
        msize = len(minify(open(path, encoding='utf-8').read()).encode('utf-8'))
        flag = 'OK ' if ok and not errs else 'BAD'
        if msize > (CORE_MAX if f == 'ibcore.py' else MAX_BYTES):
            errs.append('minified size %d > %d bytes: split the module' % (msize, MAX_BYTES))
            flag = 'BAD'
        print('%s %-12s %6d bytes (minified %d)' % (flag, f, size, msize))
        if not ok:
            print('   mpy-cross: ' + msg)
        for e in errs:
            print('   ' + e)
        ok_all = ok_all and flag == 'OK '
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
