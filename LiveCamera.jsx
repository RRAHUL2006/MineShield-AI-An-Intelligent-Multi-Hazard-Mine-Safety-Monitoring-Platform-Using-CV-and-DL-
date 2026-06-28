import { useEffect, useState } from "react";

import {

    cameraStatus,

    cameraStream

} from "../services/api";

import CameraControls from "./CameraControls";

import "../styles/liveCamera.css";

export default function LiveCamera() {

    const [status, setStatus] = useState({

        running: false,

        workers: 0,

        violations: 0,

        fps: 0,

        camera: null

    });

    useEffect(() => {

        const timer = setInterval(async () => {

            try {

                const data = await cameraStatus();

                setStatus(data);

            }

            catch (err) {

                console.log(err);

            }

        }, 1000);

        return () => clearInterval(timer);

    }, []);

    return (

        <div className="live-camera-container">

            <h2>

                🎥 Live Camera Monitoring

            </h2>

            <CameraControls />

            <div className="camera-stream-card">

                {

                    status.running ?

                    <img

                        src={cameraStream()}

                        alt="Live Camera"

                        className="camera-stream"

                    />

                    :

                    <div className="camera-offline">

                        <h3>

                            Camera Offline

                        </h3>

                        <p>

                            Click Start Camera to begin monitoring.

                        </p>

                    </div>

                }

            </div>

            <div className="camera-dashboard">

                <div className="camera-stat">

                    <h4>Status</h4>

                    <p>

                        {

                            status.running

                            ?

                            "🟢 Online"

                            :

                            "🔴 Offline"

                        }

                    </p>

                </div>

                <div className="camera-stat">

                    <h4>Workers</h4>

                    <p>

                        {status.workers}

                    </p>

                </div>

                <div className="camera-stat">

                    <h4>Violations</h4>

                    <p>

                        {status.violations}

                    </p>

                </div>

                <div className="camera-stat">

                    <h4>FPS</h4>

                    <p>

                        {status.fps}

                    </p>

                </div>

                <div className="camera-stat">

                    <h4>Camera</h4>

                    <p>

                        {

                            status.camera === null

                            ?

                            "-"

                            :

                            status.camera

                        }

                    </p>

                </div>

            </div>

        </div>

    );

}