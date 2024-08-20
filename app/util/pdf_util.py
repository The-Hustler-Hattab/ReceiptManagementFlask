import io
from typing import List

from PyPDF2 import PdfReader, PdfWriter
from werkzeug.datastructures import FileStorage


class PdfUtil:

    @staticmethod
    def get_pdf_page_count(file: FileStorage) -> int:
        """
        Returns the number of pages in a PDF file.

        Args:
            file (FileStorage): The PDF file as a FileStorage object.

        Returns:
            int: The number of pages in the PDF.
        """
        reader = PdfReader(file)
        return len(reader.pages)

    @staticmethod
    def split_pdf_pages(file: FileStorage) -> List[FileStorage]:
        """
        Splits a PDF file into individual pages and returns a list of FileStorage objects.
        Each FileStorage object represents a single-page PDF.

        Args:
            file (FileStorage): A FileStorage object representing the PDF file to be split.

        Returns:
            List[FileStorage]: A list of FileStorage objects, where each represents a single-page PDF.
            :param file:
            :param file_name:
        """
        # Create a PdfReader object
        pdf_reader = PdfReader(file)

        # Prepare the list to hold the result
        file_storage_list: List[FileStorage] = []

        # Iterate through each page in the PDF
        for i in range(len(pdf_reader.pages)):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[i])

            # Create a BytesIO object to hold the bytes of the new PDF
            pdf_bytes = io.BytesIO()
            pdf_writer.write(pdf_bytes)
            pdf_bytes.seek(0)

            # Create a unique name for the new PDF
            new_name = f"{file.name}_page_{i + 1}.pdf"

            # Create a FileStorage object from the BytesIO object
            file_storage = FileStorage(
                stream=pdf_bytes,
                filename=new_name,
                content_type='application/pdf'
            )

            # Append the FileStorage object to the list
            file_storage_list.append(file_storage)

        return file_storage_list
