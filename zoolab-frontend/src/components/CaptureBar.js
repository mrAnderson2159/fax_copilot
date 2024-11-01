import React from "react";
import "./CaptureBar.css";
import { MAX_CAPTURES } from "../utils";

const CaptureBar = ({ fiends }) => {
    return (
        <div>
            {fiends.map(({ name, was_captured, id }) => {
                // Calcola la larghezza in percentuale rispetto al massimo numero di catture
                const width = (was_captured / MAX_CAPTURES) * 100;

                // Usa una classe speciale se il numero di catture è al massimo
                const progressBarClass =
                    was_captured === MAX_CAPTURES
                        ? "progress-bar full-capture"
                        : "progress-bar";

                return (
                    <div key={id} className="capture-bar-item">
                        <p className="capture-bar-name">{name}</p>
                        <div className="progress-container">
                            <div
                                className="progress"
                                role="progressbar"
                                aria-label="Progress"
                                aria-valuenow={width}
                                aria-valuemin="0"
                                aria-valuemax="100"
                            >
                                <div
                                    className={progressBarClass}
                                    style={{ width: `${width}%` }}
                                    data-value={width}
                                ></div>
                            </div>
                            <span className="capture-count">
                                {was_captured}
                            </span>
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

export default CaptureBar;
