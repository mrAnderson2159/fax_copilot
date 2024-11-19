// src/utils/RenderCards.js
import React, { useEffect, useState } from "react";
import Card from "../components/Card";
import { debug } from "../utils";
import { phCard } from "./placeholders";

const DEBUG_MODE = false;

const RenderCards = ({
    items = [],
    type = "",
    clickHandler = () => {},
    onLongPress = () => {},
    transitionOnCard = () => "",
    onAnimationEnd = () => {},
    transitionClass = "",
    children = () => null,
    props = null,
    className = "",
    classNameFunction = (item) => "",
    imageLoadingFunction = () => true,
    placeholderMode = false,
    placeholderData = {
        items_length: 0,
    },
}) => {
    const localDebug = (functionName, ...stuff) =>
        debug(DEBUG_MODE, "RenderCards.js", functionName, ...stuff);

    const [loadedImages, setLoadedImages] = useState([]);

    useEffect(() => {
        setLoadedImages(new Array(items.length).fill(false));
    }, []);

    const imageLoader = (index, state) => {
        const newImages = [...loadedImages];
        newImages[index] = state;
        setLoadedImages(newImages);
    };

    useEffect(() => {
        if (loadedImages.every((image) => image)) {
            imageLoadingFunction(false);
        }
    }, [loadedImages]);

    const rows = [];

    if (placeholderMode) {
        for (let i = 0; i < placeholderData.items_length; i += 2) {
            rows.push(
                <div
                    className="row justify-content-center pb-3 placeholder-glow"
                    key={`row-${i}`}
                >
                    {[0, 1].map((offset) => {
                        if (i + offset >= placeholderData.items_length)
                            return null;
                        return (
                            <div
                                className="col-5 mx-2"
                                key={`placeholder-${i + offset}`}
                            >
                                {phCard({ children: children() })}
                            </div>
                        );
                    })}
                </div>
            );
        }
    } else {
        for (let i = 0; i < items.length; i += 2) {
            rows.push(
                <div
                    className="row justify-content-center pb-3"
                    key={`row-${i}`}
                >
                    {[0, 1].map((offset) => {
                        const item = items[i + offset];
                        if (!item) return null;

                        return (
                            <div
                                className={`col-5 mx-2 ${transitionOnCard(
                                    item
                                )}`}
                                key={item.id}
                                onAnimationEnd={() => {
                                    if (
                                        transitionOnCard(item) ===
                                        transitionClass
                                    ) {
                                        onAnimationEnd(item);
                                    }
                                }}
                            >
                                <Card
                                    name={item.name}
                                    imageUrl={item.image_url}
                                    clickHandler={() =>
                                        clickHandler(item, props)
                                    }
                                    onLongPress={() => onLongPress(item, props)}
                                    type={type}
                                    props={props}
                                    imageLoadingFunction={(state) =>
                                        imageLoader(i, state)
                                    }
                                    className={
                                        className +
                                        " " +
                                        classNameFunction(item)
                                    }
                                >
                                    {children(item, props)}
                                </Card>
                            </div>
                        );
                    })}
                </div>
            );
        }
    }
    return <>{rows}</>;
};

export default RenderCards;
