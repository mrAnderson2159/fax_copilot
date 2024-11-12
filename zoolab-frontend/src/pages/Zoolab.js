// zoolab-frontend/src/pages/Zoolab.js
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axios";
import renderCards from "../utils/renderCards";
import { CSSTransition, TransitionGroup } from "react-transition-group";
import { debug } from "../utils";
import { useSound } from "../context/SoundContext";
import "../styles/CommonStyles.scss";
import "./Zoolab.scss";

const DEBUG_MODE = false;

const Zoolab = () => {
    const [representatives, setRepresentatives] = useState([]);
    const [clickedCategory, setClickedCategory] = useState(null);
    const navigate = useNavigate();
    const { clickSound } = useSound();
    const localDebug = (functionName, ...stuff) =>
        debug(DEBUG_MODE, "Zoolab.js", functionName, ...stuff);

    useEffect(() => {
        const fetchRepresentatives = async () => {
            try {
                const [area_conquest, species_conquests, original_creation] =
                    await Promise.all([
                        axios.get("/area_conquests/repr"),
                        axios.get("/species_conquests/repr"),
                        axios.get("/original_creations/repr"),
                    ]);

                setRepresentatives([
                    species_conquests.data,
                    area_conquest.data,
                    original_creation.data,
                ]);
            } catch (error) {
                console.error("Errore nel recupero dei rappresentanti:", error);
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
            <TransitionGroup>
                <CSSTransition
                    in={true}
                    timeout={300}
                    classNames="fade"
                    unmountOnExit
                >
                    <div className="zoolab-content container-fluid pt-5">
                        <h2 className="display-4 list-title">Zoolab</h2>
                        {renderCards(representatives, "category", {
                            clickHandler: handleCategoryClick,
                            onLongPress: () => {}, // Puoi implementare azioni extra se necessarie
                            transitionOnCard: transitionOnCard,
                            onAnimationEnd: handleAnimationEnd,
                            transitionClass: "category-card-clicked",
                        })}
                    </div>
                </CSSTransition>
            </TransitionGroup>
        </div>
    );
};

export default Zoolab;
