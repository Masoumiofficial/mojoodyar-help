"""Build the editable DOCX companion from build/guide.md."""
import re
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

NAVY = RGBColor(0x10, 0x18, 0x28)
PURPLE = RGBColor(0x55, 0x35, 0xCF)
BODY = RGBColor(0x26, 0x32, 0x44)
GREY = RGBColor(0x66, 0x70, 0x85)
FONT = 'Vazirmatn'

INLINE = re.compile(r'(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)')


def rtl(par):
    pPr = par._p.get_or_add_pPr()
    bidi = OxmlElement('w:bidi')
    pPr.append(bidi)
    par.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    return par


def style_run(run, size=10.5, bold=False, color=BODY, font=FONT):
    run.font.name = font
    run.font.size = Pt(size)
    run.bold = bold
    run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rFonts.set(qn(attr), font)
    rtl_el = OxmlElement('w:rtl')
    rtl_el.set(qn('w:val'), '1')
    rPr.append(rtl_el)
    return run


def add_inline(par, text, size=10.5, color=BODY):
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            style_run(par.add_run(part[2:-2]), size, True, NAVY)
        elif part.startswith('`') and part.endswith('`'):
            r = style_run(par.add_run(part[1:-1]), size - 0.5, False, PURPLE)
            r.font.name = 'DejaVu Sans Mono'
        elif part.startswith('*') and part.endswith('*') and len(part) > 2:
            style_run(par.add_run(part[1:-1]), size, False, GREY)
        else:
            style_run(par.add_run(part), size, False, color)


def para(doc, text='', size=10.5, after=6, before=0, align='right', color=BODY):
    p = doc.add_paragraph()
    rtl(p)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.line_spacing = 1.55
    if align == 'center':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if text:
        add_inline(p, text, size, color)
    return p


HEADING_STYLE = {1: 'Heading 1', 2: 'Heading 2', 3: 'Heading 3'}


def heading(doc, text, level):
    p = doc.add_paragraph(style=HEADING_STYLE[level])
    rtl(p)
    p.paragraph_format.space_before = Pt(16 if level == 1 else 12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    size = {1: 17, 2: 13, 3: 11.5}[level]
    color = {1: NAVY, 2: NAVY, 3: PURPLE}[level]
    style_run(p.add_run(text), size, True, color)
    return p


def callout(doc, label, body, kind):
    fill = {'note': 'EFEBFF', 'tip': 'E6FAF7', 'warn': 'FFFAEB',
            'danger': 'FDECEA', 'limit': 'F4F6FA'}[kind]
    bar = {'note': '5535CF', 'tip': '25C6B7', 'warn': 'B54708',
           'danger': 'B42318', 'limit': '667085'}[kind]
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), fill)
    cell._tc.get_or_add_tcPr().append(shd)
    par = cell.paragraphs[0]
    rtl(par)
    par.paragraph_format.line_spacing = 1.5
    style_run(par.add_run(label + '  '), 9.5, True, RGBColor.from_string(bar))
    add_inline(par, body, 9.8)
    doc.add_paragraph()


def table(doc, header, rows):
    t = doc.add_table(rows=len(rows) + 1, cols=len(header))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = True
    for j, h in enumerate(header):
        cell = t.rows[0].cells[j]
        cell.text = ''
        par = cell.paragraphs[0]
        rtl(par)
        style_run(par.add_run(h), 9, True, NAVY)
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:fill'), 'F4F6FA')
        cell._tc.get_or_add_tcPr().append(shd)
    for i, row in enumerate(rows, start=1):
        row = (row + [''] * len(header))[:len(header)]
        for j, val in enumerate(row):
            cell = t.rows[i].cells[j]
            cell.text = ''
            par = cell.paragraphs[0]
            rtl(par)
            par.paragraph_format.line_spacing = 1.35
            add_inline(par, val, 9)
    doc.add_paragraph()
    return t


def code(doc, lines):
    t = doc.add_table(rows=1, cols=1)
    cell = t.rows[0].cells[0]
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), 'F4F6FA')
    cell._tc.get_or_add_tcPr().append(shd)
    for k, line in enumerate(lines):
        par = cell.paragraphs[0] if k == 0 else cell.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pPr = par._p.get_or_add_pPr()
        pPr.append(OxmlElement('w:bidi')) if False else None
        r = par.add_run(line)
        r.font.name = 'DejaVu Sans Mono'
        r.font.size = Pt(8.5)
        r.font.color.rgb = NAVY
        rPr = r._element.get_or_add_rPr()
        rFonts = OxmlElement('w:rFonts')
        for attr in ('w:ascii', 'w:hAnsi', 'w:cs'):
            rFonts.set(qn(attr), 'DejaVu Sans Mono')
        rPr.append(rFonts)
        ltr = OxmlElement('w:rtl')
        ltr.set(qn('w:val'), '0')
        rPr.append(ltr)
    doc.add_paragraph()


def image(doc, path, caption):
    try:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(path, width=Cm(15.2))
        cap = para(doc, caption, 8.5, after=10, color=GREY)
    except Exception as exc:  # pragma: no cover
        print('image failed', path, exc)


