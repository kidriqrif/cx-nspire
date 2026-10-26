# Builder brief: IB Math AA HL step solver (KhiCAS on TI-Nspire CX II)

Project root: the folder containing `calc/` and `dev/`.
- `calc/` = files copied to the calculator. `ibcore.py` (shared runtime), `main.py` (topic menu),
  `ibdiff.py` (REFERENCE module - read it first and copy its style).
- `dev/` = desktop tooling. `cas.py` fakes KhiCAS's `cas.caseval` using real Giac (giacpy),
  `harness.py` runs a solver with scripted inputs, `run_tests.py`, `check_mpy.py`.

Python for tools: Python 3 with `giacpy` and `mpy-cross==1.12` (`pip install giacpy mpy-cross==1.12`).
Run from `dev/` with `PYTHONIOENCODING=utf-8`:
- `python run_tests.py <module> -v`   (your tests in `dev/tests/test_<module>.py`)
- `python check_mpy.py <module>`      (MicroPython 1.12 compile + lint + size)
- quick look: `python harness.py <module> <fn> input1 input2 ...` (32-col output)

## Who uses it
IB Diploma student, Math AA HL (guide first assessment 2021, NEVER newer), exams Nov 2026.
Goal: ANY in-scope computational question keyed in gets a genuine, exam-script breakdown of steps to the
answer. Printing only Giac's final result is NOT acceptable: decompose into the working a mark scheme
expects, calling Giac for each small sub-step.

## Output style (student's standing rules)
- Exam-script working, line by line; no explanatory prose after steps. Name a rule only where a mark
  scheme would ("chain rule", "by parts", "cover-up", "factor theorem", "sine rule", "l'Hopital").
- Final answer via `ans(label, expr)`: prints `ANS: label = exact` and, when irrational, `~ 3 s.f.`
  (a spaced sum is kept as typed per term; plain text with words is printed unchanged; decimals -> 3 s.f.).
  Exact by default (surds, fractions, pi, e, ln),
  simplest form. Radians unless the user chooses degrees. Indefinite integrals end with ` + C`.
- IB notation in display (pp() handles e^x, arcsin, ln|x|, log = base 10). Lines are wrapped at 32 chars
  automatically by out(); keep labels short.
- Stay inside AA HL scope (see `dev/SCOPE.md`). If out of scope, print one line saying so.

## Module contract
```python
# ibxxx.py - <topic> (<syllabus refs>)
from ibcore import *
TITLE = 'Short title'
def solver_a():
    hdr('Title')            # resets pager, prints heading
    f = norm(rhs(ask('f(x) =')))   # ask() echoes the value into the working
    ...
    ans('x', r)
    wait()                  # ALWAYS end with wait()
ITEMS = [('Menu label <=18ch', solver_a), ...]
```
Solvers take no arguments. Errors: G() raises GErr; ibcore.run() catches it and returns to the menu,
so do not wrap everything in try/except. Never use bare `except:`.

## ibcore API (do NOT edit ibcore.py; define private helpers `_name` in your module instead)
- `G(cmd)` evaluate Giac string -> str ('^' powers; raises GErr). `Gs(cmd)` same but '' on error.
- `S(e)` best simplified form (shortest of raw/normal/simplify; skips simplify on trig).
  `N(e)` normal. `D(e,v)` diff. `I(e,v)` integrate (no +C). `F(e)` float or None.
- `GL(cmd)` -> python list of item strings from a Giac list result. `parse_list(s)`.
- `bad(r)` True if result has undef/unevaluated integrate/erf/rootof.
- strings: `norm(s)` (user input -> Giac syntax: implicit *, ** -> ^, log -> log10, |x| -> abs),
  `rhs(s)`, `lhs0(s)` ('a=b' -> '(a)-(b)'), `split_terms(s)`, `sign_body(t)`, `join_signed(parts)`,
  `unwrap(s)`, `split_top(s,ch)`, `split_factors(s)` -> (neg, [[op,f],...]), `has(s,v)`, `isnum(r)`, `has_var(r)`.
