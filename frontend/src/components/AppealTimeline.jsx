import React from 'react';
import { Building2, ArrowDown, Scale } from 'lucide-react';

const AppealTimeline = () => {
  const timeline = [
    { id: 1, court: 'District Court', status: 'Completed', date: '12 Jan 2021', outcome: 'Favorable to Petitioner', active: false },
    { id: 2, court: 'High Court', status: 'Completed', date: '05 Aug 2022', outcome: 'Overturned District Court Ruling', active: false },
    { id: 3, court: 'Supreme Court', status: 'In Progress', date: 'Current', outcome: 'Hearing Scheduled', active: true },
  ];

  return (
    <div className="max-w-3xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Appeal Flow Tracking</h1>
        <p className="text-slate-400">Visualizing the movement of this case through the judicial hierarchy.</p>
      </div>

      <div className="bg-surface border border-slate-700 rounded-2xl p-8 shadow-lg">
        <div className="relative pl-8 md:pl-0">
          {/* Vertical Line for Mobile */}
          <div className="absolute left-8 top-8 bottom-8 w-1 bg-slate-800 md:hidden"></div>

          <div className="flex flex-col md:flex-row items-center justify-between gap-8 md:gap-4 relative">
            {/* Connecting Line for Desktop */}
            <div className="hidden md:block absolute left-0 right-0 top-1/2 -translate-y-1/2 h-1 bg-slate-800 z-0"></div>

            {timeline.map((item, index) => (
              <React.Fragment key={item.id}>
                <div className={`relative z-10 flex flex-col ${index % 2 === 0 ? 'md:items-center' : 'md:items-center md:-mt-24 md:mb-24'} w-full md:w-48 text-left md:text-center ml-8 md:ml-0`}>
                  
                  <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-4 transition-all duration-300 ${
                    item.active 
                      ? 'bg-primary shadow-[0_0_20px_rgba(59,130,246,0.3)] scale-110' 
                      : 'bg-slate-800 border-2 border-slate-700'
                  }`}>
                    {index === 2 ? <Scale className={`w-8 h-8 ${item.active ? 'text-white' : 'text-slate-400'}`} /> : <Building2 className={`w-8 h-8 ${item.active ? 'text-white' : 'text-slate-400'}`} />}
                  </div>

                  <div className={`p-4 rounded-xl border ${item.active ? 'bg-primary/10 border-primary/30' : 'bg-slate-900 border-slate-800'} w-full md:w-56 shadow-sm`}>
                    <h4 className={`font-bold ${item.active ? 'text-white' : 'text-slate-300'}`}>{item.court}</h4>
                    <span className={`text-xs font-semibold px-2 py-0.5 rounded-full inline-block mt-2 mb-2 ${
                      item.status === 'Completed' ? 'bg-success/20 text-success' : 'bg-warning/20 text-warning'
                    }`}>
                      {item.status}
                    </span>
                    <p className="text-xs text-slate-400 mb-1">{item.date}</p>
                    <p className={`text-sm ${item.active ? 'text-primary font-medium' : 'text-slate-400'}`}>
                      {item.outcome}
                    </p>
                  </div>
                </div>

                {/* Desktop Arrow */}
                {index < timeline.length - 1 && (
                  <div className="hidden md:flex z-10 bg-slate-800 rounded-full p-1 text-slate-400 border border-slate-700">
                    <ArrowDown className="w-4 h-4 -rotate-90" />
                  </div>
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AppealTimeline;
