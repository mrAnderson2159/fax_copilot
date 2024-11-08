// zoolab-frontend/src/components/CaptureModal.js
import React, { useEffect, useState } from "react";
import "./CaptureModal.css";
import Card from "./Card";
import { MAX_CAPTURES } from "../utils";
import { signed, debug } from "../utils";

const DEBUG_MODE = true;

const CaptureModal = ({ show, onClose, fiend, deltas, setDeltas, badge }) => {
    const [activeButton, setActiveButton] = useState(null);
    const localDebug = (functionName, ...stuff) =>
        debug(DEBUG_MODE, "CaptureModal.js", functionName, ...stuff);

    useEffect(() => {
        if (show) {
            document.body.classList.add("modal-open");
        } else {
            document.body.classList.remove("modal-open");
            setActiveButton(null); // Resetta il bottone attivo quando il modal viene chiuso
        }

        // Cleanup function to ensure class is removed when the component unmounts
        return () => {
            document.body.classList.remove("modal-open");
        };
    }, [show]);

    useEffect(() => {
        if (fiend && activeButton !== (deltas[fiend.id] ?? null)) {
            setActiveButton(deltas[fiend.id] ?? null);
        }
    }, [fiend, deltas, activeButton]);

    if (!show) {
        return null; // Se `show` è falso, il modal non viene renderizzato
    }

    const handleButtonClick = (value) => {
        setActiveButton(value);
        // Eventualmente, aggiorna anche il delta delle catture se necessario
        setDeltas((prevDeltas) => ({
            ...prevDeltas,
            [fiend.id]: value,
        }));
    };

    const handleOverlayClick = (e) => {
        localDebug("handleOverlayClick", "triggered handleOverlayClick", e);
        if (e.target.classList.contains("modal-overlay")) {
            localDebug("handleOverlayClick", "About to use onClose");
            onClose();
        }
    };

    const computeButtons = () => {
        const buttons = [];

        const start = -fiend.was_captured;
        const end = MAX_CAPTURES - fiend.was_captured + 1;

        const btnColor = (n) =>
            n === 0 ? "success" : n > 0 ? "primary" : "danger";

        let counter = 0;

        for (let i = start; i < end; i++) {
            buttons.push(
                <div
                    className={`col-${
                        counter > 3 && counter < 7 ? "4" : "3"
                    } d-flex justify-content-center`}
                    key={i}
                >
                    <button
                        type="button"
                        className={`btn btn-${btnColor(i)} btn-select ${
                            activeButton === i ? "active" : ""
                        }`}
                        onClick={() => handleButtonClick(i)}
                        disabled={i === activeButton}
                    >
                        {signed(i)}
                    </button>
                </div>
            );
            counter++;
        }

        // Ripartisci i bottoni nelle righe
        const buttonRows = [];
        const rowSizes = [4, 3, 4]; // Distribuzione dei bottoni

        let currentIndex = 0;
        rowSizes.forEach((size, rowIndex) => {
            const rowButtons = buttons.slice(currentIndex, currentIndex + size);
            buttonRows.push(
                <div className="row mb-2" key={`row-${rowIndex}`}>
                    {rowButtons}
                </div>
            );
            currentIndex += size;
        });

        return buttonRows;
    };

    return (
        <>
            <div className="modal-overlay" onClick={handleOverlayClick}></div>
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
                                Cattura di precisione
                            </h5>
                            <button
                                type="button"
                                className="btn-close"
                                onClick={onClose}
                                aria-label="Close"
                            ></button>
                        </div>
                        <div className="modal-body container-fluid text-center">
                            <div className="row">
                                <div className="col">
                                    <Card
                                        name={fiend.name}
                                        imageUrl={fiend.image_url}
                                        className={"unclickable"}
                                    >
                                        {badge(fiend, { deltas })}
                                    </Card>
                                </div>
                                <div className="col">{computeButtons()}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default CaptureModal;
