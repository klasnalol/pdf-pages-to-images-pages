# pdf-pages-to-images-pages
convert your pdf with pages into folder with photos
A lightweight Python tool to split PDF pages into individual images (PNG or JPEG) using PyMuPDF. Works on Windows, macOS, and Linux with no external dependencies.

#installation:
download python 3.7+ than use pip to install pymupdf
pip install pymupdf

Basic Command
python pdf_to_images.py input.pdf -o out

Converts all pages of input.pdf into PNG images at 200 DPI and saves them in the out folder.

## Command-line Arguments

| Argument | Short | Type | Default | Description |
|-----------|--------|-------|-----------|-------------|
| `pdf` | — | Path | — | Path to input PDF file |
| `--outdir` | `-o` | Path | — | Output directory for images |
| `--pages` | `-p` | String | All pages | Page selection, e.g. `1-3,7,10-` |
| `--dpi` | — | Integer | 200 | Output resolution (dots per inch) |
| `--format` | `-f` | String | `png` | Output format: `png`, `jpg`, or `jpeg` |
| `--quality` | — | Integer | 92 | JPEG quality (1–100) |
| `--zero-pad` | — | Integer | 3 | Zero padding for page numbers |
| `--prefix` | — | String | `page_` | Filename prefix |
| `--suffix` | — | String | *(none)* | Filename suffix |
| `--max-dim` | — | Integer | *(none)* | Maximum long-edge dimension in pixels |

---

## Example

Convert all pages of `document.pdf` into 300-DPI JPEGs with high quality, custom filenames, and constrained long edge:

```bash
python pdf_to_images.py document.pdf \
    -o output \
    -f jpg \
    --dpi 300 \
    --quality 95 \
    --prefix img_ \
    --suffix _scan \
    --zero-pad 4 \
    --max-dim 2000
