// zoolab-frontend/src/components/ContentLoader.js
import React from "react";
import "./ContentLoader.scss";

const ContentLoader = ({ isLoading, children, showRender = false }) => {
    let placeholderContent = null;
    let renderContent = null;

    // Dividi i figli in placeholder e render in base ai loro tipi
    React.Children.forEach(children, (child) => {
        if (child.type === Placeholder) {
            placeholderContent = child;
        } else if (child.type === Render) {
            renderContent = child;
        }
    });

    // Applica le classi di visibilità in base allo stato di caricamento
    return (
        <>
            <div style={{ display: isLoading ? "block" : "none" }}>
                {placeholderContent}
            </div>
            {showRender && isLoading && <div className="loading-overlay"></div>}
            <div
                style={{
                    visibility: !showRender && isLoading ? "hidden" : "visible",
                    height: !showRender && isLoading ? 0 : "auto",
                }}
            >
                {renderContent}
            </div>
        </>
    );
};

const Placeholder = ({ children }) => <>{children}</>;
const Render = ({ children }) => <>{children}</>;

// Esporta ContentLoader insieme a Placeholder e Render per un uso agevole
ContentLoader.Placeholder = Placeholder;
ContentLoader.Render = Render;

export default ContentLoader;
