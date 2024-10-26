// src/pages/FiendList.js
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from '../api/axios';
import { titleCase } from '../utils';
import '../styles/CommonStyles.css';
import renderCards from '../utils/renderCards';

const FiendList = () => {
    const { zoneId } = useParams();
    const [fiends, setFiends] = useState([]);
    const [zone, setZone] = useState({}); // Inizializza come oggetto vuoto
    const navigate = useNavigate();

    useEffect(() => {
        // Funzione per ottenere i mostri
        const fetchFiends = async () => {
            try {
                const fiendResponse = await axios.get(`/zones/${zoneId}/fiends`);
                setFiends(fiendResponse.data);
            } catch (error) {
                console.error('Errore nel recupero dei mostri:', error);
            }
        };

        // Funzione per ottenere la zona
        const fetchZone = async () => {
            try {
                const zoneResponse = await axios.get(`/zones/${zoneId}`);
                setZone(zoneResponse.data);
            } catch (error) {
                console.error('Errore nel recupero della zona:', error);
            }
        };

        fetchFiends();
        fetchZone();
    }, [zoneId]);

    return (
        <div className="background-cover fiend-list container-fluid pt-5">
            <h2 className="display-4">{titleCase(zone.name || '')}</h2>
            {renderCards(fiends) /*(id) => navigate(`/fiends/${id}`))*/}
        </div>
    );
};

export default FiendList;
