# راهنمای کاربری موجودیار | Mojoodyar — نسخهٔ ۱٫۰٫۰

| فایل | توضیح |
| --- | --- |
| `help.pdf` | **راهنمای نصب و بروزرسانی** — ۱۸ صفحه؛ همین فایل باید در روت بستهٔ خرید و در پوشهٔ مستندات ژاکت باشد |
| `Mojoodyar-User-Guide-FA.pdf` | راهنمای جامع کاربری — ۵۷ صفحه، ۱۲ فصل |
| `Mojoodyar-User-Guide-FA.docx` | نسخهٔ ویرایش‌پذیر راهنمای جامع |
| `help.docx` | نسخهٔ ویرایش‌پذیر راهنمای نصب و بروزرسانی |
| `Mojoodyar-Documentation-QA.txt` | گزارش کنترل کیفیت و فهرست موارد آزمون‌نشده |
| `SCREENSHOTS-NEEDED.md` | شش اسکرین‌شاتی که باید جای کادرهای خط‌چین help.pdf بگذارید |

## دانلود مستقیم

- `help.pdf`: https://github.com/Masoumiofficial/mojoodyar-help/raw/guide-v1.0.0/deliverables/help.pdf
- راهنمای جامع (PDF): https://github.com/Masoumiofficial/mojoodyar-help/raw/guide-v1.0.0/deliverables/Mojoodyar-User-Guide-FA.pdf
- راهنمای جامع (DOCX): https://github.com/Masoumiofficial/mojoodyar-help/raw/guide-v1.0.0/deliverables/Mojoodyar-User-Guide-FA.docx
- گزارش QA: https://github.com/Masoumiofficial/mojoodyar-help/raw/guide-v1.0.0/deliverables/Mojoodyar-Documentation-QA.txt

## ساختار پیشنهادی بستهٔ ژاکت

```text
Mojoodyar-Documentation/
├── 01-Plugin-ZIP/Mojoodyar.zip
├── 02-Screenshots/
├── 03-Logos/
├── 04-Help/
│   ├── help.pdf                        ← نصب و بروزرسانی (روت بسته هم باشد)
│   └── Mojoodyar-User-Guide-FA.pdf     ← راهنمای جامع
└── 05-Docs/
```

طبق درخواست پشتیبان ژاکت: در پوشهٔ مستندات باید یک فایل آموزشی جامع باشد
(نه لینک به صفحهٔ اصلی ژاکت)، و `help.pdf` در روت فقط شامل نصب و بروزرسانی.

## بازتولید

```bash
python3 build/scripts/build.py   # هر دو PDF و هر دو DOCX
python3 build/scripts/qa.py      # کنترل کیفیت هر دو سند (FAILS: 0)
```
