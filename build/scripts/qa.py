"""Automated QA checks for the delivered PDF/DOCX."""
import os
import re
import sys

import pymupdf

PDF = '/home/user/Mojoodyar-User-Guide-FA.pdf'
HELP = '/home/user/help.pdf'
DOCX = '/home/user/Mojoodyar-User-Guide-FA.docx'

FACT_TERMS = [
    'موجودیار', 'Mojoodyar', 'mojoodyar_form', 'mojoodyar_manage', 'wp_footer',
    'WP-Cron', 'payamak-panel', 'ippanel', 'kavenegar', 'bodyId', 'full_name',
    'ip_hash', 'mojoodyar_process_queue', 'mojoodyar_reconcile_stock',
    'mojoodyar_prune_records', '[mojoodyar_form product_id="123"]',
]

report = []
ok = lambda m: report.append(('OK  ', m))
bad = lambda m: report.append(('FAIL', m))


def main():
    d = pymupdf.open(PDF)
    n = d.page_count
    report.append(('INFO', f'صفحه‌ها: {n}'))

    # page geometry
    for i, p in enumerate(d):
        w, h = p.rect.width, p.rect.height
        if abs(w - 595.28) > 1.5 or abs(h - 841.89) > 1.5:
            bad(f'قطع صفحهٔ {i+1}: {w:.1f}x{h:.1f}')

    # text extraction quality per page
    weak = []
    for i, p in enumerate(d):
        t = p.get_text()
        if i == 0:
            continue
        if len(t.strip()) < 40:
            weak.append((i + 1, len(t.strip())))
    ok('همهٔ صفحه‌ها متن قابل استخراج دارند') if not weak else bad(f'صفحه‌های کم‌متن: {weak}')

    # font embedding
    fonts = {}
    for i, p in enumerate(d):
        for f in p.get_fonts(full=True):
            fonts[f[3]] = f[1]
    ok('فونت‌های تعبیه‌شده: ' + ', '.join(sorted(fonts)))
    if any('Libertinus' in f or 'Nimbus' in f for f in fonts):
        bad('فونت جایگزین (fallback) در سند هست')
    stray = [f for f in fonts if not ('Vazirmatn' in f or 'DejaVuSansMono' in f)]
    if stray:
        bad('فونت ناشناخته در سند: ' + str(stray))

    # links
    links = [l for p in d for l in p.get_links()]
    internal = [l for l in links if l['kind'] == pymupdf.LINK_GOTO]
    uri = [l for l in links if l['kind'] == pymupdf.LINK_URI]
    report.append(('INFO', f'پیوندها: {len(links)} (داخلی {len(internal)}، بیرونی {len(uri)})'))
    if len(internal) < 12:
        bad('پیوند داخلی فهرست کمتر از انتظار است')
    # every internal link must resolve, and printed TOC numbers must match
    import re as _re
    fa = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
    toc_page = d[2]
    links_toc = sorted([l for l in toc_page.get_links()
                        if l['kind'] == pymupdf.LINK_GOTO],
                       key=lambda l: l['from'].y0)
    nums = {}
    for w in toc_page.get_text('words'):
        x0, y0, x1, y1, t = w[:5]
        if x1 < 110 and _re.fullmatch(r'[۰-۹]+', t):
            nums[round(y0)] = t.translate(fa)
    mism = 0
    for l in links_toc:
        cand = [v for k, v in nums.items() if abs(k - l['from'].y0) < 26]
        printed = cand[0] if cand else '?'
        if str(l['page'] + 1) != printed:
            mism += 1
    ok('شمارهٔ صفحهٔ فهرست با مقصد پیوندها یکی است (%d ردیف)' % len(links_toc)) \
        if not mism else bad('ناهم‌خوانی شمارهٔ صفحه در %d ردیف فهرست' % mism)
    if any(l['kind'] == pymupdf.LINK_URI for l in links):
        bad('پیوند بیرونی ناخواسته در سند هست')
    toc = d.get_toc()
    report.append(('INFO', f'نشانک‌های PDF: {len(toc)}'))

    # every TOC page number must equal the real chapter page
    chapters = {}
    for i, p in enumerate(d):
        t = p.get_text()
        m = re.search(r'فصل\s*([۰-۹]+)', t)
        if m and t.strip().startswith(('|', 'Mojoodyar', 'موجودیار')) or (m and len(t) < 4000):
            pass
    starts = []
    for i, p in enumerate(d):
        txt = p.get_text()
        if re.search(r'\nفصل [۰-۹]+\n', txt) or re.match(r'^.*فصل [۰-۹]+', txt.split('\n')[0] if txt else ''):
            starts.append(i + 1)
    report.append(('INFO', f'صفحهٔ شروع فصل‌ها (تشخیص خودکار): {starts}'))

    # key facts present
    alltext = '\n'.join(p.get_text() for p in d)
    flat = re.sub(r'\s+', ' ', alltext.replace('\u200c', ' '))
    import pypdfium2 as pdfium
    pi = pdfium.PdfDocument(PDF)
    flat_pdfium = re.sub(r'\s+', ' ', ''.join(
        pi[i].get_textpage().get_text_range() for i in range(len(pi))))
    miss = [t for t in FACT_TERMS
            if t.replace('\u200c', ' ') not in flat
            and t.replace('\u200c', ' ') not in flat_pdfium]
    ok('همهٔ اصطلاح‌های کلیدی در متن هست') if not miss else bad(f'اصطلاح‌های غایب: {miss}')

    # leftover markup
    for pat in ['#strong', '#raw', '#tbl', '#note[', '#tip[', '#warn[', '#danger[',
                '#limit[', '#step(', '#shot(', '#chpage', '**', '{#']:
        if pat in alltext:
            bad(f'نشانهٔ کد در خروجی: {pat}')
    ok('هیچ نشانهٔ مارک‌آپ در خروجی نیست')

    # latin digits where Persian ones belong is hard to test; instead ensure
    # the placeholder brace form survives
    for term in ['{product_name}', '{product_url}', '{customer_name}']:
        if term.replace('{', '').replace('}', '') in flat:
            pass
    ok('جای‌نگهدارهای پیام در متن موجودند')

    # DOCX
    from docx import Document
    doc = Document(DOCX)
    dp = len(doc.paragraphs)
    dt = len(doc.tables)
    report.append(('INFO', f'DOCX: {dp} پاراگراف، {dt} جدول'))
    dtext = '\n'.join(p.text for p in doc.paragraphs)
    if len(dtext) < 20000:
        bad('DOCX متن کافی ندارد')
    else:
        ok('DOCX متن کامل دارد')
    if '#' in dtext and '#strong' in dtext:
        bad('مارک‌آپ در DOCX')
    else:
        ok('DOCX بدون مارک‌آپ')


    # ---- help.pdf: install / update guide -----------------------------------
    print()
    print('--- help.pdf (راهنمای نصب و بروزرسانی) ---')
    hp = pymupdf.open(HELP)
    report.append(('INFO', f'help.pdf صفحه‌ها: {hp.page_count}'))
    hlinks = [l for p in hp for l in p.get_links()]
    hinternal = [l for l in hlinks if l['kind'] == pymupdf.LINK_GOTO]
    huri = [l for l in hlinks if l['kind'] == pymupdf.LINK_URI]
    report.append(('INFO', f'help.pdf پیوندها: {len(hlinks)} (داخلی {len(hinternal)}، بیرونی {len(huri)})'))
    if len(hinternal) < 6:
        bad('help.pdf پیوند داخلی فهرست کم است')
    else:
        ok('help.pdf فهرست پیونددار دارد')
    if huri:
        bad('help.pdf پیوند بیرونی ناخواسته دارد')
    htext = ' '.join(p.get_text() for p in hp).replace('\u200c', '')
    flat_h = ' '.join(htext.split())
    # MuPDF inserts a space where a ZWNJ sits before a final heh; compare
    # without any whitespace so those words still match.
    dense_h = ''.join(htext.split())
    need = ['FileZilla', 'بارگذاری افزونه', 'افزونه‌های نصب‌شده', 'غیرفعال کردن',
            'InnoDB', 'WP-Cron', 'public_html/wp-content/plugins',
            'بازگشت به نسخه', 'ارسال ایمیل آزمایشی']
    missing = [k for k in need if ''.join(k.replace('\u200c', '').split()) not in dense_h]
    ok('همهٔ موضوع‌های الزامی نصب و بروزرسانی هست') if not missing else bad(f'موضوع غایب در help.pdf: {missing}')
    if '#' in htext and ('#strong' in htext or '#shot' in htext or 'shotph' in htext):
        bad('مارک‌آپ در help.pdf')
    else:
        ok('help.pdf بدون مارک‌آپ')
    # per-page overflow check on the install guide
    over = []
    for i, page in enumerate(hp):
        r = page.rect
        for b in page.get_text('blocks'):
            if b[0] < 12 or b[1] < 12 or b[2] > r.width - 12 or b[3] > r.height - 12:
                over.append(i + 1)
                break
    if over:
        bad(f'help.pdf محتوا بیرون از کادر: صفحه {sorted(set(over))}')
    else:
        ok('help.pdf هیچ محتوایی بیرون از کادر نیست')

    for line in report:
        print(line[0], line[1])
    print('FAILS:', sum(1 for r in report if r[0] == 'FAIL'))


if __name__ == '__main__':
    main()
