// src/App.js
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { NavigationStackProvider } from './context/NavigationStackContext';
import AppContent from './AppContent';

const App = () => {
    return (
        <Router>
            <NavigationStackProvider>
                <AppContent />
            </NavigationStackProvider>
        </Router>
    );
};

export default App;
