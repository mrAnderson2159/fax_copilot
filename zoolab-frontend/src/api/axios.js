// src/api/axios.js
import axios from "axios";
import { API_BASE_URL } from "../config";

// console.log(API_BASE_URL);

export default axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "true", // Ignora la pagina di avviso di ngrok
    },
});
