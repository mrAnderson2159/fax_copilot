import { useState, useRef } from "react";

export const useClickHandlers = ({ clickHandler, onLongPress }) => {
    const [isPressed, setIsPressed] = useState(false);
    const [isLongPress, setIsLongPress] = useState(false);
    const alreadyClicked = useRef(false);
    const isPressedRef = useRef(false);
    let pressTimer;

    const handlePressStart = () => {
        if (alreadyClicked.current) {
            alreadyClicked.current = false;
            return;
        }

        setIsPressed(true);
        isPressedRef.current = true;

        setIsLongPress(false);
        alreadyClicked.current = false;

        pressTimer = setTimeout(() => {
            if (isPressedRef.current) {
                setIsLongPress(true);
                onLongPress();
            }
        }, 500); // Tempo per il long press
    };

    const handlePressEnd = () => {
        clearTimeout(pressTimer);

        if (isPressedRef.current && !alreadyClicked.current) {
            alreadyClicked.current = true;
            clickHandler();
        }

        setIsPressed(false);
        isPressedRef.current = false;
        setIsLongPress(false);
    };

    return {
        handlePressStart,
        handlePressEnd,
        isPressed,
    };
};
