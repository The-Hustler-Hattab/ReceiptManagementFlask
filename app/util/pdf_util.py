from typing import IO

from PyPDF2 import PdfReader
from werkzeug.datastructures import FileStorage



class PdfUtil:

    @staticmethod
    def get_pdf_page_count(file: bytes | IO[bytes]) -> int:
        """
        Returns the number of pages in a PDF file.

        Args:
            file (FileStorage): The PDF file as a FileStorage object.

        Returns:
            int: The number of pages in the PDF.
        """
        reader = PdfReader(file)
        return len(reader.pages)