import React, { useState } from "react";
import "./Login.css";
import { useNavigate } from "react-router-dom";
import { submitLogin } from "./request";
function Login() {
	const [username, setUserName] = useState("");
	const [password, setPassword] = useState("");
	const navigate = useNavigate();
	const handleLogin = () => {
		submitLogin(username, password, 'error-text', navigate);
	};
	return (
		<div className="card login">
			<h1>Login</h1>
			<div className="label">Username</div>
			<input
				className="button input"
				type="text"
				value={username}
				onChange={(event) => setUserName(event.target.value)}
			/>

			<div className="label">Password</div>
			<input
				className="button input"
				type="password"
				value={password}
				onChange={(event) => setPassword(event.target.value)}
			/>

			<button className="button" onClick={handleLogin}>
				Login
			</button>

			<div id="error-text" className="warning-text">Error</div>
		</div>
	);
}

export default Login;
