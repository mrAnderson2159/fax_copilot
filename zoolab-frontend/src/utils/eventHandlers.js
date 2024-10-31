// zoolab-frontend/src/utils/eventHandlers.js

export const preventDefaultBrowserActions = () => {
    const handleContextMenu = (e) => {
        e.preventDefault(); // Impedisce l'apertura del menu contestuale
    };

    const handleDragStart = (e) => {
        e.preventDefault(); // Impedisce il trascinamento dell'immagine
    };

    const handleTouchMove = (e) => {
        if (e.touches.length > 1) {
            e.preventDefault(); // Impedisce il pinch-to-zoom e altri comportamenti simili su dispositivi touch
        }
    };

    const handleGestureStart = (e) => {
        e.preventDefault(); // Impedisce il comportamento di zoom con le gesture (particolarmente per Safari)
    };

    // Aggiungi i listener al documento globale
    document.addEventListener("contextmenu", handleContextMenu);
    document.addEventListener("dragstart", handleDragStart);
    document.addEventListener("touchmove", handleTouchMove, { passive: false });
    document.addEventListener("gesturestart", handleGestureStart);

    // Ritorna una funzione per rimuovere i listener quando necessario
    return () => {
        document.removeEventListener("contextmenu", handleContextMenu);
        document.removeEventListener("dragstart", handleDragStart);
        document.removeEventListener("touchmove", handleTouchMove);
        document.removeEventListener("gesturestart", handleGestureStart);
    };
};
