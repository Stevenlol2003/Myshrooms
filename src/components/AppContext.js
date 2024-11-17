import React, { createContext, useState } from 'react';

export const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [population, setPopulation] = useState(null);
  const [capColorImage, setCapColorImage] = useState(null);
  const [capSizeImage, setCapSizeImage] = useState(null);
  const [result, setResult] = useState(null);

  return (
    <AppContext.Provider
      value={{
        population,
        setPopulation,
        capColorImage,
        setCapColorImage,
        capSizeImage,
        setCapSizeImage,
        result,
        setResult,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};
