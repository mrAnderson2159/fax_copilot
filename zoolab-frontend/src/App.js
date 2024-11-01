// src/App.js
import React from "react";
import { BrowserRouter as Router } from "react-router-dom";
import { NavigationStackProvider } from "./context/NavigationStackContext";
import AppContent from "./AppContent";
import GlobalEventHandler from "./components/GlobalEventHandler";

const App = () => {
    return (
        <Router>
            <NavigationStackProvider>
                <GlobalEventHandler
                // clickHandler={() => console.log("Click singolo rilevato")}
                // onLongPress={() => console.log("Tocco prolungato rilevato")}
                />
                <AppContent />
            </NavigationStackProvider>
        </Router>
    );
};

export default App;
