import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { User, Bell, Menu } from 'lucide-react';
import LanguageSelector from '../language/LanguageSelector';

const TopNavbar = ({ onMenuClick }) => {
  const { language } = useLanguage();

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
          CasePulse
        </h2>
      </div>

      <div className="flex items-center space-x-4">
        <LanguageSelector />
        
        <button className="p-2 text-slate-400 rounded-full hover:text-white hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-primary">
          <Bell className="w-5 h-5" />
        </button>
        
        <div className="relative flex items-center gap-2 px-3 py-1.5 border border-slate-700 rounded-full bg-slate-800/50 cursor-pointer hover:bg-slate-800 transition-colors">
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white font-medium">
            JD
          </div>
          <div className="hidden sm:block text-sm">
            <p className="text-white font-medium leading-none">John Doe</p>
            <p className="text-slate-400 text-xs mt-1">Reviewer</p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default TopNavbar;
