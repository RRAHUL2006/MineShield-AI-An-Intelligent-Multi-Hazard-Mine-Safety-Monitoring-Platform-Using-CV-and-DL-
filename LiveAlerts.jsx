import { useEffect, useState } from "react";

import { getLiveAlerts } from "../services/api";

import "../styles/alerts.css";

export default function LiveAlerts() {

    const [alerts, setAlerts] = useState([]);

    useEffect(() => {

        async function loadAlerts() {

            try {

                const response = await getLiveAlerts();

                setAlerts(response.alerts || []);

            }

            catch (err) {

                console.log(err);

            }

        }

        loadAlerts();

        const timer = setInterval(

            loadAlerts,

            1000

        );

        return () => clearInterval(timer);

    }, []);

    function getAlertIcon(alert){

        const type = (alert.event_type || "PPE").toUpperCase();

        if(type === "FIRE")

            return "🔥";

        if(type === "SMOKE")

            return "💨";

        if(type === "GAS")

            return "☣️";

        return "👷";

    }

    function getAlertTitle(alert){

        const type = (alert.event_type || "PPE").toUpperCase();

        if(type === "FIRE")

            return "Fire Detected";

        if(type === "SMOKE")

            return "Smoke Detected";

        if(type === "GAS")

            return "Gas Leak";

        return `Worker #${alert.worker_id}`;

    }

    return (

        <div className="live-alerts">

            <h2>

                🚨 Live Safety Alerts

            </h2>

            {

                alerts.length===0

                ?

                (

                    <div className="no-alerts">

                        ✅ No Active Alerts

                    </div>

                )

                :

                (

                    <div className="alerts-list">

                        {

                            alerts.map((alert,index)=>(

                                <div

                                    key={index}

                                    className={`alert-card ${(alert.severity || "").toLowerCase()}`}

                                >

                                    <div className="alert-top">

                                        <span>

                                            {getAlertIcon(alert)}

                                            {" "}

                                            {getAlertTitle(alert)}

                                        </span>

                                        <span>

                                            {

                                                alert.severity

                                            }

                                        </span>

                                    </div>

                                    <div className="alert-middle">

                                        <strong>

                                            Event

                                        </strong>

                                        <ul>

                                            {

                                                alert.violations?.map(

                                                    (v,i)=>(

                                                        <li key={i}>

                                                            {v}

                                                        </li>

                                                    )

                                                )

                                            }

                                        </ul>

                                    </div>

                                    <div className="alert-bottom">

                                        📍

                                        {

                                            alert.location ||

                                            "Mine"

                                        }

                                        <br/>

                                        🕒

                                        {

                                            alert.timestamp

                                        }

                                    </div>

                                </div>

                            ))

                        }

                    </div>

                )

            }

        </div>

    );

}