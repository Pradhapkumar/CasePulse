import React from 'react';
import AuthLayout from '../components/auth/AuthLayout';
import SignupForm from '../components/auth/SignupForm';

const SignupPage = () => {
  return (
    <AuthLayout 
      title="Create CasePulse Account" 
      subtitle="Join the verified judgment action workflow."
    >
      <SignupForm />
    </AuthLayout>
  );
};

export default SignupPage;
