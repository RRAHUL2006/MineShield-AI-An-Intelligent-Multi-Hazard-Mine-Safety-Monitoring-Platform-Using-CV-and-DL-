import { useEffect, useRef, useState } from "react";
import { getLiveAlerts } from "../services/api";
import "../styles/alerts.css";

export default function AlertPopup() {

    const [alert, setAlert] = useState(null);

    const [alarmMuted, setAlarmMuted] = useState(false);

    const lastAlert = useRef(null);

    const initialized = useRef(false);

    const audio = useRef(new Audio("/alarm.mp3"));

    //----------------------------------------------------

    useEffect(() => {

        async function checkAlerts() {

            try {

                const response = await getLiveAlerts();

                const alerts = response.alerts || [];

                if (alerts.length === 0)
                    return;

                const newest = alerts[0];

                const id =
                    newest.alert_id ||
                    newest.timestamp +
                    newest.worker_id;

                // Ignore existing database alerts when page opens
                if (!initialized.current) {

                    initialized.current = true;

                    lastAlert.current = id;

                    return;

                }

                if (lastAlert.current === id)
                    return;

                lastAlert.current = id;

                setAlert(newest);

                if (
                    !alarmMuted &&
                    (
                        newest.severity === "HIGH" ||
                        newest.severity === "CRITICAL"
                    )
                ) {

                    audio.current.currentTime = 0;

                    audio.current.play().catch(() => {});

                }

            }

            catch (err) {

                console.log(err);

            }

        }

        checkAlerts();

        const timer = setInterval(

            checkAlerts,

            1000

        );

        return () => clearInterval(timer);

    }, [alarmMuted]);

    //----------------------------------------------------
    // Space = Toggle Alarm
    //----------------------------------------------------

    useEffect(() => {

        function handleKeyDown(e) {

            if (e.code !== "Space")
                return;

            setAlarmMuted(prev => {

                const next = !prev;

                if (next) {

                    audio.current.pause();

                    audio.current.currentTime = 0;

                }

                return next;

            });

        }

        window.addEventListener(

            "keydown",

            handleKeyDown

        );

        return () =>

            window.removeEventListener(

                "keydown",

                handleKeyDown

            );

    }, []);

    //----------------------------------------------------
    // Auto close popup
    //----------------------------------------------------

    useEffect(() => {

        if (!alert)
            return;

        const timer = setTimeout(() => {

            setAlert(null);

        }, 6000);

        return () => clearTimeout(timer);

    }, [alert]);

    //----------------------------------------------------

    if (!alert)
        return null;

    const eventType = (

        alert.event_type ||

        "PPE"

    ).toUpperCase();

    let title = "⚠ PPE VIOLATION";

    let icon = "👷";

    let popupClass = "popup-card";

    if (eventType === "FIRE") {

        title = "🔥 FIRE DETECTED";

        icon = "🔥";

        popupClass += " fire-popup";

    }

    else if (eventType === "SMOKE") {

        title = "💨 SMOKE DETECTED";

        icon = "💨";

        popupClass += " smoke-popup";

    }

    //----------------------------------------------------

    return (

        <div className="popup-overlay">

            <div className={popupClass}>

                <h2>{title}</h2>

                {

                    eventType === "PPE"

                    ?

                    <h3>

                        👷 Worker #{alert.worker_id}

                    </h3>

                    :

                    <h3>

                        {icon} Mine Safety Alert

                    </h3>

                }

                <p>

                    <strong>Severity</strong>

                    <br />

                    {alert.severity}

                </p>

                <p>

                    <strong>Event</strong>

                </p>

                <ul>

                    {

                        alert.violations?.map(

                            (v, i) =>

                                <li key={i}>{v}</li>

                        )

                    }

                </ul>

                <p>

                    📍 {alert.location || "Mine"}

                </p>

                <p>

                    🕒 {alert.timestamp}

                </p>

                {

                    eventType === "FIRE" &&

                    <div
                        style={{
                            color: "#dc2626",
                            fontWeight: "bold",
                            marginTop: 12
                        }}
                    >

                        🚨 Immediate evacuation recommended.

                    </div>

                }

                {

                    eventType === "SMOKE" &&

                    <div
                        style={{
                            color: "#ea580c",
                            fontWeight: "bold",
                            marginTop: 12
                        }}
                    >

                        💨 Inspect ventilation immediately.

                    </div>

                }

                <hr
                    style={{
                        margin: "15px 0"
                    }}
                />

                <p>

                    {alarmMuted

                        ?

                        "🔇 Alarm Muted (Press Space)"

                        :

                        "🔊 Alarm Active (Press Space)"

                    }

                </p>

                <button

                    onClick={() => {

                        audio.current.pause();

                        audio.current.currentTime = 0;

                        setAlert(null);

                    }}

                >

                    Dismiss

                </button>

            </div>

        </div>

    );

}