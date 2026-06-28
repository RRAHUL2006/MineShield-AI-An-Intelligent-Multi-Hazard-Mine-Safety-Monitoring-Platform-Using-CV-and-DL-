import { Navigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({

    children,

    adminOnly = false

}) {

    const {

        authenticated,

        role

    } = useAuth();

    // --------------------------------------
    // Not Logged In
    // --------------------------------------

    if (!authenticated) {

        return (

            <Navigate

                to="/login"

                replace

            />

        );

    }

    // --------------------------------------
    // Admin Only Page
    // --------------------------------------

    if (

        adminOnly &&

        role !== "admin"

    ) {

        return (

            <Navigate

                to="/dashboard"

                replace

            />

        );

    }

    // --------------------------------------

    return children;

}