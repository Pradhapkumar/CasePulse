import React, { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck } from 'lucide-react';
import ExtractedDataCard from '../components/ExtractedDataCard';
import ActionPlanCard from '../components/ActionPlanCard';
import VerificationPanel from '../components/VerificationPanel';
import AudioReaderButton from '../components/common/AudioReaderButton';
import LegalSectionTable from '../components/summary/LegalSectionTable';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

const ReviewPage = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { t, translateDynamicText, selectedLanguage } = useLanguage();
  const caseId = localStorage.getItem('currentCaseId');
  const [translatedAudioText, setTranslatedAudioText] = useState("");

  useEffect(() => {
    console.log("ReviewPage mounted. caseId:", caseId);
    if (!caseId) {
      console.warn("No caseId found, redirecting to upload");
      navigate('/upload');
      return;
    }
    const fetchData = async () => {
      try {
        setLoading(true);
        console.log("Fetching review data for caseId:", caseId);
        const response = await api.getReview(caseId);
        console.log("Fetched data:", response);
        if (!response) {
          throw new Error("No data returned from API");
        }
        setData(response);
      } catch (err) {
        console.error("Error fetching review data:", err);
        setError(err.message || "Failed to load data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [caseId, navigate]);

  const handleVerify = async (status, notes) => {
    try {
      await api.verifyCase(caseId, {
        status,
        reviewer_name: "Legal Officer",
        reviewer_notes: notes
      });
      
      if (status === 'Verified' || status === 'approved') {
        // Automatically generate and navigate to summary for approved cases
        await api.generateCaseSummary(caseId);
        navigate(`/case-summary/${caseId}`);
      } else {
        // For other statuses, just refresh to show the button/status
        const response = await api.getReview(caseId);
        setData(response);
      }
      return true;
    } catch (err) {
      console.error("Verification failed", err);
      alert("Failed to verify. Ensure backend is running.");
      return false;
    }
  };

  // Memoize extracted data values with extreme safety
  const caseData = useMemo(() => {
    if (!data || !data.extracted_data) return {
      caseNumber: 'N/A',
      courtName: 'N/A',
      parties: 'N/A',
      keyDirections: 'No key directions extracted.',
      timeline: 'N/A'
    };
    
    const ext = data.extracted_data;
    return {
      caseNumber: ext.case_number || 'N/A',
      courtName: ext.court_name || 'N/A',
      parties: ext.parties_involved || 'N/A',
      keyDirections: ext.key_directions || 'No key directions extracted.',
      timeline: ext.timelines || 'N/A',
      caseType: ext.case_type || 'N/A',
      judgmentDate: ext.judgment_date || 'N/A',
      hearingsCount: ext.hearings_count || 'N/A',
      legalSections: ext.legal_sections || []
    };
  }, [data]);

  // Memoize action plans with safety
  const actionPlans = useMemo(() => {
    if (!data || !data.action_plan) return [];
    
    const ap = data.action_plan;
    // Check if ap is an object with an id, or if it's already an array (for future-proofing)
    if (Array.isArray(ap)) return ap;
    
    if (ap && ap.id) {
      return [{
        id: ap.id,
        required: ap.required_action || 'Review and Process',
        department: ap.responsible_department || 'Legal',
        deadline: ap.deadline || 'TBD',
        priority: ap.priority || 'Medium',
        risk: ap.risk_score || 0
      }];
    }
    return [];
  }, [data]);

  // Stable audio text calculation
  const audioText = useMemo(() => {
    const actionDesc = actionPlans.length > 0 
      ? `The required action is to ${actionPlans[0].required} by ${actionPlans[0].deadline}.` 
      : 'No specific action items identified.';
      
    return `Case Number ${caseData.caseNumber}. Court: ${caseData.courtName}. Parties: ${caseData.parties}. You have ${actionPlans.length} action items. ${actionDesc}`;
  }, [caseData, actionPlans]);

  useEffect(() => {
    const updateAudioText = async () => {
      if (!data) return;
      
      const apiCode = selectedLanguage?.apiCode || 'en';
      console.log("Updating audio text. Language:", apiCode);
      
      if (apiCode !== 'en') {
        try {
          const translated = await translateDynamicText(audioText);
          setTranslatedAudioText(translated);
        } catch (e) {
          console.error("Audio text translation failed", e);
          setTranslatedAudioText(audioText);
        }
      } else {
        setTranslatedAudioText(audioText);
      }
    };
    updateAudioText();
  }, [audioText, selectedLanguage?.apiCode, translateDynamicText, data]);

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
      <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      <p className="text-slate-400 animate-pulse">Loading review data...</p>
    </div>
  );

  if (error || !data) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center p-8 bg-surface border border-slate-700 rounded-3xl">
      <div className="w-16 h-16 bg-danger/10 text-danger rounded-full flex items-center justify-center mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
      <h2 className="text-2xl font-bold text-white mb-2">Failed to Load Review</h2>
      <p className="text-slate-400 max-w-md mb-6">{error || "The review data could not be retrieved. Please ensure the backend is running and you have processed a document."}</p>
      <button 
        onClick={() => navigate('/upload')}
        className="px-6 py-2 bg-primary text-white rounded-xl font-medium hover:bg-blue-600 transition-colors"
      >
        Return to Upload
      </button>
    </div>
  );

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">{t("review")}</h1>
          <p className="text-slate-400 mt-1">{t("tagline")}</p>
        </div>
        <AudioReaderButton text={translatedAudioText} label={t("playAudio")} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Data & Plans */}
        <div className="lg:col-span-2 space-y-6">
          <ExtractedDataCard data={caseData} />
          
          <div className="bg-slate-900/40 p-6 rounded-[32px] border border-slate-800 shadow-inner">
            <LegalSectionTable sections={caseData.legalSections} />
          </div>
          
          <div className="bg-surface border border-slate-700 rounded-2xl p-6 shadow-lg">
            <h3 className="text-xl font-bold text-white mb-6">{t("actionPlan")}</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {actionPlans.length > 0 ? (
                actionPlans.map(action => (
                  <ActionPlanCard key={action.id || Math.random()} action={action} />
                ))
              ) : (
                <div className="col-span-2 p-8 text-center border border-dashed border-slate-700 rounded-xl">
                  <p className="text-slate-500 italic">No action items detected in this judgment.</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Verification */}
        <div className="lg:col-span-1 space-y-6">
          <VerificationPanel onVerify={handleVerify} />
          
          {data?.action_plan?.verification_status === "Verified" && (
            <div className="bg-gradient-to-br from-primary/20 to-surface border border-primary/30 p-6 rounded-2xl shadow-2xl animate-in fade-in zoom-in duration-500 text-center">
              <div className="w-12 h-12 bg-primary text-white rounded-full flex items-center justify-center mx-auto mb-4">
                <ShieldCheck size={24} />
              </div>
              <h4 className="text-white font-bold mb-2">Record Verified</h4>
              <p className="text-slate-400 text-sm mb-6">Judgment has been successfully reviewed. You can now generate the official summary and unique CasePulse ID.</p>
              
              <button 
                onClick={() => navigate(`/case-summary/${caseId}`)}
                className="w-full flex items-center justify-center gap-2 bg-primary hover:bg-blue-600 text-white py-3 rounded-xl font-bold shadow-lg shadow-primary/20 transition-all hover:-translate-y-1 active:scale-95"
              >
                Generate Case Summary
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};


export default ReviewPage;
