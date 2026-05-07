import React from 'react';
import { Shield, Globe } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

const Profile = () => {
  const { selectedLanguage } = useLanguage();
  const user = api.getCurrentUser() || {
    name: 'Unknown User',
    email: 'not.logged.in@casepulse.gov',
    role: 'Guest'
  };

  const getUserInitials = (name) => {
    if (!name) return '??';
    const parts = name.split(' ');
    if (parts.length === 1) return parts[0][0].toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h1 className="text-3xl font-bold text-white tracking-tight">Officer Profile</h1>
      
      <div className="bg-surface border border-slate-700 rounded-2xl p-6 md:p-8 max-w-3xl shadow-lg relative overflow-hidden">
        {/* Background Decorative Element */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full -mr-16 -mt-16 blur-2xl"></div>
        
        <div className="flex flex-col md:flex-row items-center gap-8 mb-10 relative z-10">
          <div className="w-32 h-32 rounded-full bg-gradient-to-tr from-primary to-blue-400 p-1 shadow-2xl shadow-primary/20">
            <div className="w-full h-full rounded-full bg-slate-900 flex items-center justify-center text-white text-4xl font-bold border-4 border-slate-800">
              {getUserInitials(user.name)}
            </div>
          </div>
          
          <div className="text-center md:text-left space-y-2">
            <h2 className="text-3xl font-bold text-white">{user.name}</h2>
            <p className="text-primary font-medium tracking-wide flex items-center justify-center md:justify-start gap-2">
              <Shield className="w-4 h-4" />
              {user.role}
            </p>
            <p className="text-slate-400 text-sm">{user.email}</p>
            
            <div className="flex flex-wrap justify-center md:justify-start gap-2 mt-4">
              <span className="px-3 py-1 bg-green-500/10 text-green-500 text-[10px] font-bold rounded-full border border-green-500/20 uppercase tracking-widest">
                Active Officer
              </span>
              <span className="px-3 py-1 bg-blue-500/10 text-blue-500 text-[10px] font-bold rounded-full border border-blue-500/20 uppercase tracking-widest">
                Verified
              </span>
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 relative z-10">
          <div className="p-5 bg-slate-900/50 rounded-2xl border border-slate-800 backdrop-blur-sm">
            <div className="flex items-center gap-3 mb-4 text-slate-400">
              <div className="p-2 bg-primary/10 rounded-lg">
                <Shield className="w-5 h-5 text-primary" />
              </div>
              <span className="font-bold text-sm uppercase tracking-wider">Designation</span>
            </div>
            <p className="text-xl text-white font-bold">{user.role}</p>
            <p className="text-slate-500 text-xs mt-1 italic">Authorized Judicial Reviewer</p>
          </div>
          
          <div className="p-5 bg-slate-900/50 rounded-2xl border border-slate-800 backdrop-blur-sm">
            <div className="flex items-center gap-3 mb-4 text-slate-400">
              <div className="p-2 bg-success/10 rounded-lg">
                <Globe className="w-5 h-5 text-success" />
              </div>
              <span className="font-bold text-sm uppercase tracking-wider">Working Department</span>
            </div>
            <p className="text-xl text-white font-bold">Court Operations</p>
            <p className="text-slate-500 text-xs mt-1 italic">Language Preference: {selectedLanguage?.label?.toUpperCase() || 'ENGLISH'}</p>
          </div>
        </div>
        
        <div className="mt-8 pt-8 border-t border-slate-800 flex flex-col md:flex-row justify-between items-center gap-4 text-slate-500 text-sm">
          <p>Last Activity: {new Date().toLocaleDateString()}</p>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
            <span>System Status: Online</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
