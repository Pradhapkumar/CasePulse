import React from 'react';
import { Shield, Calendar, Scale, Users, FileText } from 'lucide-react';

const ExtractedDataCard = ({ data }) => {
  if (!data) return null;

  return (
    <div className="bg-surface border border-slate-700 rounded-2xl overflow-hidden shadow-lg">
      <div className="p-4 border-b border-slate-700 bg-slate-800/50 flex justify-between items-center">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <FileText className="w-5 h-5 text-primary" />
          Extracted Case Details
        </h3>
        <span className="px-3 py-1 bg-success/20 text-success text-xs font-medium rounded-full flex items-center gap-1 border border-success/30">
          <Shield className="w-3 h-3" />
          High Confidence
        </span>
      </div>
      
      <div className="p-6 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-1">
            <span className="text-sm text-slate-400 flex items-center gap-2">
              <FileText className="w-4 h-4" /> Case Number
            </span>
            <p className="text-white font-medium">{data.caseNumber || 'W.P.(C) 1234/2023'}</p>
          </div>
          
          <div className="space-y-1">
            <span className="text-sm text-slate-400 flex items-center gap-2">
              <Scale className="w-4 h-4" /> Court Name
            </span>
            <p className="text-white font-medium">{data.courtName || 'Supreme Court of India'}</p>
          </div>
        </div>

        <div className="space-y-1">
          <span className="text-sm text-slate-400 flex items-center gap-2">
            <Users className="w-4 h-4" /> Parties
          </span>
          <p className="text-white font-medium">{data.parties || 'John Doe vs. State of XYZ'}</p>
        </div>

        <div className="space-y-1 p-4 bg-slate-900 rounded-xl border border-slate-800">
          <span className="text-sm text-slate-400 font-medium block mb-2">Key Directions</span>
          <ul className="list-disc list-inside text-white space-y-2 text-sm">
            <li>State to file counter-affidavit within 4 weeks.</li>
            <li>Interim protection granted to the petitioner.</li>
            <li>Next date of hearing scheduled for 15th Nov 2023.</li>
          </ul>
        </div>

        <div className="space-y-1">
          <span className="text-sm text-slate-400 flex items-center gap-2">
            <Calendar className="w-4 h-4" /> Timeline / Next Date
          </span>
          <p className="text-warning font-semibold">15 November 2023</p>
        </div>
      </div>
    </div>
  );
};

export default ExtractedDataCard;
