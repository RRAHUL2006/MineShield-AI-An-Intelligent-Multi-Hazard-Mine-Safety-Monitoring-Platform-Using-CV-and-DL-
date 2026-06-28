import { useState } from "react";

import "../styles/addUserModal.css";

export default function AddUserModal({

    open,

    onClose,

    onSuccess

}) {

    const [username, setUsername] = useState("");

    const [fullName, setFullName] = useState("");

    const [password, setPassword] = useState("");

    const [role, setRole] = useState("operator");

    const [loading, setLoading] = useState(false);

    if (!open) return null;

    async function createUser(e) {

        e.preventDefault();

        setLoading(true);

        try {

            const token = localStorage.getItem("token");

            const response = await fetch(

                "http://127.0.0.1:8000/users",

                {

                    method: "POST",

                    headers: {

                        "Content-Type": "application/json",

                        Authorization: `Bearer ${token}`

                    },

                    body: JSON.stringify({

                        username,

                        full_name: fullName,

                        password,

                        role

                    })

                }

            );

            const data = await response.json();

            if (!response.ok)

                throw new Error(data.detail);

            onSuccess();

            onClose();

        }

        catch(err){

            alert(err.message);

        }

        finally{

            setLoading(false);

        }

    }

    return(

        <div className="modal-overlay">

            <div className="modal-card">

                <h2>

                    ➕ Add User

                </h2>

                <form onSubmit={createUser}>

                    <input

                        placeholder="Username"

                        value={username}

                        onChange={(e)=>setUsername(e.target.value)}

                        required

                    />

                    <input

                        placeholder="Full Name"

                        value={fullName}

                        onChange={(e)=>setFullName(e.target.value)}

                        required

                    />

                    <input

                        type="password"

                        placeholder="Password"

                        value={password}

                        onChange={(e)=>setPassword(e.target.value)}

                        required

                    />

                    <select

                        value={role}

                        onChange={(e)=>setRole(e.target.value)}

                    >

                        <option value="operator">

                            Operator

                        </option>

                        <option value="admin">

                            Admin

                        </option>

                    </select>

                    <div className="modal-buttons">

                        <button

                            type="submit"

                        >

                            {

                                loading

                                ?

                                "Creating..."

                                :

                                "Create User"

                            }

                        </button>

                        <button

                            type="button"

                            onClick={onClose}

                        >

                            Cancel

                        </button>

                    </div>

                </form>

            </div>

        </div>

    );

}