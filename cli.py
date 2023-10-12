from pathlib import Path
from pdfdc.main import decrypt_files

def main():
    cwd = Path(__file__).parent
    decrypt_files(cwd)

if __name__ == "__main__":
    main()
