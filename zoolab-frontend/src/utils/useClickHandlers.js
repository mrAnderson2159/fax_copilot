import { useState, useRef } from "react";

export const useClickHandlers = ({ clickHandler, onLongPress }) => {
    const [isPressed, setIsPressed] = useState(false);
    const [isLongPress, setIsLongPress] = useState(false);
    const alreadyClicked = useRef(false);
    const isPressedRef = useRef(false);
    const pressTimer = useRef(null); // Cambiato a useRef per mantenere il riferimento tra render.

    const handlePressStart = () => {
        if (alreadyClicked.current) {
            alreadyClicked.current = false;
            return;
        }

        // Gonfia la carta quando inizia il press
        setIsPressed(true);
        isPressedRef.current = true;

        setIsLongPress(false);
        alreadyClicked.current = false;

        pressTimer.current = setTimeout(() => {
            if (isPressedRef.current) {
                setIsLongPress(true);
                onLongPress();
                alreadyClicked.current = true; // Impedisce il clickHandler se è stato un long press
            }
        }, 500); // Tempo per il long press
    };

    const handlePressEnd = () => {
        // Utilizza `requestAnimationFrame` per assicurarti che l'animazione di gonfiamento inizi
        requestAnimationFrame(() => {
            // Cancella il timer di press se è ancora in esecuzione
            if (pressTimer.current) {
                clearTimeout(pressTimer.current);
            }

            // Gestione del click singolo solo se non c'è stato un long press
            if (isPressedRef.current && !isLongPress) {
                alreadyClicked.current = true;
                clickHandler();
            }

            // Sgonfia la carta al rilascio del click con un leggero ritardo
            setTimeout(() => {
                setIsPressed(false);
                isPressedRef.current = false;
                setIsLongPress(false);
            }, 50); // Ritardo per assicurare che l'animazione di gonfiamento sia visibile
        });
    };

    return {
        handlePressStart,
        handlePressEnd,
        isPressed,
    };
};
