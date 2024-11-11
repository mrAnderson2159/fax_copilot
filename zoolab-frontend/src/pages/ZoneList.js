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
        const id = zone.id;
        localDebug(
            "handleAnimationEnd",
            `about to navigate to ${`/zones/${id}/fiends/`}`
        );
        navigate(`/zones/${id}/fiends/`);
        localDebug(
            "handleAnimationEnd",
            `navigated to ${`/zones/${id}/fiends/`}`
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

    // Transitiom DEBUG
    useEffect(() => {
        const targetDiv = document.querySelector(".zone-list-content");
        if (!targetDiv) {
            localDebug(
                "useEffect",
                "Elemento target non trovato per l'event listener di debug"
            );
            return;
        }

        const handleTransitionStart = (event) => {
            localDebug("handleTransitionStart", "Transizione iniziata:", event);
        };

        const handleTransitionEnd = (event) => {
            localDebug("handleTransitionEnd", "Transizione terminata:", event);
        };

        const handleClassAddition = (event) => {
            if (event.animationName === "explode") {
                localDebug(
                    "handleClassAddition",
                    "Classe 'explode' aggiunta:",
                    event
                );
            }
        };

        const handleClassRemoval = (event) => {
            localDebug("handleClassRemoval", "Classe rimossa:", event);
        };

        // Event listeners per il debug
        targetDiv.addEventListener("transitionstart", handleTransitionStart);
        targetDiv.addEventListener("transitionend", handleTransitionEnd);
        targetDiv.addEventListener("animationstart", handleClassAddition);
        targetDiv.addEventListener("animationend", handleClassRemoval);

        // Cleanup function per rimuovere i listener
        return () => {
            targetDiv.removeEventListener(
                "transitionstart",
                handleTransitionStart
            );
            targetDiv.removeEventListener("transitionend", handleTransitionEnd);
            targetDiv.removeEventListener(
                "animationstart",
                handleClassAddition
            );
            targetDiv.removeEventListener("animationend", handleClassRemoval);
        };
    }, []);

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
