// src/utils/renderCards.js
import React from "react";
import Card from "../components/Card";
import { debug } from "../utils";

const DEBUG_MODE = false;

const renderCards = (
    items,
    type,
    {
        clickHandler = () => {},
        onLongPress = () => {},
        transitionOnCard = () => "",
        onAnimationEnd = () => {},
        transitionClass = "",
        children = () => null,
        props = null,
    }
) => {
    const rows = [];
    const localDebug = (functionName, ...stuff) =>
        debug(DEBUG_MODE, "renderCards.js", functionName, ...stuff);

    for (let i = 0; i < items.length; i += 2) {
        rows.push(
            <div className="row justify-content-center pb-3" key={`row-${i}`}>
                {[0, 1].map((offset) => {
                    const item = items[i + offset];
                    if (!item) return null;

                    return (
                        <div
                            className={`col-5 mx-2 ${transitionOnCard(item)}`}
                            key={item.id}
                            onAnimationEnd={() => {
                                if (
                                    transitionOnCard(item) === transitionClass
                                ) {
                                    onAnimationEnd(item);
                                }
                            }}
                        >
                            <Card
                                name={item.name}
                                imageUrl={item.image_url}
                                clickHandler={() => clickHandler(item, props)}
                                onLongPress={() => onLongPress(item, props)}
                                type={type} // Passa il tipo alla Card per gestire l'animazione
                                props={props}
                            >
                                {children(item, props)}
                            </Card>
                        </div>
                    );
                })}
            </div>
        );
    }

    return rows;
};

export default renderCards;
