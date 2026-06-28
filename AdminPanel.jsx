import { useState } from "react";
import ConfirmResetModal from "./ConfirmResetModal";
import "../styles/adminPanel.css";

export default function AdminPanel() {

    const [loading, setLoading] = useState(false);
    const [showModal, setShowModal] = useState(false);

    async function resetDashboard() {

        try {

            setLoading(true);

            const response = await fetch(
                "http://127.0.0.1:8000/admin/reset",
                {
                    method: "POST"
                }
            );

            const data = await response.json();

            setShowModal(false);

            alert(data.message);

            window.dispatchEvent(

    new Event("dashboard-reset")

);

        }
        catch (err) {

            console.error(err);

            alert("Unable to reset dashboard.");

        }
        finally {

            setLoading(false);

        }

    }

    return (

        <>

            <div className="admin-panel">

                <h2>

                    ⚙ Administrator Panel

                </h2>

                <p>

                    Only administrators should perform this action.

                </p>

                <button

                    className="reset-dashboard"

                    onClick={() => setShowModal(true)}

                    disabled={loading}

                >

                    {

                        loading

                            ?

                            "Resetting..."

                            :

                            "🔄 Start New Inspection"

                    }

                </button>

            </div>

            <ConfirmResetModal

                open={showModal}

                loading={loading}

                onCancel={() => setShowModal(false)}

                onConfirm={resetDashboard}

            />

        </>

    );

}