// src/utils/renderCards.js
import React from "react";
import Card from "../components/Card";

const renderCards = (items, clickHandler = () => {}, type) => {
    const rows = [];

    for (let i = 0; i < items.length; i += 2) {
        rows.push(
            <div className="row justify-content-center pb-3" key={`row-${i}`}>
                {[0, 1].map((offset) => {
                    const item = items[i + offset];
                    if (!item) return null; // Salta se non esiste un secondo elemento

                    return (
                        <div className={`col-5 mx-2 ${type}`} key={item.id}>
                            <Card
                                name={item.name}
                                imageUrl={item.image_url}
                                clickHandler={() => clickHandler(item.id)}
                                type={type} // Passa il tipo alla Card per gestire l'animazione
                            />
                        </div>
                    );
                })}
            </div>
        );
    }

    return rows;
};

export default renderCards;
