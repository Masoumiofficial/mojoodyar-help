// ============================================================================
//  موجودیار | Mojoodyar — راهنمای کاربری  (قالب اصلی)
//  Premium SaaS documentation · A4 · فارسی راست‌چین
// ============================================================================

#let C = (
  ink:       rgb("#101828"),
  brand:     rgb("#5535CF"),
  brand2:    rgb("#7C5CE6"),
  brandpale: rgb("#EFEBFF"),
  teal:      rgb("#25C6B7"),
  tealpale:  rgb("#E6FAF7"),
  white:     rgb("#FFFFFF"),
  grey:      rgb("#F4F6FA"),
  grey2:     rgb("#E4E7EC"),
  text:      rgb("#263244"),
  muted:     rgb("#667085"),
  amber:     rgb("#B54708"),
  amberpale: rgb("#FFFAEB"),
  red:       rgb("#B42318"),
  redpale:   rgb("#FEF3F2"),
  green:     rgb("#067647"),
  greenpale: rgb("#ECFDF3"),
)

#let PRODUCT     = "موجودیار"
#let PRODUCTFULL = "موجودیار | Mojoodyar"
#let VERSION     = "1.0.0"
#let VERSIONFA   = "۱.۰.۰"
#let BUILDATE    = "۱۴۰۵/۰۹/۰۲"
#let DOCREPO     = "https://github.com/Masoumiofficial/mojoodyar-help"

#let fa(n) = numbering("۰۱۲۳۴۵۶۷۸۹", n)

// ---- تنظیمات صفحه ------------------------------------------------------
#set page(
  paper: "a4",
  margin: (top: 2.6cm, bottom: 2.15cm, inside: 2.05cm, outside: 1.8cm),
)

#set text(font: "Vazirmatn", lang: "fa", region: "IR", size: 10.4pt, fill: C.text, dir: rtl)
#set par(justify: true, leading: 0.74em, spacing: 0.9em)

// ---- تیترها ------------------------------------------------------------
#let chaplabel = counter("chapter")
#let chapters = state("chapters", ())

#show heading.where(level: 1): it => context {
  let n = chaplabel.get().first()
  block(breakable: false, below: 1.25em, above: 0.1em, {
    stack(spacing: 0.48em,
      block(fill: C.brand, radius: 3pt, width: 34pt, height: 3.2pt),
      text(size: 9.4pt, weight: "bold", fill: C.brand)[فصل #fa(n)],
      text(size: 20.5pt, weight: "bold", fill: C.ink, it.body),
      block(fill: C.grey2, width: 100%, height: 0.6pt),
    )
  })
}

#show heading.where(level: 2): it => {
  block(breakable: false, above: 1.5em, below: 0.6em,
    text(size: 13.6pt, weight: "bold", fill: C.ink, it.body))
}

#show heading.where(level: 3): it => {
  block(breakable: false, above: 1.1em, below: 0.35em,
    text(size: 11.3pt, weight: "bold", fill: C.brand, it.body))
}

// ---- کد درون‌خطی و بلوکی ------------------------------------------------
#show raw.where(block: false): it => {
  let txt = text(font: "Vazirmatn", size: 9.1pt, fill: rgb("#3F2DA8"), it.text)
  box(fill: C.brandpale, inset: (x: 3.2pt, y: 1.4pt), radius: 2.5pt, txt)
}

#show raw.where(block: true): it => block(
  width: 100%, fill: rgb("#F7F8FB"), radius: 3pt,
  stroke: (left: 2.6pt + C.brand), inset: (x: 10pt, y: 7.5pt),
  above: 0.5em, below: 0.95em,
  text(dir: ltr, lang: "en", size: 8.8pt, fill: rgb("#1D2939"),
    set par(justify: false, leading: 0.6em)
    it),
)

// ---- فهرست‌ها -----------------------------------------------------------
#set list(indent: 0em, body-indent: 0em, spacing: 0.45em)
#set enum(indent: 0em, body-indent: 0em, spacing: 0.5em)

#show list: it => block(above: 0.4em, below: 0.6em, {
  for item in it.children {
    grid(columns: (11pt, 1fr), column-gutter: 4pt, align: (right + top, right),
      block(pad: (top: 5.4pt), box(width: 4pt, height: 4pt, radius: 50%, fill: C.brand2)),
      item.body,
    )
  }
})

#show enum: it => block(above: 0.4em, below: 0.6em, {
  for (i, item) in it.children.enumerate() {
    grid(columns: (15pt, 1fr), column-gutter: 3pt, align: (center + top, right),
      block(pad: (top: 1pt),
        box(width: 14pt, height: 14pt, radius: 50%, fill: C.brandpale,
          align(center + horizon, text(size: 8.2pt, weight: "bold", fill: C.brand, fa(i + 1))))),
      item.body,
    )
  }
})

