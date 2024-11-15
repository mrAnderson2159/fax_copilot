// zoolab-frontend/src/pages/ZoneList.js
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axios";
import "../styles/CommonStyles.scss";
import "./ZoneList.scss";
import renderCards from "../utils/renderCards";
import { CSSTransition, TransitionGroup } from "react-transition-group";
import { debug } from "../utils";
import { useSound } from "../context/SoundContext";

const DEBUG_MODE = false;

const ZoneList = () => {
    const [zones, setZones] = useState([]);
    const [clickedZoneId, setClickedZoneId] = useState(null); // Stato per tracciare la zona cliccata
    const navigate = useNavigate();
    const { clickSound } = useSound();
    const localDebug = (functionName, ...stuff) =>
        debug(DEBUG_MODE, "ZoneList.js", functionName, ...stuff);

    useEffect(() => {
        const fetchZones = async () => {
            try {
                const response = await axios.get("/zones/");
                setZones(response.data);
            } catch (error) {
                console.error("Errore nel recupero delle zone:", error);
            }
        };

        fetchZones();
    }, []);

    const handleZoneClick = (zone) => {
        const id = zone.id;
        localDebug("handleZoneClick", `setting setClickedZoneId(${id})`);
        clickSound();
        setClickedZoneId(id); // Imposta l'ID della zona cliccata per attivare l'animazione
        localDebug(
            "handleZoneClick",
            `set setClickedZoneId with value ${clickedZoneId}`
        );
    };

    const handleAnimationEnd = (zone) => {
        const { id, name } = zone;
        localDebug(
            "handleAnimationEnd",
            `about to navigate to ${`/zones/${id}/${name}/`}`
        );
        navigate(`/zones/${id}/${name}/`);
        localDebug(
            "handleAnimationEnd",
            `navigated to ${`/zones/${id}/${name}/`}`
        );
    };

    const showZoneDetails = (zone) => {
        const id = zone.id;
        console.log(`Showing details of zone ${id}`);
        // alert(`Showing details of zone ${id}`);
    };

    // Funzione per aggiungere la classe di transizione se l'ID è quello cliccato
    const transitionOnCard = (zone) => {
        const id = zone.id;
        localDebug(
            "transitionOnCard",
            `returning ${
                clickedZoneId === id
            } on clickedZoneId = ${clickedZoneId} and id = ${id}`
        );
        return clickedZoneId === id ? "zone-card-clicked" : "";
    };

    return (
        <div className="transparent-background">
            <TransitionGroup>
                <CSSTransition
                    in={true}
                    timeout={300}
                    classNames="fade"
                    unmountOnExit
                >
                    <div className="zone-list-content container-fluid pt-5">
                        <h2 className="display-4 list-title">Zone di Spira</h2>
                        {renderCards(zones, "zone", {
                            clickHandler: handleZoneClick,
                            onLongPress: showZoneDetails,
                            transitionOnCard: transitionOnCard,
                            onAnimationEnd: handleAnimationEnd,
                            transitionClass: "zone-card-clicked",
                        })}
                    </div>
                </CSSTransition>
            </TransitionGroup>
        </div>
    );
};

export default ZoneList;
