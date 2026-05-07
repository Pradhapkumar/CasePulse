import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, ShieldCheck, AlertCircle, ArrowRight, FileText, Calendar, Building2 } from 'lucide-react';
import api from '../services/api';

const SearchCasePage = () => {
  const [caseUid, setCaseUid] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!caseUid) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await api.searchCaseByUid(caseUid.toUpperCase().trim());
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || "No case found for this CasePulse ID.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 space-y-12">
      {/* Search Hero */}
      <div className="text-center space-y-4">
        <div className="w-16 h-16 bg-primary/10 text-primary rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg shadow-primary/10">
          <Search size={32} />
        </div>
        <h1 className="text-4xl font-bold text-white tracking-tight">Case Verification Center</h1>
        <p className="text-slate-400 max-w-md mx-auto">
          Scan a QR code or enter a unique CasePulse ID to retrieve verified judicial records.
        </p>

        <form onSubmit={handleSearch} className="max-w-lg mx-auto pt-6">
          <div className="relative group">
            <input 
              type="text" 
              className="w-full pl-14 pr-32 py-5 bg-slate-900 border-2 border-slate-700 rounded-2xl text-white text-xl font-bold focus:ring-4 focus:ring-primary/20 focus:border-primary outline-none transition-all placeholder:text-slate-600"
              placeholder="e.g. CP-2026-0001"
              value={caseUid}
              onChange={(e) => setCaseUid(e.target.value)}
            />
            <Search className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-primary" size={24} />
            <button 
              type="submit"
              disabled={loading}
              className="absolute right-3 top-1/2 -translate-y-1/2 px-6 py-2.5 bg-primary text-white rounded-xl font-bold hover:bg-blue-600 transition-all shadow-lg active:scale-95 disabled:opacity-50"
            >
              {loading ? "Searching..." : "Search"}
            </button>
          </div>
        </form>

        <div className="flex justify-center gap-4 pt-4">
          <button 
            onClick={() => alert("Initializing Camera... (Simulation: In production, this would open the device camera to scan physical QR codes)")}
            className="flex items-center gap-2 text-sm font-bold text-slate-400 hover:text-white transition-colors bg-white/5 px-4 py-2 rounded-full border border-white/10"
          >
            <ShieldCheck size={16} className="text-primary" /> Simulate QR Scan
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/20 p-6 rounded-2xl flex items-center gap-4 text-red-500 animate-in fade-in zoom-in duration-300">
          <AlertCircle size={24} />
          <p className="font-bold">{error}</p>
        </div>
      )}

      {result && (
        <div className="bg-surface border border-slate-700 rounded-3xl overflow-hidden animate-in fade-in slide-in-from-top-4 duration-500">
          <div className="p-8 border-b border-slate-700 bg-gradient-to-r from-slate-900/50 to-transparent flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-primary font-bold tracking-widest text-xs uppercase">Case Found</span>
                <ShieldCheck size={14} className="text-green-500" />
              </div>
              <h2 className="text-2xl font-bold text-white">{result.case_summary.case_title}</h2>
              <p className="text-slate-400 text-sm mt-1">{result.case_summary.case_uid} • {result.case_summary.case_type}</p>
            </div>
            <button 
              onClick={() => navigate(`/case-summary/${result.case_summary.case_id}`)}
              className="flex items-center gap-2 bg-white text-slate-900 px-6 py-3 rounded-xl font-bold hover:bg-slate-100 transition-all shadow-xl"
            >
              View Full Summary <ArrowRight size={18} />
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-slate-700/50">
            <SummaryItem icon={Building2} label="Court" value={result.case_summary.court_name} />
            <SummaryItem icon={Calendar} label="Judgment Date" value={result.case_summary.judgment_date} />
            <SummaryItem icon={FileText} label="Department" value={result.case_summary.related_department} />
          </div>

          <div className="p-8 bg-slate-900/30">
            <p className="text-slate-400 text-xs font-bold uppercase mb-3 tracking-widest">Required Action Preview</p>
            <p className="text-slate-200 line-clamp-3 leading-relaxed">
              {result.case_summary.required_action}
            </p>
            <div className="flex gap-4 mt-6">
              <span className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase border ${
                result.case_summary.priority === 'High' ? 'text-red-500 border-red-500/20 bg-red-500/10' : 'text-blue-500 border-blue-500/20 bg-blue-500/10'
              }`}>
                Priority: {result.case_summary.priority}
              </span>
              <span className="px-3 py-1 rounded-full text-[10px] font-bold uppercase border text-green-500 border-green-500/20 bg-green-500/10">
                Deadline: {result.case_summary.deadline}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Helper Info */}
      {!result && !loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-8">
          <div className="p-6 bg-slate-800/30 border border-slate-700/50 rounded-2xl">
            <h4 className="text-white font-bold mb-2">Internal Use</h4>
            <p className="text-slate-400 text-sm">Judicial officers can search for case IDs to review compliance plans and track departmental actions across courts.</p>
          </div>
          <div className="p-6 bg-slate-800/30 border border-slate-700/50 rounded-2xl">
            <h4 className="text-white font-bold mb-2">Data Security</h4>
            <p className="text-slate-400 text-sm">All search queries are audited. Only verified summaries with an active CasePulse ID are searchable in this central portal.</p>
          </div>
        </div>
      )}
    </div>
  );
};

const SummaryItem = ({ icon: Icon, label, value }) => (
  <div className="p-6 flex flex-col gap-1">
    <div className="flex items-center gap-2 text-slate-500 mb-1">
      <Icon size={16} />
      <span className="text-[10px] font-bold uppercase tracking-widest">{label}</span>
    </div>
    <p className="text-slate-200 font-bold truncate">{value}</p>
  </div>
);

export default SearchCasePage;
