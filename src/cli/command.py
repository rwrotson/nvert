from pathlib import Path
from typing import Annotated

from typer import Argument, Option, Typer

from cli import callbacks
from core.pdf import invert_pdf_colors
from utils.console import get_console

app = Typer()
console = get_console()


@app.command()
def invert(
    input_file: Path | None = Argument(
        ...,
        resolve_path=True,
        help="The path for the output PDF file. If not provided, saved as '[input]_inverted.pdf'.",
    ),
    output_file: Path | None = Option(
        None,
        "-o",
        "--output",
        resolve_path=True,
        help="The path for the output PDF file. If not provided, saved as '[input]_inverted.pdf'.",
    ),
    version: Annotated[
        bool,
        Option(
            "--version",
            "-v",
            callback=callbacks.version_cb,
            is_eager=True,
            help="Show the application's version and exit.",
        ),
    ] = False,
    authors: Annotated[
        bool,
        Option(
            "--authors",
            "-a",
            callback=callbacks.authors_cb,
            is_eager=True,
            help="Show the application's version and exit.",
        ),
    ] = False,
):
    """Invert colors in the provided document."""
    invert_pdf_colors(input_file, output_file)

    console.print()
