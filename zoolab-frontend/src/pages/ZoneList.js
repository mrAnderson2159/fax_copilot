import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axios";
import "../styles/CommonStyles.css";
import "./ZoneList.css";
import renderCards from "../utils/renderCards";
import { CSSTransition, TransitionGroup } from "react-transition-group";
import { debug } from "../utils";

const DEBUG_MODE = true;

const ZoneList = () => {
    const [zones, setZones] = useState([]);
    const [clickedZoneId, setClickedZoneId] = useState(null); // Stato per tracciare la zona cliccata
    const navigate = useNavigate();
    const localDebug = (...stuff) => debug(DEBUG_MODE, ...stuff);

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

    const handleZoneClick = ({ id }) => {
        localDebug(`setting setClickedZoneId(${id})`);
        setClickedZoneId(id); // Imposta l'ID della zona cliccata per attivare l'animazione
        localDebug(`set setClickedZoneId with value ${clickedZoneId}`);
    };

    const handleAnimationEnd = (id) => {
        localDebug(`about to navigate to ${`/zones/${id}/fiends/`}`);
        navigate(`/zones/${id}/fiends/`);
        localDebug(`navigated to ${`/zones/${id}/fiends/`}`);
    };

    const showZoneDetails = ({ id }) => {
        console.log(`Showing details of zone ${id}`);
        alert(`Showing details of zone ${id}`);
    };

    // Funzione per aggiungere la classe di transizione se l'ID è quello cliccato
    const transitionOnCard = (id) => {
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
                        {renderCards(zones, "zone", {
                            clickHandler: handleZoneClick,
                            onLongPress: showZoneDetails,
                            transitionOnCard: transitionOnCard,
                            onAnimationEnd: handleAnimationEnd,
                        })}
                    </div>
                </CSSTransition>
            </TransitionGroup>
        </div>
    );
};

export default ZoneList;
