// zoolab-frontend/src/pages/ZoneList.js
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axios";
import RenderCards from "../utils/RenderCards";
import ContentLoader from "../components/ContentLoader";
import { CSSTransition, TransitionGroup } from "react-transition-group";
import { debug } from "../utils";
import { useSound } from "../context/SoundContext";
import "../styles/CommonStyles.scss";
import "./ZoneList.scss";

const DEBUG_MODE = true;

const ZoneList = () => {
    const [zones, setZones] = useState([]);
    const [clickedZoneId, setClickedZoneId] = useState(null); // Stato per tracciare la zona cliccata
    const [dataLoading, setDataLoading] = useState(true);
    const [imageLoading, setImageLoading] = useState(true);
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
            } finally {
                setDataLoading(false);
            }
        };

        fetchZones();
    }, []);

    const handleZoneClick = (zone) => {
        const id = zone.id;
        // localDebug("handleZoneClick", `setting setClickedZoneId(${id})`);
        clickSound();
        setClickedZoneId(id); // Imposta l'ID della zona cliccata per attivare l'animazione
        // localDebug(
        //     "handleZoneClick",
        //     `set setClickedZoneId with value ${clickedZoneId}`
        // );
    };

    const handleAnimationEnd = (zone) => {
        const { id, name } = zone;
        // localDebug(
        //     "handleAnimationEnd",
        //     `about to navigate to ${`/zones/${id}/${name}/`}`
        // );
        navigate(`/zones/${id}/${name}/`);
        // localDebug(
        //     "handleAnimationEnd",
        //     `navigated to ${`/zones/${id}/${name}/`}`
        // );
    };

    const showZoneDetails = (zone) => {
        const id = zone.id;
        console.log(`Showing details of zone ${id}`);
    };

    // Funzione per aggiungere la classe di transizione se l'ID è quello cliccato
    const transitionOnCard = (zone) => {
        const id = zone.id;
        // localDebug(
        //     "transitionOnCard",
        //     `returning ${
        //         clickedZoneId === id
        //     } on clickedZoneId = ${clickedZoneId} and id = ${id}`
        // );
        return clickedZoneId === id ? "zone-card-clicked" : "";
    };

    const zoneShadow = (zone) => {
        return `zone-${zone.status.replace(/_/g, "-")}`;
    };

    return (
        <div className="transparent-background">
            <div className="zone-list-content container-fluid pt-5">
                <ContentLoader isLoading={dataLoading || imageLoading}>
                    <ContentLoader.Placeholder>
                        <h2 className="display-4 list-title">Loading...</h2>
                    </ContentLoader.Placeholder>
                    <ContentLoader.Render>
                        <TransitionGroup>
                            <CSSTransition
                                in={true}
                                timeout={300}
                                classNames="fade"
                                unmountOnExit
                            >
                                <div>
                                    <h2 className="display-4 list-title">
                                        Zone di Spira
                                    </h2>
                                    <RenderCards
                                        items={zones}
                                        type="zone"
                                        clickHandler={handleZoneClick}
                                        onLongPress={showZoneDetails}
                                        transitionOnCard={transitionOnCard}
                                        onAnimationEnd={handleAnimationEnd}
                                        transitionClass="zone-card-clicked"
                                        classNameFunction={zoneShadow}
                                        imageLoadingFunction={setImageLoading}
                                    />
                                </div>
                            </CSSTransition>
                        </TransitionGroup>
                    </ContentLoader.Render>
                </ContentLoader>
            </div>
        </div>
    );
};

export default ZoneList;
