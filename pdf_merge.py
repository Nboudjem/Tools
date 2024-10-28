from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(pdf_paths, output_pdf_path):
    pdf_writer = PdfWriter()

    for pdf_path in pdf_paths:
        pdf_reader = PdfReader(pdf_path)
        
        # Add all pages of each PDF to the writer
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

    # Write out the merged PDF
    with open(output_pdf_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)
    print(f"Merged PDF saved as: {output_pdf_path}")

# Example usage
pdf_files = ["C:/Users/User/Desktop/ID1.pdf", "C:/Users/User/Desktop/ID2.pdf"]  # List of PDF file paths
output_file = "C:/Users/User/Desktop/ID.pdf"  # Output file path
merge_pdfs(pdf_files, output_file)
