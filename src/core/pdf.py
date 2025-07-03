import os
from pathlib import Path

import pymupdf

from core.files import File


def invert_pdf_colors(input_path: str | Path, output_path: str | Path):
    """
    Inverts the colors of a PDF file while preserving vector quality.

    This function works by creating a new PDF. For each page of the input
    PDF, it creates a corresponding page in the new PDF. It then lays down
    a white background and "stamps" the original page content on top using
    the 'Difference' blend mode. This effectively inverts all colors.

    - Black (0) on white (1) becomes abs(0 - 1) = 1 (White).
    - White (1) on white (1) becomes abs(1 - 1) = 0 (Black).
    - A color C on white (1) becomes abs(C - 1), which is its inverse.
    """
    file = File(input_path)

    try:
        source_pdf = pymupdf.open(filetype="pdf", stream=file.content)

        inverted_pdf = pymupdf.open()

        print(f"Processing {len(source_pdf)} pages from '{os.path.basename(input_path)}'...")

        for i, page in enumerate(source_pdf):
            print(f"Processing page {i} of '{os.path.basename(input_path)}'...")
            new_page = inverted_pdf.new_page(width=page.rect.width, height=page.rect.height)

            new_page.show_pdf_page(new_page.rect, source_pdf, i)

            points = [page.rect.tl, page.rect.tr, page.rect.br, page.rect.bl]
            annotation = new_page.add_polygon_annot(points)
            annotation.set_colors(fill=(1, 1, 1))
            annotation.set_blendmode("Difference")
            annotation.set_opacity(1)
            annotation.set_border(width=0)
            annotation.update()

            print(f"  - Page {i + 1} inverted.")

        inverted_pdf.save(output_path)

        print(f"\nSuccessfully created inverted PDF: '{output_path}'")

    except Exception as e:
        print(f"An error occurred during PDF processing: {e}")
        if os.path.exists(output_path):
            os.remove(output_path)
        raise e

    finally:
        if "source_pdf" in locals() and source_pdf:
            source_pdf.close()
        if "inverted_pdf" in locals() and inverted_pdf:
            inverted_pdf.close()
