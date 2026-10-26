"""Write the keying-in guide as a tiny PDF sized for the CX screen (320x240).

    python make_keying_pdf.py OUT.pdf [OUT2.pdf.tns ...]

Only the built-in Courier fonts are used (nothing embedded), so the file is a
few KB. On the calculator open the .pdf.tns copy with nPDF (Ndless).
Every example here is checked by keychk.py against ibcore.norm and Giac.
"""
import sys

W, H = 320, 240

LEGEND = [
    ('x^2', '[x\xb2]  (shows **2, fine)'),
    ('^  any power', '[^]'),
    ('sqrt(', '[ctrl] [x\xb2]'),
    ('e^(   (exp)', '[e^x]  types exp(  close with )'),
    ('ln(', '[ctrl] [e^x]'),
    ('log(  base 10', '[ctrl] [10^x]  types log10('),
    ('sin(  cos(  tan(', '[trig]  [shift][trig]  [ctrl][trig]'),
    ('pi', '[pi] key'),
    ('|  modulus', '[shift] [=]'),
    ('i  complex', 'letter i'),
    ('"  quote', '[ctrl] [\xd7]'),
    ('<   >', '[ctrl][-]   [shift][+]'),
    ('_  (log_3)', '[shift] [-]'),
    ('negative', '[(-)] or [-]'),
]

# (function type, text to type, hint, jump code)
EXAMPLES = [
    ('Polynomial', '-2x^4+3x^3-x/2+7', 'leading minus: [(-)]', '511'),
    ('Rational', '(2x^2-3x+1)/((x-1)(x+2)^2)', 'bracket the whole top and bottom', '511'),
    ('Root / power', 'x^2sqrt(4-x^2)+(x^2+1)^(1/3)', 'cube root = ^(1/3)', '511'),
    ('Exponential', '3e^(-2x+1)-2^(x+1)+e^-x', 'e^( = [e^x]; e^-x needs no brackets', '511'),
    ('Logarithm', 'ln(x^2+1)-2log(x)+ln(x)/ln(3)', 'log=base 10; log3(x): ln(x)/ln(3)', '511'),
    ('Log equation', 'log_3(x)+log_3(x-8)=2', 'log_b( only in this solver', '121'),
    ('Trig', '3sin(2x-pi/3)^2+cos(x/2)', 'sin^2(u): type sin(u)^2; theta: t', '511'),
    ('Trig equation', '2sin(2x-pi/3)=1', 'then d/r and the interval', '331'),
    ('Reciprocal trig', 'sec(x)^2-cosec(2x)+cot(x)', 'type the letters; csc also ok', '511'),
    ('Inverse trig', 'arcsin(x/2)+arctan(3x^2)', 'asin( acos( atan( also ok', '511'),
    ('Modulus', '|2x-3|=|x+1|', '| = [shift][=]; nested: abs(abs(x)-1)', '232'),
    ('Composite', 'ln(sqrt(1+e^(2x)))', 'close every bracket', '511'),
    ('Product/quot.', 'x^3e^(-x^2)/(1+x)', 'no * needed: 2x(x+1), x^2y', '511'),
    ('Implicit x,y', 'x^2y+y^3=2x+1', 'then the point: (1,1)', '514'),
    ('Diff. eqn', '(x^2+y^2)/(xy)', 'type only the right side of dy/dx =', '573'),
    ('Complex', '1+sqrt(3)i', 'then n = 5 for z^5 (De Moivre)', '132'),
]

PITFALLS = [
    ('sinx^2', 'means sin(x^2)', 'sin(x)^2'),
    ('sin^2(x)', 'error', 'sin(x)^2'),
    ('1/2x', 'means x/2', '1/(2x)'),
    ('theta', 'becomes t*h*e*t*a', 't'),
    ('f(x)=x^2', 'f(x) breaks it', 'x^2'),
    ('||x|-1|', 'error', 'abs(abs(x)-1)'),
    ('inf, oo', 'not supported', '-'),
    ('log(x)', 'is base 10', 'ln(x) for base e'),
]


