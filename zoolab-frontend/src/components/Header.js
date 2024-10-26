// src/components/Header.js
import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useNavigationStack } from '../context/NavigationStackContext';

const Header = ({ headerTitle }) => {
    const { goBack, navigationStack } = useNavigationStack();

    // Determina se la freccia indietro dovrebbe essere visibile
    const isChildPath = navigationStack.length > 1;

    return (
        <header className="navbar navbar-dark bg-dark fixed-top">
            <div className="container-fluid d-flex align-items-center justify-content-between">
                <div className="d-flex align-items-center">
                    <button
                        className="navbar-toggler"
                        type="button"
                        data-bs-toggle="offcanvas"
                        data-bs-target="#offcanvasNavbar"
                        aria-controls="offcanvasNavbar"
                    >
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    {isChildPath && (
                        <button className="btn btn-link text-light me-2 ms-3" onClick={goBack}>
                            <i className="bi bi-arrow-left"></i>
                        </button>
                    )}
                </div>
                <div className="d-flex align-items-center ms-auto">
                    <span className="navbar-text me-3">{headerTitle}</span>
                    <span className="navbar-brand">FFX Copilot</span>
                </div>
            </div>
        </header>
    );
};

export default Header;
