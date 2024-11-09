import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Offcanvas.scss";
import { useSound } from "../context/SoundContext";

const Offcanvas = () => {
    const { clickSound, backSound } = useSound();

    const handleLinkClick = (e) => {
        e.preventDefault();
        clickSound();
        setTimeout(() => {
            window.location.href = e.target.href;
        }, 200);
    };

    return (
        <div
            className="offcanvas offcanvas-start"
            tabIndex="-1"
            id="offcanvasNavbar"
            aria-labelledby="offcanvasNavbarLabel"
        >
            <div className="offcanvas-header">
                <h5 className="offcanvas-title" id="offcanvasNavbarLabel">
                    Menu
                </h5>
                <button
                    type="button"
                    className="btn-close text-reset"
                    data-bs-dismiss="offcanvas"
                    aria-label="Close"
                    onClick={backSound}
                ></button>
            </div>
            <div className="offcanvas-body">
                <ul className="navbar-nav">
                    <li className="nav-item">
                        <a
                            className="nav-link"
                            href="/zones"
                            onClick={handleLinkClick}
                        >
                            Mostri Catturati
                        </a>
                    </li>
                    {/* Aggiungi altri link qui */}
                </ul>
            </div>
        </div>
    );
};

export default Offcanvas;
