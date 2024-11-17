import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def preprocess_image(image_path):
    # Load image
    image = cv2.imread(image_path)

    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Perform Canny edge detection
    edges = cv2.Canny(blurred_image, 50,150)
    # cv2.imshow("edge",edges)

    return edges, image  # Returning edges and original image for contour drawing


def extract_geometrical_features(edges):
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours


def finding_edges():
    # Example image path (replace with an actual path to your image)
       
    image_path = "./uploads/capSizeImage.jpg"
    # Step 1: Preprocess image (convert to grayscale, apply blur, and detect edges)
    edges, original_image = preprocess_image(image_path)

    # Step 2: Extract geometric features (aspect ratio, area, perimeter, compactness)
    contours = extract_geometrical_features(edges)
    print(f"contours: {len(contours)}")

    #    # Display the extracted features
    #    print("Extracted features:", features)

    # Optionally, visualize the contours on the original image

    gray_original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    gray_original_image_to_BGR = cv2.cvtColor(gray_original_image, cv2.COLOR_GRAY2BGR)

    for contour in contours:
        cv2.drawContours(gray_original_image_to_BGR, [contour], -1, (0, 255, 0), 3)  # Draw contours in green

    # Show the image with contours

    # Example image (assuming it's a numpy array)
    #imageSaved = cv2.imread(imageWithContours)

    cv2.imwrite(f"./uploads/capSizeImage_grayScaled.png",gray_original_image_to_BGR)

    original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    # plt.imshow(original_image_rgb)
    # plt.title('Contours on Original Image')
    # plt.show()