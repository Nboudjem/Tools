from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf_path, output_folder):
    # Open the original PDF
    with open(input_pdf_path, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        
        # Split each page
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])
            
            # Save each page as a separate PDF
            output_pdf_path = f"{output_folder}/page_{page_num + 1}.pdf"
            with open(output_pdf_path, "wb") as output_pdf:
                pdf_writer.write(output_pdf)
            print(f"Saved: {output_pdf_path}")

# Example usage
input_pdf = "C:/Users/User/Desktop/BOUDJEMIA.pdf"  # Replace with your PDF path
output_dir = "C:/Users/User/Desktop"  # Replace with your output directory
split_pdf(input_pdf, output_dir)