# IB Math AA HL step solver for KhiCAS (TI-Nspire CX / CX II)

Menu-driven MicroPython app for KhiCAS (Ndless). Every solver prints exam-script working: the method a
mark scheme expects, intermediate lines, `ANS:` in exact simplest form, and a 3 s.f. value when irrational.
Scope: IB Math AA HL, guide first assessment 2021. All maths is done by KhiCAS's Giac engine via
`cas.caseval` (there is no `giac` module in KhiCAS; the app detects `cas`/`xcas` itself).

## Install
0. Prerequisites: Ndless, then KhiCAS. Ndless r2022 supports CX / CX CAS OS 4.0.3.93, 4.2.0.532,
   4.4.0.532, 4.5.0.1180, 4.5.3.14, 4.5.4.48, 4.5.5.79 and CX II OS 5.2.0.771, 5.3.0.564, 6.2.0.333,
   6.4.0.74. A CX II cannot be downgraded (boot2 minimum-OS lock), so never update the OS past a
   supported one. Same app files for CX and CX II; the CX is slower, so heavy steps take longer.
1. Copy **all 24 files in `dist/`** (`main.py.tns`, `ibcore.py.tns`, `ib*.py.tns`) plus
   `dev/ibsetup.py.tns` to the calculator (the same files are ready to copy in `kit/`, see below) (n-link or TI-Nspire computer software), into the **Xcas**
   folder KhiCAS created (the folder holding `session.xw.tns`). Keep the names exactly. They are split
   into modules so each fits the calculator's small Python memory; only the topic you open is loaded.
2. Open KhiCAS (Home > My Documents > ndless > khicas).
3. Switch to MicroPython: type `python` on an empty line (or shift + `)` then 8). `print(type(1))`
   must show `<class 'int'>`; if not, you are still in Xcas's Python-compatible mode.
4. KhiCAS's `import` only finds `name.py`, not `name.py.tns`, and the computer software only sends
   `.tns` files. Once (and again after uploading new versions) make the `.py` copies on the calculator:
   `f=open("ibsetup.py.tns")`, `s=f.read()`, `exec(s)` (quotes: ctrl + ×). It prints `ok: 24 files`.
5. Type `from main import *` and press enter. Later in the same session, type `main()`.

On an original CX Ndless is lost on every reboot: re-run `ndless/ndless_installer_...` (language
English; on OS 4.5.5 press the key for your Boot1, 3.0.0 -> `3`, 4.0.1 -> `4`) before opening KhiCAS.

Optional first-run check: `from cas import caseval` then `caseval("diff(x^2,x)")` should give `2*x`.

## Using it
- Type the menu number and press enter; `0` goes back.
- Jump codes: each menu and solver title shows its code, e.g. `== Differentiate [511] ==`. Type the
  code on the main menu (`511`) to go straight there; on a topic-group menu the first digit is implied
  (`11`).
- Search: type a word on the main menu (`parts`, `normal`, `bayes`) to list matching solvers with codes.
- Each solver ends with `[enter] = again, 0 = menu`: enter reruns the same solver.
- KhiCAS pre-fills each input box with your previous answer. Type over it; an unedited repeat of your
  previous expression on an optional prompt counts as blank.
- Long output pauses at `-- more --` (press enter). Main menu > Settings: line width, lines per page,
  Unicode symbols, paging. If `∫ √ π` show as boxes, set Unicode symbols to `n`.
- Typing maths: `3x^2+5x`, `2sin(x)`, `sinx`, `e^(2x)`, `e^-x`, `ln(x)`, `log(x)` (= base 10), `sqrt(x)`,
  `|x|`, `pi`, `arcsin(x)`, `(x+1)/(x-1)`. Write powers of functions as `sin(x)^2` (not `sin^2x`).
  Use `t` for theta.
- `ANS:` lines are exact; `~` lines are 3 s.f. Indefinite integrals end in `+ C`.

