import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './layouts/Layout';
import { useWorkflow } from './context/WorkflowContext';

// Auth Pages
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import Profile from './auth/Profile';

// Workflow Pages
import Home from './pages/Home';
import UploadPage from './pages/UploadPage';
import ProcessingPage from './pages/ProcessingPage';
import ReviewPage from './pages/ReviewPage';
import DashboardPage from './pages/DashboardPage';
import CaseSummaryPage from './pages/CaseSummaryPage';
import SearchCasePage from './pages/SearchCasePage';
import PublicCasePage from './pages/PublicCasePage';

// Feature Pages
import SectionAnalyzer from './section/SectionAnalyzer';
import QRScannerPage from './qr/QRScannerPage';
import AppealTimeline from './components/AppealTimeline';

import ProtectedRoute from './components/auth/ProtectedRoute';

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        
        {/* Protected Routes inside Layout */}
        <Route path="/" element={<Layout><Home /></Layout>} />
        
        <Route path="/upload" element={
          <Layout>
            <ProtectedRoute>
              <UploadPage />
            </ProtectedRoute>
          </Layout>
        } />
        
        <Route path="/processing" element={
          <Layout>
            <ProtectedRoute>
              <ProcessingPage />
            </ProtectedRoute>
          </Layout>
        } />
        
        <Route path="/review" element={
          <Layout>
            <ProtectedRoute>
              <ReviewPage />
            </ProtectedRoute>
          </Layout>
        } />
        
        <Route path="/dashboard" element={
          <Layout>
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          </Layout>
        } />

        <Route path="/profile" element={
          <Layout>
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          </Layout>
        } />
        
        <Route path="/section-analyzer" element={
          <Layout>
            <ProtectedRoute>
              <SectionAnalyzer />
            </ProtectedRoute>
          </Layout>
        } />
        
        <Route path="/qr-scanner" element={
          <Layout>
            <ProtectedRoute>
              <QRScannerPage />
            </ProtectedRoute>
          </Layout>
        } />
        
        <Route path="/appeal-tracking" element={
          <Layout>
            <ProtectedRoute>
              <AppealTimeline />
            </ProtectedRoute>
          </Layout>
        } />

        <Route path="/case/:caseId" element={
          <Layout>
            <ProtectedRoute>
              <ReviewPage />
            </ProtectedRoute>
          </Layout>
        } />

        <Route path="/case-summary/:caseId" element={
          <Layout>
            <ProtectedRoute>
              <CaseSummaryPage />
            </ProtectedRoute>
          </Layout>
        } />

        <Route path="/search-case" element={
          <Layout>
            <ProtectedRoute>
              <SearchCasePage />
            </ProtectedRoute>
          </Layout>
        } />

        <Route path="/public/case/:caseUid" element={<PublicCasePage />} />
        
        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
