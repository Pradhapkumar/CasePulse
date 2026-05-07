import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Upload, FileCheck, Scale, QrCode, UserCircle, X, Search } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useWorkflow } from '../context/WorkflowContext';

const Sidebar = ({ isOpen, onClose }) => {
  const { language } = useLanguage();
  const { currentStep } = useWorkflow();

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Upload Case', path: '/upload', icon: Upload },
    { name: 'Review & Verify', path: '/review', icon: FileCheck },
    { name: 'Section Analyzer', path: '/section-analyzer', icon: Scale },
    { name: 'QR Scanner', path: '/qr-scanner', icon: QrCode },
    { name: 'Profile', path: '/profile', icon: UserCircle },
  ];

  const sidebarClasses = `fixed inset-y-0 left-0 z-40 w-64 bg-surface border-r border-slate-700 transform transition-transform duration-300 ease-in-out md:translate-x-0 ${
    isOpen ? 'translate-x-0' : '-translate-x-full'
  } md:static md:flex-shrink-0`;

  return (
    <>
      <div className={sidebarClasses}>
        <div className="flex items-center justify-between h-16 px-6 border-b border-slate-700 bg-surface">
          <div className="flex items-center gap-2 text-primary">
            <Scale className="w-8 h-8" />
            <span className="text-xl font-bold text-white tracking-tight">CasePulse</span>
          </div>
          <button onClick={onClose} className="md:hidden text-slate-400 hover:text-white">
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="flex flex-col h-[calc(100vh-4rem)] justify-between overflow-y-auto">
          <nav className="flex-1 px-4 py-6 space-y-2">
            {navItems.map((item) => (
              <NavLink
                key={item.name}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${
                    isActive
                      ? 'bg-primary/10 text-primary border border-primary/20 shadow-[0_0_15px_rgba(59,130,246,0.1)]'
                      : 'text-slate-400 hover:bg-slate-800 hover:text-slate-100'
                  }`
                }
              >
                <item.icon className="w-5 h-5 mr-3" />
                {item.name}
              </NavLink>
            ))}
          </nav>

          <div className="p-4 border-t border-slate-700/50">
            <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700 text-sm">
              <p className="text-slate-400 mb-2">Current Step</p>
              <div className="flex items-center text-white capitalize font-medium">
                <div className="w-2 h-2 rounded-full bg-success mr-2 animate-pulse"></div>
                {currentStep}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Overlay for mobile */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-30 bg-black/50 backdrop-blur-sm md:hidden"
          onClick={onClose}
        />
      )}
    </>
  );
};

export default Sidebar;
