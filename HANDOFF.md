# Handoff: IB Math AA HL solver for KhiCAS (TI-Nspire CX)

## Status
- App: complete. 22 topic modules plus `main.py` and `ibcore.py`, built into `dist/` as 24 `.py.tns` files. 1150 tests pass on PC (`dev/run_tests.py`); `dev/fuzz.py` finds no crashes, hangs or leaked Giac internals.
- Runs on an original TI-Nspire CX: OS 4.5.5.79, Ndless r2022, KhiCAS CX build.
- Working style: each solver prints the lines a mark scheme expects (method, substitution, simplification), then `ANS:` in exact form and a `~` 3 s.f. value when the answer is irrational.

## Calculator setup (original CX)
- OS: 4.5.5.79 (newest TI release for the original CX). Check Settings > Status first; do not update past a version Ndless supports.
- Ndless: `ndless_installer_4.5.5-6.2.0-6.4.0.tns` + `ndless_resources.tns` from `ndless-r2022.zip`, in a top-level `ndless` folder. The installer asks for the boot1 version (Settings > Status > About). Re-run it after every reboot.
- KhiCAS: the CX build, `khicas.zip` > `ndless/khicas.tns` (also in `kit/ndless/` and `gdc/to-calculator/ndless/`). `khicas52.zip` is the CX II build and does not run on the original CX.
- App files: `dist/*.py.tns` (or `kit/app-files/`) go into the `Xcas` folder next to `session.xw.tns`; then run `ibsetup.py.tns` once (README step 4).

## Files
- `calc/`: source modules. `dist/`: minified `.py.tns` build. `dev/`: tooling, tests (`dev/tests/`), `BRIEF.md` (core API and conventions), `SCOPE.md`.
- `kit/`: ready-to-copy bundle (app files, setup script, KhiCAS, keying-in guide PDFs).
- `downloads/`, `gdc/downloads/`: third-party archives (Ndless, KhiCAS); see `THIRD_PARTY.md`.

## Commands (PC)
- Python 3 with `giacpy` and `mpy-cross==1.12`. Set `PYTHONIOENCODING=utf-8` on Windows.
- From `dev/`: `python run_tests.py`, `python check_mpy.py` (MicroPython 1.12 compile and size limits: topic module <= 13000 bytes minified, `ibcore` <= 14500), `python build.py`, `python fuzz.py`, `python keychk.py`.

## Notes
- PC tests run under CPython, and KhiCAS's MicroPython 1.12 lacks some methods (for example `str.isalnum`). Keep to the subset `ibcore.py` already uses.
- A CX II cannot be downgraded (boot2 minimum-OS lock), and backSpire only supports OS 5.2, 5.3 and 6.2.

## Possible polish
- Spacing and ordering in some printed forms: `x^2 (2-x)`, `ln(2)*2^x`, `8pi (3)^2`.
- Some optimisation answers print Giac's unsimplified form.
