// zoolab-frontend/src/components/Card.js
import { useState, useEffect } from "react";
import { resolveImagePath, titleCase } from "../utils";
import "./Card.scss";
import { debug } from "../utils";
import { useClickHandlers } from "../utils/useClickHandlers";

const placeholderImage = "/images/black_placeholder.jpeg";

const Card = ({
    children,
    imageUrl,
    name,
    clickHandler = () => {},
    onLongPress = () => {},
    type = "",
    className = "",
    showName = true,
}) => {
    const DEBUG = false;
    const localDebug = (...stuff) => debug(DEBUG, "Card.js", ...stuff);
    const [imgSrc, setImgSrc] = useState(resolveImagePath(imageUrl));

    useEffect(() => {
        setImgSrc(resolveImagePath(imageUrl));
    }, [imageUrl]);

    // Uso del nostro hook personalizzato per gestire i click e lo stato
    const { handlePressStart, handlePressEnd, isPressed } = useClickHandlers({
        clickHandler,
        onLongPress,
    });

    const handleImageError = () => {
        localDebug("handleImageError", "Image error, loading placeholder");
        setImgSrc(placeholderImage);
    };

    return (
        <div
            className={`card ml-3 mb-4 ${type} ${isPressed ? "pressed" : ""} ${
                className || ""
            }`} // Aggiunge la classe "pressed" quando l'utente preme il tasto
            onMouseDown={handlePressStart}
            onMouseUp={handlePressEnd}
            onTouchStart={handlePressStart}
            onTouchEnd={handlePressEnd}
            draggable="false" // Disabilita il drag su tutto l'elemento
            style={{ userSelect: "none", WebkitUserDrag: "none" }} // Stili per disabilitare selezione e drag
        >
            <img
                src={imgSrc}
                className="card-img-top"
                alt={name}
                onError={handleImageError}
                draggable="false" // Disabilita il drag sull'immagine
                style={{ userSelect: "none", WebkitUserDrag: "none" }} // Stili per disabilitare selezione e drag
            />
            {children}
            {
                // Mostra il nome solo se showName è true
                showName && (
                    <div className="card-body">
                        <p className="card-text">{titleCase(name)}</p>
                    </div>
                )
            }
        </div>
    );
};

export default Card;
