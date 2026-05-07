import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Upload, FileText, ArrowRight } from 'lucide-react';
import { useWorkflow } from '../context/WorkflowContext';

const Home = () => {
  const navigate = useNavigate();
  const { advanceStep } = useWorkflow();
  const [court, setCourt] = useState('');
  const [caseName, setCaseName] = useState('');
  
  const courts = ['Supreme Court', 'High Court of Delhi', 'Bombay High Court', 'District Court'];
  const cases = {
    'Supreme Court': ['Kesavananda Bharati v. State of Kerala', 'Maneka Gandhi v. Union of India'],
    'High Court of Delhi': ['State v. Navjot Sandhu', 'Naz Foundation v. Govt. of NCT of Delhi'],
  };

  const handleStartWorkflow = () => {
    advanceStep('upload');
    navigate('/upload');
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="bg-gradient-to-r from-primary/20 to-surface border border-primary/20 rounded-2xl p-8 relative overflow-hidden">
        <div className="absolute -right-20 -top-20 w-64 h-64 bg-primary/10 rounded-full blur-3xl"></div>
        <h1 className="text-4xl md:text-5xl font-bold text-white tracking-tight mb-4">
          AI-Powered Court Judgment Assistant
        </h1>
        <p className="text-lg text-slate-300 max-w-2xl mb-8 leading-relaxed">
          Streamline legal workflows with automated extraction, action plan generation, and intelligent multilingual verification.
        </p>
        <button 
          onClick={handleStartWorkflow}
          className="flex items-center gap-2 bg-primary hover:bg-blue-600 text-white px-6 py-3 rounded-xl font-medium shadow-lg shadow-primary/25 transition-all hover:-translate-y-1"
        >
          <Upload className="w-5 h-5" />
          Start New Case Workflow
        </button>
      </div>

      <div className="bg-surface border border-slate-700 rounded-2xl p-6 shadow-lg">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-slate-800 rounded-lg text-primary">
            <Search className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-semibold text-white">Smart Case Search</h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">Select Court</label>
            <select 
              className="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:border-transparent appearance-none"
              value={court}
              onChange={(e) => {
                setCourt(e.target.value);
                setCaseName('');
              }}
            >
              <option value="">Select a court...</option>
              {courts.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          
          <div className={`transition-opacity duration-300 ${!court ? 'opacity-50 pointer-events-none' : 'opacity-100'}`}>
            <label className="block text-sm font-medium text-slate-400 mb-2">Search Case</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
              <input 
                type="text"
                list="cases-list"
                className="w-full pl-10 pr-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
                placeholder="Type or select case name..."
                value={caseName}
                onChange={(e) => setCaseName(e.target.value)}
              />
              <datalist id="cases-list">
                {court && cases[court]?.map(c => <option key={c} value={c} />)}
              </datalist>
            </div>
          </div>
        </div>
        
        <div className="mt-6 flex justify-end">
          <button 
            disabled={!court || !caseName}
            className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-white px-6 py-2.5 rounded-xl font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed border border-slate-600"
          >
            Search <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
