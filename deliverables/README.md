# راهنمای کاربری موجودیار | Mojoodyar — نسخهٔ ۱٫۰٫۰

فایل‌های آمادهٔ تحویل و انتشار در ژاکت:

| فایل | توضیح |
| --- | --- |
| `Mojoodyar-User-Guide-FA.pdf` | نسخهٔ چاپی — ۵۷ صفحه A4، متن انتخاب‌پذیر، فهرست پیونددار، نشانک‌دار |
| `Mojoodyar-User-Guide-FA.docx` | نسخهٔ ویرایش‌پذیر، فارسی و راست‌چین |
| `Mojoodyar-Documentation-QA.txt` | گزارش کنترل کیفیت و فهرست موارد آزمون‌نشده |

## دانلود مستقیم

- PDF: `https://raw.githubusercontent.com/Masoumiofficial/mojoodyar-help/arena/50d91c4e-mojoodyar-help/deliverables/Mojoodyar-User-Guide-FA.pdf`
- DOCX: `https://raw.githubusercontent.com/Masoumiofficial/mojoodyar-help/arena/50d91c4e-mojoodyar-help/deliverables/Mojoodyar-User-Guide-FA.docx`
- QA: `https://raw.githubusercontent.com/Masoumiofficial/mojoodyar-help/arena/50d91c4e-mojoodyar-help/deliverables/Mojoodyar-Documentation-QA.txt`

> اگر فایل در مرورگر باز شد، از دکمهٔ دانلود صفحه استفاده کنید یا `?raw=true` را به انتهای نشانی اضافه کنید.

## فهرست فصل‌ها

معرفی · پیش‌نیازها و نصب · شروع سریع · تنظیمات · پیامک و ایمیل · الگوها و متغیرها ·
مدیریت لیست انتظار · پیگیری تلفنی · داشبورد و آمار · ابزارها و گزارش رویدادها ·
حریم خصوصی و امنیت · عیب‌یابی و پرسش‌های متداول · واژه‌نامه و منابع

## بازتولید

منبع حروف‌چینی و اسکریپت‌های ساخت در پوشهٔ `build/` است:

```bash
python3 build/scripts/build.py   # ساخت PDF و DOCX
python3 build/scripts/qa.py      # کنترل کیفیت خودکار (FAILS: 0)
```

## دربارهٔ صحت محتوا

همهٔ گزینه‌ها، دکمه‌ها، پیش‌فرض‌ها، کدهای رویداد و شورت‌کدها از کد واقعی افزونه
نسخهٔ ۱٫۰٫۰ استخراج شده‌اند. هیچ قابلیت ساختگی یا آزمون‌نشده‌ای «تضمین‌شده» معرفی
نشده است؛ موارد آزمون‌نشده در بخش «آنچه در این نسخه آزمون نشده است» و در گزارش
QA فهرست شده‌اند.
