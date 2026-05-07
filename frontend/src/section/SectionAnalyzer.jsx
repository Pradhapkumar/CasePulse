import React, { useState } from 'react';
import { Scale, Search, FileText, CheckCircle } from 'lucide-react';

const SectionAnalyzer = () => {
  const [section, setSection] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);

  const handleAnalyze = () => {
    if (!section) return;
    setIsAnalyzing(true);
    // Simulate AI analysis delay
    setTimeout(() => {
      setResult({
        meaning: "This section relates to the punishment for criminal breach of trust. It specifies the penalties applicable when an individual entrusted with property dishonestly misappropriates or converts it to their own use.",
        legalSteps: [
          "File an FIR at the local police station.",
          "Gather evidence of entrustment (receipts, agreements).",
          "Prove dishonest intention (mens rea) through correspondence or actions."
        ],
        actionRequired: "Collect all documentary evidence of the transaction and draft the initial complaint focusing on the specific entrustment clause."
      });
      setIsAnalyzing(false);
    }, 1500);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in duration-500">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Legal Section Analyzer</h1>
        <p className="text-slate-400">Instantly decode complex legal sections into plain language and actionable steps.</p>
      </div>

      <div className="bg-surface border border-slate-700 rounded-2xl p-6 shadow-lg">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1">
            <Scale className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
            <input 
              type="text" 
              placeholder="e.g., Section 406 IPC"
              value={section}
              onChange={(e) => setSection(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>
          <button 
            onClick={handleAnalyze}
            disabled={!section || isAnalyzing}
            className="flex items-center justify-center gap-2 bg-primary hover:bg-blue-600 disabled:bg-slate-800 disabled:text-slate-500 text-white px-8 py-3 rounded-xl font-medium transition-all min-w-[140px]"
          >
            {isAnalyzing ? (
              <span className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                Analyzing
              </span>
            ) : (
              <span className="flex items-center gap-2"><Search className="w-5 h-5"/> Analyze</span>
            )}
          </button>
        </div>
      </div>

      {result && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 animate-in slide-in-from-bottom-4">
          <div className="bg-surface border border-slate-700 rounded-2xl p-6 shadow-lg">
            <div className="flex items-center gap-3 mb-4 text-primary">
              <FileText className="w-6 h-6" />
              <h3 className="text-lg font-bold text-white">Meaning</h3>
            </div>
            <p className="text-slate-300 leading-relaxed text-sm">{result.meaning}</p>
          </div>

          <div className="bg-surface border border-slate-700 rounded-2xl p-6 shadow-lg">
            <div className="flex items-center gap-3 mb-4 text-warning">
              <Scale className="w-6 h-6" />
              <h3 className="text-lg font-bold text-white">Legal Steps</h3>
            </div>
            <ul className="space-y-3 text-sm">
              {result.legalSteps.map((step, i) => (
                <li key={i} className="flex gap-2 text-slate-300">
                  <span className="text-warning font-bold">{i+1}.</span> {step}
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-surface border border-slate-700 rounded-2xl p-6 shadow-lg border-t-4 border-t-success">
            <div className="flex items-center gap-3 mb-4 text-success">
              <CheckCircle className="w-6 h-6" />
              <h3 className="text-lg font-bold text-white">Action Required</h3>
            </div>
            <p className="text-slate-300 leading-relaxed text-sm">{result.actionRequired}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default SectionAnalyzer;
