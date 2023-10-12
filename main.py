import os
import logging
from pathlib import Path
from dotenv import load_dotenv

from pypdf import PdfReader, PdfWriter

PREFIX = "dc-"
SUFFIX = ""
CWD = Path(__file__).parent


def init_logger() -> logging.Logger:
    """
    initialize an logger (console output and file output)
    returns existing logger if already initialized before
    """
    logger_name = __name__
    logger = logging.getLogger(logger_name)
    if logger.hasHandlers():
        return logger
    c_handler = logging.StreamHandler()
    c_format = logging.Formatter("%(levelname)-8s: %(message)s")
    c_handler.setFormatter(c_format)
    c_handler.setLevel(logging.INFO)
    logger.addHandler(c_handler)
    logger_filename = f"{logger_name}.log" if logger_name != "__main__" else "main.log"
    f_handler = logging.FileHandler(logger_filename)
    f_format = logging.Formatter(
        "[%(asctime)s]%(levelname)-8s: %(message)s", "%d-%b-%y %H:%M"
    )
    f_handler.setFormatter(f_format)
    f_handler.setLevel(logging.INFO)
    logger.addHandler(f_handler)
    logger.setLevel(logging.INFO)
    logger.info(f"logger initialized - {logger_filename}")
    return logger


class PdfManager:
    def __init__(self):
        self.log = init_logger()

    def get_pdf_files(self) -> list:
        files = []
        for fp in CWD.glob("*.[pP][dD][fF]"):
            if PREFIX and SUFFIX:
                if (PREFIX not in fp.name) and (SUFFIX not in fp.name):
                    files.append(fp)
                else:
                    continue
            elif PREFIX:
                if PREFIX not in fp.name:
                    files.append(fp)
                else:
                    continue
            elif SUFFIX:
                if SUFFIX not in fp.name:
                    files.append(fp)
                else:
                    continue

        return files

    def get_password(self, env_key: str = "PASSWORD") -> str:
        pwd = os.getenv(env_key)
        return pwd if pwd else ""

    def decrypt(self, fp: Path) -> None:
        fp_out = fp.parent / f"{PREFIX}{fp.stem}{SUFFIX}.pdf"
        reader = PdfReader(fp)
        writer = PdfWriter()
        if reader.is_encrypted:
            reader.decrypt(self.get_password())

        for page in reader.pages:
            writer.add_page(page)  # Add all pages to the writer

        with open(fp_out, "wb") as f:
            writer.write(f)

        self.log.info(f" >> decrypted {fp_out.name}")

    def decrypt_files(self) -> None:
        files = self.get_pdf_files()
        for fp in files:
            self.decrypt(fp)


def main():
    """
    Search root directory for PDF files, decrypt all of them
    """
    pm = PdfManager()
    pm.decrypt_files()


if __name__ == "__main__":
    load_dotenv()
    main()
