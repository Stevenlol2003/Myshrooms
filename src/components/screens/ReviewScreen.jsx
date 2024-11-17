import React, { useContext } from 'react';
import { View, Text, Button, Image, StyleSheet } from 'react-native';
import { Card } from 'react-native-paper';
import { AppContext } from '../AppContext';

const ReviewScreen = ({ navigation }) => {
    const { population, capColorImage, capSizeImage } = useContext(AppContext);

    return (
    <View style={styles.container}>
        <Text style={{fontSize: 20, textAlign: "center"}}>Review Your Mushroom</Text>
        <Card style={styles.card}>
            <Text style={{fontSize: 14, margin: 12, textAlign: "center"}}>Population: {population}</Text>

            <Text style={styles.text}>Top View</Text>
            <Image style={styles.image} source={{uri: capColorImage}}/>
            <Text style={{fontSize: 10}}>{"\n"}</Text>

            <Text style={styles.text}>Side View</Text>
            <Image style={styles.image} source={{uri: capSizeImage}}/>
            <Text style={{fontSize: 10}}>{"\n"}</Text>

            <Button title="Predict Edibility" onPress={() => navigation.navigate("Result")}/>
        </Card>
    </View>
    );
};

export default ReviewScreen;

const styles = StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: "center",
      alignItems: "center",
      backgroundColor: "lightgreen",
    },
    card: {
        margin: 12,
        paddingHorizontal: 60,
        paddingVertical: 15,
    },
    text: {
        fontSize: 14,
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