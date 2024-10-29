import cv2
import numpy as np
import os

def process_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours, img, thresh

def extract_characters(contours, img, output_folder):
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if w > 5 and h > 10:  # Filter out small noises
            char_img = img[y:y+h, x:x+w]
            char_img = cv2.resize(char_img, (32, 32))  # Resize to a consistent size
            cv2.imwrite(os.path.join(output_folder, f'char_{i}.png'), char_img)

def main():
    input_folder = input("Enter the path to your images folder: ")
    output_folder = os.path.join(os.path.dirname(input_folder), 'extracted_characters')
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('.jpeg'):
            image_path = os.path.join(input_folder, filename)
            contours, img, thresh = process_image(image_path)
            extract_characters(contours, img, output_folder)

    print("Character extraction completed.")

if __name__ == '__main__':
    main()