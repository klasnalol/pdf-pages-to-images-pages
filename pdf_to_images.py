import argparse
import os
import re
import sys
from dataclasses import dataclass
from typing import List, Optional, Sequence

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF is required. Install with: pip install pymupdf", file=sys.stderr)
    sys.exit(1)

PAGE_SPEC_RE = re.compile(r"^\s*(\d+)?\s*(?:-\s*(\d+)\s*)?$")


def parse_page_spec(spec: str, num_pages: int) -> List[int]:
    pages = set()
    if not spec:
        return list(range(1, num_pages + 1))
    tokens = [t.strip() for t in spec.split(",") if t.strip()]
    for tok in tokens:
        m = PAGE_SPEC_RE.match(tok)
        if not m:
            raise ValueError(f"Invalid page token: {tok}")
        start_s, end_s = m.groups()
        start = int(start_s) if start_s else None
        end = int(end_s) if end_s else None
        if start is None and end is None:
            raise ValueError(f"Empty range in token: {tok}")
        if start is None:
            for p in range(1, min(end or num_pages, num_pages) + 1):
                pages.add(p)
        elif end is None:
            for p in range(start, num_pages + 1):
                pages.add(p)
        else:
            for p in range(start, end + 1):
                if 1 <= p <= num_pages:
                    pages.add(p)
    return sorted(pages)


@dataclass
class ConvertOptions:
    dpi: int = 200
    fmt: str = "png"
    quality: int = 92
    zero_pad: int = 3
    prefix: str = "page_"
    suffix: str = ""
    max_dim: Optional[int] = None


def page_to_pix(page, dpi: int, max_dim: Optional[int]):
    scale = dpi / 72.0
    m = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=m, alpha=False)
    if max_dim:
        long_edge = max(pix.width, pix.height)
        if long_edge > max_dim:
            ratio = max_dim / long_edge
            new_w, new_h = int(pix.width * ratio), int(pix.height * ratio)
            pix = fitz.Pixmap(pix, 0)
            pix = pix.resize(new_w, new_h)
    return pix


def ensure_outdir(path: str):
    os.makedirs(path, exist_ok=True)


def build_filename(outdir: str, idx: int, opts: ConvertOptions) -> str:
    return os.path.join(outdir, f"{opts.prefix}{str(idx).zfill(opts.zero_pad)}{opts.suffix}.{opts.fmt}")


def convert_pdf(pdf_path: str, outdir: str, pages=None, opts=None) -> List[str]:
    opts = opts or ConvertOptions()
    ensure_outdir(outdir)
    out_paths = []
    with fitz.open(pdf_path) as doc:
        total = doc.page_count
        pages_to_do = pages or list(range(1, total + 1))
        for pnum in pages_to_do:
            if not (1 <= pnum <= total):
                continue
            page = doc.load_page(pnum - 1)
            pix = page_to_pix(page, opts.dpi, opts.max_dim)
            outfile = build_filename(outdir, pnum, opts)
            if opts.fmt.lower() in {"jpg", "jpeg"}:
                pix.save(outfile, jpg_quality=int(opts.quality))
            else:
                pix.save(outfile)
            out_paths.append(outfile)
    return out_paths


def positive_int(val: str) -> int:
    i = int(val)
    if i <= 0:
        raise argparse.ArgumentTypeError("must be > 0")
    return i


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Split a PDF into images.")
    ap.add_argument("pdf", help="Path to input PDF")
    ap.add_argument("-o", "--outdir", required=True, help="Output directory")
    ap.add_argument("-p", "--pages", default="", help="Pages like '1-3,7,10-'")
    ap.add_argument("--dpi", type=positive_int, default=200)
    ap.add_argument("-f", "--format", choices=["png", "jpg", "jpeg"], default="png")
    ap.add_argument("--quality", type=positive_int, default=92)
    ap.add_argument("--zero-pad", type=positive_int, default=3)
    ap.add_argument("--prefix", default="page_")
    ap.add_argument("--suffix", default="")
    ap.add_argument("--max-dim", type=positive_int, default=None)

    args = ap.parse_args(argv)

    if not os.path.exists(args.pdf):
        print(f"PDF not found: {args.pdf}", file=sys.stderr)
        return 2

    try:
        with fitz.open(args.pdf) as doc:
            num_pages = doc.page_count
    except Exception as e:
        print(f"Failed to open PDF: {e}", file=sys.stderr)
        return 2

    try:
        pages = parse_page_spec(args.pages, num_pages) if args.pages else None
    except ValueError as e:
        print(f"Invalid page spec: {e}", file=sys.stderr)
        return 2

    opts = ConvertOptions(
        dpi=args.dpi,
        fmt=args.format,
        quality=args.quality,
        zero_pad=args.zero_pad,
        prefix=args.prefix,
        suffix=args.suffix,
        max_dim=args.max_dim,
    )

    try:
        out = convert_pdf(args.pdf, args.outdir, pages, opts)
    except Exception as e:
        print(f"Conversion failed: {e}", file=sys.stderr)
        return 1

    print(f"Wrote {len(out)} image(s) to {os.path.abspath(args.outdir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
