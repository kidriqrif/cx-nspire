"""Regression guard for ibcore.sf3 (3 significant figures).

    python check_sf3.py

The bug: rounding a value up across a power of ten gave 4 s.f. (9.996 -> '10.00').
"""
import sys
sys.path.insert(0, 'tests')
import harness  # noqa: F401  (sets sys.path, fake cas)
from ibcore import sf3

CASES = {
    9.996: '10.0', 99.96: '100', 999.6: '1000',   # power-of-ten boundaries
    1.41421: '1.41', 0.7853: '0.785', 15.24: '15.2',
    0.0: '0', 0.0012345: '0.00123', 1234567.0: '1.23 x 10^6',
    -9.996: '-10.0', 6.0: '6.00',
}
bad = 0
for v, want in CASES.items():
    got = sf3(v)
    ok = got == want
    bad += not ok
    print('%-5s sf3(%s) = %r' % ('OK' if ok else 'FAIL', v, got) + ('' if ok else ' want %r' % want))
print('failures', bad)
sys.exit(1 if bad else 0)
