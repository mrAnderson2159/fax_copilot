// src/pages/FiendList.js
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "../api/axios";
import { titleCase } from "../utils";
import "../styles/CommonStyles.css";
import "./FiendList.css";
import renderCards from "../utils/renderCards";
import CaptureBar from "../components/CaptureBar";

const FiendList = () => {
    const { zoneId } = useParams();
    const [fiends, setFiends] = useState([]);
    const [otherFiends, setOtherFiends] = useState([]);
    const [zone, setZone] = useState({});

    useEffect(() => {
        const fetchFiendsWithFound = async () => {
            try {
                const fiendResponse = await axios.get(
                    `/zones/${zoneId}/fiends_with_found`
                );
                setFiends(fiendResponse.data.native || []);
                setOtherFiends(fiendResponse.data.others || []);
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

    const funzioneCattura1 = (id) => {
        console.log(`Cattura singola del mostro con id ${id}`);
    };

    const funzioneCattura2 = (id) => {
        console.log(`Cattura profonda del mostro con id ${id}`);
    };

    return (
        <div className="background-cover">
            <div className="overlay"></div>
            <div className="fiend-list-content container-fluid pt-5">
                <h2 className="display-4">{titleCase(zone.name || "")}</h2>
                <div className="fiend-cards fiend-cards-native">
                    {renderCards(fiends, "fiend", {
                        clickHandler: funzioneCattura1,
                        onLongPress: funzioneCattura2,
                    })}
                </div>

                {otherFiends.length > 0 && (
                    <>
                        <h3 className="section-title">Extra</h3>
                        <div className="divider"></div>
                        <div className="fiend-cards fiend-cards-extra">
                            {renderCards(otherFiends, "fiend", {
                                clickHandler: funzioneCattura1,
                                onLongPress: funzioneCattura2,
                            })}
                        </div>
                    </>
                )}

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
