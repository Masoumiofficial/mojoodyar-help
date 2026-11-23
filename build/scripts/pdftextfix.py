"""Improve text extraction for the Typst-rendered RTL PDF.

Typst paints Persian as visually ordered glyph runs; each multi-character
glyph (lam-alef, heh+hamza, letter+ZWNJ, alef+fathatan) is one glyph whose
ToUnicode entry lists its code points in visual order. Reversing those
multi-code-point targets makes extraction engines emit the logical
sequence. Only /ToUnicode changes: glyph painting, layout, links and
bookmarks are untouched.

usage: python3 pdftextfix.py in.pdf out.pdf
"""
import re
import sys
import pymupdf


def fix_tounicode(data: bytes) -> bytes:
    txt = data.decode('latin-1')

    def one(m):
        code, hexs = m.group(1), m.group(2)
        if len(hexs) <= 4:
            return m.group(0)
        try:
            s = bytes.fromhex(hexs).decode('utf-16-be')
        except Exception:
            return m.group(0)
        s = ''.join(reversed(s))
        return '<%s> <%s>' % (code, s.encode('utf-16-be').hex().upper())

    return re.sub(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', one, txt).encode('latin-1')


def fix(src, dst):
    doc = pymupdf.open(src)
    seen, n = set(), 0
    for page in doc:
        for font in page.get_fonts(full=True):
            fx = font[0]
            if fx in seen:
                continue
            seen.add(fx)
            kind, val = doc.xref_get_key(fx, 'ToUnicode')
            if kind != 'xref':
                continue
            tx = int(val.split()[0])
            data = doc.xref_stream(tx)
            if data is None:
                continue
            new = fix_tounicode(data)
            if new != data:
                doc.update_stream(tx, new)
                n += 1
    doc.save(dst, garbage=3, deflate=True)
    doc.close()
    return n


if __name__ == '__main__':
    print(fix(sys.argv[1], sys.argv[2]))
