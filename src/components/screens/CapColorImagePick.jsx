import React, { useContext, useState, useEffect } from 'react';
import { View, Text, Button, Image, StyleSheet, ScrollView } from 'react-native';
import { Card } from 'react-native-paper';
import * as ImagePicker from 'expo-image-picker';
import { AppContext } from '../AppContext';

const CapColorImagePick = ({ navigation }) => {
  const { capColorImage, setCapColorImage } = useContext(AppContext);
  const [isDisabled, setIsDisabled] = useState(true);
  const topViewImg = require("../top_view.png");

  useEffect(() => {
    if (capColorImage) {
      setIsDisabled(false);
    } else {
      setIsDisabled(true);
    }
  }, [capColorImage]);

  const selectPhoto = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
        setCapColorImage(result.assets[0].uri);
        setIsDisabled(false);
    }
  };

  const takePhoto = async () => {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert("Error","We need camera roll permissions for this!");
      return;
    }

    let result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      setCapColorImage(result.assets[0].uri);
      setIsDisabled(false);
    }
  };

  return (
    <View style={styles.container}>
        <Text style={{fontSize: 20, textAlign: "center"}}>Mushroom Top View Photo</Text>
        <Card style={styles.card}>
            <Text style={styles.text}>What your photo should look like:</Text>
            <Image style={styles.image} source={topViewImg}/>
            <Text style={{fontSize: 14, margin: 12, textAlign: "center"}}>Please zoom in and capture{"\n"}the mushroom only!</Text>
            {capColorImage ? (
                <>
                <Text style={styles.smallText}>Photo Selected!</Text>
                <Image style={styles.image} source={{uri: capColorImage}}/>
                </>
            ) : (
                <Text style={styles.smallText}>Upload A Photo!</Text>
            )}

            <View style={styles.buttonView}>
                <Button style={styles.button} title="Select Photo" onPress={() => selectPhoto()}/>
                <Button style={styles.button} title="Take Photo" onPress={() => takePhoto()}/>
            </View>
        </Card>
        <Button style={styles.button} disabled={isDisabled} title="Next" onPress={() => navigation.navigate("Side View")}/>
    </View>
  );
};

export default CapColorImagePick;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "lightgreen",
  },
  card: {
      margin: 12,
      paddingVertical: 15,
      paddingHorizontal: 50,
  },
  text: {
      fontSize: 14,
      margin: 12,
      textAlign: "center",
  },
  smallText: {
      fontSize: 14,
      color: "darkred",
      textAlign: "center",
  },
  buttonView: {
      flexDirection: "row", 
      justifyContent: "space-evenly"
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