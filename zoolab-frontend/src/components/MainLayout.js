// src/components/MainLayout.js
import React from "react";
import { useLocation } from "react-router-dom";
import Header from "./Header";
import "./MainLayout.scss";
import "./Offcanvas";
import "bootstrap/dist/css/bootstrap.min.css";
import Offcanvas from "./Offcanvas";

const MainLayout = ({ children, headerTitle }) => {
    const location = useLocation();

    // Mappa delle classi di background ai pattern di espressioni regolari
    const backgroundMapping = {
        "zoolab-bg": [/^\/zones$/],
        "fiends-bg": [/^\/zones\/\d+\/fiends\/$/],
        "homepage-bg": [/^\/$/],
        // Aggiungi altre associazioni di pattern qui
    };

    // Trova la classe di background in base al percorso corrente utilizzando le espressioni regolari
    const backgroundClass = Object.keys(backgroundMapping).find((bgClass) =>
        backgroundMapping[bgClass].some((pattern) =>
            pattern.test(location.pathname)
        )
    );

    return (
        <div className="main-layout">
            <Header headerTitle={headerTitle} />
            <Offcanvas />
            {/* Background image e overlay mostrati se viene trovata una classe di background per il percorso corrente */}
            {backgroundClass && (
                <>
                    <div className="background-wrapper">
                        <div className={backgroundClass}></div>
                    </div>

                    <div className="overlay"></div>
                </>
            )}
            <div className="overflow-trap"></div>
            <main className="mt-5 pt-1">{children}</main>
        </div>
    );
};

export default MainLayout;
