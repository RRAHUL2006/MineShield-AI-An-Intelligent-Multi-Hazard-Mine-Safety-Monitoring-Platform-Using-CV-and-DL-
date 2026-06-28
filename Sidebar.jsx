import { NavLink } from "react-router-dom";

import {
    FaChartBar,
    FaVideo,
    FaFileAlt,
    FaUsersCog,
    FaCog,
    FaUserShield
} from "react-icons/fa";

import { useAuth } from "../context/AuthContext";

import "../styles/sidebar.css";

export default function Sidebar() {

    const { role } = useAuth();

    return (

        <div className="sidebar">

            <h2>

                ⛑ Mine Safety AI

            </h2>

            <ul>

                <li>

                    <NavLink

                        to="/dashboard"

                        className={({isActive})=>

                            isActive

                            ?

                            "menu-item active"

                            :

                            "menu-item"

                        }

                    >

                        <FaChartBar />

                        Dashboard

                    </NavLink>

                </li>

                <li>

                    <NavLink

                        to="/live"

                        className={({isActive})=>

                            isActive

                            ?

                            "menu-item active"

                            :

                            "menu-item"

                        }

                    >

                        <FaVideo />

                        Live Detection

                    </NavLink>

                </li>

                <li>

                    <NavLink

                        to="/compliance"

                        className={({isActive})=>

                            isActive

                            ?

                            "menu-item active"

                            :

                            "menu-item"

                        }

                    >

                        <FaFileAlt />

                        Compliance

                    </NavLink>

                </li>

                {

                    role === "admin"

                    &&

                    <>

                        <li>

                            <NavLink

                                to="/users"

                                className={({isActive})=>

                                    isActive

                                    ?

                                    "menu-item active"

                                    :

                                    "menu-item"

                                }

                            >

                                <FaUsersCog />

                                User Management

                            </NavLink>

                        </li>

                        <li>

                            <NavLink

                                to="/settings"

                                className={({isActive})=>

                                    isActive

                                    ?

                                    "menu-item active"

                                    :

                                    "menu-item"

                                }

                            >

                                <FaCog />

                                Settings

                            </NavLink>

                        </li>

                        <li>

                            <NavLink

                                to="/admin"

                                className={({isActive})=>

                                    isActive

                                    ?

                                    "menu-item active"

                                    :

                                    "menu-item"

                                }

                            >

                                <FaUserShield />

                                Admin Panel

                            </NavLink>

                        </li>

                    </>

                }

            </ul>

        </div>

    );

}