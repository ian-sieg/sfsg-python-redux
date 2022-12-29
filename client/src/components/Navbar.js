import React from "react";

export default function Navbar() {
    return (
        <div className="w3-bar w3-black">
            <a className="w3-bar-item w3-button" href="/">
                Quickr
            </a>
            <div style={{ float: "right" }}>
                <a className="w3-bar-item w3-button" href="/">
                    Login
                </a>
                <a className="w3-bar-item w3-button" href="/">
                    Register
                </a>
            </div>
        </div>
    );
}