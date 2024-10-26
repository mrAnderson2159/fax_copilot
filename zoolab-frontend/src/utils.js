// src/utils.js
export function titleCase(str) {
    return str
        .toLowerCase()
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}


export function resolveImagePath(relativePath) {
    // Costruisce il percorso assoluto delle immagini
    return `http://localhost:8000/${relativePath}`;
}
