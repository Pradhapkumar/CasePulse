import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import UploadPage from './pages/UploadPage';
import ReviewPage from './pages/ReviewPage';
import DashboardPage from './pages/DashboardPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/upload">Upload</a></li>
            <li><a href="/review">Review</a></li>
            <li><a href="/dashboard">Dashboard</a></li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/review" element={<ReviewPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