def build(md_path, out_path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_height = Cm(29.7)
    sec.page_width = Cm(21.0)
    sec.top_margin = Cm(2.2)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.0)
    sec.right_margin = Cm(2.0)
    # RTL section
    sectPr = sec._sectPr
    bidi = OxmlElement('w:bidi')
    sectPr.append(bidi)

    for lvl in (1, 2, 3):
        st = doc.styles[HEADING_STYLE[lvl]]
        st.font.name = FONT
        st.font.size = Pt({1: 17, 2: 13, 3: 11.5}[lvl])
        rPr = st.element.get_or_add_rPr()
        rFonts = rPr.find(qn('w:rFonts'))
        if rFonts is None:
            rFonts = OxmlElement('w:rFonts')
            rPr.append(rFonts)
        for attr in ('w:ascii', 'w:hAnsi', 'w:cs'):
            rFonts.set(qn(attr), FONT)
        bidi = OxmlElement('w:bidi')
        pPr = st.element.get_or_add_pPr()
        pPr.append(bidi)

    style = doc.styles['Normal']
    style.font.name = FONT
    style.font.size = Pt(10.5)
    style.element.rPr.rFonts.set(qn('w:cs'), FONT)

    # footer
    footer = sec.footer.paragraphs[0]
    rtl(footer)
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style_run(footer.add_run('موجودیار | Mojoodyar — راهنمای کاربری، نسخهٔ ۱٫۰٫۰   |   صفحهٔ '), 8.5, False, GREY)
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), 'PAGE')
    footer._p.append(fld)

    # ---- cover ----
    para(doc, '', after=90)
    p = doc.add_paragraph(); rtl(p); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture('build/assets/mojoodyar-logo.png', width=Cm(4.2))
    p = doc.add_paragraph(); rtl(p); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(18)
    style_run(p.add_run('موجودیار'), 30, True, NAVY)
    p = doc.add_paragraph(); rtl(p); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style_run(p.add_run('Mojoodyar'), 16, False, PURPLE)
    p = doc.add_paragraph(); rtl(p); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    style_run(p.add_run('راهنمای جامع کاربری'), 15, True, BODY)
    p = doc.add_paragraph(); rtl(p); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style_run(p.add_run('افزونهٔ اعلان بازگشت موجودی برای وردپرس و ووکامرس · نسخهٔ ۱٫۰٫۰'), 10, False, GREY)
    p = doc.add_paragraph(); rtl(p); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(30)
    style_run(p.add_run('اتحاد وردپرس · توزیع در ژاکت'), 9.5, False, GREY)
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ---- table of contents (Word field: refresh with F9) ----
    p = doc.add_paragraph(); rtl(p)
    style_run(p.add_run('فهرست مطالب'), 18, True, NAVY)
    p = doc.add_paragraph(); rtl(p)
    add_inline(p, 'این فهرست در Word به‌صورت فیلد ساخته شده است؛ برای به‌روزرسانی شماره صفحه‌ها، روی فهرست راست‌کلیک کنید و «Update Field» را بزنید.', 9, GREY)
    toc_par = doc.add_paragraph(); rtl(toc_par)
    run = toc_par.add_run()
    fld_begin = OxmlElement('w:fldChar'); fld_begin.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'), 'preserve')
    instr.text = 'TOC \\o "1-2" \\h \\z \\u'
    fld_sep = OxmlElement('w:fldChar'); fld_sep.set(qn('w:fldCharType'), 'separate')
    holder = OxmlElement('w:t'); holder.text = 'برای نمایش فهرست، اینجا کلیک کنید و F9 را بزنید.'
    fld_end = OxmlElement('w:fldChar'); fld_end.set(qn('w:fldCharType'), 'end')
    for el in (fld_begin, instr, fld_sep, holder, fld_end):
        run._r.append(el)
    # settings: ask Word to rebuild fields (TOC) when the file is opened
    settings = doc.settings.element
    upd = OxmlElement('w:updateFields')
    upd.set(qn('w:val'), 'true')
    settings.append(upd)
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    lines = open(md_path).read().split('\n')
    i = 0
    in_code = False
    code_buf = []
    while i < len(lines):
        line = lines[i]
        s = line.strip()

        if s.startswith('```'):
            if in_code:
                code(doc, code_buf)
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        m = re.match(r'!\[(.*?)\]\((.*?)\)', s)
        if m:
            caption, path = m.groups()
            image(doc, 'build/' + path, caption)
            i += 1
            continue
        if s.startswith('|') and i + 1 < len(lines) and set(lines[i + 1].strip()) <= set('|- '):
            header = [c.strip() for c in s.strip('|').split('|')]
            rows = []
            i += 2
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            table(doc, header, rows)
            continue
        if s.startswith('# '):
            if s.startswith('# فصل') or s.startswith('# واژه'):
                doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            heading(doc, s[2:].strip(), 1)
            i += 1
            continue
        if s.startswith('## '):
            heading(doc, s[3:].strip(), 2)
            i += 1
            continue
        if s.startswith('### '):
            heading(doc, s[4:].strip(), 3)
            i += 1
            continue
        m = re.match(r'\*\*(نکته|پیشنهاد|هشدار|خطر|محدودیت واقعی|آزمون‌شده)\.\*\*\s*(.*)', s)
        if m:
            label, body = m.groups()
            kind = {'نکته': 'note', 'پیشنهاد': 'tip', 'هشدار': 'warn',
                    'خطر': 'danger', 'محدودیت واقعی': 'limit', 'آزمون‌شده': 'tip'}[label]
            callout(doc, label, body, kind)
            i += 1
            continue
        if s.startswith('> '):
            para(doc, '*%s*' % s[2:].strip(), 10.5, after=8)
            i += 1
            continue
        if not s:
            i += 1
            continue
        para(doc, s)
        i += 1

    doc.save(out_path)
    print('wrote', out_path)


if __name__ == '__main__':
    build('build/guide.md', sys.argv[1] if len(sys.argv) > 1 else 'build/guide.docx')
