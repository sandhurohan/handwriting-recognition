import cv2
import os

input_folder = input("Enter the path to your images folder: ").strip()
output_folder = os.path.join(os.path.dirname(input_folder), 'cropped_images')
os.makedirs(output_folder, exist_ok=True)

threshold_value = 150
min_contour_area = 100  # Try reducing this value if needed

for filename in os.listdir(input_folder):
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):  # Include jpeg
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        
        if img is None:
            print(f"Failed to read image: {filename}")
            continue
        
        print(f"Processing image: {filename}")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, threshold_value, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            print(f"No contours found in image: {filename}")
            continue

        cropped_count = 0
        
        for cnt in contours:
            contour_area = cv2.contourArea(cnt)
            print(f"Contour area: {contour_area}")  # Print contour area for debugging
            
            if contour_area > min_contour_area:
                x, y, w, h = cv2.boundingRect(cnt)
                char_img = img[y:y+h, x:x+w]
                output_filename = os.path.join(output_folder, f'{filename[:-4]}_crop_{x}_{y}.png')
                cv2.imwrite(output_filename, char_img)
                cropped_count += 1

        if cropped_count == 0:
            print(f"No valid contours found in image: {filename}")
        else:
            print(f"Cropped {cropped_count} images from {filename}")

print("Cropping completed!")