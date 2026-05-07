import React, { createContext, useState, useContext } from 'react';

const WorkflowContext = createContext();

export const WorkflowProvider = ({ children }) => {
  const [currentStep, setCurrentStep] = useState('upload'); // upload, processing, review, dashboard
  const [caseData, setCaseData] = useState(null); // Will hold extracted data
  
  const advanceStep = (step, data = null) => {
    setCurrentStep(step);
    if (data) {
      setCaseData(prev => ({ ...prev, ...data }));
    }
  };

  const resetWorkflow = () => {
    setCurrentStep('upload');
    setCaseData(null);
  };

  return (
    <WorkflowContext.Provider value={{ currentStep, caseData, advanceStep, resetWorkflow }}>
      {children}
    </WorkflowContext.Provider>
  );
};

export const useWorkflow = () => useContext(WorkflowContext);
