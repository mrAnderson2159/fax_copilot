import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Offcanvas.css'

const Offcanvas = () => {
    return (
        <div
                className="offcanvas offcanvas-start"
                tabIndex="-1"
                id="offcanvasNavbar"
                aria-labelledby="offcanvasNavbarLabel"
            >
                <div className="offcanvas-header">
                    <h5 className="offcanvas-title" id="offcanvasNavbarLabel">Menu</h5>
                    <button
                        type="button"
                        className="btn-close text-reset"
                        data-bs-dismiss="offcanvas"
                        aria-label="Close"
                    ></button>
                </div>
                <div className="offcanvas-body">
                    <ul className="navbar-nav">
                        <li className="nav-item">
                            <a className="nav-link" href="/zones">Cattura Mostri</a>
                        </li>
                        {/* Aggiungi altri link qui */}
                    </ul>
                </div>
            </div>
    )
}

export default Offcanvas;