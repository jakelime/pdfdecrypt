import os
from pathlib import Path
from pdfdc.pdfmanager import PdfManager
from pdfdc.utils import init_logger

APP_NAME = "pdfdc"

lg = init_logger(APP_NAME)


class CustommPdfManager(PdfManager):
    def __init__(self, input_folder: Path):
        super().__init__(input_folder)

    def rename_files(self):
        counter = 0
        for fp in self.get_pdf_files():
            datetimestr = fp.name.split("-")[2]

            if len(datetimestr) == 8 and ("(daily)" not in fp.name):
                new_path = fp.parent / f"(daily){fp.name}"
                os.rename(fp, new_path)
                counter += 1
        match counter:
            case 0:
                lg.info("no files renamed")
            case _:
                lg.info(f"renamed {counter} files")


def rename_daily_pdfs(folder: Path):
    """
    Search root directory for PDF files, decrypt all of them
    """
    pm = CustommPdfManager(folder)
    pm.rename_files()
