// config.js
const ENV = process.env.REACT_APP_ENV || "local";

const CONFIG = {
    local: {
        API_BASE_URL: "http://localhost:8000",
    },
    ngrok: {
        API_BASE_URL: process.env.REACT_APP_API_BASE_URL,
    },
};

export const API_BASE_URL = CONFIG[ENV].API_BASE_URL;
