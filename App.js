import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { AppProvider } from './src/components/AppContext';

import HomeScreen from './src/components/screens/HomeScreen';
import PopulationPick from './src/components/screens/PopulationPick';
import CapColorImagePick from './src/components/screens/CapColorImagePick';
import CapSizeImagePick from './src/components/screens/CapSizeImagePick';
import ReviewScreen from './src/components/screens/ReviewScreen';
import ResultScreen from './src/components/screens/ResultScreen';

const Stack = createNativeStackNavigator();

function App() {
  return (
    <AppProvider>
      <NavigationContainer>
        <Stack.Navigator initialRouteName="Home">
          <Stack.Screen name="Home" component={HomeScreen} options={{headerShown: false}}/>
          <Stack.Screen name="Population" component={PopulationPick} />
          <Stack.Screen name="Top View" component={CapColorImagePick} />
          <Stack.Screen name="Side View" component={CapSizeImagePick} />
          <Stack.Screen name="Review" component={ReviewScreen} />
          <Stack.Screen name="Result" component={ResultScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </AppProvider>
  );
}

export default App;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});