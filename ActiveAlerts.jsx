import "../styles/activeAlerts.css";

export default function ActiveAlerts({ alerts }) {

    if (!alerts || alerts.length === 0) return null;

    return (

        <div className="alerts-container">

            <h2>🚨 Active Alerts</h2>

            <div className="alerts-grid">

                {alerts.map((alert, index) => {

                    const violations = Array.isArray(alert.violations)

                        ? alert.violations

                        : String(alert.violations || "")

                              .split(",")

                              .filter(Boolean);

                    return (

                        <div

                            key={alert.alert_id || index}

                            className={`alert-card ${(alert.severity || "LOW").toLowerCase()}`}

                        >

                            <div className="alert-header">

                                <h3>

                                    Worker #{alert.worker_id}

                                </h3>

                                <span className="severity">

                                    {alert.severity}

                                </span>

                            </div>

                            <div className="alert-body">

                                <p>

                                    <strong>📷 Camera:</strong>

                                    {alert.camera_id}

                                </p>

                                <p>

                                    <strong>📍 Location:</strong>

                                    {alert.location}

                                </p>

                                <p>

                                    <strong>🕒 Time:</strong>

                                    {alert.timestamp}

                                </p>

                                <p>

                                    <strong>Status:</strong>

                                    {alert.status}

                                </p>

                                <h4>Violations</h4>

                                <ul>

                                    {

                                        violations.map((v, i) => (

                                            <li key={i}>

                                                {v}

                                            </li>

                                        ))

                                    }

                                </ul>

                            </div>

                        </div>

                    );

                })}

            </div>

        </div>

    );

}