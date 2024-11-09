// src/context/SoundContext.js
import React, { createContext, useContext } from "react";
import { Howl } from "howler";
import backSound from "../assets/sounds/back.mp3";
import clickSound from "../assets/sounds/click.mp3";
import highConfirmSound from "../assets/sounds/high_conferm.mp3";
import lowConfirmSound from "../assets/sounds/low_confirm.mp3";
import errorSound from "../assets/sounds/error.mp3";

// Crea il contesto
const SoundContext = createContext();

// Provider per il contesto dei suoni
export const SoundProvider = ({ children }) => {
    // Crea gli oggetti Howl per ogni suono
    const soundRefs = {
        backSound: new Howl({ src: [backSound], preload: true }),
        clickSound: new Howl({ src: [clickSound], preload: true }),
        highConfirmSound: new Howl({ src: [highConfirmSound], preload: true }),
        lowConfirmSound: new Howl({ src: [lowConfirmSound], preload: true }),
        errorSound: new Howl({ src: [errorSound], preload: true }),
    };

    const playSound = (audioKey) => {
        const sound = soundRefs[audioKey];
        if (sound) {
            sound.stop(); // Ferma eventuali riproduzioni precedenti
            sound.play(); // Riproduci il suono
        } else {
            console.error(`Suono non trovato: ${audioKey}`);
        }
    };

    const sounds = {
        backSound: () => playSound("backSound"),
        clickSound: () => playSound("clickSound"),
        highConfirmSound: () => playSound("highConfirmSound"),
        lowConfirmSound: () => playSound("lowConfirmSound"),
        errorSound: () => playSound("errorSound"),
    };

    return (
        <SoundContext.Provider value={sounds}>{children}</SoundContext.Provider>
    );
};

export const useSound = () => {
    return useContext(SoundContext);
};
