import "../styles/multiCamera.css";
import { getCameraStream } from "../services/api";
export default function CameraCard({ camera }) {

    if (!camera) return null;

    return (

        <div className="camera-card">

            <div className="camera-header">

                <div>

                    <h3>

                        📷 Camera

                    </h3>

                    <small>

                        {camera.camera_id}

                    </small>

                </div>

                <div
                    className={
                        camera.running
                            ? "status online"
                            : "status offline"
                    }
                >
                    {
                        camera.running
                            ? "🟢 Online"
                            : "🔴 Offline"
                    }
                </div>

            </div>

            <div className="camera-video">

                {

                    camera.running ?

                    <img

    src={getCameraStream(camera.camera_id)}

    alt={camera.camera_id}

/>

                    :

                    <div className="camera-placeholder">

                        Camera Offline

                    </div>

                }

            </div>

            <div className="camera-stats">

                <div className="stat-box">

                    <span>

                        👷

                    </span>

                    <h4>

                        Workers

                    </h4>

                    <p>

                        {camera.workers}

                    </p>

                </div>

                <div className="stat-box">

                    <span>

                        ⚠

                    </span>

                    <h4>

                        Violations

                    </h4>

                    <p>

                        {camera.violations}

                    </p>

                </div>

                <div className="stat-box">

                    <span>

                        🎥

                    </span>

                    <h4>

                        FPS

                    </h4>

                    <p>

                        {camera.fps}

                    </p>

                </div>

            </div>

        </div>

    );

}