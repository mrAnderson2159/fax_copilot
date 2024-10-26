// src/components/MainLayout.js
import React from 'react';
import Header from './Header';
import './MainLayout.css';
import './Offcanvas'
import 'bootstrap/dist/css/bootstrap.min.css';
import Offcanvas from './Offcanvas';

const MainLayout = ({ children, headerTitle }) => {
    return (
        <div className="main-layout">
            <Header headerTitle={headerTitle} />
            <Offcanvas />
            <div className="overflow-trap"></div>
            <main className="mt-5 pt-1">
                {children}
            </main>
        </div>
    );
};

export default MainLayout;
