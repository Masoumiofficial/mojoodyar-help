// ============================================================================
//  موجودیار | Mojoodyar — راهنمای کاربری  (قالب اصلی)
//  Premium SaaS documentation · A4 · فارسی راست‌چین
//  نکته: قواعد set/show در این فایل، چون ماژول وارد‌شده است، روی سند اصلی
//  اثر نمی‌کند؛ بنابراین همه‌چیز داخل تابع «page-style» بسته شده است.
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
  code:      rgb("#3F2DA8"),
)

#let PRODUCT     = "موجودیار"
#let PRODUCTFULL = "موجودیار | Mojoodyar"
#let VERSION     = "1.0.0"
#let VERSIONFA   = "۱٫۰٫۰"
#let AUCTION     = "اتحاد وردپرس"

#let fadigits = ("۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹")
#let rule(color: C.grey2, thickness: 0.5pt) = grid(columns: 1fr, line(length: 100%, stroke: thickness + color))

#let fa(n) = {
  let s = str(int(n))
  s.clusters().map(c => {
    let i = "0123456789".position(c)
    if i == none { c } else { fadigits.at(i) }
  }).join()
}

// ---- شمارنده فصل ---------------------------------------------------------
#let chaplabel = counter("chapter")

// ---- سبک صفحه (باید در سند اصلی فراخوانی شود) ---------------------------
#let page-style(body) = {
  set page(
    paper: "a4",
    margin: (top: 2.55cm, bottom: 2.1cm, inside: 2.05cm, outside: 1.8cm),
  )
  set text(font: "Vazirmatn", fallback: false, lang: "fa", region: "IR", size: 10.4pt, fill: C.text, dir: rtl)
  set par(justify: true, leading: 0.74em, spacing: 0.88em)

  // ---- تیترها
  show heading.where(level: 1): it => context {
    let n = chaplabel.get().first()
    block(breakable: false, width: 100%, below: 1.2em, above: 0.1em, {
      stack(spacing: 0.42em,
        block(fill: C.brand, radius: 3pt, width: 32pt, height: 3.2pt),
        text(size: 9.2pt, weight: "bold", fill: C.brand, [فصل #fa(n)]),
        text(size: 20pt, weight: "bold", fill: C.ink, it.body),
        rule(thickness: 0.6pt),
      )
    })
  }
  show heading.where(level: 2): it => block(
    breakable: false, above: 1.45em, below: 0.55em,
    grid(columns: (9pt, 1fr), column-gutter: 5pt, align: (center + horizon, right),
      box(width: 5.5pt, height: 5.5pt, radius: 1.2pt, fill: C.brand2),
      text(size: 13.3pt, weight: "bold", fill: C.ink, it.body),
    ),
  )
  show heading.where(level: 3): it => block(
    breakable: false, above: 1.05em, below: 0.3em,
    text(size: 11.1pt, weight: "bold", fill: C.brand, it.body),
  )

  // نشانی‌های نمونه نباید پیوند خودکار شوند (جای‌نگهدارند، نه نشانی واقعی)
  show link: it => if type(it.dest) == label { it } else { it.body }

  // ---- کد
  show raw.where(block: false): it => box(
    fill: C.brandpale, inset: (x: 3.2pt, y: 1.4pt), radius: 2.5pt,
    // کد درون‌خطی نباید پیوند خودکار شود؛ متن ساده بازتولید می‌شود
    text(font: "Vazirmatn", size: 9.05pt, fill: C.code, str(it.text)),
  )
  show raw.where(block: true): it => block(
    width: 100%, fill: rgb("#F7F8FB"), radius: 3pt,
    stroke: (left: 2.6pt + C.brand), inset: (x: 10pt, y: 7.5pt),
    above: 0.45em, below: 0.9em,
    [
      #set text(dir: ltr, lang: "en", size: 8.75pt, fill: rgb("#1D2939"))
      #set par(justify: false, leading: 0.82em)
      #it
    ],
  )

  // ---- فهرست‌ها
  set list(spacing: 0.42em)
  set enum(spacing: 0.46em)
  show list: it => block(above: 0.3em, below: 0.55em, {
    for item in it.children {
      grid(columns: (10pt, 1fr), column-gutter: 4pt, align: (right + top, right),
        pad(top: 5.6pt, box(width: 4pt, height: 4pt, radius: 50%, fill: C.brand2)),
        item.body,
      )
    }
  })
  show enum: it => block(above: 0.3em, below: 0.55em, {
    for (i, item) in it.children.enumerate() {
      grid(columns: (16pt, 1fr), column-gutter: 3pt, align: (center + top, right),
        pad(top: 1pt,
          box(width: 15pt, height: 15pt, radius: 50%, fill: C.brandpale,
            align(center + horizon, text(size: 8.3pt, weight: "bold", fill: C.brand, fa(i + 1))))),
        item.body,
      )
    }
  })

  // ---- نقل قول
  show quote: it => block(
    width: 100%, fill: C.grey, radius: 4pt, inset: (x: 11pt, y: 9pt),
    stroke: (left: 2.6pt + C.teal), above: 0.5em, below: 0.85em,
    text(size: 9.7pt, it.body),
  )

  // ---- جدول
  set table(
    stroke: (x, y) => if y == 0 { none } else { (top: 0.45pt + C.grey2) },
    inset: (x: 6.5pt, y: 5.6pt),
    fill: (col, row) => if row == 0 { C.grey } else { C.white },
    align: (col, row) => right,
  )
  show table.cell: it => {
    set par(justify: false, leading: 0.82em)
    it
  }
  show table: it => block(above: 0.45em, below: 1.0em, width: 100%, it)

  // ---- سربرگ
  set page(header: context {
    let pg = counter(page).get().first()
    if pg <= 1 { return }
    set text(size: 7.8pt, fill: C.muted)
    block(width: 100%, below: 1.05em, {
      grid(columns: (1fr, auto, 1fr), align: (right, center, left),
        text(weight: "medium", fill: C.ink, PRODUCTFULL),
        text[راهنمای کاربری],
        align(left, text[نسخهٔ #VERSION]),
      )
      v(-1pt)
      rule()
    })
  })

  // ---- پابرگ
  set page(footer: context {
    let pg = counter(page).get().first()
    if pg <= 1 { return }
    set text(size: 7.8pt, fill: C.muted)
    block(width: 100%, above: 0.95em, {
      rule()
      v(2.5pt)
      grid(columns: (1fr, 1.4fr, 1fr), align: (right, center, left),
        text[صفحهٔ #fa(pg)],
        text(size: 7.2pt)[محصول #PRODUCT — #AUCTION],
        align(left, text(size: 7.2pt, [راهنمای کاربری · نسخهٔ #VERSION])),
      )
    })
  })

  body
}

// ---- ساختار فصل ---------------------------------------------------------
#let chapter(title) = {
  chaplabel.step()
  pagebreak(weak: true)
  heading(level: 1, bookmarked: true, outlined: false, title)
}

#let chapterplain(title) = {
  pagebreak(weak: true)
  heading(level: 1, bookmarked: true, outlined: false, title)
}

// ---- جدول ---------------------------------------------------------------
// ---- متن خانهٔ جدول: escapes markup specials, then parses ----
#let mkcell(c) = {
  let s = c
  for (from, to) in (("#", "\\#"), ("_", "\\_"), ("$", "\\$"), ("@", "\\@"), ("<", "\\<"), (">", "\\>")) {
    s = s.replace(from, to)
  }
  eval(s, mode: "markup")
}
#let tbl(header: (), rows: (), widths: auto, size: 9.15pt, aligns: auto, pad-y: 5pt) = {
  let cells = ()
  for r in rows {
    for c in r {
      cells.push(par(justify: false, leading: 0.8em,
        if type(c) == str { mkcell(c) } else { c }))
    }
  }
  table(
    columns: widths,
    inset: (x: 6.5pt, y: pad-y),
    align: (col, row) => right,
    table.header(..header.map(h => text(size: size, weight: "bold", fill: C.ink, h))),
    ..cells,
  )
}


// ---- جدول متراکم ---------------------------------------------------------
#let tblc(header: (), rows: (), widths: auto, size: 8.9pt) = {
  set par(justify: false, leading: 0.82em)
  tbl(header: header, rows: rows, widths: widths, size: size, pad-y: 2.9pt)
}


// ---- صفحهٔ پیوست (بدون شمارهٔ فصل) --------------------------------------
#let appx(title) = {
  pagebreak(weak: true)
  show heading.where(level: 1): it => block(
    breakable: false, width: 100%, below: 1.2em, above: 0.1em,
    stack(spacing: 0.42em,
      block(fill: C.teal, radius: 3pt, width: 32pt, height: 3.2pt),
      text(size: 9.2pt, weight: "bold", fill: C.teal)[پیوست],
      text(size: 20pt, weight: "bold", fill: C.ink, it.body),
      rule(thickness: 0.6pt),
    ),
  )
  heading(level: 1, bookmarked: true, outlined: true, title)
}

// ---- صفحهٔ آغاز فصل ------------------------------------------------------
#let chpage(num, title, lede, cheadline) = {
  chaplabel.step()
  pagebreak(weak: true)
  block(breakable: false, width: 100%, above: 0.1cm, below: 0.55cm,
    grid(columns: (1fr, 2.15cm), column-gutter: 12pt, align: (right + top, center + top),
      block(width: 100%, heading(level: 1, bookmarked: true, outlined: false, title)),
      image("assets/mojoodyar-logo.png", width: 2.15cm),
    ),
  )
  block(width: 100%, text(size: 11.2pt, fill: C.text, lede))
  v(0.5cm)
  if cheadline != none {
    block(width: 100%, fill: C.grey, radius: 3pt, inset: (x: 11pt, y: 8pt),
      text(size: 9pt, fill: C.muted, cheadline))
    v(0.35cm)
  }
}

// ---- کادرهای آموزشی -----------------------------------------------------
#let labelchip(label, color) = box(
  fill: C.white, radius: 2.5pt, inset: (x: 4.6pt, y: 1.6pt),
  text(size: 8.2pt, weight: "bold", fill: color, label),
)

