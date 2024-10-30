// zoolab-frontend/src/components/Card.js
import { useEffect, useState } from "react";
import { resolveImagePath, titleCase } from "../utils";
import "./Card.css";
import { debug } from "../utils";
import { useClickHandlers } from "../utils/useClickHandlers";
import { preventDefaultBrowserActions } from "../utils/eventHandlers";

const placeholderImage = "/images/black_placeholder.jpeg";

const Card = ({
    children,
    imageUrl,
    name,
    clickHandler,
    onLongPress,
    type,
    props,
}) => {
    const DEBUG = true;
    const localDebug = (...stuff) => debug(DEBUG, ...stuff);
    const [imgSrc, setImgSrc] = useState(resolveImagePath(imageUrl));

    // Uso del nostro hook personalizzato per gestire i click e lo stato
    const { handlePressStart, handlePressEnd, isPressed } = useClickHandlers({
        clickHandler,
        onLongPress,
    });

    const handleImageError = () => {
        localDebug("Image error, loading placeholder");
        setImgSrc(placeholderImage);
    };

    useEffect(() => {
        // Attiva la prevenzione dei comportamenti del browser e conserva la funzione di pulizia
        const removeEventListeners = preventDefaultBrowserActions();

        // Funzione di pulizia per rimuovere i listener quando il componente si smonta
        return () => {
            removeEventListeners();
        };
    }, []);

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
            {children}
            <div className="card-body">
                <p className="card-text">{titleCase(name)}</p>
            </div>
        </div>
    );
};

export default Card;