def esc(s):
    b = s.encode('cp1252')
    return b.replace(b'\\', b'\\\\').replace(b'(', b'\\(').replace(b')', b'\\)')


class Page:
    def __init__(self):
        self.ops = []

    def text(self, x, y, s, font='F1', size=8):
        self.ops.append(b'BT /%s %g Tf %g %g Td (' % (font.encode(), size, x, y) + esc(s) + b') Tj ET')

    def line(self, x1, y1, x2, y2, gray=0.6):
        self.ops.append(b'%g G 0.5 w %g %g m %g %g l S' % (gray, x1, y1, x2, y2))

    def bar(self, y, h, gray=0.88):
        self.ops.append(b'%g g 0 %g %g %g re f 0 g' % (gray, y, W, h))


def title(p, t, n, total):
    p.bar(H - 18, 18, 0.15)
    p.ops.append(b'1 g')
    p.text(6, H - 13, t, 'F2', 10)
    p.text(W - 36, H - 13, '%d/%d' % (n, total), 'F1', 8)
    p.ops.append(b'0 g')


def pages():
    total = 4
    out = []
    p = Page()
    title(p, 'Keying in: KhiCAS keys', 1, total)
    y = H - 32
    p.text(6, y, 'To get', 'F2', 8)
    p.text(118, y, 'Press', 'F2', 8)
    y -= 4
    p.line(4, y, W - 4, y, 0)
    for a, b in LEGEND:
        y -= 14
        p.text(6, y, a, 'F2', 8)
        p.text(118, y, b, 'F1', 8)
        p.line(4, y - 4, W - 4, y - 4)
    out.append(p)
    for part in (0, 1):
        p = Page()
        title(p, 'Examples (type this)  code', 2 + part, total)
        y = H - 22
        for k, (ty, s, hint, code) in enumerate(EXAMPLES[part * 8:part * 8 + 8]):
            y -= 26
            if k % 2:
                p.bar(y - 8, 26)
            p.text(6, y + 7, ty, 'F2', 7.5)
            p.text(W - 26, y + 7, code, 'F2', 8)
            p.text(6, y - 3, s, 'F2', 9)
            p.text(W - 4 - 4.2 * len(hint), y - 3, hint, 'F1', 7)
        out.append(p)
    p = Page()
    title(p, 'Pitfalls', 4, total)
    y = H - 32
    p.text(6, y, "Don't type", 'F2', 8)
    p.text(96, y, 'because', 'F2', 8)
    p.text(204, y, 'Type', 'F2', 8)
    y -= 4
    p.line(4, y, W - 4, y, 0)
    for a, b, c in PITFALLS:
        y -= 17
        p.text(6, y, a, 'F2', 8.5)
        p.text(96, y, b, 'F1', 8)
        p.text(204, y, c, 'F2', 8.5)
        p.line(4, y - 5, W - 4, y - 5)
    y -= 18
    p.text(6, y, 'Codes: type on the main menu, e.g. 511.', 'F1', 8)
    out.append(p)
    return out


def build(pgs):
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)

    f1 = add(b'<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>')
    f2 = add(b'<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold /Encoding /WinAnsiEncoding >>')
    pages_id = len(objs) + 1 + 2 * len(pgs) + 1
    kids = []
    for p in pgs:
        data = b'\n'.join(p.ops)
        c = add(b'<< /Length %d >>\nstream\n' % len(data) + data + b'\nendstream')
        kids.append(add(b'<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %d %d] /Contents %d 0 R '
                        b'/Resources << /Font << /F1 %d 0 R /F2 %d 0 R >> >> >>'
                        % (pages_id, W, H, c, f1, f2)))
    cat = add(b'<< /Type /Catalog /Pages %d 0 R >>' % pages_id)
    assert add(b'<< /Type /Pages /Kids [%s] /Count %d >>'
               % (b' '.join(b'%d 0 R' % k for k in kids), len(kids))) == pages_id
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


if __name__ == '__main__':
    pdf = build(pages())
    for path in sys.argv[1:]:
        with open(path, 'wb') as f:
            f.write(pdf)
    print('%d bytes, %d pages' % (len(pdf), 4))
