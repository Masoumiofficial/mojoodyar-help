"""Reproducible build: Typst -> PDF (text-extraction repaired) -> MD -> DOCX.

Two documents are produced:

* ``guide.typ``   -> the full user guide (all 12 chapters)
* ``install.typ`` -> ``help.pdf``: install, activation, access and update only

The install guide is the file the marketplace reviewer asked for inside the
package root, so it also goes next to the other deliverables.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)
ROOT = os.path.dirname(BUILD)

OUT_PDF = '/home/user/Mojoodyar-User-Guide-FA.pdf'
OUT_DOCX = '/home/user/Mojoodyar-User-Guide-FA.docx'
OUT_HELP = '/home/user/help.pdf'
OUT_HELP_DOCX = '/home/user/help.docx'

TMP = '/tmp/mjy_build.pdf'
TMP_HELP = '/tmp/mjy_help.pdf'


def render(source, tmp_pdf, out_pdf):
    import typst
    sys.path.insert(0, HERE)
    from pdftextfix import fix

    typst.compile(os.path.join(BUILD, source), output=tmp_pdf,
                  font_paths=[os.path.join(BUILD, 'fonts')])
    fix(tmp_pdf, out_pdf)
    print('pdf  ->', out_pdf)


def main():
    render('guide.typ', TMP, OUT_PDF)
    subprocess.run([sys.executable, os.path.join(HERE, 'mdbook.py')], check=True, cwd=ROOT)
    subprocess.run([sys.executable, os.path.join(HERE, 'md2docx.py'), OUT_DOCX], check=True, cwd=ROOT)
    print('docx ->', OUT_DOCX)

    render('install.typ', TMP_HELP, OUT_HELP)
    subprocess.run([sys.executable, os.path.join(HERE, 'mdbook.py'),
                    'build/install.typ', 'build/install.md'], check=True, cwd=ROOT)
    subprocess.run([sys.executable, os.path.join(HERE, 'md2docx.py'),
                    OUT_HELP_DOCX, 'build/install.md'], check=True, cwd=ROOT)
    print('docx ->', OUT_HELP_DOCX)

    # ship help.pdf inside the deliverables folder as well
    shutil.copyfile(OUT_HELP, os.path.join(ROOT, 'deliverables', 'help.pdf'))


if __name__ == '__main__':
    main()
