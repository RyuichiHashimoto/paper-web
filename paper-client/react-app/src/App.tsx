// App.tsx

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginForm from './components/login/login-form';
import Main from './components/Main'
import PaperDetail from "./components/paper/paper-detail"
import Home from "./components/sample/Home"

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" Component={LoginForm} />
        <Route path="/login" Component={LoginForm} />
        <Route path="/main" Component={Main} />
        <Route path="/home" Component={Home} />
        <Route path="/paper-detail/:paper_id" Component={PaperDetail} />
      </Routes>
    </Router>
  );
}

export default App;
