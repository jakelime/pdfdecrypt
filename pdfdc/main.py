from pathlib import Path
from pdfdc.pdfmanager import PdfManager

APP_NAME = "pdfdc"


def decrypt_files(folder: Path):
    """
    Search root directory for PDF files, decrypt all of them
    """
    pm = PdfManager(folder)
    pm.decrypt_files()
