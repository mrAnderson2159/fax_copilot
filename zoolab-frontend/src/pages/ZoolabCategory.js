// zoolab-frontend/src/pages/FiendList.js
import React, { useEffect, useState, useCallback } from "react";
import { useParams } from "react-router-dom";
import axios from "../api/axios";
import { titleCase } from "../utils";
import renderCards from "../utils/renderCards";
import { useSound } from "../context/SoundContext";
import "../styles/CommonStyles.scss";
import "./ZoolabCategory.scss";

const ZoolabCategory = () => {
    const { category, title } = useParams();
    const [fiends, setFiends] = useState([]);
    const { clickSound } = useSound();

    const fetchFiends = useCallback(async () => {
        try {
            const response = await axios.get(`/${category}`);
            setFiends(response.data);
        } catch (error) {
            console.error(error);
        }
    }, [category]);

    useEffect(() => {
        fetchFiends();
    }, [fetchFiends]);

    const renderCardsKeywords = {
        clickHandler: () => {},
        props: {},
    };

    return (
        <div className="trasparent-background">
            <div className="fiend-list-content container-fluid pt-5">
                <h2 className="display-4 list-title">{titleCase(title)}</h2>
                <div className="fiend-cards">
                    {renderCards(
                        fiends,
                        "zoolab-category",
                        renderCardsKeywords
                    )}
                </div>
            </div>
        </div>
    );
};

export default ZoolabCategory;
