import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "../api/axios";
import { titleCase, MAX_CAPTURES } from "../utils";
import "../styles/CommonStyles.css";
import "./FiendList.css";
import renderCards from "../utils/renderCards";
import CaptureBar from "../components/CaptureBar";
import Badge from "../components/Badge";
import CaptureModal from "../components/CaptureModal";
import AlertModal from "../components/AlertModal";

const FiendList = () => {
    const { zoneId } = useParams();
    const [fiends, setFiends] = useState([]);
    const [otherFiends, setOtherFiends] = useState([]);
    const [zone, setZone] = useState({});
    const [deltas, setDeltas] = useState({});
    const [selectedFiend, setSelectedFiend] = useState(null);
    const [alert, setAlert] = useState({ show: false, action: null });

    useEffect(() => {
        const fetchFiendsWithFound = async () => {
            try {
                const fiendResponse = await axios.get(
                    `/zones/${zoneId}/fiends_with_found`
                );
                const nativeFiends = fiendResponse.data.native || [];
                const otherFiendsData = fiendResponse.data.others || [];

                setFiends(nativeFiends);
                setOtherFiends(otherFiendsData);

                const initialDeltas = nativeFiends.reduce((acc, fiend) => {
                    acc[fiend.id] = 0;
                    return acc;
                }, {});

                setDeltas(initialDeltas);
            } catch (error) {
                console.error("Errore nel recupero dei mostri:", error);
            }
        };

        const fetchZone = async () => {
            try {
                const zoneResponse = await axios.get(`/zones/${zoneId}`);
                setZone(zoneResponse.data);
            } catch (error) {
                console.error("Errore nel recupero della zona:", error);
            }
        };

        fetchFiendsWithFound();
        fetchZone();
    }, [zoneId]);

    const funzioneCattura1 = (fiend) => {
        setDeltas((prevDeltas) => {
            const newDelta = Math.min(
                (prevDeltas[fiend.id] || 0) + 1,
                MAX_CAPTURES - fiend.was_captured
            );
            return {
                ...prevDeltas,
                [fiend.id]: newDelta,
            };
        });
    };

    const funzioneCattura2 = (fiend) => {
        setSelectedFiend(fiend);
    };

    const badge = (fiend, { deltas }) => {
        return <Badge delta={deltas[fiend.id]} />;
    };

    const handleCloseModal = () => {
        setSelectedFiend(null);
    };

    const confirmSaveChanges = () => {
        setAlert({ show: true, action: "save" });
    };

    const confirmResetChanges = () => {
        setAlert({ show: true, action: "reset" });
    };

    const saveChanges = async () => {
        try {
            await axios.post("/update_captures", {
                updates: Object.entries(deltas)
                    .filter(([_, delta]) => delta !== 0)
                    .map(([fiend_id, delta]) => ({ fiend_id, delta })),
            });
            setDeltas((prev) =>
                Object.fromEntries(
                    Object.entries(prev).map(([key]) => [key, 0])
                )
            );
        } catch (error) {
            console.error("Errore nell'aggiornamento delle catture:", error);
        }
        setAlert({ show: false, action: null });
    };

    const resetChanges = () => {
        setDeltas((prev) =>
            Object.fromEntries(Object.entries(prev).map(([key]) => [key, 0]))
        );
        setAlert({ show: false, action: null });
    };

    const handleAlertConfirm = () => {
        if (alert.action === "save") {
            saveChanges();
        } else if (alert.action === "reset") {
            resetChanges();
        }
    };

    const handleAlertCancel = () => {
        setAlert({ show: false, action: null });
    };

    const renderCardsKeywords = {
        clickHandler: funzioneCattura1,
        onLongPress: funzioneCattura2,
        children: badge,
        props: {
            deltas,
        },
    };

    return (
        <div className="transparent-background">
            <div className="fiend-list-content container-fluid pt-5">
                <h2 className="display-4">{titleCase(zone.name || "")}</h2>
                <div className="fiend-cards fiend-cards-native">
                    {renderCards(fiends, "fiend", renderCardsKeywords)}
                </div>

                {otherFiends.length > 0 && (
                    <>
                        <h3 className="section-title">Extra</h3>
                        <div className="divider"></div>
                        <div className="fiend-cards fiend-cards-extra">
                            {renderCards(
                                otherFiends,
                                "fiend",
                                renderCardsKeywords
                            )}
                        </div>
                    </>
                )}

                <CaptureModal
                    show={selectedFiend !== null}
                    onClose={handleCloseModal}
                    fiend={selectedFiend}
                    deltas={deltas}
                    setDeltas={setDeltas}
                    badge={badge}
                />

                <AlertModal
                    show={alert.show}
                    onConfirm={handleAlertConfirm}
                    onCancel={handleAlertCancel}
                    message={
                        alert.action === "save"
                            ? "Sei sicuro di voler salvare le modifiche?"
                            : "Sei sicuro di voler annullare tutte le modifiche?"
                    }
                />

                <h2 className="display-4">Mostri Catturati</h2>
                <div className="container-fluid capture-bar">
                    <CaptureBar fiends={fiends} />
                </div>
                {otherFiends.length > 0 && (
                    <>
                        <h3 className="section-title">Extra</h3>
                        <div className="divider"></div>
                        <div className="container-fluid capture-bar">
                            <CaptureBar fiends={otherFiends} />
                        </div>
                    </>
                )}

                {Object.values(deltas).some((delta) => delta !== 0) && (
                    <>
                        <button
                            className="floating-btn save-btn btn btn-success"
                            onClick={confirmSaveChanges}
                        >
                            <i className="bi bi-check"></i>
                        </button>
                        <button
                            className="floating-btn reset-btn btn btn-danger"
                            onClick={confirmResetChanges}
                        >
                            <i className="bi bi-x"></i>
                        </button>
                    </>
                )}
            </div>
        </div>
    );
};

export default FiendList;
