import React, {useEffect} from "react";
import { logout } from "../utils/login";

export default function Logout() {
    useEffect(() => {
        logout()
    }, [])

    return(
        <>
            <div className="w3-container w3-xlarge">
                <p>Please wait, logging you out...</p>
            </div>
        </>
    )
}