import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "../api/axios";
import { boolToItalian, titleCase } from "../utils";
import Card from "../components/Card";
import { useSound } from "../context/SoundContext";
import "../styles/CommonStyles.scss";
import "./FiendDetails.scss";

const FiendDetails = () => {
    const { category, title, fiendId } = useParams();
    const [fiend, setFiend] = useState({});
    const [defeatButton, setDefeatButton] = useState(false);
    const { lowConfirmSound } = useSound();

    useEffect(() => {
        const fetchFiend = async () => {
            try {
                const fiendResponse = await axios.get(
                    `/${category}/${fiendId}/full_details`
                );
                // console.log("Fiend details:", fiendResponse.data);

                const data = Object.fromEntries(
                    Object.entries(fiendResponse.data).map(([key, value]) => {
                        if (Number.isInteger(value))
                            return [key, value.toLocaleString("it-IT")];
                        return [key, value];
                    })
                );

                setFiend(data);
                setDefeatButton(data.defeated);
            } catch (error) {
                console.error("Errore nel recupero del mostro:", error);
            }
        };

        fetchFiend();
    }, [defeatButton]);

    const renderRequiredFiends = (fiend) => {
        return (fiend.required_fiends || [])
            .map(([id, name]) => titleCase(name))
            .join(", ");
    };

    const renderReward = (reward) => {
        if (!reward) return "-";
        const [item, quantity] = reward;
        return `${titleCase(item)} x ${quantity}`;
    };

    const renderSpecificDetails = (fiend) => {
        switch (category) {
            case "area_conquests":
                return (
                    <div>
                        <p>
                            <strong>Zona:</strong>{" "}
                            {titleCase(fiend.zone_name || "")}
                        </p>
                        <p>
                            <strong>Condizioni di creazione: </strong>
                            Cattura almeno un esemplare di{" "}
                            {renderRequiredFiends(fiend)}
                        </p>
                    </div>
                );
            case "species_conquests":
                return (
                    <div>
                        <p>
                            <strong>Condizioni di creazione:</strong> Cattura
                            almeno {fiend.required_fiends_amount} esemplari di{" "}
                            {renderRequiredFiends(fiend)}
                        </p>
                    </div>
                );
            case "original_creations":
                return (
                    <div>
                        <p>
                            <strong>Condizioni di creazione:</strong>{" "}
                            {fiend.creation_rule}
                        </p>
                    </div>
                );
            default:
                return null;
        }
    };

    const defeatButtonHandler = async () => {
        try {
            if (defeatButton) {
                await axios.post(`/${category}/${fiendId}/undefeated`);
                setDefeatButton(false);
            } else {
                await axios.post(`/${category}/${fiendId}/defeated`);
                setDefeatButton(true);
            }
            lowConfirmSound();
        } catch (error) {
            console.error(
                "Errore nel segnare il mostro come sconfitto:",
                error
            );
        }
    };

    const renderDefeatButton = (created) => {
        if (created)
            return (
                <button
                    className={`defeat-btn btn btn-${
                        defeatButton ? "danger" : "primary"
                    } bold`}
                    onClick={defeatButtonHandler}
                >
                    {defeatButton
                        ? "Segna come non sconfitto"
                        : "Segna come sconfitto"}
                </button>
            );
        return (
            <button className="defeat-btn btn btn-secondary" disabled>
                Segna come sconfitto
            </button>
        );
    };

    return (
        <div className="transparent-background">
            <div className="fiend-details container-fluid pt-5">
                <h2 className="display-4 list-title">
                    {titleCase(fiend.name || "")}
                </h2>
                <div className="row">
                    <div className="col-6">
                        <Card
                            name={fiend.name}
                            imageUrl={fiend.image_url}
                            type="creation"
                            showName={false}
                            className="unclickable"
                        />
                    </div>
                    <div className="col-6">
                        <div className="main_info">
                            <p>
                                <strong>Categoria:</strong>
                                <span className="d-block">
                                    {titleCase(title)}
                                </span>
                            </p>
                            <p>
                                <strong>HP:</strong> {fiend.hp}
                            </p>
                            <p>
                                <strong>MP:</strong> {fiend.mp}
                            </p>
                            <p>
                                <strong>AP:</strong> {fiend.ap}
                            </p>
                        </div>
                    </div>
                    <div className="col-6">
                        <div className="main_info">
                            <p>
                                <strong>Danni per Ultracidio:</strong>{" "}
                                <span className="d-block">
                                    {fiend.overkill}
                                </span>
                            </p>
                        </div>
                    </div>
                    <div className="col-6">
                        <div className="main_info">
                            <p>
                                <strong>AP Ultracidio:</strong>{" "}
                                <span className="d-block">
                                    {fiend.ap_overkill}
                                </span>
                            </p>
                        </div>
                    </div>
                </div>
                <div className="secondary-info mt-4">
                    {renderSpecificDetails(fiend)}
                    <p>
                        <strong>Creato:</strong> {boolToItalian(fiend.created)}
                    </p>
                    <p>
                        <strong>Sconfitto:</strong>{" "}
                        {boolToItalian(fiend.defeated)}
                    </p>
                    <div className="table-info">
                        <table className="table table-dark table-striped">
                            <thead>
                                <tr>
                                    <th>Creazione</th>
                                    <th>Battaglia</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>
                                        {renderReward(fiend.creation_reward)}
                                    </td>
                                    <td>{renderReward(fiend.battle_reward)}</td>
                                </tr>
                                <tr>
                                    <th>Ruba comune</th>
                                    <th>Ruba raro</th>
                                </tr>
                                <tr>
                                    <td>{renderReward(fiend.common_steal)}</td>
                                    <td>{renderReward(fiend.rare_steal)}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div className="btn-container ">
                    {renderDefeatButton(fiend.created)}
                </div>
            </div>
        </div>
    );
};

export default FiendDetails;