## Menu map (80 solvers)
| Topic | Modules and solvers |
|---|---|
| Number & algebra | **Sequences/finance**: arithmetic, geometric (incl. S∞), sigma, compound interest/depreciation, nPr/nCr · **Logs/binom/parfrac**: exp/log equations, binomial (natural, fractional, negative n), partial fractions with cover-up · **Complex/systems**: forms and operations, De Moivre, nth roots, conjugate roots, 3×3 systems by row reduction |
| Functions | **Roots/quadratics**: polynomial roots by factor theorem, quadratic analysis incl. discriminant parameter questions, remainder/factor theorem · **Lines/comp/rational**: lines, composite/inverse, rational-function asymptotes, odd/even · **Inequal./modulus**: polynomial/rational inequalities with sign table, modulus equations and inequalities |
| Trig & geometry | **Triangles/solids**: sine/cosine rule incl. ambiguous case, area, arcs/sectors, 3D solids · **Trig values/ident**: exact values, inverse, ratios from one ratio, compound angles, identities (expand/simplify/verify) · **Trig eq/graphs**: equations in an interval, graph features · **Vectors**: operations, angle, lines, intersections/skew, vector motion · **Lines/planes**: plane equations, intersections, angles |
| Stats & probability | **Data/regression**: summary, outliers, transforms, regression and r · **Binomial/normal**: binomial, normal, unknown μ or σ · **Probability/Bayes**: rules/Venn, tree and Bayes, draws from a bag · **Random variables**: discrete (unknown k, E, Var, fair game), continuous pdf (k, P, mode, median, E, Var) |
| Calculus | **Differentiation**: rule-by-rule working (chain, product, quotient, textbook forms), first principles, higher, implicit · **Tangents/optimise**: tangent and normal, f'(x)=k, optimisation incl. end points, related rates · **Curves/kinematics**: stationary points, inflexion, concavity, increasing/decreasing, s(t) motion · **Integration**: term by term, linear composites, reverse chain, substitution, by parts (LIATE with override, repeated, cyclic), partial fractions, trig identities · **Areas/volumes**: definite integrals, f from f' and a point, areas (x-axis, two curves, y-axis), volumes of revolution, v(t)/a(t) kinematics · **Limits/series**: l'Hôpital, Maclaurin limits, Maclaurin series by derivatives/substitution/product/ODE/integration · **Diff. equations**: Euler, separable, homogeneous (y = vx), integrating factor |

## Calculator notes
Runs on an original TI-Nspire CX (OS 4.5.5.79, Ndless r2022, KhiCAS CX build). The CX II should work
with its own KhiCAS build but has not been tried.
- Python memory: if you get `Out of memory` or `Memory full`, restart KhiCAS and start MicroPython
  before doing heavy Xcas work.
- If `∫ √ π` show as boxes, set Settings > Unicode `n`; line width is Settings > Chars per line
  (default 32).
- Press ON to stop a long computation.

## Kit
`kit/` is a ready-to-copy bundle:
- `app-files/`: the 24 `.py.tns` app files (same as `dist/`); `app-files-py/`: the same files named
  `.py`, for transfer tools that keep file names (then step 4 is not needed).
- `ibsetup.py.tns`: the setup script from step 4.
- `ndless/khicas.tns`: KhiCAS for the original CX (third-party, see `THIRD_PARTY.md`).
- `keying.pdf`: keying-in guide sized for the CX screen (`keying.pdf.tns` for nPDF on the calculator);
  `keying-phone.pdf`: the same guide for a phone or PC. Every example is checked by `dev/keychk.py`.

## Exams
IB does not allow CAS or Ndless-modified calculators in exams. Use this for revision only, and restore
the calculator to Press-to-Test before Papers 2 and 3.

## Development (PC)
`dev/` holds the tooling. Requires `pip install giacpy mpy-cross==1.12`.
```
cd dev
python run_tests.py          # 1150 solver tests against real Giac
python check_mpy.py          # MicroPython 1.12 compile + lint + size limits
python build.py              # calc/*.py -> dist/*.py.tns (minified)
python sim_main.py           # drive the whole menu with scripted keys
python fuzz.py               # 9 blunt input profiles x every solver: crashes, hangs, leaks
python keychk.py             # every keying-guide example through its solver
```
`dev/BRIEF.md` documents the core API and conventions for adding solvers.
