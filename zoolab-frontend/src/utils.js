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

// zoolab-frontend/src/utils/debug.js
export function debug(flag, fileName, functionName, ...stuff) {
    if (flag) {
        console.log(`[DEBUG - ${fileName} - ${functionName}]`, ...stuff);
    }
}

export function signed(value) {
    return value > 0 ? `+${value}` : value;
}

export const MAX_CAPTURES = 10;
