import RenderCards from "./RenderCards";
import CaptureBar from "../components/CaptureBar";
import Card from "../components/Card";

export function phCaptureBar(item) {
    return (
        <div className="container-fluid list-title capture-bar">
            <CaptureBar
                placeholderMode={true}
                placeholderData={{
                    fiends_length: item?.length,
                }}
            />
        </div>
    );
}

export function phCard({ children = null, showName = true }) {
    return (
        <Card placeholderMode={true} name="" imageUrl="" showName={showName}>
            {children}
        </Card>
    );
}

export function phRenderCards(item, defaultLength = 8) {
    return (
        <RenderCards
            placeholderMode={true}
            placeholderData={{
                items_length: item?.length || defaultLength,
            }}
        />
    );
}

export function phTitle(classNames) {
    return (
        <h2 className={`display-4 ${classNames} placeholder-wave`}>
            <span
                className="placeholder col-7 mb-1"
                style={{ visibility: "hidden" }}
            ></span>
        </h2>
    );
}
