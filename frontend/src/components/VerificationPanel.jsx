import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Check, Edit2, X, MessageSquare } from 'lucide-react';
import { useWorkflow } from '../context/WorkflowContext';
import { useLanguage } from '../context/LanguageContext';

const VerificationPanel = ({ onVerify }) => {
  const navigate = useNavigate();
  const { advanceStep } = useWorkflow();
  const { t } = useLanguage();
  const [notes, setNotes] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);

  const handleApprove = async () => {
    if (onVerify) {
      setIsVerifying(true);
      const success = await onVerify('approved', notes);
      setIsVerifying(false);
      if (success) {
        advanceStep('dashboard');
        navigate('/dashboard');
      }
    } else {
      advanceStep('dashboard');
      navigate('/dashboard');
    }
  };

  const handleReject = async () => {
    if (onVerify) {
      setIsVerifying(true);
      const success = await onVerify('rejected', notes);
      setIsVerifying(false);
      if (success) {
        advanceStep('dashboard');
        navigate('/dashboard');
      }
    }
  };

  return (
    <div className="bg-surface border border-slate-700 rounded-2xl p-6 shadow-lg sticky top-6">
      <h3 className="text-xl font-bold text-white mb-6">{t("humanVerification")}</h3>
      
      <div className="space-y-4 mb-6">
        <label className="block text-sm font-medium text-slate-400 flex items-center gap-2">
          <MessageSquare className="w-4 h-4" /> {t("reviewerNotes")}
        </label>
        <textarea
          rows={4}
          className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
          placeholder={t("addNotesPlaceholder")}
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-2 gap-3 mb-4">
        <button 
          onClick={() => setIsEditing(!isEditing)}
          className={`flex items-center justify-center gap-2 py-2.5 rounded-xl font-medium transition-colors border ${
            isEditing 
              ? 'bg-warning/20 text-warning border-warning/50' 
              : 'bg-slate-800 text-slate-300 hover:bg-slate-700 border-slate-600'
          }`}
        >
          <Edit2 className="w-4 h-4" />
          {isEditing ? 'Cancel Edit' : t("editFields")}
        </button>
        
        <button 
          onClick={handleReject}
          disabled={isVerifying}
          className="flex items-center justify-center gap-2 bg-danger/10 hover:bg-danger/20 text-danger border border-danger/30 py-2.5 rounded-xl font-medium transition-colors"
        >
          <X className="w-4 h-4" />
          {t("reject")}
        </button>
      </div>

      <button 
        onClick={handleApprove}
        disabled={isVerifying}
        className="w-full flex items-center justify-center gap-2 bg-success hover:bg-green-600 text-white py-3 rounded-xl font-bold shadow-lg shadow-success/20 transition-all"
      >
        <Check className="w-5 h-5" />
        {isVerifying ? t("processing") : t("approveFinalize")}
      </button>

      {isEditing && (
        <div className="absolute inset-0 bg-surface/95 backdrop-blur-sm rounded-2xl border border-warning flex flex-col p-6 z-10 animate-in fade-in zoom-in duration-200">
          <div className="flex justify-between items-center mb-4">
            <h4 className="text-white font-bold text-lg">Edit Mode Active</h4>
            <button onClick={() => setIsEditing(false)} className="text-slate-400 hover:text-white">
              <X className="w-5 h-5" />
            </button>
          </div>
          <p className="text-slate-300 text-sm mb-6">Click on any field in the Extracted Data or Action Plan to edit its contents before approving.</p>
          <div className="mt-auto">
            <button onClick={() => setIsEditing(false)} className="w-full bg-warning text-yellow-950 font-bold py-2.5 rounded-xl">
              Save Changes
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default VerificationPanel;
