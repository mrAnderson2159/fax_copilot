// src/pages/FiendList.js
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

const FiendList = () => {
    const { zoneId } = useParams();
    const [fiends, setFiends] = useState([]);
    const [otherFiends, setOtherFiends] = useState([]);
    const [zone, setZone] = useState({});
    const [deltas, setDeltas] = useState({});
    const [selectedFiend, setSelectedFiend] = useState(null); // Stato per il modal

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

                // Inizializza deltas per ogni mostro dopo aver ottenuto i dati
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
        console.log(`Cattura singola del mostro con id ${fiend.id}`);
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
        console.log(`Cattura profonda del mostro con id ${fiend.id}`);
        setSelectedFiend(fiend); // Mostra il modal per il mostro selezionato
    };

    const badge = (fiend, { deltas }) => {
        return <Badge delta={deltas[fiend.id]} />;
    };

    const handleCloseModal = () => {
        setSelectedFiend(null); // Nasconde il modal
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
            </div>
        </div>
    );
};

export default FiendList;
