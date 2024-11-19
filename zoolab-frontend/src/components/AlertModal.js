// src/components/AlertModal.js
import "./AlertModal.scss";
import React from "react";

const AlertModal = ({ show, onConfirm, onCancel, message, details }) => {
    if (!show) {
        return null; // Non renderizzare il modal se `show` è false
    }

    const handleOverlayClick = (e) => {
        if (e.target.classList.contains("alert-modal-overlay")) {
            onCancel();
        }
    };

    return (
        <>
            <div
                className="alert-modal-overlay"
                onClick={handleOverlayClick}
            ></div>
            <div
                className="alert-modal fade show"
                tabIndex="-1"
                style={{ display: "block" }}
            >
                <div className="alert-modal-dialog alert-modal-dialog-centered">
                    <div className="alert-modal-content">
                        <div className="alert-modal-header">
                            <h5 className="alert-modal-title">
                                Conferma Azione
                            </h5>
                        </div>
                        <div className="alert-modal-body">
                            <p>{message}</p>
                            {details && (
                                <pre className="alert-details">{details}</pre>
                            )}
                        </div>
                        <div className="alert-modal-footer">
                            <button
                                className="btn btn-danger me-2"
                                onClick={onCancel}
                            >
                                Annulla
                            </button>
                            <button
                                className="btn btn-primary"
                                onClick={onConfirm}
                            >
                                Conferma
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default AlertModal;
