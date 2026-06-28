import { useState } from "react";

export default function UserActions({

    user,

    onRefresh

}) {

    const [loading, setLoading] = useState(false);

    async function deleteUser() {

        if (

            !window.confirm(

                `Delete ${user.username}?`

            )

        ) return;

        try {

            setLoading(true);

            const token = localStorage.getItem("token");

            const response = await fetch(

                `http://127.0.0.1:8000/users/${user.username}`,

                {

                    method: "DELETE",

                    headers: {

                        Authorization: `Bearer ${token}`

                    }

                }

            );

            const data = await response.json();

            if (!response.ok)

                throw new Error(data.detail);

            onRefresh();

        }

        catch(err){

            alert(err.message);

        }

        finally{

            setLoading(false);

        }

    }

    async function resetPassword(){

        const password = prompt(

            "Enter new password"

        );

        if(!password)

            return;

        try{

            setLoading(true);

            const token = localStorage.getItem("token");

            const response = await fetch(

                `http://127.0.0.1:8000/users/${user.username}/password`,

                {

                    method:"PUT",

                    headers:{

                        "Content-Type":"application/json",

                        Authorization:`Bearer ${token}`

                    },

                    body:JSON.stringify({

                        password

                    })

                }

            );

            const data = await response.json();

            if(!response.ok)

                throw new Error(data.detail);

            alert(

                "Password Updated"

            );

        }

        catch(err){

            alert(err.message);

        }

        finally{

            setLoading(false);

        }

    }

    return(

        <>

            <button

                onClick={resetPassword}

                disabled={loading}

            >

                🔒 Password

            </button>

            <button

                onClick={deleteUser}

                disabled={

                    loading ||

                    user.username==="admin"

                }

            >

                🗑 Delete

            </button>

        </>

    );

}