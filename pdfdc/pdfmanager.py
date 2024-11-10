import os
from pathlib import Path
from dotenv import load_dotenv
from pypdf import PdfReader, PdfWriter
from pdfdc.utils import init_logger

APP_NAME = "pdfdc"
PREFIX = "dc-"
SUFFIX = ""


class PdfManager:
    def __init__(self, input_folder: Path):
        load_dotenv()
        if not input_folder.is_dir():
            raise NotADirectoryError(f"{input_folder=}")
        self.input_folder = input_folder
        self.log = init_logger(APP_NAME)

    def get_pdf_files(self) -> list:
        files = []
        for fp in self.input_folder.glob("*.[pP][dD][fF]"):
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

    def get_password(self, env_key: str = "PASSWORD", check: bool = True) -> str:
        pwd = os.getenv(env_key)
        if check and not pwd:
            raise RuntimeError(f"{env_key=} not found")
        return pwd if pwd else ""

    def decrypt(self, fp: Path) -> None:
        if not fp.is_file():
            raise FileNotFoundError(f"{fp=}")
        fp_out = fp.parent / f"{PREFIX}{fp.stem}{SUFFIX}.pdf"
        reader = PdfReader(fp)
        writer = PdfWriter()

        if reader.is_encrypted:
            try:
                reader.decrypt(self.get_password())
            except Exception as e:
                raise RuntimeError(f"decrypt function failed, {e=}")

        for page in reader.pages:
            writer.add_page(page)  # Add all pages to the writer

        with open(fp_out, "wb") as f:
            writer.write(f)

        self.log.info(f" >> decrypted {fp_out.name}")

    def decrypt_files(self) -> None:
        files = self.get_pdf_files()
        [self.decrypt(fp) for fp in files]
