import React from "react";
import { resolveImagePath, titleCase } from "../utils";
import "./Card.css";
import { debug } from "../utils";
import { useClickHandlers } from "../utils/useClickHandlers";

const placeholderImage = "/images/black_placeholder.jpeg";

const Card = ({
    children,
    imageUrl,
    name,
    clickHandler,
    onLongPress,
    type,
}) => {
    const DEBUG = true;
    const localDebug = (...stuff) => debug(DEBUG, ...stuff);
    const [imgSrc, setImgSrc] = React.useState(resolveImagePath(imageUrl));

    // Uso del nostro hook personalizzato per gestire i click e lo stato
    const { handlePressStart, handlePressEnd, isPressed } = useClickHandlers({
        clickHandler,
        onLongPress,
    });

    const handleImageError = () => {
        localDebug("Image error, loading placeholder");
        setImgSrc(placeholderImage);
    };

    return (
        <div
            className={`card ml-3 mb-4 ${type} ${isPressed ? "pressed" : ""}`}
            onMouseDown={handlePressStart}
            onMouseUp={handlePressEnd}
            onTouchStart={handlePressStart}
            onTouchEnd={handlePressEnd}
        >
            <img
                src={imgSrc}
                className="card-img-top"
                alt={name}
                onError={handleImageError}
            />
            <div className="card-body">
                <p className="card-text">{titleCase(name)}</p>
                {children}
            </div>
        </div>
    );
};

export default Card;
