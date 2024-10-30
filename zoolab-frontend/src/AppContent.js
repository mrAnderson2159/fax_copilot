// zoolab-frontend/src/AppContent.js
import React, { useEffect } from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import MainLayout from "./components/MainLayout";
import Home from "./pages/Home";
import ZoneList from "./pages/ZoneList";
import FiendList from "./pages/FiendList";
import { useNavigationStack } from "./context/NavigationStackContext";

const AppContent = () => {
    const location = useLocation();
    const { pushToStack } = useNavigationStack();

    useEffect(() => {
        pushToStack(location.pathname);
    }, [location.pathname, pushToStack]);

    const layout = (headerTitle, content) => (
        <MainLayout headerTitle={headerTitle}>{content}</MainLayout>
    );

    return (
        <Routes>
            <Route
                path="/zones"
                element={layout("Cattura Mostri", <ZoneList />)}
            />
            <Route
                path="/zones/:zoneId/fiends"
                element={layout("Cattura Mostri", <FiendList />)}
            />
            <Route path="/" element={layout("", <Home />)} />
            {/* Aggiungi altre rotte usando la funzione `layout` */}
        </Routes>
    );
};

export default AppContent;
