// zoolab-frontend/src/components/GlobalEventHandler.js
import { useEffect } from "react";
import { useClickHandlers } from "../utils/useClickHandlers";
import { debug } from "../utils";

const DEBUG_MODE = false;

const GlobalEventHandler = ({
    clickHandler = () => {},
    onLongPress = () => {},
}) => {
    const { handlePressStart, handlePressEnd } = useClickHandlers({
        clickHandler,
        onLongPress,
    });

    // Funzione locale per il debug
    const localDebug = (functionName, ...stuff) =>
        debug(DEBUG_MODE, "GlobalEventHandler", functionName, ...stuff);

    useEffect(() => {
        // Aggiungi i listener per `touchstart` e `touchend` utilizzando i metodi di `useClickHandlers`
        const handlePressStartDebug = (e) => {
            localDebug("handlePressStartDebug", "Event triggered:", e.type);
            handlePressStart(e);
        };

        const handlePressEndDebug = (e) => {
            localDebug("handlePressEndDebug", "Event triggered:", e.type);
            handlePressEnd(e);
        };

        document.addEventListener("mousedown", handlePressStartDebug, {
            passive: false,
        });
        document.addEventListener("mouseup", handlePressEndDebug, {
            passive: false,
        });
        document.addEventListener("touchstart", handlePressStartDebug, {
            passive: false,
        });
        document.addEventListener("touchend", handlePressEndDebug, {
            passive: false,
        });

        // Aggiungi altri listener per prevenire comportamenti indesiderati
        const handleContextMenu = (e) => {
            localDebug("handleContextMenu", "Event triggered:", e.type);
            e.preventDefault();
        };

        const handleDragStart = (e) => {
            localDebug("handleDragStart", "Event triggered:", e.type);
            e.preventDefault();
        };

        const handleTouchMove = (e) => {
            localDebug("handleTouchMove", "Event triggered:", e.type, {
                touches: e.touches.length,
            });
            if (e.touches.length > 1) {
                e.preventDefault();
            }
        };

        document.addEventListener("contextmenu", handleContextMenu);
        document.addEventListener("dragstart", handleDragStart);
        document.addEventListener("touchmove", handleTouchMove, {
            passive: false,
        });

        // Funzione di pulizia per rimuovere tutti i listener
        return () => {
            document.removeEventListener("mousedown", handlePressStartDebug);
            document.removeEventListener("mouseup", handlePressEndDebug);
            document.removeEventListener("touchstart", handlePressStartDebug);
            document.removeEventListener("touchend", handlePressEndDebug);
            document.removeEventListener("contextmenu", handleContextMenu);
            document.removeEventListener("dragstart", handleDragStart);
            document.removeEventListener("touchmove", handleTouchMove);
        };
    }, [handlePressStart, handlePressEnd]);

    return null; // Questo componente non deve rendere nulla
};

export default GlobalEventHandler;
