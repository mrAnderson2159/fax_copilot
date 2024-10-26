// src/pages/ZoneList.js
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../api/axios';
import '../styles/CommonStyles.css';
import './ZoneList.css';
import renderCards from '../utils/renderCards';

const ZoneList = () => {
    const [zones, setZones] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        // Funzione per recuperare le zone
        const fetchZones = async () => {
            try {
                const response = await axios.get('/zones/');
                setZones(response.data);
            } catch (error) {
                console.error('Errore nel recupero delle zone:', error);
            }
        };

        fetchZones();
    }, []);

    return (
        <div className="background-cover zone-list container-fluid pt-5">
            {renderCards(zones, (id) => navigate(`/zones/${id}/fiends/`))}
        </div>
    );
};

export default ZoneList;
