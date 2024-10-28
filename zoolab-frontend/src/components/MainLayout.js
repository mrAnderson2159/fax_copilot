// src/components/MainLayout.js
import React from "react";
import { useLocation } from "react-router-dom";
import Header from "./Header";
import "./MainLayout.css";
import "./Offcanvas";
import "bootstrap/dist/css/bootstrap.min.css";
import Offcanvas from "./Offcanvas";

const MainLayout = ({ children, headerTitle }) => {
    const location = useLocation();

    // Verifica se il percorso inizia con "/zones/"
    const shouldShowBackground = location.pathname.startsWith("/zones");

    return (
        <div className="main-layout">
            <Header headerTitle={headerTitle} />
            <Offcanvas />
            {/* Background image e overlay mostrati solo se siamo in una pagina /zones/* */}
            {shouldShowBackground && (
                <>
                    <div className="zoolab-image"></div>
                    <div className="overlay"></div>
                </>
            )}
            <div className="overflow-trap"></div>
            <main className="mt-5 pt-1">{children}</main>
        </div>
    );
};

export default MainLayout;
