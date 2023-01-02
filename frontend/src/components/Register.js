import React, {useState} from "react"
import Alert from "./Alert"

export default function Register() {
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        password: ''
    })

    const [registerMsg, setRegisterMsg] = useState({err: ''})

    const register = (e) => {
        e.preventDefault()

        fetch('http://localhost:5000/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: formData.email,
                username: formData.username,
                password: formData.password,
            })
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.error) {
                    setRegisterMsg({err: data.error})
                } else {
                    setRegisterMsg({'registered': true})
                }
            })
    }

    return (
        <div className="w3-card-4" style={{ margin: "2rem" }}>
            <div className="w3-container w3-blue w3-center w3-xlarge">
                REGISTER
            </div>
            <div className="w3-container">
                {registerMsg.err ? (
                    <Alert
                        message={`Check the form and try again! (${registerMsg.err})`}
                    />
                ) : null}

                <form onSubmit={register}>
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
                        <label htmlFor="username">Username</label>
                        <input
                            type="username"
                            class="w3-input w3-border"
                            id="text"
                            value={formData.username}
                            onChange={(e) => setFormData({...formData, username: e.target.value})}
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
                            Register
                        </button>
                        {registerMsg.registered ? <p>You've been registered!</p> : null}
                    </p>
                </form>
            </div>
        </div>
    );
}