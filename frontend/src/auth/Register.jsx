import React from 'react';
import { Link } from 'react-router-dom';

const Register = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="w-full max-w-md p-8 bg-surface border border-slate-700 rounded-2xl shadow-xl">
        <h2 className="text-2xl font-bold text-white mb-6 text-center">Create Account</h2>
        <p className="text-center text-slate-400 mb-8">Join CasePulse platform</p>
        
        {/* Placeholder form to avoid taking too much time on boilerplate */}
        <div className="space-y-4">
          <input className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white" placeholder="Full Name" />
          <input className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white" placeholder="Email" />
          <input className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white" placeholder="Password" type="password" />
          <button className="w-full py-3 bg-primary hover:bg-blue-600 text-white font-medium rounded-lg transition-colors">
            Register
          </button>
        </div>
        
        <p className="text-center text-slate-400 mt-6 text-sm">
          Already have an account? <Link to="/login" className="text-primary hover:text-blue-400 font-medium">Log in</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
