import zipfile, os, shutil
from PyPDF2 import PdfWriter, PdfReader


class PDFMerger:
    def __init__(self, zip_filename):
        self.zip_filename = zip_filename
        self.temp_dir = "temp_pdfs"
        self.output_pdf = os.path.join(os.path.dirname(zip_filename), "merged_output.pdf")

    def check_zip_file(self):
        if not os.path.isfile(self.zip_filename):
            print(f"Error: ZIP file '{self.zip_filename}' not found.")
            return False
        return True

    def extract_zip(self):
        try:
            with zipfile.ZipFile(self.zip_filename, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
                print(f"Extracted ZIP file: {self.zip_filename}")
        except zipfile.BadZipFile:
            print(f"Error: '{self.zip_filename}' is not a valid ZIP file.")
            return False
        return True

    def get_pdf_files(self):
        pdf_files = []
        for root, _, files in os.walk(self.temp_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        return pdf_files

    def merge_pdfs(self, pdf_files):
        writer = PdfWriter()
        for pdf_file in pdf_files:
            try:
                reader = PdfReader(pdf_file)
                for page in range(len(reader.pages)):
                    writer.add_page(reader.pages[page])
                print(f"Added: {pdf_file}")
            except Exception as e:
                print(f"Error while adding {pdf_file}: {str(e)}")
                continue  # Skip this file and continue with the next one

        if len(writer.pages) == 0:
            print("No valid PDF files were added. Exiting.")
            return False

        try:
            with open(self.output_pdf, 'wb') as output_file:
                writer.write(output_file)
                print(f"Merged PDF saved as: {self.output_pdf}")
        except Exception as e:
            print(f"Error while saving merged PDF: {str(e)}")
            return False

        return True

    def cleanup(self):
        # Remove the temporary directory and its contents
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print(f"Deleted temporary directory: {self.temp_dir}")

    def run(self):
        if not self.check_zip_file():
            return

        if not self.extract_zip():
            return

        pdf_files = self.get_pdf_files()
        if not pdf_files:
            print("Error: No PDF files found in the ZIP archive.")
            self.cleanup()  # Cleanup if no PDF files found
            return

        self.merge_pdfs(pdf_files)
        self.cleanup()  # Cleanup after merging

if __name__ == "__main__":
    zip_path = input("Please enter the path to the ZIP file: ")
    merger = PDFMerger(zip_path)
    merger.run()