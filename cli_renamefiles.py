from pathlib import Path
from pdfdc import rename_files

def main():
    cwd = Path(__file__).parent
    rename_files.rename_daily_pdfs(cwd)

if __name__ == "__main__":
    main()
