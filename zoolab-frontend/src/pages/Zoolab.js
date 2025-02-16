// zoolab-frontend/src/pages/Zoolab.js
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axios";
import RenderCards from "../utils/RenderCards";
import { CSSTransition, TransitionGroup } from "react-transition-group";
import { checkError, debug } from "../utils";
import { useSound } from "../context/SoundContext";
import ContentLoader from "../components/ContentLoader";
import { phRenderCards, phTitle } from "../utils/placeholders";
import "../styles/CommonStyles.scss";
import "./Zoolab.scss";

const DEBUG_MODE = false;

const Zoolab = () => {
    const [representatives, setRepresentatives] = useState([]);
    const [clickedCategory, setClickedCategory] = useState(null);
    const [dataLoading, setDataLoading] = useState(true);
    const [imageLoading, setImageLoading] = useState(true);
    const navigate = useNavigate();
    const { clickSound } = useSound();
    const localDebug = (functionName, ...stuff) =>
        debug(DEBUG_MODE, "Zoolab.js", functionName, ...stuff);

    useEffect(() => {
        const fetchRepresentatives = async () => {
            try {
                const [area_conquest, species_conquests, original_creation] =
                    await Promise.all([
                        axios.get("/area_conquests/repr").then(checkError),
                        axios.get("/species_conquests/repr").then(checkError),
                        axios.get("/original_creations/repr").then(checkError),
                    ]);
                setRepresentatives([
                    species_conquests.data,
                    area_conquest.data,
                    original_creation.data,
                ]);
                setDataLoading(false);
            } catch (error) {
                console.error("Errore nel recupero dei rappresentanti:", error);
                if (error instanceof Error) {
                    alert(
                        `Errore durante il recupero: ${
                            error.response.data.detail || error.message
                        }`
                    );
                }
            }
        };

        fetchRepresentatives();
    }, []);

    const handleCategoryClick = (category) => {
        const { name } = category;
        clickSound();
        localDebug(
            "handleCategoryClick",
            `setting setClickedCategory(${name})`
        );
        setClickedCategory(name);
    };

    const handleAnimationEnd = (category) => {
        const { destination, name } = category;
        localDebug(
            "handleAnimationEnd",
            `Navigating to /zoolab/${destination}/${name}`
        );
        navigate(`/zoolab/${destination}/${name}`);
    };

    // Funzione per aggiungere la classe di transizione se l'ID è quello cliccato
    const transitionOnCard = (category) => {
        return clickedCategory === category.name ? "category-card-clicked" : "";
    };

    return (
        <div className="transparent-background">
            <div className="zoolab-content container-fluid pt-5">
                <ContentLoader isLoading={false || dataLoading || imageLoading}>
                    <ContentLoader.Placeholder>
                        {phTitle("mb-5")}
                        {phRenderCards(representatives, 3)}
                    </ContentLoader.Placeholder>
                    <ContentLoader.Render>
                        <TransitionGroup>
                            <CSSTransition
                                in={true}
                                timeout={300}
                                classNames="fade"
                                unmountOnExit
                            >
                                <>
                                    <h2 className="display-4 list-title">
                                        Zoolab
                                    </h2>
                                    <RenderCards
                                        items={representatives}
                                        type="category"
                                        clickHandler={handleCategoryClick}
                                        transitionOnCard={transitionOnCard}
                                        onAnimationEnd={handleAnimationEnd}
                                        transitionClass="category-card-clicked"
                                        imageLoadingFunction={setImageLoading}
                                    />
                                </>
                            </CSSTransition>
                        </TransitionGroup>
                    </ContentLoader.Render>
                </ContentLoader>
            </div>
        </div>
    );
};

export default Zoolab;
