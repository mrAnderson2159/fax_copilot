// zoolab-frontend/src/components/Card.js
import { useState, useEffect } from "react";
import { resolveImagePath, titleCase } from "../utils";
import { debug } from "../utils";
import { useClickHandlers } from "../utils/useClickHandlers";
import "./Card.scss";

const blackPlaceholder = "/images/black_placeholder.webp";

const Card = ({
    children,
    imageUrl,
    name,
    clickHandler = () => {},
    onLongPress = () => {},
    type = "",
    className = "",
    showName = true,
    imageLoadingFunction = () => true,
    placeholderMode = false,
}) => {
    const DEBUG = false;
    const localDebug = (...stuff) => debug(DEBUG, "Card.js", ...stuff);
    const [imgSrc, setImgSrc] = useState(resolveImagePath(imageUrl));
    const [showImage, setShowImage] = useState(false);

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
        setImgSrc(blackPlaceholder);
    };

    if (placeholderMode) {
        return (
            <div className="card ml-3 mb-4">
                <div className="placeholder-image"></div>
                {
                    // Mostra il nome solo se showName è true
                    showName && (
                        <div className="card-body">
                            <p className="card-text">
                                <span className="placeholder col-10 ms-1"></span>
                            </p>
                        </div>
                    )
                }
            </div>
        );
    } else {
        return (
            <div
                className={`card ml-3 mb-4 ${type} ${
                    isPressed ? "pressed" : ""
                } ${className || ""}`} // Aggiunge la classe "pressed" quando l'utente preme il tasto
                onMouseDown={handlePressStart}
                onMouseUp={handlePressEnd}
                onTouchStart={handlePressStart}
                onTouchEnd={handlePressEnd}
                draggable="false" // Disabilita il drag su tutto l'elemento
                style={{ userSelect: "none", WebkitUserDrag: "none" }} // Stili per disabilitare selezione e drag
            >
                <div
                    className={`placeholder-image ${
                        showImage ? "devnulled" : ""
                    }`}
                ></div>
                <img
                    src={imgSrc}
                    className={`card-img-top ${showImage ? "" : "hidden"}`}
                    alt={name}
                    onError={handleImageError}
                    draggable="false" // Disabilita il drag sull'immagine
                    onLoad={() => {
                        imageLoadingFunction(false);
                        setShowImage(true);
                    }}
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
    }
};

export default Card;
