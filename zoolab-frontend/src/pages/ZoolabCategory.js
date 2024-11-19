// zoolab-frontend/src/pages/FiendList.js
import React, { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { CSSTransition, TransitionGroup } from "react-transition-group";
import axios from "../api/axios";
import { titleCase } from "../utils";
import RenderCards from "../utils/RenderCards";
import { useSound } from "../context/SoundContext";
import ContentLoader from "../components/ContentLoader";
import { phRenderCards, phTitle } from "../utils/placeholders";
import "../styles/CommonStyles.scss";
import "./ZoolabCategory.scss";

const ZoolabCategory = () => {
    const { category, title } = useParams();
    const [creations, setCreations] = useState([]);
    const [clickedCreation, setClickedCreation] = useState(null);
    const [dataLoading, setDataLoading] = useState(true);
    const [imageLoading, setImageLoading] = useState(true);
    const { clickSound } = useSound();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchCreations = async () => {
            try {
                const response = await axios.get(`/${category}`);
                setCreations(response.data);
                setDataLoading(false);
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
            <div className="fiend-list-content container-fluid pt-5">
                <ContentLoader isLoading={false || dataLoading || imageLoading}>
                    <ContentLoader.Placeholder>
                        {phTitle("mb-5")}
                        {phRenderCards(creations)}
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
                                        {titleCase(title)}
                                    </h2>
                                    <RenderCards
                                        items={creations}
                                        type="creation"
                                        transitionClass="creation-card-clicked"
                                        clickHandler={handleCreationClick}
                                        onAnimationEnd={handleAnimationEnd}
                                        transitionOnCard={transitionOnCard}
                                        classNameFunction={progressStyle}
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

export default ZoolabCategory;
