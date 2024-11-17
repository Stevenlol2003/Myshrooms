import React, { useState }  from 'react';
import { View, Text, Button, StyleSheet, Modal, Image } from 'react-native';
import { Card } from 'react-native-paper';

const HomeScreen = ({ navigation }) => {
    const [modalVisible, setModalVisible] = useState(false);
    const myshroomsImg = require("../myshrooms.jpg");

    return (
    <View style={styles.homeView}>
        <Text style={styles.text}>{"\n"}</Text>
        <Text style={styles.text}>{"\n"}</Text>
        <Text style={styles.text}>{"\n"}</Text>
        <Text style={styles.text}>{"\n"}</Text>
        <Card style={styles.card}>
            <Image style={styles.image} source={myshroomsImg}/>
            <Text style={{fontSize: 20, margin: 12}}>A Mushroom Edibility Predictor</Text>
            <Button title="Get Started" onPress={() => navigation.navigate("Population")}/>
        </Card>
        <Text style={styles.text}>{"\n"}</Text>
        <Text style={styles.text}>{"\n"}</Text>
        <Text style={styles.text}>{"\n"}</Text>
        <Button title="About Us" onPress={() => setModalVisible(true)}/>
        <Modal
            animationType="fade"
            transparent={true}
            visible={modalVisible}
            onRequestClose={() => {setModalVisible(!modalVisible)}}>
            <View style={styles.centeredView}>
                <View style={styles.modalView}>
                    <Text style={{fontSize: 20, margin: 12}}>About Us</Text>
                    <Text style={{fontSize: 13, textAlign: "center"}}>This is a project made by UW-Madison students Steven Ren, Rushil Sambangi, and Aditya Goyal in the CheeseHacks 2024 hackathon through November 16 to November 17.</Text>
                    <Button style={styles.button} title="Close" onPress={() => setModalVisible(!modalVisible)}/>
                </View>
            </View>
        </Modal>
        <Text style={styles.text}>Disclaimer: Eat wild mushrooms at your own risk!</Text>
    </View>
    );
};

export default HomeScreen;

const styles = StyleSheet.create({
    homeView: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "lightgreen",
    },
    card: {
        margin: 15,
        padding: 25,
        justifyContent: "center",
        alignItems: "center",
    },
    centeredView: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        marginTop: 22,
    },
    modalView: {
        margin: 15,
        backgroundColor: "white",
        borderRadius: 20,
        padding: 25,
        alignItems: "center",
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 2,
        },
        shadowOpacity: 0.25,
        shadowRadius: 4,
        elevation: 5,
    },
    button: {
        fontSize: 15,
    },
    submitButton: {
    position: 'absolute',
    bottom:0,
    left:0,
    },
    text: {
        fontSize: 15,
        textAlign: "center",
    },
    image: {
        width: 250,
        height: 250,
        alignSelf: "center",
    },
});