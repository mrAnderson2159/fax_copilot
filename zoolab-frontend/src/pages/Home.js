// zoolab-frontend/src/pages/Home.js

import React, { useEffect, useState } from "react";
import axios from "../api/axios";
import "../styles/CommonStyles.css";

const Home = () => {
    const [message, setMessage] = useState([]);

    useEffect(() => {
        const fetchMessage = async () => {
            try {
                const response = await axios.get("/");
                console.log(response.data);

                setMessage(response.data.message);
            } catch (error) {
                console.error("Errore nel recupero del titolo:", error);
            }
        };

        fetchMessage();
    }, []);

    return (
        <div className="transparent-background">
            <h1>{message}</h1>
        </div>
    );
};

export default Home;
