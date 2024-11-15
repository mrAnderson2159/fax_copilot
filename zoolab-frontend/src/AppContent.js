// zoolab-frontend/src/AppContent.js
import React, { useEffect } from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import { useNavigationStack } from "./context/NavigationStackContext";
import MainLayout from "./components/MainLayout";
import Home from "./pages/Home";
import ZoneList from "./pages/ZoneList";
import FiendList from "./pages/FiendList";
import Zoolab from "./pages/Zoolab";
import ZoolabCategory from "./pages/ZoolabCategory";
import FiendDetails from "./pages/FiendDetails";

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
            <Route path="/" element={layout("", <Home />)} />
            <Route
                path="/zones"
                element={layout("Mostri Catturati", <ZoneList />)}
            />
            <Route
                path="/zones/:zoneId/:zoneName"
                element={layout("Mostri Catturati", <FiendList />)}
            />
            <Route path="/zoolab" element={layout("Zoolab", <Zoolab />)} />
            <Route
                path="/zoolab/:category/:title"
                element={layout("Zoolab", <ZoolabCategory />)}
            />
            <Route
                path="/zoolab/:category/:title/:fiendId"
                element={layout("Zoolab", <FiendDetails />)}
            />
        </Routes>
    );
};

export default AppContent;