- display: `pp(s)` pretty one expression, `ps(s)` pretty a sum with spaced signs, `INT()` integral sign,
  `out(line)`, `hdr(title)`, `wait()`, `sf3(float)`, `ans(label, expr, approx=1)`.
- input: `ask(prompt, default)` raw str, `askx` normalised expression, `askn` exact number expression,
  `askv(prompt, default)` comma list -> normalised list, `yes(prompt, 'y')`.
- `CFG`, `ST`, `LET`, `DIG`, `OPN`, `CLS`.

## Giac facts learned (verified with giacpy)
- NEVER use '_' in Giac identifiers (`zz_l` is parsed as a unit). Avoid assignments; if you must, use
  plain names like `zzq` and `purge(zzq)` after. Never `assume()`.
- `simplify` on trig rewrites into tan(x/2) forms: use S() or texpand/tcollect/tsimplify deliberately.
- `solve(eq,x)` -> list (maybe 'list[...]'): use GL(). Empty list = no real solution.
  `zeros` of an irreducible cubic returns `rootof(...)` -> fall back to `fsolve(eq,x)` / `proot([coeffs])`
  numeric and say "(GDC)". `czeros`/`csolve` for complex.
- `integrate` adds no constant, gives `ln(abs(x))`; non-elementary -> erf/unevaluated (use bad()).
- `series(f,x=0,n)` / `taylor` include an `order_size` term: strip it.
- `desolve(y'=..., y)` uses `c_0` for constants; `desolve([y'=..., y(0)=1], y)` for IVPs.
- `limit(f,x,a)`, `limit(f,x,inf)`, one-sided `limit(f,x,0,1)`.
- stats: `normald_cdf(mu,sigma,x)`, `normald_cdf(mu,sigma,a,b)`?, `normald_icdf(mu,sigma,p)`,
  `binomial(n,p,k)` = P(X=k), `binomial_cdf(n,p,k)` = P(X<=k), `comb`, `perm`.
- linear algebra: `linsolve([eqs],[vars])`, `rref(M)`, `det`, `inv`, `cross`, `dot`, `l2norm`.
- `factor`, `partfrac(f,x)`, `quo(p,q,x)`, `rem(p,q,x)`, `degree(p,x)`, `coeff(p,x,k)`, `numer`, `denom`,
  `expand`, `subst(e,x=a)` or `subst(e,[x,y],[a,b])`, `texpand`, `tcollect`, `abs`, `arg`, `re`, `im`, `conj`.
- On the calculator lists come back wrapped; ibcore already normalises, so treat results like giacpy's.

## Hard constraints (MicroPython 1.12, checked by check_mpy.py)
- No f-strings, walrus, annotations, `re`, recursion; avoid str.partition/center/ljust/rjust/zfill;
  `math.log10` may be missing (use math.log(x)/math.log(10)). Use `%` or `+` string building.
- Bounded loops only. Keep each module <= 13000 bytes MINIFIED (check_mpy.py; it is compiled on a small heap). If your topic does
  not fit, split it into two modules (e.g. `ibode.py` + `iblim.py`), give each TITLE/ITEMS, and report the
  extra module name so it can be added to main.py.
- Only create/edit YOUR files (listed in your task) and `dev/tests/test_<yourmodule>.py`. Other builders
  are editing other modules in parallel. Do not edit ibcore.py, main.py, harness, run_tests, check_mpy.

## Tests (required)
`dev/tests/test_<module>.py` with `MODULE = '<module>'` and `CASES = [(fn, [inputs...], [must_contain], [must_not])]`.
Inputs are consumed in prompt order; '' accepts a default. At least 3 cases per solver, covering normal, edge
and out-of-scope inputs, with the EXACT expected final answer in must_contain (spaces are ignored).
Hand-check each expected answer mathematically - do not just copy what the code prints.
Iterate until `run_tests.py <module>` and `check_mpy.py <module>` are all green.

## Runtime notes
- ibcore.run() calls reset() before each solver: if a previous result contained `rootof`, the Giac context
  is restarted (Giac keeps hidden state after such results that changes later `factor` output).
- pp() gathers each term as numbers, constants, x^n, functions over one denominator (`1/e/2` -> `1/(2e)`);
  terms containing a lone `1` factor are left as written (substitution lines).
