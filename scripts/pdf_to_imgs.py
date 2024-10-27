import fitz  # PyMuPDF
import os

def extract_images_from_pdf(pdf_path):
    output_folder = os.path.join(os.path.dirname(pdf_path), "extracted_images")
    os.makedirs(output_folder, exist_ok=True)

    pdf_document = fitz.open(pdf_path)
    image_count = 0

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_count += 1

            # Save with a simple filename like 1.jpeg, 2.jpeg, etc.
            image_filename = os.path.join(output_folder, f"{image_count}.{image_ext}")
            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)

    pdf_document.close()
    print(f"Extracted {image_count} images to '{output_folder}'")

def main():
    pdf_file_path = input("Enter the PDF file path: ")
    
    if not pdf_file_path.lower().endswith('.pdf'):
        print("Error: The specified file is not a PDF.")
        return

    if not os.path.isfile(pdf_file_path):
        print("Error: The specified file does not exist.")
        return

    try:
        extract_images_from_pdf(pdf_file_path)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()