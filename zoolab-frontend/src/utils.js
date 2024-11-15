// src/utils.js
import { API_BASE_URL } from "./config";

export function boolToItalian(bool) {
    return bool ? "Sì" : "No";
}

export function debug(flag, fileName, functionName, ...stuff) {
    if (flag) {
        console.log(`[DEBUG - ${fileName} - ${functionName}]`, ...stuff);
    }
}

export function modalShow({ show, onShow = () => {}, onClose = () => {} }) {
    if (show) {
        document.body.classList.add("modal-open");
        onShow();
    } else {
        document.body.classList.remove("modal-open");
        onClose();
    }

    // Cleanup function to ensure class is removed when the component unmounts
    return () => {
        document.body.classList.remove("modal-open");
    };
}

export function resolveImagePath(relativePath) {
    // Costruisce il percorso assoluto delle immagini
    return relativePath ? `${API_BASE_URL}/${relativePath}` : relativePath;
}

export function signed(value) {
    return value > 0 ? `+${value}` : value;
}

export function titleCase(str) {
    return str
        .toLowerCase()
        .split(" ")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
}

export const MAX_CAPTURES = 10;
