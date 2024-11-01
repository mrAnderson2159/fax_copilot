// zoolab-frontend/src/components/Badge.js
import "./Badge.css";
import { signed } from "../utils";

const Badge = ({ delta }) => {
    let className;

    if (delta === 0) className = "visually-hidden";
    else if (delta > 0) className = "bg-primary";
    else className = "bg-danger";

    return (
        <span
            className={`${className} position-absolute top-0 start-100 translate-middle badge rounded-pill fs-6`}
        >
            {signed(delta)}
        </span>
    );
};

export default Badge;