// ---- نقل قول ------------------------------------------------------------
#show quote: it => block(
  width: 100%, fill: C.grey, radius: 4pt, inset: (x: 11pt, y: 9pt),
  stroke: (left: 2.6pt + C.teal), above: 0.55em, below: 0.9em,
  text(size: 9.7pt, it.body),
)

// ---- جدول ---------------------------------------------------------------
#set table(
  stroke: none,
  inset: (x: 7pt, y: 6pt),
  fill: (col, row) => if row == 0 { C.grey } else if calc.odd(row) { rgb("#FBFCFE") } else { C.white },
  align: (col, row) => right,
)
#show table: it => block(above: 0.55em, below: 1.05em, it)

#let tbl(header: (), rows: (), widths: auto, size: 9.2pt) = {
  table(
    columns: widths,
    table.header(..header.map(h => text(size: size - 0.2pt, weight: "bold", fill: C.ink, h))),
    ..rows.map(r => r.map(c => text(size: size, c))),
  )
}

// ---- کادرهای آموزشی -----------------------------------------------------
#let labelchip(label, color) = box(
  fill: C.white, radius: 2.5pt, inset: (x: 5pt, y: 1.8pt),
  text(size: 8.4pt, weight: "bold", fill: color, label),
)

#let boxed(label, color, pale, body) = block(
  width: 100%, breakable: false, fill: pale, radius: 4pt,
  stroke: (left: 2.8pt + color), inset: (x: 11pt, y: 9pt),
  above: 0.7em, below: 1.0em,
  {
    set par(justify: true, leading: 0.7em, spacing: 0.62em)
    set text(size: 9.7pt, fill: C.text)
    [#labelchip(label, color) #h(2pt) #body]
  },
)

#let note(body)   = boxed("نکته", C.brand, C.brandpale, body)
#let tip(body)    = boxed("پیشنهاد", C.green, C.greenpale, body)
#let warn(body)   = boxed("هشدار", C.amber, C.amberpale, body)
#let danger(body) = boxed("خطر", C.red, C.redpale, body)
#let limit(body)  = boxed("محدودیت واقعی", C.muted, C.grey, body)
#let tested(body) = boxed("وضعیت آزمون", rgb("#0F766E"), C.tealpale, body)

// ---- کارت مرحله ---------------------------------------------------------
#let step(n, title, body) = block(
  width: 100%, breakable: false, above: 0.45em, below: 0.75em,
  grid(columns: (18pt, 1fr), column-gutter: 6pt, align: (center + top, right),
    box(width: 16pt, height: 16pt, radius: 50%, fill: C.brand,
      align(center + horizon, text(size: 8.4pt, weight: "bold", fill: C.white, n))),
    block({
      text(size: 10.5pt, weight: "bold", fill: C.ink)[#title]
      par(leading: 0.68em, body)
    }),
  ),
)

// ---- تصویر --------------------------------------------------------------
#let shot(path, caption, width: 100%, keep: true) = block(
  breakable: false, width: 100%, above: 0.75em, below: 1.05em,
  stack(spacing: 0.45em,
    block(width: width, radius: 4pt, clip: true, stroke: 0.7pt + C.grey2,
      image(path, width: 100%)),
    par(justify: false, leading: 0.55em, text(size: 8.4pt, fill: C.muted, caption)),
  ),
)

// ---- سربرگ و پابرگ ------------------------------------------------------
#set page(
  header: context {
    let pg = counter(page).get().first()
    if pg <= 1 { return }
    set text(size: 7.9pt, fill: C.muted)
    block(width: 100%, below: 1.1em, {
      grid(columns: (1fr, auto, 1fr), align: (right, center, left),
        text(weight: "medium", fill: C.ink, PRODUCTFULL),
        text[راهنمای کاربری],
        align(left, text[نسخهٔ #VERSION]),
      )
      v(-1pt)
      block(width: 100%, height: 0.5pt, fill: C.grey2)
    })
  },
  footer: context {
    let pg = counter(page).get().first()
    if pg <= 1 { return }
    set text(size: 7.9pt, fill: C.muted)
    block(width: 100%, above: 1.0em, {
      block(width: 100%, height: 0.5pt, fill: C.grey2)
      v(2.5pt)
      grid(columns: (1fr, 1.15fr, 1fr), align: (right, center, left),
        text[صفحهٔ #fa(pg)],
        text(size: 7.3pt)[محصول #PRODUCT — اتحاد وردپرس],
        align(left, text(size: 7.3pt, link(DOCREPO, "مستندات و تصاویر محصول"))),
      )
    })
  },
)

// ---- ساختار فصل ---------------------------------------------------------
#let chapter(title, lbl) = {
  chaplabel.step()
  chapters.update(c => c + (title: title, lbl: lbl))
  pagebreak(weak: true)
  heading(level: 1, bookmarked: true, outlined: false)[#title] <#lbl>
}

#let chapterplain(title, lbl) = {
  pagebreak(weak: true)
  heading(level: 1, bookmarked: true, outlined: false)[#title] <#lbl>
}
