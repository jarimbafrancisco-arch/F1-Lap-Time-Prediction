r"""Export saved notebook contents to HTML and PDF without running its cells.

Usage: .\.venv\Scripts\python.exe scripts/export_notebook.py notebooks/02_EDA.ipynb
Requires: pip install "nbconvert[webpdf]"
          python -m playwright install chromium
"""

import argparse
from pathlib import Path

from nbconvert import HTMLExporter, WebPDFExporter


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("exports"))
    args = parser.parse_args()
    if not args.notebook.is_file():
        parser.error(f"Notebook not found: {args.notebook}")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    html, _ = HTMLExporter(embed_images=True).from_filename(str(args.notebook))
    html_path = args.output_dir / f"{args.notebook.stem}.html"
    html_path.write_text(html, encoding="utf-8")
    print(f"HTML: {html_path}", flush=True)

    # Use the exporter directly: nbconvert's CLI selects a Windows event loop
    # that cannot start the browser subprocess required by Playwright.
    pdf, _ = WebPDFExporter(embed_images=True).from_filename(str(args.notebook))
    pdf_path = args.output_dir / f"{args.notebook.stem}.pdf"
    pdf_path.write_bytes(pdf)
    print(f"PDF:  {pdf_path}", flush=True)


if __name__ == "__main__":
    main()
