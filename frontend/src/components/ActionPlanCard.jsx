import React from 'react';
import { AlertTriangle, Clock, Briefcase, Activity } from 'lucide-react';

const ActionPlanCard = ({ action }) => {
  // Using dummy data if no prop provided
  const mockAction = action || {
    id: 1,
    required: 'File Counter-Affidavit',
    department: 'Legal Cell',
    deadline: '2023-11-10',
    priority: 'High',
    risk: 85
  };

  const priorityColors = {
    High: 'text-danger bg-danger/10 border-danger/30',
    Medium: 'text-warning bg-warning/10 border-warning/30',
    Low: 'text-success bg-success/10 border-success/30'
  };

  return (
    <div className="bg-surface border border-slate-700 rounded-xl p-5 hover:border-primary/50 transition-colors shadow-sm">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h4 className="text-white font-semibold text-lg">{mockAction.required}</h4>
          <div className="flex items-center gap-2 text-sm text-slate-400 mt-1">
            <Briefcase className="w-4 h-4" />
            {mockAction.department}
          </div>
        </div>
        <span className={`px-2.5 py-1 text-xs font-semibold rounded-md border ${priorityColors[mockAction.priority]}`}>
          {mockAction.priority} Priority
        </span>
      </div>

      <div className="flex items-center justify-between mb-4 mt-6">
        <div className="flex items-center gap-2 text-sm">
          <Clock className="w-4 h-4 text-warning" />
          <span className="text-slate-300">Due: <span className="text-white font-medium">{mockAction.deadline}</span></span>
        </div>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between items-center text-xs">
          <span className="text-slate-400 flex items-center gap-1"><Activity className="w-3 h-3"/> Risk Level</span>
          <span className={mockAction.risk > 70 ? 'text-danger font-medium' : 'text-success font-medium'}>
            {mockAction.risk}%
          </span>
        </div>
        <div className="w-full bg-slate-800 rounded-full h-1.5">
          <div 
            className={`h-1.5 rounded-full ${mockAction.risk > 70 ? 'bg-danger' : 'bg-success'}`}
            style={{ width: `${mockAction.risk}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default ActionPlanCard;
