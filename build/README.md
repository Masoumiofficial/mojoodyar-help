# ساخت راهنمای کاربری موجودیار

این پوشه منبع حروف‌چینی و اسکریپت‌های ساخت راهنمای فارسی موجودیار است.
خروجی‌ها در `/home/user` ساخته می‌شوند:

- `Mojoodyar-User-Guide-FA.pdf`
- `Mojoodyar-User-Guide-FA.docx`
- `Mojoodyar-Documentation-QA.txt`

## اجرا

```bash
cd /home/user/mojoodyar-help
python3 build/scripts/build.py     # PDF + DOCX
python3 build/scripts/qa.py        # بررسی‌های خودکار (باید FAILS: 0 باشد)
```

پیش‌نیازها: `typst` (پایتون)، `pymupdf`، `pypdfium2`، `pypdf`، `python-docx`.

## فایل‌ها

| فایل | نقش |
| --- | --- |
| `guide.typ` | متن کامل سند (جلد، شناسنامه، فهرست، ۱۲ فصل، پیوست) |
| `template.typ` | قالب: پالت رنگ، سرصفحه/پاصفحه، کادرها، جدول، گام، تصویر |
| `scripts/build.py` | Typst → PDF (با اصلاح نگاشت متن) → Markdown → DOCX |
| `scripts/pdftextfix.py` | اصلاح `ToUnicode` برای استخراج درست متن راست‌چین |
| `scripts/mdbook.py` | تبدیل `guide.typ` به Markdown ویرایش‌پذیر |
| `scripts/md2docx.py` | ساخت DOCX راست‌چین با سبک‌های Heading و فیلد TOC |
| `scripts/qa.py` | کنترل کیفیت خودکار (فونت، پیوند، فهرست، مارک‌آپ، DOCX) |
| `fonts/` | Vazirmatn (نسخهٔ ۳۳، مجوز OFL) |
| `assets/` | تصاویر واقعی رابط کاربری، لوگوی موجودیار و لوگوی ژاکت |

نکته: `# MD-START` در `guide.typ` ابتدای بخشی است که به Markdown منتقل می‌شود
(جلد و صفحهٔ شناسنامه فقط در PDF هستند).
