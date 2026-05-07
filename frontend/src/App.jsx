import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './layouts/Layout';
import { useWorkflow } from './context/WorkflowContext';

// Auth Pages
import Login from './auth/Login';
import Register from './auth/Register';
import Profile from './auth/Profile';

// Workflow Pages
import Home from './pages/Home';
import UploadPage from './pages/UploadPage';
import ProcessingPage from './pages/ProcessingPage';
import ReviewPage from './pages/ReviewPage';
import DashboardPage from './pages/DashboardPage';

// Feature Pages
import SectionAnalyzer from './section/SectionAnalyzer';
import QRScannerPage from './qr/QRScannerPage';
import AppealTimeline from './components/AppealTimeline';

// Strict navigation guard
const ProtectedRoute = ({ children, requiredStep }) => {
  const { currentStep } = useWorkflow();
  
  // A simple linear progression simulation
  const steps = ['upload', 'processing', 'review', 'dashboard'];
  const currentIndex = steps.indexOf(currentStep);
  const requiredIndex = steps.indexOf(requiredStep);

  // Allow going back, but not skipping forward beyond the current progress
  if (requiredStep && requiredIndex > currentIndex) {
    return <Navigate to={`/${currentStep === 'upload' ? '' : currentStep}`} replace />;
  }

  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* Protected Routes inside Layout */}
        <Route path="/" element={<Layout><Home /></Layout>} />
        
        <Route path="/upload" element={
          <Layout>
            <ProtectedRoute requiredStep="upload">
              <UploadPage />
            </ProtectedRoute>
          </Layout>
        } />
        
        <Route path="/processing" element={
          <Layout>
            <ProtectedRoute requiredStep="processing">
              <ProcessingPage />
            </ProtectedRoute>
          </Layout>
        } />
        
        <Route path="/review" element={
          <Layout>
            <ProtectedRoute requiredStep="review">
              <ReviewPage />
            </ProtectedRoute>
          </Layout>
        } />
        
        <Route path="/dashboard" element={
          <Layout>
            <ProtectedRoute requiredStep="dashboard">
              <DashboardPage />
            </ProtectedRoute>
          </Layout>
        } />

        <Route path="/profile" element={<Layout><Profile /></Layout>} />
        <Route path="/section-analyzer" element={<Layout><SectionAnalyzer /></Layout>} />
        <Route path="/qr-scanner" element={<Layout><QRScannerPage /></Layout>} />
        <Route path="/appeal-tracking" element={<Layout><AppealTimeline /></Layout>} />
        
        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
