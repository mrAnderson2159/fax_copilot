import React from "react";
import "./LoadingOverlay.css"; // Aggiungi uno stile per l'overlay

const LoadingOverlay = ({ isLoading }) => {
    if (!isLoading) return null;

    return (
        <div className="loading-overlay">
            <div className="spinner"></div>
        </div>
    );
};

export default LoadingOverlay;
