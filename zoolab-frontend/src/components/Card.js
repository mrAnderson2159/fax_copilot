// src/components/Card.js
import React, { useState } from 'react';
import { resolveImagePath, titleCase } from '../utils';
import './Card.css';

const placeholderImage = "/images/black_placeholder.jpeg"; // Percorso esatto nel public

const Card = ({ imageUrl, name, clickHandler }) => {
    const [imgSrc, setImgSrc] = useState(resolveImagePath(imageUrl));

    const handleImageError = () => {
        setImgSrc(placeholderImage); // Imposta il placeholder se l'immagine non viene trovata
    };

    return (
        <div className="card ml-3 mb-4" style={{ width: '100%' }} onClick={clickHandler}>
            <img
                src={imgSrc}
                className="card-img-top"
                alt={name}
                onError={handleImageError} // Aggiungi il gestore di errore
            />
            <div className="card-body">
                <p className="card-text">{titleCase(name)}</p>
            </div>
        </div>
    );
};

export default Card;
