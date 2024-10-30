// src/utils.js
import { API_BASE_URL } from "./config";

export function titleCase(str) {
    return str
        .toLowerCase()
        .split(" ")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
}

export function resolveImagePath(relativePath) {
    // Costruisce il percorso assoluto delle immagini
    return `${API_BASE_URL}/${relativePath}`;
}

export function debug(flag, ...stuff) {
    if (flag) {
        console.log(...stuff);
    }
}

export const MAX_CAPTURES = 10;