#let boxed(label, color, pale, body) = block(
  width: 100%, breakable: false, fill: pale, radius: 3.5pt,
  stroke: (left: 2.8pt + color), inset: (x: 10.5pt, y: 8.5pt),
  above: 0.6em, below: 0.95em,
  {
    set text(size: 9.65pt, fill: C.text)
    set par(justify: true, leading: 0.7em, spacing: 0.6em)
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
  width: 100%, breakable: false, above: 0.4em, below: 0.7em,
  grid(columns: (17pt, 1fr), column-gutter: 6pt, align: (center + top, right),
    pad(top: 1.5pt,
      box(width: 15pt, height: 15pt, radius: 50%, fill: C.brand,
        align(center + horizon, text(size: 8.3pt, weight: "bold", fill: C.white, n)))),
    block(width: 100%, {
      set par(justify: false, leading: 0.68em)
      text(size: 10.4pt, weight: "bold", fill: C.ink)[#title]
      v(0.12em)
      body
    }),
  ),
)

// ---- تصویر --------------------------------------------------------------
#let shot(path, caption, width: 100%, inset: 0pt, maxh: 21.2cm) = block(
  breakable: false, width: 100%, above: 0.7em, below: 1.0em,
  stack(spacing: 0.45em,
    block(width: width, fill: C.white, radius: 4pt, clip: true,
      stroke: 0.7pt + C.grey2, inset: inset,
      image(path, width: 100%, height: auto, fit: "contain")),
    par(justify: false, leading: 0.55em, text(size: 8.35pt, fill: C.muted, caption)),
  ),
)

// تصویر بلند برای صفحهٔ اختصاصی (ارتفاع محدود تا از صفحه بیرون نزند)
#let shot-tall(path, caption, width: 78%) = block(
  breakable: false, width: 100%, above: 0.5em, below: 0.8em,
  align(center, stack(spacing: 0.45em,
    block(width: width, fill: C.white, radius: 4pt, clip: true,
      stroke: 0.7pt + C.grey2, image(path, width: 100%)),
    par(justify: false, leading: 0.55em, text(size: 8.35pt, fill: C.muted, caption)),
  )),
)

// ---- فهرست مطالب --------------------------------------------------------
#let toc-entry(num, title, lbl) = {
  grid(columns: (1fr, 22pt), column-gutter: 6pt, align: (right, left),
    link(lbl, text(size: 10.2pt, weight: "medium", fill: C.ink, title)),
    link(lbl, context text(size: 9pt, fill: C.muted, fa(locate(lbl).page()))),
  )
  v(2.8pt)
  rule(thickness: 0.4pt)
  v(3.6pt)
}
