import React from 'react';
import { User, Shield, Globe } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

const Profile = () => {
  const { language } = useLanguage();

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h1 className="text-3xl font-bold text-white tracking-tight">User Profile</h1>
      
      <div className="bg-surface border border-slate-700 rounded-2xl p-6 md:p-8 max-w-2xl shadow-lg">
        <div className="flex flex-col md:flex-row items-center gap-6 mb-8">
          <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-primary to-blue-400 flex items-center justify-center text-white text-3xl font-bold shadow-lg shadow-primary/30">
            JD
          </div>
          <div className="text-center md:text-left">
            <h2 className="text-2xl font-bold text-white">John Doe</h2>
            <p className="text-slate-400 mt-1">john.doe@casepulse.gov</p>
            <span className="inline-block mt-3 px-3 py-1 bg-primary/20 text-primary text-sm font-medium rounded-full border border-primary/30">
              Senior Reviewer
            </span>
          </div>
        </div>
        
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-4 bg-slate-900 rounded-xl border border-slate-800">
              <div className="flex items-center gap-3 mb-2 text-slate-400">
                <Shield className="w-5 h-5 text-primary" />
                <span className="font-medium">System Role</span>
              </div>
              <p className="text-lg text-white font-medium pl-8">Reviewer Level II</p>
            </div>
            
            <div className="p-4 bg-slate-900 rounded-xl border border-slate-800">
              <div className="flex items-center gap-3 mb-2 text-slate-400">
                <Globe className="w-5 h-5 text-success" />
                <span className="font-medium">Preferred Language</span>
              </div>
              <p className="text-lg text-white font-medium pl-8 uppercase">{language}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
