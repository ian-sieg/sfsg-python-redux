import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
    return (
        <div className="w3-bar w3-black">
            <Link to='/'>
            <a className="w3-bar-item w3-button" href="/">
                Quickr
            </a>
            </Link>
            <div style={{ float: "right" }}>
                <Link to='/login'>
                <a className="w3-bar-item w3-button" href="/login">
                    Login
                </a>
                </Link>
                <Link to='/register'>
                <a className="w3-bar-item w3-button" href="/register">
                    Register
                </a>
                </Link>
            </div>
        </div>
    );
}