import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useWorkflow } from '../context/WorkflowContext';
import { FileUp, FileSearch, Sparkles, CheckCircle } from 'lucide-react';

const ProcessingPage = () => {
  const navigate = useNavigate();
  const { advanceStep } = useWorkflow();
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  const steps = [
    { id: 'upload', title: 'PDF Uploaded', description: 'Document securely stored in our system.', icon: FileUp },
    { id: 'extract', title: 'Extracting Data', description: 'AI is parsing entities, dates, and core context.', icon: FileSearch },
    { id: 'plan', title: 'Generating Action Plan', description: 'Formulating legal steps and assigning departments.', icon: Sparkles },
    { id: 'ready', title: 'Ready for Review', description: 'All data processed and ready for human verification.', icon: CheckCircle },
  ];

  useEffect(() => {
    if (currentStepIndex < steps.length) {
      const timer = setTimeout(() => {
        setCurrentStepIndex(prev => prev + 1);
      }, 2500); // 2.5s per step
      return () => clearTimeout(timer);
    } else {
      // Auto-advance after a short delay when complete
      const timer = setTimeout(() => {
        advanceStep('review');
        navigate('/review');
      }, 1500);
      return () => clearTimeout(timer);
    }
  }, [currentStepIndex, navigate, advanceStep]);

  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-white mb-4">Processing Document</h1>
          <p className="text-slate-400 text-lg">Our AI is analyzing the judgment and extracting key insights.</p>
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
                <div key={step.id} className="relative flex items-start gap-8">
                  {/* Icon Circle */}
                  <div className="relative z-10 flex-shrink-0">
                    <motion.div
                      initial={{ scale: 0.8, opacity: 0.5 }}
                      animate={{ 
                        scale: isActive ? 1.2 : 1, 
                        opacity: isPending ? 0.4 : 1,
                        backgroundColor: isCompleted || isActive ? '#3b82f6' : '#1e293b',
                        borderColor: isActive ? '#60a5fa' : 'transparent'
                      }}
                      className={`w-14 h-14 rounded-full flex items-center justify-center border-2 ${isActive ? 'shadow-[0_0_20px_rgba(59,130,246,0.5)]' : ''}`}
                    >
                      <step.icon className={`w-6 h-6 ${isCompleted || isActive ? 'text-white' : 'text-slate-500'}`} />
                    </motion.div>
                  </div>

                  {/* Content Box */}
                  <motion.div 
                    className={`flex-1 p-6 rounded-2xl border transition-all duration-300 ${
                      isActive 
                        ? 'bg-primary/5 border-primary/30 transform translate-x-2' 
                        : isCompleted
                          ? 'bg-surface border-slate-700/50'
                          : 'bg-transparent border-transparent opacity-40'
                    }`}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: isPending ? 0.4 : 1, x: isActive ? 8 : 0 }}
                    transition={{ duration: 0.4 }}
                  >
                    <h3 className={`text-xl font-bold mb-2 ${isActive ? 'text-primary' : 'text-white'}`}>
                      {step.title}
                    </h3>
                    <p className="text-slate-400">{step.description}</p>
                    
                    {isActive && (
                      <motion.div 
                        className="mt-4 h-1.5 w-32 bg-slate-800 rounded-full overflow-hidden"
                      >
                        <motion.div 
                          className="h-full bg-primary rounded-full"
                          initial={{ width: "0%" }}
                          animate={{ width: "100%" }}
                          transition={{ duration: 2.5, ease: "linear" }}
                        />
                      </motion.div>
                    )}
                  </motion.div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProcessingPage;
