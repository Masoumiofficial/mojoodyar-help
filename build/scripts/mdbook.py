"""Convert the guide's Typst source into a plain Persian Markdown book.

Only the markup this document actually uses is handled: chapter pages,
headings, callout blocks, tables, code fences, steps, screenshots,
bullet/ordered lists and inline emphasis. The output is the editable
text companion for the PDF (DOCX source).
"""
import json
import re
import sys

SRC = 'build/guide.typ'
OUT = 'build/guide.md'

INLINE = [
    (re.compile(r'#strong\[([^\]]*)\]'), r'**\1**'),
    (re.compile(r'#raw\("((?:[^"\\]|\\.)*)"\)'), lambda m: '`' + m.group(1).replace('\\"', '"') + '`'),
    (re.compile(r'`([^`]*)`'), lambda m: '`' + m.group(1) + '`'),
]


def inline(text):
    text = text.strip()
    for rx, rep in INLINE:
        text = rx.sub(rep, text)
    return text


def strip_hash(s):
    return s.replace('\\#', '#')


def read_balanced(s, i):
    """s[i] is the opening bracket; return (content, index_after_close)."""
    open_ch = s[i]
    close_ch = ']' if open_ch == '[' else ')'
    depth = 0
    j = i
    in_str = None
    while j < len(s):
        c = s[j]
        if in_str:
            if c == '\\':
                j += 2
                continue
            if c == in_str:
                in_str = None
        elif c == '"':
            in_str = c
        elif c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    return s[i + 1:], len(s)


def parse_tbl(block):
    """Return (header:list[str], rows:list[list[str]])."""
    header = []
    rows = []
    m = re.search(r'header:\s*\(', block)
    if m:
        content, _ = read_balanced(block, m.end() - 1)
        header = [inline(c) for c in re.findall(r'"((?:[^"\\]|\\.)*)"', content)]
    m = re.search(r'rows:\s*\(', block)
    if m:
        content, _ = read_balanced(block, m.end() - 1)
        for row in re.finditer(r'\(([^()]*)\)', content):
            cells = [inline(c) for c in re.findall(r'"((?:[^"\\]|\\.)*)"', row.group(1))]
            if cells:
                rows.append([strip_hash(c) for c in cells])
    return header, rows


def parse_cells(block):
    return [inline(c) for c in re.findall(r'"((?:[^"\\]|\\.)*)"', block)]


