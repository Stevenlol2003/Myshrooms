import React, { useEffect, useContext } from 'react';
import { View, Text, Button, Image, StyleSheet } from 'react-native';
import { Card } from 'react-native-paper';
import { AppContext } from '../AppContext';

const PopulationPick = ({ navigation }) => {
  const { setPopulation } = useContext(AppContext);
  const singleImg = require("../single.jpeg");
  const severalImg = require("../several.jpg");
  const scatteredImg = require("../scattered.jpg");

  const handleSelection = (pop) => {
    setPopulation(pop);
    navigation.navigate("Top View");
  };

  return (
    <View style={styles.container}>
      <Text style={{fontSize: 18, margin: 12, textAlign: "center"}}>What population does the mushroom have?</Text>

      <Card style={styles.card}>
        <Text style={styles.text}>Single</Text>
        <Image style={styles.image} source={singleImg}/>
        <Text style={styles.text}>{"\n"}</Text>

        <Text style={styles.text}>Several</Text>
        <Image style={styles.image} source={severalImg}/>
        <Text style={styles.text}>{"\n"}</Text>

        <Text style={styles.text}>Scattered</Text>
        <Image style={styles.image} source={scatteredImg}/>
      </Card>
      
      <View style={styles.buttonView}>
        <View style={[styles.buttonContainer, styles.alignLeft]}>
          <Button title="Single" onPress={() => handleSelection("Single")} />
        </View>
        <View style={[styles.buttonContainer, styles.alignCenter]}>
          <Button title="Several" onPress={() => handleSelection("Several")} />
        </View>
        <View style={[styles.buttonContainer, styles.alignRight]}>
          <Button title="Scattered" onPress={() => handleSelection("Scattered")} />
        </View>
      </View>
    </View>
  );
};

export default PopulationPick;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "lightgreen",
  },
  card: {
    margin: 20,
    paddingHorizontal: 50,
    paddingVertical: 20,
  },
  buttonView: {
    flexDirection: "row", 
    justifyContent: "space-evenly"
  },
  buttonContainer: {
    width: "30%",
  },
  alignLeft: {
    alignItems: "flex-start",
  },
  alignCenter: {
    alignItems: "center",
  },
  alignRight: {
    alignItems: "flex-end",
  },
  text: {
    fontSize: 15,
    textAlign: "center",
  },
  image: {
    width: 125,
    height: 125,
    alignSelf: "center",
  },
});
