import cv2
import pytesseract
import numpy as np

def preprocess(img_path):
    
    return 0

def detect_type(image_path):

    # Load the image using OpenCV imread()
    img = cv2.imread(image_path)
    if img is None:
        return "Image not found."

    # Convert to grayscale for analysis
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 1. Check for 'Blurriness' / Noise (Laplacian Variance)
    # Higher values often indicate photos; lower values can indicate flat screenshots.
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    # 2. Detect Straight Lines (Hough Lines)
    # Screenshots are built on grids and windows.
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, 
                            minLineLength=100, maxLineGap=5)
    
    line_count = len(lines) if lines is not None else 0

    # Decision logic (thresholds vary by image resolution)
    if line_count > 50 and laplacian_var < 500:
        return f"Likely a Screenshot (Lines: {line_count}, Noise: {laplacian_var:.2f})"
    else:
        return f"Likely a Photo (Lines: {line_count}, Noise: {laplacian_var:.2f})"

def main():
    ss_img_path = '/home/erinmq/Projects/chuni-cv-ovr/img/verse-results-1.png'
    cam_img_path = '/home/erinmq/Projects/chuni-cv-ovr/img/para-lost-cam.jpg'

    print(detect_type(ss_img_path) + " SS")
    print(detect_type(cam_img_path) + " PH")

if __name__ == "__main__":
    main()
