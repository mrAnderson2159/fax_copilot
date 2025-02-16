// zoolab-frontend/src/pages/FiendList.js
import React, { useEffect, useState, useCallback } from "react";
import { useParams } from "react-router-dom";
import axios from "../api/axios";
import { checkError, titleCase, MAX_CAPTURES } from "../utils";
import ContentLoader from "../components/ContentLoader";
import RenderCards from "../utils/RenderCards";
import CaptureBar from "../components/CaptureBar";
import Badge from "../components/Badge";
import CaptureModal from "../components/CaptureModal";
import AlertModal from "../components/AlertModal";
import CreationAlertModal from "../components/CreationAlertModal";
import { phCaptureBar, phRenderCards, phTitle } from "../utils/placeholders";
import { useSound } from "../context/SoundContext";
import "../styles/CommonStyles.scss";
import "./FiendList.scss";

const FiendList = () => {
    const { zoneId, zoneName } = useParams();
    const [fiends, setFiends] = useState([]);
    const [otherFiends, setOtherFiends] = useState([]);
    const [deltas, setDeltas] = useState({});
    const [selectedFiend, setSelectedFiend] = useState(null);
    const [alert, setAlert] = useState({
        show: false,
        action: null,
        details: "",
    });
    const [dataLoading, setDataLoading] = useState(true);
    const [imageLoading, setImageLoading] = useState(true);
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [currentCreation, setCurrentCreation] = useState(null);
    const [creationQueue, setCreationQueue] = useState([]);
    const {
        errorSound,
        clickSound,
        backSound,
        highConfirmSound,
        lowConfirmSound,
    } = useSound();

    // Funzione per ottenere i dati sui mostri con le informazioni sulle catture
    const fetchFiendsWithFound = useCallback(async () => {
        try {
            const fiendResponse = checkError(
                await axios.get(`/zones/${zoneId}/fiends_with_found`)
            );

            const nativeFiends = fiendResponse.data.native || [];
            const otherFiendsData = fiendResponse.data.others || [];

            setFiends(nativeFiends);
            setOtherFiends(otherFiendsData);

            const initialDeltas = nativeFiends.reduce((acc, fiend) => {
                acc[fiend.id] = 0;
                return acc;
            }, {});

            setDeltas(initialDeltas);
        } catch (error) {
            console.error("Errore nel recupero dei mostri:", error);
        } finally {
            setDataLoading(false);
        }
    }, [zoneId]);

    // Recupera i dati all'inizio e ogni volta che zoneId cambia
    useEffect(() => {
        fetchFiendsWithFound();
    }, [zoneName, fetchFiendsWithFound]);

    // Funzione per il click normale
    const funzioneCattura1 = useCallback((fiend) => {
        setDeltas((prevDeltas) => {
            const newDelta = Math.min(
                (prevDeltas[fiend.id] || 0) + 1,
                MAX_CAPTURES - fiend.was_captured
            );
            newDelta ? clickSound() : errorSound();
            return {
                ...prevDeltas,
                [fiend.id]: newDelta,
            };
        });
    }, []);

    // Funzione per il click prolungato
    const funzioneCattura2 = useCallback((fiend) => {
        clickSound();
        setSelectedFiend(fiend);
    }, []);

    // Funzione per chiudere il modal
    const handleCloseModal = () => {
        backSound();
        setSelectedFiend(null);
    };

    const confirmSaveChanges = () => {
        clickSound();
        const details = Object.entries(deltas)
            .filter(([_, delta]) => delta !== 0)
            .map(([fiend_id, delta]) => {
                const fiend = fiends
                    .concat(otherFiends)
                    .find((f) => f.id === parseInt(fiend_id));
                return `${titleCase(fiend.name)}: ${delta}`;
            })
            .join("\n");

        setAlert({ show: true, action: "save", details });
    };

    const confirmResetChanges = () => {
        clickSound();
        setAlert({ show: true, action: "reset", details: "" });
    };

    const saveChanges = async () => {
        try {
            const response = await axios.post("/fiends/update_captures", {
                updates: Object.entries(deltas)
                    .filter(([_, delta]) => delta !== 0)
                    .map(([fiend_id, delta]) => ({ fiend_id, delta })),
            });

            setDeltas((prev) =>
                Object.fromEntries(
                    Object.entries(prev).map(([key]) => [key, 0])
                )
            );
            setConfirmLoading(false);
            highConfirmSound();
            fetchFiendsWithFound(); // Aggiorna i mostri dopo aver salvato
            enqueueConquests(response.data);
        } catch (error) {
            console.error("Errore nell'aggiornamento delle catture:", error);
        } finally {
            setAlert({ show: false, action: null, details: "" });
        }
    };

    const resetChanges = () => {
        setDeltas((prev) =>
            Object.fromEntries(Object.entries(prev).map(([key]) => [key, 0]))
        );
        lowConfirmSound();
        setAlert({ show: false, action: null, details: "" });
    };

    const enqueueConquests = ({
        area_conquests,
        species_conquests,
        original_creations,
    }) => {
        const allConquests = [
            ...(area_conquests || []).map((conquest) => ({
                ...conquest,
                type: "Campione di Zona",
                destinationName: "Campioni di Zona",
            })),
            ...(species_conquests || []).map((conquest) => ({
                ...conquest,
                type: "Campione di Specie",
                destinationName: "Campioni di Specie",
            })),
            ...(original_creations || []).map((conquest) => ({
                ...conquest,
                type: "Prototipo",
                destinationName: "Prototipi Zoolab",
            })),
        ];

        setCreationQueue((prevQueue) => [...prevQueue, ...allConquests]);
    };

    // Mostra il prossimo elemento nella coda
    useEffect(() => {
        if (!currentCreation && creationQueue.length > 0) {
            setCurrentCreation(creationQueue[0]);
            setCreationQueue((prevQueue) => prevQueue.slice(1));
        }
    }, [currentCreation, creationQueue]);

    const handleAlertConfirm = () => {
        if (alert.action === "save") {
            saveChanges();
        } else if (alert.action === "reset") {
            resetChanges();
        }
    };

    const handleAlertCancel = () => {
        backSound();
        setAlert({ show: false, action: null, details: "" });
    };

    const handleCreationAlertClose = () => {
        backSound();
        setCurrentCreation(null);
    };

    const badge = useCallback(
        (fiend, { deltas }) => <Badge delta={deltas[fiend.id]} />,
        [deltas]
    );

    const maxCaptured = (fiend) => {
        return fiend.was_captured === MAX_CAPTURES
            ? "max-captured"
            : "not-max-captured";
    };

    const renderCardsKeywords = {
        clickHandler: funzioneCattura1,
        onLongPress: funzioneCattura2,
        children: badge,
        props: {
            deltas,
        },
        classNameFunction: maxCaptured,
        imageLoadingFunction: setImageLoading,
    };

    return (
        <div className="transparent-background">
            <div className="fiend-list-content container-fluid pt-5">
                <ContentLoader isLoading={false || dataLoading || imageLoading}>
                    <ContentLoader.Placeholder>
                        {phTitle("mb-5")}
                        {phRenderCards(fiends)}
                        {phTitle("fiendlist-title capturebar-title")}
                        {phCaptureBar(fiends)}
                    </ContentLoader.Placeholder>
                    <ContentLoader.Render>
                        <h2 className="display-4 fiendlist-title">
                            {titleCase(zoneName || "")}
                        </h2>
                        <div className="fiend-cards fiend-cards-native">
                            <RenderCards
                                items={fiends}
                                type="fiend"
                                {...renderCardsKeywords}
                            />
                        </div>

                        {otherFiends.length > 0 && (
                            <>
                                <h3 className="section-title">Extra</h3>
                                <div className="divider"></div>
                                <div className="fiend-cards fiend-cards-extra">
                                    <RenderCards
                                        items={otherFiends}
                                        type="fiend"
                                        {...renderCardsKeywords}
                                    />
                                </div>
                            </>
                        )}

                        <CaptureModal
                            show={selectedFiend !== null}
                            onClose={handleCloseModal}
                            fiend={selectedFiend}
                            deltas={deltas}
                            setDeltas={setDeltas}
                            badge={badge}
                        />

                        <AlertModal
                            show={alert.show}
                            onConfirm={handleAlertConfirm}
                            onCancel={handleAlertCancel}
                            message={
                                alert.action === "save"
                                    ? "Sei sicuro di voler salvare le modifiche?"
                                    : "Sei sicuro di voler annullare tutte le modifiche?"
                            }
                            details={alert.details}
                            loadingFunction={setConfirmLoading}
                            isLoading={confirmLoading}
                        />

                        <CreationAlertModal
                            show={!!currentCreation}
                            onClose={handleCreationAlertClose}
                            creation={currentCreation}
                        />

                        <h2 className="display-4 fiendlist-title capturebar-title">
                            Mostri Catturati
                        </h2>
                        <div className="container-fluid capture-bar">
                            <CaptureBar fiends={fiends} />
                        </div>
                        {otherFiends.length > 0 && (
                            <>
                                <h3 className="section-title">Extra</h3>
                                <div className="divider"></div>
                                <div className="container-fluid capture-bar">
                                    <CaptureBar fiends={otherFiends} />
                                </div>
                            </>
                        )}

                        {Object.values(deltas).some((delta) => delta !== 0) && (
                            <>
                                <button
                                    className="floating-btn save-btn btn btn-success"
                                    onClick={confirmSaveChanges}
                                >
                                    <i className="bi bi-check"></i>
                                </button>
                                <button
                                    className="floating-btn reset-btn btn btn-danger"
                                    onClick={confirmResetChanges}
                                >
                                    <i className="bi bi-x"></i>
                                </button>
                            </>
                        )}
                    </ContentLoader.Render>
                </ContentLoader>
            </div>
        </div>
    );
};

export default FiendList;
