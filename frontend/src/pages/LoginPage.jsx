import React from 'react';
import AuthLayout from '../components/auth/AuthLayout';
import LoginForm from '../components/auth/LoginForm';

const LoginPage = () => {
  return (
    <AuthLayout 
      title="Welcome Back to CasePulse" 
      subtitle="Sign in to review court action plans and monitor compliance."
    >
      <LoginForm />
    </AuthLayout>
  );
};

export default LoginPage;
