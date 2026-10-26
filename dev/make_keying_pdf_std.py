"""Keying-in guide as a normal portrait PDF for reading on a phone / PC.

    python make_keying_pdf_std.py OUT.pdf

A4 portrait, built-in Helvetica only (nothing embedded), so a few KB. Shares
its data (and so its keychk.py verification) with make_keying_pdf.py.
"""
import sys
from make_keying_pdf import LEGEND, EXAMPLES, PITFALLS, esc

W, H = 595, 842  # A4 portrait, points
M = 48           # margin


class Page:
    def __init__(self):
        self.ops = []

    def text(self, x, y, s, font='F1', size=11):
        self.ops.append(b'BT /%s %g Tf %g %g Td (' % (font.encode(), size, x, y) + esc(s) + b') Tj ET')

    def line(self, x1, y1, x2, y2, gray=0.75):
        self.ops.append(b'%g G 0.7 w %g %g m %g %g l S' % (gray, x1, y1, x2, y2))

    def bar(self, x, y, w, h, gray):
        self.ops.append(b'%g g %g %g %g %g re f 0 g' % (gray, x, y, w, h))


def wrap(s, n):
    out, line = [], ''
    for w in s.split(' '):
        if len(line) + len(w) + 1 > n and line:
            out.append(line)
            line = w
        else:
            line = (line + ' ' + w).strip()
    if line:
        out.append(line)
    return out or ['']


def build(pgs):
    fonts = [
        b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>',
        b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>',
        b'<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>',
    ]
    objs = list(fonts)
    pages_id = len(fonts) + 2 * len(pgs) + 2  # fonts + (content,page)/page + catalog, then Pages
    kids = []
    for p in pgs:
        data = b'\n'.join(p.ops)
        objs.append(b'<< /Length %d >>\nstream\n' % len(data) + data + b'\nendstream')
        cid = len(objs)
        objs.append(b'<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %d %d] /Contents %d 0 R '
                    b'/Resources << /Font << /F1 1 0 R /F2 2 0 R /F3 3 0 R >> >> >>'
                    % (pages_id, W, H, cid))
        kids.append(len(objs))
    cat = len(objs) + 1
    objs.append(b'<< /Type /Catalog /Pages %d 0 R >>' % pages_id)
    objs.append(b'<< /Type /Pages /Kids [%s] /Count %d >>'
                % (b' '.join(b'%d 0 R' % k for k in kids), len(kids)))
    out = b'%PDF-1.4\n'
    offs = []
    for i, o in enumerate(objs):
        offs.append(len(out))
        out += b'%d 0 obj\n' % (i + 1) + o + b'\nendobj\n'
    x = len(out)
    out += b'xref\n0 %d\n0000000000 65535 f \n' % (len(objs) + 1)
    out += b''.join(b'%010d 00000 n \n' % o for o in offs)
    out += b'trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objs) + 1, cat, x)
    return out


def render():
    pgs = [Page()]
    st = {'p': pgs[0], 'y': H - M}

    def newpage():
        st['p'] = Page()
        pgs.append(st['p'])
        st['y'] = H - M

    def need(h):
        if st['y'] - h < M:
            newpage()

    def head(t):
        need(40)
        st['y'] -= 4
        st['p'].text(M, st['y'], t, 'F2', 13)
        st['y'] -= 6
        st['p'].line(M, st['y'], W - M, st['y'], 0.3)
        st['y'] -= 16

    p = st['p']
    p.text(M, st['y'], 'IB AA HL Solver - keying-in guide', 'F2', 17)
    st['y'] -= 16
    p.text(M, st['y'], 'KhiCAS on TI-Nspire CX. Jump code = type on the main menu, e.g. 511.', 'F1', 9)
    st['y'] -= 20

    head('Keys')
    for a, b in LEGEND:
        need(15)
        st['p'].text(M, st['y'], a, 'F3', 10)
        st['p'].text(M + 150, st['y'], b, 'F1', 9.5)
        st['y'] -= 15
    st['y'] -= 10

    head('Examples')
    shade = True
    for ty, s, hint, code in EXAMPLES:
        rows = wrap(hint, 52)
        block = 15 + 13 + 13 * len(rows)  # title + expr + hint rows
        need(block + 10)
        top = st['y']
        if shade:
            st['p'].bar(M - 6, top - block - 2, W - 2 * M + 12, block + 9, 0.94)
        shade = not shade
        st['y'] -= 15
        st['p'].text(M, st['y'], ty, 'F2', 10)
        st['p'].text(W - M - 7 * len(code), st['y'], code, 'F2', 11)
        st['y'] -= 13
        st['p'].text(M + 8, st['y'], s, 'F3', 11)
        for r in rows:
            st['y'] -= 13
            st['p'].text(M + 8, st['y'], r, 'F1', 9)
        st['y'] = top - block - 10

    st['y'] -= 8
    head('Pitfalls')
    st['p'].text(M, st['y'], "Don't type", 'F2', 9.5)
    st['p'].text(M + 150, st['y'], 'because', 'F2', 9.5)
    st['p'].text(M + 330, st['y'], 'type instead', 'F2', 9.5)
    st['y'] -= 4
    st['p'].line(M, st['y'], W - M, st['y'], 0.6)
    st['y'] -= 15
    for a, b, c in PITFALLS:
        need(15)
        st['p'].text(M, st['y'], a, 'F3', 10)
        st['p'].text(M + 150, st['y'], b, 'F1', 9.5)
        st['p'].text(M + 330, st['y'], c, 'F3', 10)
        st['y'] -= 15
    return build(pgs)


if __name__ == '__main__':
    pdf = render()
    for path in sys.argv[1:]:
        with open(path, 'wb') as f:
            f.write(pdf)
    print('%d bytes' % len(pdf))
