# pdfdecrypt

Simple python code to decrypt pdf files using pypdf.PdfReader

## Quick start

1. Update your environment variables for `PASSWORD`

   Recommended: Use `python-dotenv`. Create `.env` file in root directory (same dir as `cli.py`) with the following line

   ```text
   PASSWORD="your_password"
   ```

1. Copy your encrypted files to the root directory (same dir as `cli.py`)

1. Run `cli.py`

   ```console
   git clone git clone git@github.com:jakelime/pdfdecrypt.git
   # Download your "encrypted.pdf" file
   python cli.py
   ```
