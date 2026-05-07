import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileText, X, ArrowRight, CheckCircle, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useWorkflow } from '../context/WorkflowContext';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';
import Loader from '../components/common/Loader';

const UploadPage = () => {
  const navigate = useNavigate();
  const { advanceStep } = useWorkflow();
  const { t } = useLanguage();
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragging(true);
    } else if (e.type === 'dragleave') {
      setIsDragging(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = async (selectedFile) => {
    if (selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setIsUploading(true);
      setUploadProgress(10);
      
      try {
        // Mock progress for better UX
        const interval = setInterval(() => {
          setUploadProgress(prev => {
            if (prev >= 90) {
              clearInterval(interval);
              return 90;
            }
            return prev + 10;
          });
        }, 300);

        const response = await api.uploadPDF(selectedFile);
        clearInterval(interval);
        setUploadProgress(100);
        localStorage.setItem('currentCaseId', response.case_id);
        setTimeout(() => setIsUploading(false), 500);
      } catch (error) {
        setIsUploading(false);
        console.error("Upload failed", error);
        alert("Failed to upload PDF to server. Please ensure backend is running.");
        setFile(null);
        setUploadProgress(0);
      }
    } else {
      alert('Please upload a PDF file.');
    }
  };

  const proceedToProcessing = () => {
    advanceStep('processing', { fileName: file.name });
    navigate('/processing');
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">{t("uploadPDF")}</h1>
        <p className="text-slate-400">{t("tagline")}</p>
      </div>

      <div 
        className={`border-2 border-dashed rounded-3xl p-12 text-center transition-all duration-300 ${
          isDragging 
            ? 'border-primary bg-primary/10 shadow-[0_0_30px_rgba(59,130,246,0.15)]' 
            : 'border-slate-700 bg-surface hover:border-primary/50'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => !file && fileInputRef.current?.click()}
      >
        <input 
          ref={fileInputRef}
          type="file" 
          accept=".pdf" 
          onChange={handleChange} 
          className="hidden" 
        />
        
        {!file ? (
          <div className="flex flex-col items-center cursor-pointer">
            <div className="w-20 h-20 bg-slate-800 rounded-full flex items-center justify-center mb-6">
              <Upload className="w-10 h-10 text-primary" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">{t("uploadPDF")}</h3>
            <p className="text-slate-400 mb-6">{t("processing")}</p>
            <div className="px-6 py-2 bg-slate-800 text-slate-300 rounded-full text-sm font-medium border border-slate-700">
              Supports: PDF up to 50MB
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center w-full">
            <AnimatePresence mode="wait">
              {isUploading ? (
                <motion.div 
                  key="loader"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 1.1 }}
                  className="py-12"
                >
                  <Loader text={t("processing")} />
                </motion.div>
              ) : (
                <motion.div 
                  key="file-info"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="w-full max-w-md bg-slate-900 border border-slate-700 rounded-xl p-4 relative"
                >
                  <button 
                    onClick={(e) => { e.stopPropagation(); setFile(null); }}
                    className="absolute -top-3 -right-3 p-1.5 bg-danger text-white rounded-full hover:bg-red-600 shadow-lg"
                  >
                    <X className="w-4 h-4" />
                  </button>
                  
                  <div className="flex items-center gap-4 mb-4">
                    <div className="p-3 bg-primary/10 rounded-lg">
                      <FileText className="w-8 h-8 text-primary" />
                    </div>
                    <div className="flex-1 text-left overflow-hidden">
                      <p className="text-white font-medium truncate" title={file.name}>{file.name}</p>
                      <p className="text-slate-400 text-xs mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                    </div>
                    {uploadProgress === 100 && (
                      <CheckCircle className="w-6 h-6 text-success" />
                    )}
                  </div>
                  
                  <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden">
                    <div 
                      className="bg-gradient-to-r from-primary to-blue-400 h-2.5 rounded-full transition-all duration-300 ease-out"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                  <p className="text-right text-xs text-slate-400 mt-2 font-medium">{uploadProgress}% Uploaded</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}
      </div>

      <div className="flex justify-end">
        <button
          onClick={proceedToProcessing}
          disabled={!file || uploadProgress < 100}
          className="flex items-center gap-2 bg-primary hover:bg-blue-600 disabled:bg-slate-800 disabled:text-slate-500 text-white px-8 py-3 rounded-xl font-medium transition-all shadow-lg shadow-primary/20"
        >
          {t("processing")} <ArrowRight className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default UploadPage;
