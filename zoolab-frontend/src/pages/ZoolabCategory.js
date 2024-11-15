// zoolab-frontend/src/pages/FiendList.js
import React, { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { CSSTransition, TransitionGroup } from "react-transition-group";
import axios from "../api/axios";
import { titleCase } from "../utils";
import renderCards from "../utils/renderCards";
import { useSound } from "../context/SoundContext";
import "../styles/CommonStyles.scss";
import "./ZoolabCategory.scss";

const ZoolabCategory = () => {
    const { category, title } = useParams();
    const [creations, setCreations] = useState([]);
    const [clickedCreation, setClickedCreation] = useState(null);
    const { clickSound } = useSound();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchCreations = async () => {
            try {
                const response = await axios.get(`/${category}`);
                setCreations(response.data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchCreations();
    }, []);

    const handleCreationClick = (creation) => {
        clickSound();
        setClickedCreation(creation.id);
    };

    const handleAnimationEnd = (creation) => {
        const { id } = creation;
        navigate(`/zoolab/${category}/${title}/${id}`);
    };

    const transitionOnCard = (creation) => {
        return clickedCreation === creation.id ? "creation-card-clicked" : "";
    };

    const progressStyle = (creation) => {
        if (creation.defeated) return "creation-defeated";
        else if (creation.created) return "creation-created";
        return "";
    };

    return (
        <div className="trasparent-background">
            <TransitionGroup>
                <CSSTransition
                    in={true}
                    timeout={300}
                    classNames="fade"
                    unmountOnExit
                >
                    <div className="fiend-list-content container-fluid pt-5">
                        <h2 className="display-4 list-title">
                            {titleCase(title)}
                        </h2>
                        {renderCards(creations, "creation", {
                            clickHandler: handleCreationClick,
                            transitionOnCard: transitionOnCard,
                            onAnimationEnd: handleAnimationEnd,
                            transitionClass: "creation-card-clicked",
                            classNameFunction: progressStyle,
                        })}
                    </div>
                </CSSTransition>
            </TransitionGroup>
        </div>
    );
};

export default ZoolabCategory;
