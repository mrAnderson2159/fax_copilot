// zoolab-frontend/src/utils/useClickHandlers.js
import { useState, useRef } from "react";
import { debug } from "../utils";

const DEBUG_MODE = true;

export const useClickHandlers = ({ clickHandler, onLongPress }) => {
    const [isPressed, setIsPressed] = useState(false);
    const [isLongPress, setIsLongPress] = useState(false);
    const alreadyClicked = useRef(false);
    const isPressedRef = useRef(false);
    const pressTimer = useRef(null); // Cambiato a useRef per mantenere il riferimento tra render
    const lastClick = useRef(0);
    const localDebug = (functionName, ...stuff) =>
        debug(DEBUG_MODE, "useClickHandlers.js", functionName, ...stuff);

    const allowClick = (threshold = 60) => {
        const currentTime = performance.now();
        const delta = currentTime - lastClick.current;

        localDebug("handlePressStart", "Checking if click is allowed", {
            lastClick: lastClick.current,
            delta,
            currentTime,
            threshold,
        });

        if (lastClick.current === 0 || delta >= threshold) {
            lastClick.current = currentTime;
            return true;
        }
        return false;
    };

    const handlePressStart = () => {
        localDebug("handlePressStart", "Press start detected");

        const clickAllowed = allowClick();

        if (!clickAllowed || alreadyClicked.current) {
            localDebug(
                "handlePressStart",
                clickAllowed ? "Already clicked" : "Click not allowed",
                "resetting states"
            );
            alreadyClicked.current = false;
            setIsPressed(false);
            setIsLongPress(false);
            isPressedRef.current = false;
            return;
        }

        localDebug(
            "handlePressStart",
            "Setting isPressed to true and initializing pressTimer",
            "Setting isLongPress to false and alreadyClicked to false"
        );
        // Gonfia la carta quando inizia il press
        setIsPressed(true);
        isPressedRef.current = true;

        setIsLongPress(false);
        alreadyClicked.current = false;

        pressTimer.current = setTimeout(() => {
            localDebug("handlePressStart", "Long press timer expired");
            if (isPressedRef.current) {
                localDebug(
                    "handlePressStart",
                    "Setting isLongPress to true and triggering onLongPress"
                );
                setIsLongPress(true);
                onLongPress();
                alreadyClicked.current = true; // Impedisce il clickHandler se è stato un long press
            }
        }, 500); // Tempo per il long press
    };

    const handlePressEnd = () => {
        localDebug("handlePressEnd", "Press end detected");
        // Utilizza `requestAnimationFrame` per assicurarti che l'animazione di gonfiamento inizi
        requestAnimationFrame(() => {
            localDebug(
                "handlePressEnd",
                "RequestAnimationFrame callback executed"
            );
            // Cancella il timer di press se è ancora in esecuzione
            if (pressTimer.current) {
                localDebug("handlePressEnd", "Clearing pressTimer");
                clearTimeout(pressTimer.current);
            }

            // Gestione del click singolo solo se non c'è stato un long press
            localDebug(
                "handlePressEnd",
                `Checking if should call clickHandler on condition`,
                {
                    "isPressedRef.current && !isLongPress":
                        isPressedRef.current && !isLongPress,
                    isPressedRef: isPressedRef.current,
                    isLongPress,
                }
            );
            if (isPressedRef.current && !isLongPress) {
                localDebug("handlePressEnd", "Handling single click");
                alreadyClicked.current = true;
                clickHandler();
            }

            // Sgonfia la carta al rilascio del click con un leggero ritardo
            setTimeout(() => {
                localDebug(
                    "handlePressEnd",
                    "Setting isPressed to false and resetting states"
                );
                setIsPressed(false);
                isPressedRef.current = false;
                setIsLongPress(false);
                alreadyClicked.current = false;
            }, 150); // Ritardo per assicurare che l'animazione di gonfiamento sia visibile
        });
    };

    return {
        handlePressStart,
        handlePressEnd,
        isPressed,
    };
};
