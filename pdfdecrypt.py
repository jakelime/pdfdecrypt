
from pypdf import PdfReader, PdfWriter

input_filename = "encrypted_pdffile.pdf"
password = "password"
output_filename = "decrypted_pdffile.pdf"

reader = PdfReader(input_filename)
writer = PdfWriter()

if reader.is_encrypted:
    reader.decrypt("password")

# Add all pages to the writer
for page in reader.pages:
    writer.add_page(page)

# Save the new PDF to a file
with open(output_filename, "wb") as f:
    writer.write(f)
