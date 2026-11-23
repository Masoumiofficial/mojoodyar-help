"""Reproducible build: Typst -> PDF (text-extraction repaired) -> MD -> DOCX."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)
ROOT = os.path.dirname(BUILD)
OUT_PDF = '/home/user/Mojoodyar-User-Guide-FA.pdf'
OUT_DOCX = '/home/user/Mojoodyar-User-Guide-FA.docx'
TMP = '/tmp/mjy_build.pdf'

def main():
    import typst
    typst.compile(os.path.join(BUILD, 'guide.typ'), output=TMP,
                  font_paths=[os.path.join(BUILD, 'fonts')])
    sys.path.insert(0, HERE)
    from pdftextfix import fix
    fix(TMP, OUT_PDF)
    print('pdf  ->', OUT_PDF)
    subprocess.run([sys.executable, os.path.join(HERE, 'mdbook.py')], check=True, cwd=ROOT)
    subprocess.run([sys.executable, os.path.join(HERE, 'md2docx.py'), OUT_DOCX], check=True, cwd=ROOT)
    print('docx ->', OUT_DOCX)

if __name__ == '__main__':
    main()
