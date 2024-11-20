// zoolab-frontend/src/components/CreationAlertModal.js
import React, { useEffect, useState } from "react";
import Card from "./Card";
import { titleCase } from "../utils";
import { useNavigate } from "react-router-dom";
import { useSound } from "../context/SoundContext";
import "./CreationAlertModal.scss";

const CreationAlertModal = ({ show, onClose, creation }) => {
    const navigate = useNavigate();
    const { clickSound } = useSound();

    useEffect(() => {
        console.log(show);
        console.log(creation);
    }, [show, creation]);

    if (!show || !creation) {
        return null; // Non renderizzare se `show` è false o `creation` non è presente
    }

    const {
        id,
        name,
        created,
        type,
        image_url,
        reward,
        destination,
        destinationName,
    } = creation;

    let rewardItem, rewardQuantity;

    if (reward) {
        [rewardItem, rewardQuantity] = reward;
    }

    const handleOverlayClick = (e) => {
        if (e.target.classList.contains("creation-alert-modal-overlay")) {
            onClose();
        }
    };

    const handleCreationClick = () => {
        clickSound();
        navigate(`/zoolab/${destination}/${destinationName}/${id}`);
        onClose();
    };

    return (
        <>
            <div
                className="creation-alert-modal-overlay"
                onClick={handleOverlayClick}
            ></div>
            <div
                className="creation-alert-modal fade show mt-4"
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
                            <Card
                                name={name}
                                imageUrl={image_url}
                                clickHandler={handleCreationClick}
                            />
                            {reward && (
                                <div className="reward-container">
                                    <h3 className="section-title mt-3">
                                        Ricompensa
                                    </h3>
                                    <div className="divider"></div>
                                    <p className="no-mt">
                                        {rewardQuantity > 1
                                            ? rewardQuantity
                                            : ""}{" "}
                                        {titleCase(rewardItem)}
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default CreationAlertModal;
