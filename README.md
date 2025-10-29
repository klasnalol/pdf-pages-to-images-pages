# pdf-pages-to-images-pages
convert your pdf with pages into folder with photos
A lightweight Python tool to split PDF pages into individual images (PNG or JPEG) using PyMuPDF. Works on Windows, macOS, and Linux with no external dependencies.

#installation:
download python than use pip to install pymupdf
pip install pymupdf

Basic Command
python pdf_to_images.py input.pdf -o out

Converts all pages of input.pdf into PNG images at 200 DPI and saves them in the out folder.

Common Examples
Action	Command
Convert to PNG (default)	python pdf_to_images.py input.pdf -o out
Convert to JPEG at 300 DPI	python pdf_to_images.py input.pdf -o out -f jpg --dpi 300
Custom JPEG quality	python pdf_to_images.py input.pdf -o out -f jpg --quality 90
Specific pages	python pdf_to_images.py input.pdf -o out -p 1-3,7,10-
Constrain long edge to 2000px	python pdf_to_images.py input.pdf -o out --max-dim 2000
Custom prefix/suffix	python pdf_to_images.py input.pdf -o out --prefix img_ --suffix _scan

#Command Line Options
Option	       Description	                        Default
pdf	           Input PDF file	                      Required
-o, --outdir	 Output directory for images	        Required
-p, --pages	   Page range (e.g. 1-3,7,10-)	        All pages
--dpi	         Image DPI (resolution)	              200
-f, --format	 Output format (png, jpg, jpeg)	      png
--quality	     JPEG quality (1–100)	                92
--zero-pad	   Zero-padding for page numbers	      3
--prefix	     Filename prefix	                    page_
--suffix	     Filename suffix	                    (none)
--max-dim	     Max long edge in pixels	            (no limit)
