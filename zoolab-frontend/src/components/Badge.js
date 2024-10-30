// zoolab-frontend/src/components/Badge.js
import "./Badge.css";

const Badge = ({ delta }) => {
    let className;

    if (delta === 0) className = "visually-hidden";
    else if (delta > 0) className = "bg-primary";
    else className = "bg-danger";

    // Determina il prefisso per il valore, se è positivo aggiunge un "+"
    const displayValue = delta > 0 ? `+${delta}` : delta;

    return (
        <span
            className={`${className} position-absolute top-0 start-100 translate-middle badge rounded-pill fs-6`}
        >
            {displayValue}
        </span>
    );
};

export default Badge;
