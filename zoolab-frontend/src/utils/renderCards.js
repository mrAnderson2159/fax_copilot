// src/utils/renderCards.js
import React from "react";
import Card from "../components/Card";

const renderCards = (
    items,
    type,
    {
        clickHandler = () => {},
        onLongPress = () => {},
        transitionOnCard = () => "",
        onAnimationEnd = () => {},
    }
) => {
    const rows = [];

    for (let i = 0; i < items.length; i += 2) {
        rows.push(
            <div className="row justify-content-center pb-3" key={`row-${i}`}>
                {[0, 1].map((offset) => {
                    const item = items[i + offset];
                    if (!item) return null;

                    return (
                        <div
                            className={`col-5 mx-2 ${transitionOnCard(
                                item.id
                            )}`}
                            key={item.id}
                            onAnimationEnd={() => {
                                if (
                                    transitionOnCard(item.id) ===
                                    "zone-card-clicked"
                                ) {
                                    onAnimationEnd(item.id);
                                }
                            }}
                        >
                            <Card
                                name={item.name}
                                imageUrl={item.image_url}
                                clickHandler={() => clickHandler(item.id)}
                                onLongPress={() => onLongPress(item.id)}
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