def convert(src):
    out = []
    lines = src.split('\n')
    i = 0
    chapter = 0
    in_code = False
    code_buf = []

    def flush_code():
        if code_buf:
            out.append('```text')
            out.extend(code_buf)
            out.append('```')
            out.append('')
            code_buf.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()

        if s.startswith('```'):
            if in_code:
                in_code = False
                flush_code()
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # chapter page
        m = re.match(r'#chpage\("([^"]*)",\s*"([^"]*)",\s*\[(.*?)\],\s*\[(.*?)\]\)', s)
        if m:
            chapter += 1
            num, title, lede, head = m.groups()
            out.append('')
            out.append('# فصل %s — %s' % (num, title))
            out.append('')
            out.append('> ' + inline(lede))
            out.append('')
            out.append('*' + inline(head) + '*')
            out.append('')
            i += 1
            continue

        m = re.match(r'#appx\[(.*?)\]', s)
        if m:
            out.append('')
            out.append('# ' + inline(m.group(1)))
            out.append('')
            i += 1
            continue

        m = re.match(r'#heading\(level:\s*1,.*?\)\[(.*)\]', s)
        if m:
            out.append('')
            out.append('# ' + inline(m.group(1)))
            out.append('')
            i += 1
            continue

        if s.startswith('== '):
            out.append('')
            out.append('## ' + inline(s[3:]))
            out.append('')
            i += 1
            continue
        if s.startswith('=== '):
            out.append('')
            out.append('### ' + inline(s[4:]))
            out.append('')
            i += 1
            continue

        # callouts: #note[ ... ]  (may span lines until closing bracket)
        m = re.match(r'#(note|tip|warn|danger|limit|tested)\[', s)
        if m:
            kind = m.group(1)
            start = i
            text = s[s.index('[', s.index(m.group(0)) - len(m.group(0))) + 0:]
            buf = [line[line.index('[') + 1:]]
            depth = 1
            # walk forward to find closing ']'
            rest = lines[i][line.index('[') + 1:]
            depth = rest.count('[') - rest.count(']') + 1
            if depth <= 0:
                body = rest.rsplit(']', 1)[0]
                i += 1
            else:
                i += 1
                while i < len(lines):
                    buf.append(lines[i])
                    depth += lines[i].count('[') - lines[i].count(']')
                    if depth <= 0:
                        i += 1
                        break
                    i += 1
                body = '\n'.join(buf)
                if ']' in body:
                    body = body.rsplit(']', 1)[0]
            label = {'note': 'نکته', 'tip': 'پیشنهاد', 'warn': 'هشدار',
                     'danger': 'خطر', 'limit': 'محدودیت واقعی', 'tested': 'آزمون‌شده'}[kind]
            body = re.sub(r'\s*\n\s*', ' ', body.strip())
            out.append('')
            out.append('**%s.** %s' % (label, inline(body)))
            out.append('')
            continue

        # step
        m = re.match(r'#step\("([^"]*)",\s*\[(.*?)\],\s*\[', s)
        if m:
            num, title = m.groups()
            rest = s[m.end():]
            buf = [rest]
            depth = rest.count('[') - rest.count(']') + 1
            i += 1
            while depth > 0 and i < len(lines):
                buf.append(lines[i])
                depth += lines[i].count('[') - lines[i].count(']')
                i += 1
            body = '\n'.join(buf).rsplit(']', 1)[0]
            out.append('')
            out.append('**گام %s — %s** %s' % (num, inline(title),
                       inline(re.sub(r'\s*\n\s*', ' ', body))))
            out.append('')
            continue

        # screenshot
        m = re.match(r'#shot\("([^"]*)",\s*"(.*?)"(?:,|\))', s)
        if m:
            img, cap = m.groups()
            out.append('')
            out.append('![%s](%s)' % (inline(cap), img))
            out.append('')
            out.append('*%s*' % inline(cap))
            out.append('')
            i += 1
            continue

        # tables
        if s.startswith('#tbl(') or s.startswith('#tblc('):
            buf = [line]
            depth = line.count('(') - line.count(')')
            i += 1
            while depth > 0 and i < len(lines):
                buf.append(lines[i])
                depth += lines[i].count('(') - lines[i].count(')')
                i += 1
            block = '\n'.join(buf)
            header, rows = parse_tbl(block)
            if header:
                out.append('')
                out.append('| ' + ' | '.join(header) + ' |')
                out.append('|' + '|'.join([' --- '] * len(header)) + '|')
                for r in rows:
                    r = (r + [''] * len(header))[:len(header)]
                    out.append('| ' + ' | '.join(r) + ' |')
                out.append('')
            continue

        if s.startswith('#toc') or s.startswith('//') or s == '':
            out.append('')
            i += 1
            continue

        # list items: normalise Typst markers and run inline formatting
        if s.startswith(('- ', '+ ')):
            body = s[2:].strip()
            buf = [body]
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if (not nxt or nxt.startswith(('#', '```', '|', '>', '==', '![',
                                               '- ', '+ '))):
                    break
                buf.append(nxt)
                i += 1
            out.append('- ' + inline(' '.join(buf)))
            continue

        # plain prose: glue the hard-wrapped source lines of one paragraph
        buf = [s]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (not nxt or nxt.startswith(('#', '```', '|', '>', '==', '!['))
                    or nxt.startswith('**نکته') or nxt.startswith('**پیشنهاد')
                    or nxt.startswith('**هشدار') or nxt.startswith('**خطر')
                    or nxt.startswith('**محدودیت') or nxt.startswith('**آزمون')):
                break
            buf.append(nxt)
            i += 1
        out.append(inline(' '.join(buf)))
        out.append('')

    flush_code()
    text = '\n'.join(out)
    # drop leftover Typst scaffolding that has no Markdown equivalent
    text = re.sub(r'#pagebreak\(\)', '', text)
    text = re.sub(r'#v\([^)]*\)', '', text)
    text = re.sub(r'#text\([^)]*\)\[([^\]]*)\]', r'\1', text)
    text = re.sub(r'#block\([^\n]*$', '', text, flags=re.M)
    text = re.sub(r'^\]\)$', '', text, flags=re.M)
    text = re.sub(r'^\]$', '', text, flags=re.M)
    text = re.sub(r'\s*\]\)\s*$', '', text)
    text = re.sub(r'^#[a-z]+\(.*$', '', text, flags=re.M)
    return text


if __name__ == '__main__':
    src = open(SRC).read()
    if '// MD-START' in src:
        src = src.split('// MD-START', 1)[1]
    md = convert(src)
    md = re.sub(r'\n{3,}', '\n\n', md)
    open(OUT, 'w').write(md)
    print('wrote', OUT, len(md.split()), 'words')
