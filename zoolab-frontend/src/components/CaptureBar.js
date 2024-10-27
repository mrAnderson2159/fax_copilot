// src/components/CaptureBar.js

import React from "react";
import "./CaptureBar.css";

const CaptureBar = ({ fiends }) => {
    return (
        <div>
            {fiends.map(({ name, was_captured, id }) => {
                // console.log(
                //     `Rendering: ${name}, Catture: ${was_captured}, ID: ${id}`
                // );

                const width = was_captured * 10; // Calcola la larghezza in percentuale

                return (
                    <div key={id} className="capture-bar-item">
                        <p className="capture-bar-name">{name}</p>
                        <div
                            className="progress"
                            role="progressbar"
                            aria-label="Progress"
                            aria-valuenow={width}
                            aria-valuemin="0"
                            aria-valuemax="100"
                        >
                            <div
                                className="progress-bar"
                                style={{ width: `${width}%` }}
                                data-value={width}
                            >
                                {was_captured}
                            </div>
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

export default CaptureBar;
