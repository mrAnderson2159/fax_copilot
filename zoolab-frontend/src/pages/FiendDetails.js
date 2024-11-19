import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "../api/axios";
import { boolToItalian, titleCase } from "../utils";
import Card from "../components/Card";
import { useSound } from "../context/SoundContext";
import ContentLoader from "../components/ContentLoader";
import { phCard, phTitle } from "../utils/placeholders";
import "../styles/CommonStyles.scss";
import "./FiendDetails.scss";

const FiendDetails = () => {
    const { category, title, fiendId } = useParams();
    const [fiend, setFiend] = useState({});
    const [defeatButton, setDefeatButton] = useState(false);
    const [dataLoading, setDataLoading] = useState(true);
    const [imageLoading, setImageLoading] = useState(true);
    const [buttonLoading, setButtonLoading] = useState(false);
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
                setDataLoading(false);
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

    const renderSpecificDetails = (fiend, placeholderMode = false) => {
        switch (category + (placeholderMode ? "_placeholder" : "")) {
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
            case "area_conquests_placeholder":
                return (
                    <div>
                        <p>
                            <span className="placeholder col-6"></span>
                        </p>
                        <p>
                            <span className="placeholder col-12"></span>
                            <span className="placeholder col-12"></span>
                            <span className="placeholder col-6"></span>
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
            case "species_conquests_placeholder":
                return (
                    <div>
                        <p>
                            <span className="placeholder col-12"></span>
                            <span className="placeholder col-12"></span>
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
            setButtonLoading(false);
            lowConfirmSound();
        } catch (error) {
            console.error(
                "Errore nel segnare il mostro come sconfitto:",
                error
            );
        }
    };

    const renderDefeatButton = (
        created,
        { placeholderMode = false, loadingMode = false }
    ) => {
        if (placeholderMode)
            return (
                <button className="defeat-btn btn btn-secondary w-50" disabled>
                    <span className="placeholder"></span>
                </button>
            );

        const classNames = `defeat-btn btn btn-${
            defeatButton ? "danger" : "primary"
        } bold`;

        if (loadingMode)
            return (
                <button className={classNames} disabled>
                    <span className="spinner-border spinner-border-sm"></span>
                </button>
            );

        if (created)
            return (
                <button
                    className={classNames}
                    onClick={() => {
                        setButtonLoading(true);
                        defeatButtonHandler();
                    }}
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
                <ContentLoader isLoading={false || dataLoading || imageLoading}>
                    <ContentLoader.Placeholder>
                        {phTitle("mb-5")}
                        <div className="row placeholder-glow">
                            <div className="col-6">
                                {phCard({ showName: false })}
                            </div>
                            <div className="col-6 main_info">
                                <p>
                                    <span className="placeholder col-5"></span>
                                    <span className="placeholder col-7 d-block"></span>
                                </p>
                                <p>
                                    <span className="placeholder col-6"></span>
                                </p>
                                <p>
                                    <span className="placeholder col-4"></span>
                                </p>
                                <p>
                                    <span className="placeholder col-5"></span>
                                </p>
                            </div>
                            <div className="col-6 main_info">
                                <p>
                                    <span className="placeholder col-8"></span>
                                    <span className="d-block placeholder col-4"></span>
                                </p>
                            </div>
                            <div className="col-6 main_info">
                                <p>
                                    <span className="placeholder col-6"></span>
                                    <span className="d-block placeholder col-4"></span>
                                </p>
                            </div>
                        </div>
                        <div className="secondary-info mt-4 placeholder-glow">
                            {renderSpecificDetails(null, true)}
                            <p className="mt-5">
                                <span className="placeholder col-3"></span>
                            </p>
                            <p>
                                <span className="placeholder col-4"></span>
                            </p>
                        </div>
                        <div className="table-info">
                            <table className="table table-dark table-striped placeholder-glow">
                                <thead>
                                    <tr>
                                        <th>
                                            <span className="placeholder"></span>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>
                                            <span className="placeholder"></span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <th>
                                            <span className="placeholder"></span>
                                        </th>
                                    </tr>
                                    <tr>
                                        <td>
                                            <span className="placeholder"></span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div className="btn-container">
                            {renderDefeatButton(null, {
                                placeholderMode: true,
                            })}
                        </div>
                    </ContentLoader.Placeholder>
                    <ContentLoader.Render>
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
                                    imageLoadingFunction={setImageLoading}
                                />
                            </div>
                            <div className="col-6 main_info">
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
                            <div className="col-6 main_info">
                                <p>
                                    <strong>Danni per Ultracidio:</strong>{" "}
                                    <span className="d-block">
                                        {fiend.overkill}
                                    </span>
                                </p>
                            </div>
                            <div className="col-6 main_info">
                                <p>
                                    <strong>AP Ultracidio:</strong>{" "}
                                    <span className="d-block">
                                        {fiend.ap_overkill}
                                    </span>
                                </p>
                            </div>
                        </div>
                        <div className="secondary-info mt-4">
                            {renderSpecificDetails(fiend)}
                            <p>
                                <strong>Creato:</strong>{" "}
                                {boolToItalian(fiend.created)}
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
                                                {renderReward(
                                                    fiend.creation_reward
                                                )}
                                            </td>
                                            <td>
                                                {renderReward(
                                                    fiend.battle_reward
                                                )}
                                            </td>
                                        </tr>
                                        <tr>
                                            <th>Ruba comune</th>
                                            <th>Ruba raro</th>
                                        </tr>
                                        <tr>
                                            <td>
                                                {renderReward(
                                                    fiend.common_steal
                                                )}
                                            </td>
                                            <td>
                                                {renderReward(fiend.rare_steal)}
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div className="btn-container">
                            <ContentLoader isLoading={false || buttonLoading}>
                                <ContentLoader.Placeholder>
                                    {renderDefeatButton(fiend.created, {
                                        loadingMode: true,
                                    })}
                                </ContentLoader.Placeholder>
                                <ContentLoader.Render>
                                    {renderDefeatButton(fiend.created, {})}
                                </ContentLoader.Render>
                            </ContentLoader>
                        </div>
                    </ContentLoader.Render>
                </ContentLoader>
            </div>
        </div>
    );
};

export default FiendDetails;
