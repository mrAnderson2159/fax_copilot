// src/pages/FiendList.js
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from '../api/axios';
import { titleCase } from '../utils';
import '../styles/CommonStyles.css';
import './FiendList.css';
import renderCards from '../utils/renderCards';

const FiendList = () => {
    const { zoneId } = useParams();
    const [fiends, setFiends] = useState([]);
    const [otherFiends, setOtherFiends] = useState([]); // Per mostri non nativi
    const [zone, setZone] = useState({}); // Inizializza come oggetto vuoto

    useEffect(() => {
        // Funzione per ottenere i mostri nativi e altri mostri
        const fetchFiendsWithFound = async () => {
            try {
                const fiendResponse = await axios.get(`/zones/${zoneId}/fiends_with_found`);
                setFiends(fiendResponse.data.native); // Imposta i mostri nativi
                setOtherFiends(fiendResponse.data.others); // Imposta i mostri trovabili
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

        fetchFiendsWithFound();
        fetchZone();
    }, [zoneId]);

    return (
        <div className="background-cover fiend-list container-fluid pt-5">
            <h2 className="display-4">{titleCase(zone.name || '')}</h2>
            <div className="fiend-cards fiend-cards-native">
                {renderCards(fiends)}
            </div>

            {otherFiends.length > 0 && (
                <>
                    <h3 className="section-title">Extra</h3>
                    <div className="divider"></div>
                    <div className="fiend-cards fiend-cards-extra">
                        {renderCards(otherFiends)}
                    </div>
                </>
            )}
        </div>
    );
};

export default FiendList;
