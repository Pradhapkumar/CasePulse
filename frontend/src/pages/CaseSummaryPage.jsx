import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ShieldCheck, FileText, Calendar, Building2, User, Users, Clock, AlertCircle, ArrowLeft, LayoutDashboard, Search } from 'lucide-react';
import api from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import TranslatedText from '../components/common/TranslatedText';
import CopyIdButton from '../components/summary/CopyIdButton';
import QRCodeCard from '../components/summary/QRCodeCard';
import LegalSectionTable from '../components/summary/LegalSectionTable';

const CaseSummaryPage = () => {
  const { caseId } = useParams();
  const navigate = useNavigate();
  const { t } = useLanguage();
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const data = await api.generateCaseSummary(caseId);
        // Requirement: If frontend port is dynamic, use window.location.origin
        const publicUrl = `${window.location.origin}/public/case/${data.case_uid}`;
        setSummary({ ...data, dynamic_qr_url: publicUrl });
      } catch (err) {
        setError(err.response?.data?.detail || "Failed to generate case summary");
      } finally {
        setLoading(false);
      }
    };
    fetchSummary();
  }, [caseId]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <div className="w-12 h-12 border-4 border-primary/30 border-t-primary rounded-full animate-spin"></div>
        <p className="text-slate-400 font-medium">Generating official CasePulse summary...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-500/10 border border-red-500/20 p-8 rounded-3xl text-center max-w-2xl mx-auto my-12">
        <AlertCircle size={48} className="text-red-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-white mb-2">Generation Failed</h2>
        <p className="text-red-200/70 mb-6">{error}</p>
        <button 
          onClick={() => navigate('/dashboard')}
          className="bg-white text-slate-900 px-6 py-2 rounded-xl font-bold hover:bg-slate-100 transition-all"
        >
          Return to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {/* Header Actions */}
      <div className="flex flex-wrap justify-between items-center gap-4">
        <button 
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft size={20} />
          Back to Records
        </button>
        <div className="flex gap-3">
          <button 
            onClick={() => navigate('/search-case')}
            className="flex items-center gap-2 px-4 py-2 bg-slate-800 text-white rounded-xl border border-slate-700 hover:bg-slate-700 transition-all"
          >
            <Search size={18} /> Search Case
          </button>
          <button 
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-xl font-bold hover:bg-blue-600 transition-all shadow-lg shadow-primary/20"
          >
            <LayoutDashboard size={18} /> Dashboard
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Summary Details */}
        <div className="lg:col-span-2 space-y-8">
          {/* Main ID Card */}
          <div className="bg-gradient-to-r from-[#1e293b] to-[#0f172a] rounded-3xl p-8 border border-slate-700 relative overflow-hidden shadow-2xl">
            <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-3xl -mr-32 -mt-32"></div>
            
            <div className="flex justify-between items-start mb-8 relative z-10">
              <div className="space-y-1">
                <p className="text-slate-400 text-xs font-bold uppercase tracking-widest">CasePulse Unique ID</p>
                <h2 className="text-4xl font-black text-white tracking-tighter">{summary.case_uid}</h2>
              </div>
              <CopyIdButton text={summary.case_uid} />
            </div>

            <div className="space-y-2 relative z-10">
              <h1 className="text-2xl font-bold text-white leading-tight">
                {summary.case_title}
              </h1>
              <div className="flex flex-wrap gap-3">
                <span className="px-3 py-1 bg-primary/20 text-primary text-xs font-bold rounded-full border border-primary/30 uppercase tracking-wider">
                  <TranslatedText text={summary.case_type} />
                </span>
                <span className="px-3 py-1 bg-green-500/20 text-green-500 text-xs font-bold rounded-full border border-green-500/30 uppercase tracking-wider flex items-center gap-1.5">
                  <ShieldCheck size={14} /> {t("verified")}
                </span>
              </div>
            </div>
          </div>

          {/* Metadata Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <MetaCard icon={FileText} label={t("caseNumber")} value={summary.case_number} />
            <MetaCard icon={Building2} label={t("courtName")} value={<TranslatedText text={summary.court_name} />} />
            <MetaCard icon={Calendar} label={t("judgmentDate")} value={<TranslatedText text={summary.judgment_date} />} />
            <MetaCard icon={Clock} label={t("hearings")} value={<TranslatedText text={summary.hearings_count} />} />
            <MetaCard icon={User} label={t("petitioner")} value={<TranslatedText text={summary.petitioner} />} />
            <MetaCard icon={Users} label={t("respondent")} value={<TranslatedText text={summary.respondent} />} />
          </div>

          {/* Summary Text Card */}
          <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-sm">
            <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
              <div className="w-2 h-6 bg-primary rounded-full"></div>
              <TranslatedText text="Case Narrative Summary" />
            </h3>
            <p className="text-slate-600 leading-relaxed text-lg italic">
              "<TranslatedText text={summary.summary_text} />"
            </p>
          </div>

          {/* Legal Sections Analysis */}
          <div className="pt-8">
            <LegalSectionTable sections={summary.legal_sections} />
          </div>

          {/* Compliance & Action Plan */}
          <div className="bg-slate-900 border border-slate-700 rounded-3xl p-8 space-y-6">
            <h3 className="text-xl font-bold text-white flex items-center gap-3">
              <TranslatedText text="Action Plan Compliance" />
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="space-y-4">
                <InfoRow label={t("actionType") || "Action Type"} value={<TranslatedText text={summary.action_type} />} />
                <InfoRow label={t("department")} value={<TranslatedText text={summary.related_department} />} />
                <InfoRow label={t("deadline")} value={<TranslatedText text={summary.deadline} />} />
              </div>
              <div className="space-y-4">
                <InfoRow label={t("priority")} value={<TranslatedText text={summary.priority} />} color={summary.priority === 'High' ? 'text-red-500' : 'text-yellow-500'} />
                <InfoRow label="Risk Level" value={<TranslatedText text={summary.risk_level} />} color={summary.risk_level === 'High' ? 'text-red-500' : 'text-blue-500'} />
                <InfoRow label="AI Confidence" value={`${summary.confidence_score}%`} />
              </div>
            </div>
            <div className="pt-6 border-t border-slate-800">
              <p className="text-slate-400 text-xs font-bold uppercase mb-2 tracking-widest"><TranslatedText text="Required Action Details" /></p>
              <p className="text-slate-200"><TranslatedText text={summary.required_action} /></p>
            </div>
          </div>
        </div>

        {/* Right Column: QR & Public Link */}
        <div className="space-y-8">
          <QRCodeCard value={summary.dynamic_qr_url} caseUid={summary.case_uid} />
          
          <div className="bg-slate-800 border border-slate-700 rounded-3xl p-6 text-center">
            <p className="text-slate-400 text-sm mb-4">Official Public Link:</p>
            <a 
              href={summary.dynamic_qr_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="block bg-slate-900 p-4 rounded-xl text-primary text-xs font-mono break-all hover:bg-slate-950 transition-all border border-slate-700 mb-4"
            >
              {summary.dynamic_qr_url}
            </a>
            <button 
              onClick={() => window.open(summary.dynamic_qr_url, '_blank')}
              className="w-full py-3 bg-white text-slate-900 rounded-xl font-bold hover:bg-slate-100 transition-all"
            >
              Open Public View
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const MetaCard = ({ icon: Icon, label, value }) => (
  <div className="bg-white border border-slate-100 p-5 rounded-2xl flex items-center gap-4 shadow-sm">
    <div className="p-3 bg-slate-50 rounded-xl text-slate-400">
      <Icon size={24} />
    </div>
    <div>
      <p className="text-slate-400 text-xs font-bold uppercase tracking-wider">{label}</p>
      <p className="text-slate-900 font-bold">{value}</p>
    </div>
  </div>
);

const InfoRow = ({ label, value, color = "text-white" }) => (
  <div className="flex justify-between items-center py-2 border-b border-slate-800/50">
    <span className="text-slate-400 text-sm">{label}</span>
    <span className={`font-bold ${color}`}>{value}</span>
  </div>
);

export default CaseSummaryPage;
