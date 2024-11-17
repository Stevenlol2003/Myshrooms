from flask import Flask, jsonify, request
import random
import os
import pandas as pd
import numpy as np
import pickle as pl
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from color import get_dominant_color
from color import classify_color
from color import classify_bgr_value
from color import train_and_learn_color
from edgeDetection import finding_edges


app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the uploads folder if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def preprocess_image(image_path):
    # Load the image with OpenCV and resize to (224, 224) for MobileNet
    img = load_img(image_path, target_size=(224, 224))
    
    # Convert image to numpy array
    img_array = img_to_array(img)
    
    # Add batch dimension (shape will be (1, 224, 224, 3))
    img_array = np.expand_dims(img_array, axis=0)
    
    # Normalize pixel values to be between 0 and 1
    img_array = img_array / 255.0

    return img_array

@app.route('/')
def home():
    with open("index.html") as f:
        html = f.read()

    return html

@app.route('/predict', methods=['POST'])
def predict():
    capColorImage = request.files['capColorImage']
    capSizeImage = request.files['capSizeImage']
    population = request.form.get('population')
    print("population: ", population)

    if capColorImage and capSizeImage and population:
        capColorImage_path = os.path.join(app.config['UPLOAD_FOLDER'], capColorImage.filename)
        capSizeImage_path = os.path.join(app.config['UPLOAD_FOLDER'], capSizeImage.filename)

        capColorImage.save(capColorImage_path)
        capSizeImage.save(capSizeImage_path)        

        match population:
            case "Single":
                population = "y"
            case "Several":
                population = "v"
            case "Scattered":
                population = "s"
        print("population letter: ", population)

        # create a img file for dominant color
        value = get_dominant_color("./uploads/capColorImage.jpg")
        model = train_and_learn_color("./color_classification_dataset.csv")
        # return color classification as a letter: e, p, k, w, n
        color = classify_color("swatch.jpg")
        #color = classify_bgr_value(value, model)
        #match color:
         #   case "black":
          #      color = "k"
           # case "white":
            #    color = "w"
            #case "red":
             #   color = "e"
            #case "pink":
             #   color = "p"
            #case "brown":
             #   color = "n"
        print("color letter: ", color)

        finding_edges()

        with open('sizeModel.pkl','rb') as modelFile:
            size_model = pl.load(modelFile)

        size_predict = size_model.predict(preprocess_image("./uploads/capSizeImage_grayScaled.png"))
        print(size_predict)
        size = np.argmax(size_predict[0])
        print("size: 0", size)
        if (size == 0):
            size = "b"
        elif (size == 1) :
            size ="n"

        print("size letter: ", size)

        # Deserializing objects 
        with open('ecoders.pkl','rb') as encoderFile:
            labelEncoders = pl.load(encoderFile)

        with open('finalModel.pkl','rb') as modelFile:
            xgBoost_model = pl.load(modelFile)
        
        labelledDf1 = pd.DataFrame({"gill-size": [size], 
                   "gill-color": [color],   
                   "population": [population]
                }, index = [0])
        
        encodedDf = pd.DataFrame({})
        for i in labelledDf1.columns:
            encodedDf[i] = labelEncoders[i].transform(labelledDf1[i])

        featureArr = encodedDf.to_numpy()
        # print(featureArr)
        
        # binary classification
        prediction = xgBoost_model.predict(featureArr)
        # print("prediction 0 for safe/edible, 1 for not safe/poisonous: ")
        # print(prediction)

        is_edible = False
        if (prediction == 0):
            is_edible = True
        elif (prediction == 1): 
            is_edible = False

        return jsonify({"edible": is_edible})

    return jsonify({"error": "Invalid file"}), 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")