import cv2
import numpy as np
from sklearn.cluster import KMeans
import math
import os
from os import listdir
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
import requests
import json

def get_dominant_color(image_path, num_colors=3, central_crop_fraction=0.5):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found!")
        return

    # Resize for faster processing
    resized_image = cv2.resize(image, (500, 500))

    # Get dimensions and crop to the central region
    height, width, _ = resized_image.shape
    center_x, center_y = width // 2, height // 2
    crop_w, crop_h = int(width * central_crop_fraction), int(height * central_crop_fraction)
    x1, y1 = center_x - crop_w // 2, center_y - crop_h // 2
    x2, y2 = center_x + crop_w // 2, center_y + crop_h // 2
    central_crop = resized_image[y1:y2, x1:x2]

    # Reshape the cropped region for K-Means clustering
    reshaped_crop = central_crop.reshape((-1, 3))

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    labels = kmeans.fit_predict(reshaped_crop)
    dominant_colors = kmeans.cluster_centers_.astype("uint8")  # Get dominant colors (BGR)

    # Find the most frequent label
    label_counts = np.bincount(labels)
    dominant_label = np.argmax(label_counts)

    # Get the color corresponding to the dominant label
    best_color = dominant_colors[dominant_label]

    print(f"Dominant Color (BGR): {best_color}")

    # Visualize results
    #cv2.imshow("Original Image", resized_image)

    # Show the central cropped region
    cv2.rectangle(resized_image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw rectangle around the crop
    #cv2.imshow("Central Crop", central_crop)

    # Display the dominant color as a color swatch
    color_swatch = np.zeros((100, 100, 3), dtype=np.uint8)
    color_swatch[:] = best_color
    # cv2.imshow("Dominant Color Swatch", color_swatch)
    # print("debug")
    cv2.imwrite("swatch.jpg", color_swatch)

    # Wait for user input to close windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return best_color[:3]


def determine_color(avg_color):
    colors = {}
    colors["k"] = [64, 64, 64]
    colors["w"] = [220, 249, 255]
    colors["e"] = [0, 0, 255]
    colors["p"] = [204, 153, 255]
    colors["n"] = [119, 136, 157]

    x1, y1, z1 = avg_color[:3]

    distances = {}
    for key, value in colors.items():
        x2, y2, z2 = value
        distance =  math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        distances[key] = distance

    return min(distances, key=distances.get)

def train_and_learn_color(dataset):
    # Load dataset
    data = pd.read_csv(dataset)
    X = data[["Blue", "Green", "Red"]]
    y = data["Label"]

    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train k-NN classifier
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)

    # Evaluate the model
    #y_pred = knn.predict(X_test)
    #print(classification_report(y_test, y_pred))

    return knn

def classify_bgr_value(bgr_value, model):
    """
    Classify a single BGR color value using a trained model.
    
    Parameters:
        bgr_value (list or array): The BGR color value to classify, e.g., [50, 60, 200].
        model: Trained machine learning model.
        
    Returns:
        str: Predicted color class label.
    """
    # Ensure the input is a 2D array as expected by scikit-learn
    bgr_array = np.array(bgr_value).reshape(1, -1)
    
    # Predict the color class
    predicted_label = model.predict(bgr_array)[0]
    
    return predicted_label

def classify_color(swatch):
    url = 'https://www.nyckel.com/v1/functions/the-color-of-a-couch/invoke'
    headers = {
        'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCJ9.eyJuYmYiOjE3MzE4NDUxNDIsImV4cCI6MTczMTg0ODc0MiwiaXNzIjoiaHR0cHM6Ly93d3cubnlja2VsLmNvbSIsImNsaWVudF9pZCI6ImV2Y25ncHJudjU4NWNzdXZsMTNvZWVnM2Q5aWNjMXJvIiwianRpIjoiMzY2MDY4RDM0RTZDMjFCQTM0NTA3RUQ2NTYxQjJCODkiLCJpYXQiOjE3MzE4NDUxNDIsInNjb3BlIjpbImFwaSJdfQ.NAa25kri930wezpaLvzogehLVmB-bGr3_lmt_eaE7qoM_bF-IZVgxWfeyCAKGNt1wBqfseiLYErXOVRBLZdsDnSs4RN8x2-dE3F1AKylsibud8Aw23SIA3dvK-NrmKgbJ-nR65AGyynid92LllfYBK1FYb1MHgG9AccvzyfrMzYGOalNJ9noZPlHZomBu4SrH-f9wAOcZtzPfpcSMF-dEBPOUca72AhAqU9wHRVfM5fmIph0E43u4Qa5lbB1JjUlX6Q-thTejKHvx1YeAq4CIH769B6la_bQaqhmHyPlvaCELHjzY9Oik1i8zy2X3jiSQ5HhHUHm4Zz9rGtTE40pVA',
    }
    with open(swatch, 'rb') as f:
        result = requests.post(url, headers=headers, files={'data': f})
    response_data = json.loads(result.text)

    # Extract the "labelName" value
    label_name = response_data.get("labelName")
    match label_name:
        case "Orange":
            return "n"
        case "Red":
            return "e"
        case "Pink":
            return "p"
        case "Black":
            return "k"
        case "Purple":
            return "k"
        case "Blue":
            return "k"
        case "Green":
            return "k"
        case "White":
            return "w"
        case "Yellow":
            return "w"
        case "Beige":
            return "w"
        case "Brown":
            return "n"
        case "Silver":
            return "w"
        case "Gold":
            return "w"
        case "Grey":
            return "w"
        case "Light Blue":
            return "w"
        case "Dark Blue":
            return "k"
        case _:
            return "n"

def test_classification(file_path):
    outputs = {}
    index = 1
    colors = []
    for image in os.listdir(file_path):
        avg_color = get_dominant_color(f'{file_path}/{image}')
        outputs[index] = classify_color("swatch.jpg")
        colors.append(avg_color)
        index += 1
    print(outputs)


# Run the function with your image
#color = get_dominant_color("brown.png")
#print(classify_color("swatch.jpg"))
#print(determine_color(avg_color))
#test_classification("white_domecap")
#model = train_and_learn_color("color_classification_dataset.csv")
#test_classification("pink", model)