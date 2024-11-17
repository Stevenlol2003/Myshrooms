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
    edges = cv2.Canny(blurred_image, 100,200)
    # cv2.imshow("edge",edges)

    return edges, image  # Returning edges and original image for contour drawing


def extract_geometrical_features(edges):
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours



if __name__ == '__main__':

   # Example image path (replace with an actual path to your image)

    broad_image_paths = []
    narrow_image_paths = []
    image_paths = [broad_image_paths,narrow_image_paths]

    broad_dir = "./mushroom pics/broad/"
    narrow_dir = "./mushroom pics/narrow/"

   # Read images from the "broad" directory
    for filename in os.listdir(broad_dir):
     if filename.endswith('.jpg') or filename.endswith('.png'):
        broad_image_paths.append(os.path.join(broad_dir, filename))

    # Read images from the "narrow" directory
    for filename in os.listdir(narrow_dir):
     if filename.endswith('.jpg') or filename.endswith('.png'):
        narrow_image_paths.append(os.path.join(narrow_dir, filename))


    idx = 0
    for i in range(len(image_paths)):
      image_paths_dir = image_paths[i]
      for j in range(len(image_paths_dir)):
       
       image_path = image_paths_dir[j]

       # Step 1: Preprocess image (convert to grayscale, apply blur, and detect edges)
       edges, original_image = preprocess_image(image_path)

       # Step 2: Extract geometric features (aspect ratio, area, perimeter, compactness)
       contours = extract_geometrical_features(edges)

       #    # Display the extracted features
       #    print("Extracted features:", features)

       # Optionally, visualize the contours on the original image

       gray_original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
       gray_original_image_to_BGR = cv2.cvtColor(gray_original_image, cv2.COLOR_GRAY2BGR)


       for contour in contours:
         cv2.drawContours(gray_original_image_to_BGR, [contour], -1, (0, 255, 0), 2)  # Draw contours in green

       # Show the image with contours

       # Example image (assuming it's a numpy array)
       #imageSaved = cv2.imread(imageWithContours)

       if(i==0):
        cv2.imwrite(f"./new Mushroom Pics/broad/{idx}.png",gray_original_image_to_BGR)
       else:
        cv2.imwrite(f"./new Mushroom Pics/narrow/{idx}.png",gray_original_image_to_BGR)
          

        

       original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
       # plt.imshow(original_image_rgb)
       # plt.title('Contours on Original Image')
       # plt.show()
       idx+=1