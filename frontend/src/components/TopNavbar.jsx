import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { User, Bell, Menu, LogOut, ChevronDown } from 'lucide-react';
import LanguageSelector from './common/LanguageSelector';
import api from '../services/api';
import { useNavigate, Link } from 'react-router-dom';

const TopNavbar = ({ onMenuClick }) => {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const user = api.getCurrentUser();

  const handleLogout = () => {
    api.logoutUser();
    navigate('/login');
  };

  const getUserInitials = (name) => {
    if (!name) return '??';
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
  };

  return (
    <header className="sticky top-0 z-30 flex items-center justify-between h-16 px-4 sm:px-6 border-b border-slate-700 bg-surface/80 backdrop-blur-md">
      <div className="flex items-center">
        <button 
          onClick={onMenuClick}
          className="p-2 mr-4 text-slate-400 rounded-lg md:hidden hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <Menu className="w-6 h-6" />
        </button>
        <h2 className="text-lg font-semibold text-slate-100 hidden sm:block">
          {t("appTitle")}
        </h2>
      </div>

      <div className="flex items-center space-x-3 sm:space-x-4">
        {user ? (
          <div className="flex items-center gap-3">
            <button className="relative p-2 text-slate-400 rounded-full hover:text-white hover:bg-slate-800 transition-all">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-surface"></span>
            </button>
            
            <LanguageSelector />

            <div className="hidden md:block text-right ml-2">
              <p className="text-white text-sm font-bold leading-none">{user.name}</p>
              <p className="text-slate-500 text-[10px] uppercase tracking-wider mt-1">{user.role}</p>
            </div>
            <div className="group relative">
              <button className="flex items-center gap-2 p-1 border border-slate-700 rounded-full bg-slate-800 hover:bg-slate-700 transition-all">
                <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary to-blue-400 flex items-center justify-center text-white text-xs font-bold shadow-lg">
                  {getUserInitials(user.name)}
                </div>
                <ChevronDown size={14} className="text-slate-400 mr-1" />
              </button>
              
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-2xl border border-slate-100 py-2 hidden group-hover:block animate-in fade-in slide-in-from-top-2 duration-200">
                <div className="px-4 py-2 border-b border-slate-50 md:hidden">
                  <p className="text-slate-900 font-bold text-sm">{user.name}</p>
                  <p className="text-slate-500 text-[10px] uppercase tracking-widest">{user.role}</p>
                </div>
                <Link to="/profile" className="flex items-center gap-2 px-4 py-2 text-sm text-slate-700 hover:bg-slate-50">
                  <User size={16} /> Profile Settings
                </Link>
                <button 
                  onClick={handleLogout}
                  className="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                >
                  <LogOut size={16} /> Logout Official
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex items-center gap-3">
            <LanguageSelector />
            <Link to="/login" className="px-5 py-1.5 bg-primary hover:bg-blue-600 text-white text-sm font-bold rounded-full transition-all shadow-lg shadow-primary/20">
              Sign In
            </Link>
          </div>
        )}
      </div>
    </header>
  );
};

export default TopNavbar;
