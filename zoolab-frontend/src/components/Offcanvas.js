// Offcanvas.js
import React from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Offcanvas.scss";
import { useSound } from "../context/SoundContext";

const Offcanvas = () => {
    const { clickSound, backSound } = useSound();
    const navigate = useNavigate(); // Usa il navigate hook

    const handleLinkClick = (e, href) => {
        e.preventDefault();
        clickSound();

        navigate(href); // Usa navigate invece di window.location.href
    };

    const li_a = (href, body, icon) => {
        return (
            <li className="nav-item" key={icon}>
                <div className="container-fluid">
                    <a
                        href={href}
                        className="nav-link"
                        data-bs-dismiss="offcanvas"
                        aria-label="Close"
                        onClick={(e) => handleLinkClick(e, href)} // Passa href come argomento
                    >
                        <div className="row">
                            <div className="col-1 me-3">
                                <i className={`bi bi-${icon}`}></i>
                            </div>
                            <div className="col">{body}</div>
                        </div>
                    </a>
                </div>
            </li>
        );
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
                    {[
                        li_a("/zones", "Mostri Catturati", "feather"),
                        li_a("/zoolab", "Zoolab", "trophy-fill"),
                    ]}
                </ul>
            </div>
        </div>
    );
};

export default Offcanvas;
