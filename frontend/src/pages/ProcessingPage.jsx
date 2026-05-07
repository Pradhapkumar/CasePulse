import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useWorkflow } from '../context/WorkflowContext';
import { useLanguage } from '../context/LanguageContext';
import { FileUp, FileSearch, Sparkles, CheckCircle, Brain } from 'lucide-react';
import api from '../services/api';
import Loader from '../components/common/Loader';

const ProcessingPage = () => {
  const navigate = useNavigate();
  const { advanceStep } = useWorkflow();
  const { t } = useLanguage();
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  const steps = [
    { id: 'upload', title: t('pdfUploaded'), description: t('pdfUploaded'), icon: FileUp },
    { id: 'extract', title: t('extractingText'), description: t('parsingEntities'), icon: FileSearch },
    { id: 'plan', title: t('generatingActionPlan'), description: t('formulatingSteps'), icon: Sparkles },
    { id: 'ready', title: t('readyForReview'), description: t('allDataProcessed'), icon: CheckCircle },
  ];

  useEffect(() => {
    let isMounted = true;
    const processDocument = async () => {
      const caseId = localStorage.getItem('currentCaseId');
      if (!caseId) {
        console.error("No case ID found in storage.");
        return;
      }
      try {
        if (!isMounted) return;
        setCurrentStepIndex(1); // Extracting Data
        await api.extractCase(caseId);
        
        if (!isMounted) return;
        setCurrentStepIndex(2); // Generating Plan
        await api.generateActionPlan(caseId);
        
        if (!isMounted) return;
        setCurrentStepIndex(3); // Ready
        
        setTimeout(() => {
          if (!isMounted) return;
          advanceStep('review');
          navigate('/review');
        }, 1500);
      } catch (error) {
        console.error("Processing failed", error);
        alert("Failed during document processing.");
      }
    };
    processDocument();
    return () => { isMounted = false; };
  }, [navigate, advanceStep]);

  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        <div className="text-center mb-16 relative">
          <div className="absolute -top-12 left-1/2 transform -translate-x-1/2 opacity-20">
             <Loader size="lg" text="" />
          </div>
          <h1 className="text-4xl font-bold text-white mb-4 relative z-10">{t("processing")}</h1>
          <p className="text-slate-400 text-lg relative z-10">{t("tagline")}</p>
        </div>

        <div className="relative">
          {/* Vertical connecting line */}
          <div className="absolute left-[27px] top-4 bottom-4 w-1 bg-slate-800 rounded-full">
            <motion.div 
              className="w-full bg-gradient-to-b from-primary to-blue-400 rounded-full origin-top"
              initial={{ scaleY: 0 }}
              animate={{ scaleY: currentStepIndex / (steps.length - 1) }}
              transition={{ duration: 0.5, ease: "easeInOut" }}
            />
          </div>

          <div className="space-y-12">
            {steps.map((step, index) => {
              const isCompleted = index < currentStepIndex;
              const isActive = index === currentStepIndex;
              const isPending = index > currentStepIndex;

              return (
                <motion.div 
                  key={step.id} 
                  className="relative flex items-start gap-8"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.2 }}
                >
                  {/* Icon Circle */}
                  <div className="relative z-10 flex-shrink-0">
                    <motion.div
                      initial={{ scale: 0.8, opacity: 0.5 }}
                      animate={{ 
                        scale: isActive ? [1, 1.15, 1] : 1, 
                        opacity: isPending ? 0.3 : 1,
                        backgroundColor: isCompleted ? '#22c55e' : (isActive ? '#3b82f6' : '#1e293b'),
                        borderColor: isActive ? '#60a5fa' : (isCompleted ? '#4ade80' : 'transparent'),
                        rotate: isCompleted ? [0, 10, -10, 0] : 0
                      }}
                      transition={{ 
                        scale: { repeat: isActive ? Infinity : 0, duration: 2 },
                        rotate: { duration: 0.5 }
                      }}
                      className={`w-14 h-14 rounded-full flex items-center justify-center border-2 ${isActive ? 'shadow-[0_0_25px_rgba(59,130,246,0.5)]' : isCompleted ? 'shadow-[0_0_15px_rgba(34,197,94,0.3)]' : ''}`}
                    >
                      {isCompleted ? (
                        <CheckCircle className="w-7 h-7 text-white" />
                      ) : (
                        <step.icon className={`w-6 h-6 ${isActive ? 'text-white' : 'text-slate-500'}`} />
                      )}
                    </motion.div>

                    {/* Active pulse rings */}
                    {isActive && (
                      <>
                        <motion.div 
                          animate={{ scale: [1, 1.8], opacity: [0.5, 0] }}
                          transition={{ duration: 2, repeat: Infinity }}
                          className="absolute inset-0 rounded-full bg-primary/30 -z-10"
                        />
                        <motion.div 
                          animate={{ scale: [1, 2.2], opacity: [0.3, 0] }}
                          transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
                          className="absolute inset-0 rounded-full bg-primary/20 -z-10"
                        />
                      </>
                    )}
                  </div>

                  {/* Content Box */}
                  <motion.div 
                    className={`flex-1 p-6 rounded-2xl border transition-all duration-500 relative overflow-hidden ${
                      isActive 
                        ? 'bg-primary/10 border-primary/40 shadow-xl shadow-primary/5 translate-x-2' 
                        : isCompleted
                          ? 'bg-surface/80 border-success/30'
                          : 'bg-surface/30 border-slate-800 opacity-40'
                    }`}
                    animate={{ 
                      x: isActive ? 12 : 0,
                      scale: isActive ? 1.02 : 1
                    }}
                  >
                    {/* Scanning light effect for active step */}
                    {isActive && (
                      <motion.div 
                        className="absolute inset-0 bg-gradient-to-r from-transparent via-primary/20 to-transparent -translate-x-full"
                        animate={{ translateX: ['100%', '-100%'] }}
                        transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                      />
                    )}

                    <div className="relative z-10">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className={`text-xl font-bold ${isActive ? 'text-primary' : isCompleted ? 'text-success' : 'text-white'}`}>
                          {step.title}
                        </h3>
                        {isActive && (
                          <motion.span 
                            animate={{ opacity: [0, 1, 0] }}
                            transition={{ duration: 1.5, repeat: Infinity }}
                            className="text-[10px] bg-primary/20 text-primary px-2 py-0.5 rounded-full font-bold uppercase tracking-wider"
                          >
                            Live Processing
                          </motion.span>
                        )}
                      </div>
                      <p className="text-slate-400 text-sm leading-relaxed">{step.description}</p>
                      
                      {isActive && (
                        <div className="mt-5 space-y-2">
                          <div className="flex justify-between text-[10px] font-bold text-primary/70 uppercase">
                            <span>AI Engine Analysis</span>
                            <span>{Math.round(currentStepIndex * 25 + 25)}%</span>
                          </div>
                          <motion.div 
                            className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden"
                          >
                            <motion.div 
                              className="h-full bg-gradient-to-r from-primary to-blue-400 rounded-full"
                              initial={{ width: "0%" }}
                              animate={{ width: "100%" }}
                              transition={{ duration: 3, ease: "easeInOut" }}
                            />
                          </motion.div>
                        </div>
                      )}
                    </div>
                  </motion.div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProcessingPage;
