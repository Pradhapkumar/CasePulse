import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Scale, Lock, Mail, CheckCircle2 } from 'lucide-react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [captchaVerified, setCaptchaVerified] = useState(false);
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (captchaVerified && email && password) {
      // Simulate auth
      navigate('/');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="w-full max-w-md p-8 space-y-8 bg-surface border border-slate-700 rounded-2xl shadow-xl">
        <div className="flex flex-col items-center">
          <div className="p-3 bg-primary/10 rounded-full mb-4">
            <Scale className="w-10 h-10 text-primary" />
          </div>
          <h2 className="text-3xl font-bold text-white tracking-tight">CasePulse</h2>
          <p className="text-slate-400 mt-2">Sign in to your account</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-900 border border-slate-700 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent text-white placeholder-slate-500"
                  placeholder="name@example.com"
                  required
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-900 border border-slate-700 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent text-white placeholder-slate-500"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>
          </div>

          {/* CAPTCHA Simulation */}
          <div 
            onClick={() => setCaptchaVerified(!captchaVerified)}
            className={`flex items-center justify-between p-4 border rounded-xl cursor-pointer transition-colors ${
              captchaVerified ? 'bg-success/10 border-success/30' : 'bg-slate-900 border-slate-700 hover:border-primary/50'
            }`}
          >
            <div className="flex items-center gap-3">
              <div className={`w-6 h-6 rounded border flex items-center justify-center transition-colors ${
                captchaVerified ? 'bg-success border-success' : 'border-slate-500 bg-slate-800'
              }`}>
                {captchaVerified && <CheckCircle2 className="w-4 h-4 text-white" />}
              </div>
              <span className={captchaVerified ? 'text-success font-medium' : 'text-slate-300'}>
                {captchaVerified ? 'Verification Successful' : 'I am human'}
              </span>
            </div>
            <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/RecaptchaLogo.svg" alt="captcha" className="h-6 opacity-60" />
          </div>

          <button
            type="submit"
            disabled={!captchaVerified || !email || !password}
            className="w-full py-3 px-4 flex justify-center items-center gap-2 bg-primary hover:bg-blue-600 disabled:bg-slate-700 disabled:text-slate-500 text-white font-semibold rounded-xl shadow-lg shadow-primary/25 transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary focus:ring-offset-surface"
          >
            Sign In
          </button>
        </form>

        <p className="text-center text-slate-400 text-sm">
          Don't have an account? <Link to="/register" className="text-primary hover:text-blue-400 font-medium transition-colors">Register here</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
