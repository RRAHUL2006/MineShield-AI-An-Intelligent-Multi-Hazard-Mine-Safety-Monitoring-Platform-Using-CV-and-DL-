import { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

import "../styles/navbar.css";

export default function Navbar() {

    const navigate = useNavigate();

    const {

        username,

        role,

        signOut

    } = useAuth();

    const [

        currentTime,

        setCurrentTime

    ] = useState(new Date());

    useEffect(() => {

        const timer = setInterval(() => {

            setCurrentTime(new Date());

        }, 1000);

        return () => clearInterval(timer);

    }, []);

    function logout() {

        signOut();

        navigate("/login");

    }

    return (

        <div className="navbar">

            <div className="navbar-left">

                <h1>

                    ⛑ Mine Safety AI Dashboard

                </h1>

            </div>

            <div className="navbar-right">

                <div className="navbar-user">

                    <div>

                        <strong>

                            👤 {username}

                        </strong>

                        <br />

                        <span>

                            🛡 {role?.toUpperCase()}

                        </span>

                    </div>

                </div>

                <div className="navbar-clock">

                    {currentTime.toLocaleString()}

                </div>

                <button

                    className="logout-btn"

                    onClick={logout}

                >

                    🚪 Logout

                </button>

            </div>

        </div>

    );

}