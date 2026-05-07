import React from 'react';
import ExtractedDataCard from '../components/ExtractedDataCard';
import ActionPlanCard from '../components/ActionPlanCard';
import VerificationPanel from '../components/VerificationPanel';
import AudioSummary from '../audio/AudioSummary';

const ReviewPage = () => {
  const dummyCaseData = {
    caseNumber: 'C.A. No. 4567/2023',
    courtName: 'High Court of Delhi',
    parties: 'TechCorp India vs. Union of India',
  };

  const actionPlans = [
    { id: 1, required: 'File Counter-Affidavit', department: 'Legal Cell', deadline: '10 Nov 2023', priority: 'High', risk: 85 },
    { id: 2, required: 'Collect Evidence from IT Dept', department: 'IT Operations', deadline: '15 Nov 2023', priority: 'Medium', risk: 45 },
    { id: 3, required: 'Brief Senior Advocate', department: 'External Counsel', deadline: '20 Nov 2023', priority: 'High', risk: 90 },
  ];

  const audioText = `Case Number ${dummyCaseData.caseNumber}. Court: ${dummyCaseData.courtName}. Parties: ${dummyCaseData.parties}. You have ${actionPlans.length} action items. The highest priority item is to ${actionPlans[0].required} by ${actionPlans[0].deadline}.`;

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Review & Verify</h1>
          <p className="text-slate-400 mt-1">Review AI-extracted data and generated action plans before final approval.</p>
        </div>
        <AudioSummary text={audioText} title="Listen to Case Summary" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Data & Plans */}
        <div className="lg:col-span-2 space-y-6">
          <ExtractedDataCard data={dummyCaseData} />
          
          <div className="bg-surface border border-slate-700 rounded-2xl p-6 shadow-lg">
            <h3 className="text-xl font-bold text-white mb-6">Generated Action Plan</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {actionPlans.map(action => (
                <ActionPlanCard key={action.id} action={action} />
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Verification */}
        <div className="lg:col-span-1">
          <VerificationPanel />
        </div>
      </div>
    </div>
  );
};

export default ReviewPage;
