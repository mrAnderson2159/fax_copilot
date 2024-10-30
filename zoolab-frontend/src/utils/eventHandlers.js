// zoolab-frontend/src/utils/eventHandlers.js

export const preventDefaultBrowserActions = () => {
    const handleContextMenu = (e) => {
        e.preventDefault(); // Impedisce l'apertura del menu contestuale
    };

    const handleDragStart = (e) => {
        e.preventDefault(); // Impedisce il trascinamento dell'immagine
    };

    // Aggiungi i listener al documento globale
    document.addEventListener("contextmenu", handleContextMenu);
    document.addEventListener("dragstart", handleDragStart);

    // Ritorna una funzione per rimuovere i listener quando necessario
    return () => {
        document.removeEventListener("contextmenu", handleContextMenu);
        document.removeEventListener("dragstart", handleDragStart);
    };
};
