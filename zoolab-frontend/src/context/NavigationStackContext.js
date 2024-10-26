// src/context/NavigationStackContext.js
import React, { createContext, useContext, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';

const NavigationStackContext = createContext();

export const NavigationStackProvider = ({ children }) => {
    const [navigationStack, setNavigationStack] = useState([]);
    const navigate = useNavigate();

    const pushToStack = useCallback((path) => {
        setNavigationStack((prevStack) => {
            // Verifica se il percorso esiste già come ultimo elemento
            if (prevStack[prevStack.length - 1] !== path) {
                return [...prevStack, path];
            }
            return prevStack; // Ritorna lo stack invariato se il percorso è già l'ultimo
        });
    }, []);
    

    const goBack = useCallback(() => {
        setNavigationStack((prevStack) => {
            if (prevStack.length > 1) {
                const newStack = [...prevStack];
                newStack.pop();
                navigate(newStack[newStack.length - 1]); // Torna alla pagina precedente nello stack
                return newStack;
            }
            return prevStack;
        });
    }, [navigate]);

    return (
        <NavigationStackContext.Provider value={{ navigationStack, pushToStack, goBack }}>
            {children}
        </NavigationStackContext.Provider>
    );
};

export const useNavigationStack = () => useContext(NavigationStackContext);
