import "../styles/complianceStats.css";

export default function ComplianceStats({ statistics }) {

    if (!statistics) return null;

    const safeWorkers =
        statistics.total_workers -
        statistics.total_violations;

    return (

        <div className="compliance-stats">

            <h2>Compliance Statistics</h2>

            <div className="stats-grid">

                <div className="stats-card">

                    <h3>Total Workers</h3>

                    <p>{statistics.total_workers}</p>

                </div>

                <div className="stats-card">

                    <h3>Safe Workers</h3>

                    <p>{safeWorkers}</p>

                </div>

                <div className="stats-card">

                    <h3>Workers with Violations</h3>

                    <p>{statistics.total_violations}</p>

                </div>

            </div>

        </div>

    );

}