import { useState } from "react";

import {

    startCamera,

    stopCamera

} from "../services/api";

export default function CameraControls() {

    const [cameraType, setCameraType] = useState("webcam");

    const [customSource, setCustomSource] = useState("");

    const [running, setRunning] = useState(false);

    async function handleStart() {

        let source = 0;

        switch (cameraType) {

            case "webcam":

                source = 0;

                break;

            case "usb":

                source = 1;

                break;

            case "rtsp":

                source = customSource;

                break;

            case "ip":

                source = customSource;

                break;

            default:

                source = 0;

        }

        const res = await startCamera(source);

        if (res.status === "started") {

            setRunning(true);

        }

        else {

            alert(res.message || "Unable to start camera.");

        }

    }

    async function handleStop() {

        await stopCamera();

        setRunning(false);

    }

    return (

        <div className="camera-controls">

            <div className="camera-row">

                <label>

                    Camera Type

                </label>

                <select

                    value={cameraType}

                    onChange={(e) =>

                        setCameraType(e.target.value)

                    }

                >

                    <option value="webcam">

                        Webcam

                    </option>

                    <option value="usb">

                        USB Camera

                    </option>

                    <option value="rtsp">

                        RTSP Camera

                    </option>

                    <option value="ip">

                        IP Camera

                    </option>

                </select>

            </div>

            {

                (cameraType === "rtsp" ||

                cameraType === "ip") &&

                <div className="camera-row">

                    <label>

                        Camera URL

                    </label>

                    <input

                        type="text"

                        placeholder={

                            cameraType === "rtsp"

                            ? "rtsp://username:password@ip:554/stream"

                            : "http://192.168.1.100:8080/video"

                        }

                        value={customSource}

                        onChange={(e)=>

                            setCustomSource(e.target.value)

                        }

                    />

                </div>

            }

            <div className="camera-buttons">

                <button

                    className="start-btn"

                    onClick={handleStart}

                    disabled={running}

                >

                    ▶ Start Camera

                </button>

                <button

                    className="stop-btn"

                    onClick={handleStop}

                    disabled={!running}

                >

                    ■ Stop Camera

                </button>

            </div>

        </div>

    );

}