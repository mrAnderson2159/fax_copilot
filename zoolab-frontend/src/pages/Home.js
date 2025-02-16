// zoolab-frontend/src/pages/Home.js
import React, { useEffect, useState } from "react";
import axios from "../api/axios";
import { checkError } from "../utils";
import "../styles/CommonStyles.scss";

const Home = () => {
    const [message, setMessage] = useState([]);

    useEffect(() => {
        const fetchMessage = async () => {
            try {
                const response = checkError(await axios.get("/"));
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
            <h1 className="display-4">{message}</h1>
        </div>
    );
};

export default Home;
