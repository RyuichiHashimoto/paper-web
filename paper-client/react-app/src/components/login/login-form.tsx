// LoginForm.tsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './login-form.css';


const LoginForm: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();


    const handleLogin = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        // ここで実際のログイン処理を行う（例えばAPIの呼び出しなど）

        // ログイン成功後、Mainページに移動する
        if (true) {
            // ログイン成功後、Mainページに移動する
            navigate('/main');
        } else {
            // エラーハンドリング（例：アラートを表示）
            setErrorMessage('Your username or password is incorrect');
        }
    };

    const GoToHome = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        navigate('/Home');
    };


    return (
        <div className="login-container">
            <div className="login-box">
                <h2>Login</h2>
                {errorMessage && (
                    <div className="error-message">
                        {errorMessage}
                    </div>
                )}

                <form onSubmit={handleLogin}>
                    <div className="form-group">
                        <label htmlFor="username">User</label>
                        <input type="text" id="username" name="username" />
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input type="password" id="password" name="password" />
                    </div>
                    <button type="submit" className="btn btn-primary">Submit</button>
                </form>
                <button className="btn btn-secondary">Forgot your passwrod?</button>
                <form onSubmit={GoToHome}>
                    <button type="submit" className="btn btn-primary">Go to Home</button>
                </form>

            </div>
        </div>
    );
};

export default LoginForm;
