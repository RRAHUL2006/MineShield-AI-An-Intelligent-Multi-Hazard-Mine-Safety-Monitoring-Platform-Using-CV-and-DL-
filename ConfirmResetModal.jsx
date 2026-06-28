import "../styles/confirmResetModal.css";

export default function ConfirmResetModal({

    open,

    onCancel,

    onConfirm,

    loading

}) {

    if (!open) return null;

    return (

        <div className="modal-overlay">

            <div className="modal-card">

                <h2>

                    ⚠ Start New Inspection

                </h2>

                <p>

                    This action will permanently remove:

                </p>

                <ul>

                    <li>Dashboard Statistics</li>

                    <li>All Alerts</li>

                    <li>Worker History</li>

                    <li>Compliance History</li>

                    <li>Uploaded Images</li>

                    <li>Uploaded Videos</li>

                    <li>Reports (CSV / Excel / PDF)</li>

                    <li>All Camera Sessions</li>

                </ul>

                <p>

                    This action cannot be undone.

                </p>

                <div className="modal-buttons">

                    <button

                        className="cancel-btn"

                        onClick={onCancel}

                    >

                        Cancel

                    </button>

                    <button

                        className="confirm-btn"

                        onClick={onConfirm}

                        disabled={loading}

                    >

                        {

                            loading

                            ?

                            "Resetting..."

                            :

                            "Start New Inspection"

                        }

                    </button>

                </div>

            </div>

        </div>

    );

}