import React from "react";
import "./CreationAlertModal.css";
import Card from "./Card";

const CreationAlertModal = ({ show, onClose, creation }) => {
    if (!show || !creation) {
        return null; // Non renderizzare se `show` è false o `creation` non è presente
    }

    const { name, created, type, image_url } = creation;

    const handleOverlayClick = (e) => {
        if (e.target.classList.contains("creation-alert-modal-overlay")) {
            onClose();
        }
    };

    return (
        <>
            <div
                className="creation-alert-modal-overlay"
                onClick={handleOverlayClick}
            ></div>
            <div
                className="creation-alert-modal fade show"
                tabIndex="-1"
                style={{ display: "block" }}
            >
                <div className="creation-alert-modal-dialog creation-alert-modal-dialog-centered">
                    <div className="creation-alert-modal-content">
                        <div className="creation-alert-modal-header">
                            <h5 className="creation-alert-modal-title">
                                {created ? "Congratulazioni" : "Correzione"}
                            </h5>
                            <button
                                type="button"
                                className="btn-close"
                                onClick={onClose}
                                aria-label="Close"
                            ></button>
                        </div>
                        <div className="creation-alert-modal-body">
                            <p>
                                {created
                                    ? `È stato creato il ${type}`
                                    : `È stato rimosso il ${type}`}
                            </p>
                            <Card name={name} imageUrl={image_url} />
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default CreationAlertModal;
