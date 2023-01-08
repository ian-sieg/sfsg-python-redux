import React, {useState, useEffect} from "react"
import Alert from "./Alert"
import { checkLogin } from "../utils/login"

export default function Login () {
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    }) 

    const [loginState, setLoginState] = useState({err: ''})

    useEffect(() => {
        async function check() {
            await checkLogin()
            .then((res) => {
                if (res) {
                    window.location = '/'
                }
            })
        }

        check()
    },[])

    const login = async (e) => {
        e.preventDefault()
        await fetch("/api/login", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: formData.email,
                password: formData.password,
            })
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.error) {
                    setLoginState({err: data.error})
                } else {
                    window.location='/'
                    return setLoginState({login: true})
                }
            })
    }

    return (
        <div className="w3-card-4" style={{ margin: "2rem" }}>
            <div className="w3-container w3-blue w3-center w3-xlarge">
                LOGIN
            </div>
            <div className="w3-container">
                {loginState.err ? (<Alert
                    message={`Check the form and try again! (${loginState.err})`}
                />) : null}
                <form onSubmit={login}>
                    <p>
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            class="w3-input w3-border"
                            id="email"
                            value={formData.email}
                            onChange={(e) => setFormData({...formData, email: e.target.value})}
                        />
                    </p>
                    <p>
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            class="w3-input w3-border"
                            id="password"
                            value={formData.password}
                            onChange={(e) => setFormData({...formData, password: e.target.value})}
                        />
                    </p>
                    <p>
                        <button type="submit" class="w3-button w3-blue">
                            Login
                        </button>
                        {loginState.login ? <p>You're logged in!</p> : null}
                    </p>
                </form>
            </div>
        </div>
    );
}