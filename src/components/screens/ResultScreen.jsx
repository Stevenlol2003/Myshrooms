import React, { useContext, useState, useEffect } from 'react';
import { View, Text, Button, Image, StyleSheet, ActivityIndicator } from 'react-native';
import { Card } from 'react-native-paper';
import { AppContext } from '../AppContext';
import safeImg from "../safe.jpg";
import poisonousImg from "../poisonous.jpg";

const ResultScreen = ({ navigation }) => {
  const { population, capColorImage, capSizeImage, setResult, result } = useContext(AppContext);
  const [isLoading, setIsLoading] = useState(true);
  const [isSafe, setIsSafe] = useState(true);
  const [safeOrNot, setSafeOrNot] = useState("");
  const [img, setImg] = useState();

  // formData example: https://stackoverflow.com/questions/61763057/react-native-upload-image-file-to-django-backend
  const sendImagesToBackend = async () => {
    const formData = new FormData();

    // add the population as a string
    formData.append('population', population);

    // add the images as files using FormData
    if (capColorImage) {
      formData.append('capColorImage', {
        uri: capColorImage,
        type: 'image/jpeg',
        name: 'capColorImage.jpg',
      });
    }

    if (capSizeImage) {
      formData.append('capSizeImage', {
        uri: capSizeImage,
        type: 'image/jpeg',
        name: 'capSizeImage.jpg',
      });
    }
    
    console.log(formData);

    // replace with current server device's ip
    try {
      const response = await fetch('http://10.140.88.122:5000/predict', {
        method: 'POST',
        body: formData,
      });

      // const text = await response.text(); // raw response text for debugging
      // console.log('Response text:', text);

      const data = await response.json();
      console.log(data)
      setIsLoading(false);
      setIsSafe(data.edible);
      setSafeOrNot(data.edible ? "safe to eat!" : "poisonous!");
      setImg(data.edible ? safeImg : poisonousImg);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    sendImagesToBackend();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={{fontSize: 20, textAlign: "center"}}>Prediction Result</Text>
        <Card style={styles.card}>
            {!isLoading ? (
              <>
                <Text style={styles.text}>Your mushroom is {safeOrNot}</Text>
                {img && <Image style={styles.image} source={img}/>}
              </>
            ) : (
              <>
                <ActivityIndicator size="large" color="grey"/>
                <Text style={styles.text}>Loading...</Text>
              </>
            )}
            
            <Text style={{fontSize: 10}}>{"\n"}</Text>
            <Button title="Go back home" onPress={() => navigation.navigate("Home")}/>
        </Card>
    </View>
  );
};

export default ResultScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: "lightgreen",
  },
  card: {
      margin: 12,
      paddingHorizontal: 50,
      paddingVertical: 20,
  },
  text: {
      fontSize: 14,
      margin: 12,
      textAlign: "center",
  },
  button: {
      fontSize: 14,
  },
  image: {
      width: 200,
      height: 200,
      alignSelf: "center",
  }
});
