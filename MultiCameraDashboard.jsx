import { useEffect, useState } from "react";

import CameraCard from "./CameraCard";

import {

    listCameras,

    addCamera,

    removeCamera

} from "../services/api";

import "../styles/multiCamera.css";

export default function MultiCameraDashboard() {

    const [dashboard, setDashboard] = useState({

        total_cameras: 0,

        total_workers: 0,

        total_violations: 0,

        cameras: []

    });

    async function loadDashboard() {

        try {

            const data = await listCameras();

            setDashboard(data);

        }

        catch (err) {

            console.error(err);

        }

    }

    useEffect(() => {

        loadDashboard();

        const timer = setInterval(

            loadDashboard,

            1000

        );

        return () => clearInterval(timer);

    }, []);

    async function handleAddCamera() {

        const source = prompt(

            "Enter Camera Source\n\n0 = Webcam\n1 = USB Camera\nRTSP/IP URL"

        );

        if (source === null)

            return;

        const value =

            source === "0"

                ? 0

                : source === "1"

                ? 1

                : source;

        await addCamera(value);

        loadDashboard();

    }

    async function handleRemoveCamera(cameraId) {

        if (

            !window.confirm(

                "Remove this camera?"

            )

        )

            return;

        await removeCamera(cameraId);

        loadDashboard();

    }

    return (

        <div className="multi-camera-dashboard">

            <div className="multi-camera-header">

                <h2>

                    🎥 Multi Camera Surveillance

                </h2>

                <button

                    className="add-camera"

                    onClick={handleAddCamera}

                >

                    + Add Camera

                </button>

            </div>

            <div className="camera-summary">

                <div className="summary-card">

                    <h3>

                        {

                            dashboard.total_cameras

                        }

                    </h3>

                    <p>

                        Cameras

                    </p>

                </div>

                <div className="summary-card">

                    <h3>

                        {

                            dashboard.total_workers

                        }

                    </h3>

                    <p>

                        Workers

                    </p>

                </div>

                <div className="summary-card">

                    <h3>

                        {

                            dashboard.total_violations

                        }

                    </h3>

                    <p>

                        Violations

                    </p>

                </div>

            </div>

            {

                dashboard.cameras.length === 0 ?

                (

                    <div
                        style={{
                            textAlign: "center",
                            padding: "60px"
                        }}
                    >

                        <h2>

                            No Cameras Connected

                        </h2>

                        <p>

                            Click "Add Camera" to begin.

                        </p>

                    </div>

                )

                :

                (

                    <div className="camera-grid">

                        {

                            dashboard.cameras.map(

                                (camera) => (

                                    <div

                                        key={camera.camera_id}

                                    >

                                        <CameraCard

                                            camera={camera}

                                        />

                                        <button

                                            className="remove-camera"

                                            onClick={() =>

                                                handleRemoveCamera(

                                                    camera.camera_id

                                                )

                                            }

                                        >

                                            Remove Camera

                                        </button>

                                    </div>

                                )

                            )

                        }

                    </div>

                )

            }

        </div>

    );

}