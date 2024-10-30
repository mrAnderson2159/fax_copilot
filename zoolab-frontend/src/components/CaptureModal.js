// zoolab-frontend/src/components/CaptureModal.js
import React from "react";
import "./CaptureModal.css";

const CaptureModal = ({ show, onClose, fiend }) => {
    if (!show) {
        return null; // Se `show` è falso, il modal non viene renderizzato
    }

    return (
        <div
            className="modal fade show"
            tabIndex="-1"
            aria-labelledby={`captureModalLabel-${fiend.id}`}
            aria-hidden="true"
            style={{ display: "block" }}
        >
            <div className="modal-dialog modal-dialog-centered">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5
                            className="modal-title"
                            id={`captureModalLabel-${fiend.id}`}
                        >
                            Modal title for fiend {fiend.id}
                        </h5>
                        <button
                            type="button"
                            className="btn-close"
                            onClick={onClose}
                            aria-label="Close"
                        ></button>
                    </div>
                    <div className="modal-body">
                        Content for fiend {fiend.id}
                    </div>
                    <div className="modal-footer">
                        <button
                            type="button"
                            className="btn btn-secondary"
                            onClick={onClose}
                        >
                            Close
                        </button>
                        <button type="button" className="btn btn-primary">
                            Save changes
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CaptureModal;
