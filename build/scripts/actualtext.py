"""Wrap every /ReversedChars glyph run in an /ActualText span holding the
run's logical Persian string, so any extractor returns correct text.

Typst paints RTL text as visually ordered runs inside /ReversedChars marked
content. We keep the glyph operators untouched (the page still looks
identical) and replace the marker with a /Span whose /ActualText is the run
read in logical order, which is what PDF readers prefer when copying or
searching.
"""
import re
import sys

import pymupdf

RUN = re.compile(rb'/ReversedChars\s+BMC(.*?)\bEMC\b', re.S)
TOK = re.compile(rb'/([A-Za-z0-9]+)\s+[\d.]+\s+Tf'
                 rb'|\(((?:\\.|[^\\)])*)\)\s*(?:Tj|TJ|)'
                 rb'|\[((?:[^\[\]\\]|\\.)*)\]\s*TJ')
HEXOCT = re.compile(rb'\\([0-7]{1,3})')


def cmap_of(doc, xref):
    kind, val = doc.xref_get_key(xref, 'ToUnicode')
    if kind != 'xref':
        return {}
    data = doc.xref_stream(int(val.split()[0]))
    out = {}
    for a, b in re.findall(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', data):
        try:
            out[int(a, 16)] = bytes.fromhex(b.decode()).decode('utf-16-be')
        except Exception:
            pass
    return out


def font_maps(doc, page):
    maps = {}
    kind, val = doc.xref_get_key(page.xref, 'Resources/Font')
    if kind != 'dict':
        return maps
    for name, ref in re.findall(r'/([A-Za-z0-9]+)\s+(\d+)\s+0\s+R', val):
        maps[name.encode()] = cmap_of(doc, int(ref))
    return maps


def run_text(block, maps, cur=None):
    units = []
    for m in TOK.finditer(block):
        if m.group(1):
            cur = m.group(1)
            continue
        seq = m.group(2) if m.group(2) is not None else m.group(3)
        if seq is None:
            continue
        cmap = maps.get(cur, {})
        for code in HEXOCT.finditer(seq):
            s = cmap.get(int(code.group(1), 8))
            if s:
                units.append(s)
    return ''.join(reversed(units))


def fix(src, dst):
    doc = pymupdf.open(src)
    n = 0
    for page in doc:
        maps = font_maps(doc, page)
        for xref in (page.get_contents() or []):
            data = doc.xref_stream(xref)
            if not data or b'ReversedChars' not in data:
                continue
            edits = []
            for m in RUN.finditer(data):
                word = run_text(m.group(1), maps)
                if not word.strip():
                    continue
                hexs = word.encode('utf-16-be').hex().upper().encode()
                inner = m.group(1).lstrip()
                edits.append((m.start(), m.end(),
                              b'/Span<</ActualText<FEFF' + hexs + b'>>>BDC '
                              + inner + b'\nEMC'))
                n += 1
            if not edits:
                continue
            buf = bytearray(data)
            for s, e, rep in sorted(edits, reverse=True):
                buf[s:e] = rep
            doc.update_stream(xref, bytes(buf))
    doc.save(dst, garbage=3, deflate=True)
    doc.close()
    return n


if __name__ == '__main__':
    print(fix(sys.argv[1], sys.argv[2]))
