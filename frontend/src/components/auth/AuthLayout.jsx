import React from 'react';
import { Scale } from 'lucide-react';

const AuthLayout = ({ children, title, subtitle }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0F172A] p-4 font-sans">
      <div className="max-w-4xl w-full grid grid-cols-1 md:grid-cols-2 bg-white rounded-3xl overflow-hidden shadow-2xl">
        {/* Left Side: Branding */}
        <div className="hidden md:flex flex-col justify-center p-12 bg-gradient-to-br from-[#1e293b] to-[#0f172a] text-white relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-3xl -mr-32 -mt-32"></div>
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-primary/10 rounded-full blur-3xl -ml-32 -mb-32"></div>
          
          <div className="relative z-10">
            <div className="flex items-center gap-3 mb-8">
              <div className="p-3 bg-white/10 rounded-2xl backdrop-blur-md border border-white/20 shadow-xl">
                <Scale className="w-10 h-10 text-[#D4AF37]" />
              </div>
              <h1 className="text-4xl font-bold tracking-tight">CasePulse</h1>
            </div>
            
            <h2 className="text-3xl font-bold mb-6 leading-tight">
              From Court Judgments to <span className="text-[#D4AF37]">Verified Action Plans</span>
            </h2>
            
            <p className="text-slate-400 text-lg leading-relaxed mb-8">
              Empowering judicial officers with AI-driven analysis, automated action planning, and departmental compliance monitoring.
            </p>
            
            <div className="pt-8 border-t border-white/10">
              <div className="flex items-center gap-4">
                <div className="flex -space-x-2">
                  {[1, 2, 3].map(i => (
                    <div key={i} className="w-10 h-10 rounded-full border-2 border-[#0f172a] bg-slate-700 flex items-center justify-center text-xs font-bold">
                      {String.fromCharCode(64 + i)}
                    </div>
                  ))}
                </div>
                <p className="text-sm text-slate-400 font-medium">Trusted by Judicial Officers across states.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Side: Form */}
        <div className="p-8 md:p-12 flex flex-col justify-center">
          <div className="mb-8">
            <div className="w-12 h-1.5 bg-[#D4AF37] rounded-full mb-4"></div>
            <h2 className="text-2xl font-bold text-slate-900 mb-2">{title}</h2>
            <p className="text-slate-500">{subtitle}</p>
          </div>
          
          {children}
          
          <div className="mt-8 pt-8 border-t border-slate-100 text-center">
            <p className="text-xs text-slate-400 uppercase tracking-widest font-bold">Government of India | CasePulse Portal</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
