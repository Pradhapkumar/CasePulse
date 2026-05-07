import React from 'react';
import { QrCode, ScanLine } from 'lucide-react';
import { QRCodeSVG } from 'qrcode.react';

const QRScannerPage = () => {
  // Dummy data to encode in the QR code
  const caseData = {
    caseId: "SC-2023-892",
    actionPlan: "File Counter-Affidavit",
    deadline: "2023-11-10",
    language: "English"
  };
  
  const qrString = JSON.stringify(caseData);

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">QR Code Center</h1>
        <p className="text-slate-400">Scan physical documents to link to digital records, or share digital cases.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Scanner Placeholder */}
        <div className="bg-surface border border-slate-700 rounded-2xl p-8 flex flex-col items-center justify-center text-center shadow-lg min-h-[400px]">
          <div className="relative mb-6">
            <div className="absolute inset-0 border-2 border-primary/50 rounded-xl animate-pulse"></div>
            <div className="p-8 bg-slate-900 rounded-xl relative z-10 border border-slate-800">
              <ScanLine className="w-16 h-16 text-primary" />
            </div>
            {/* Scanning line animation */}
            <div className="absolute left-0 right-0 top-1/2 h-0.5 bg-primary shadow-[0_0_10px_#3b82f6] z-20 animate-[scan_2s_ease-in-out_infinite]"></div>
          </div>
          <h3 className="text-xl font-bold text-white mb-2">Camera Scanner Placeholder</h3>
          <p className="text-slate-400 max-w-xs">
            In a production environment, this would initialize the device camera to scan physical QR codes attached to case files.
          </p>
          <button className="mt-8 px-6 py-2.5 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-medium transition-colors border border-slate-600">
            Simulate Scan
          </button>
        </div>

        {/* Generator */}
        <div className="bg-surface border border-slate-700 rounded-2xl p-8 flex flex-col items-center justify-center text-center shadow-lg min-h-[400px]">
          <h3 className="text-xl font-bold text-white mb-6 w-full text-left flex items-center gap-2">
            <QrCode className="w-5 h-5 text-success" /> Generate Case QR
          </h3>
          
          <div className="p-6 bg-white rounded-2xl shadow-[0_0_20px_rgba(16,185,129,0.15)] mb-6">
            <QRCodeSVG 
              value={qrString}
              size={200}
              bgColor={"#ffffff"}
              fgColor={"#0f172a"}
              level={"M"}
            />
          </div>
          
          <div className="w-full text-left space-y-2 bg-slate-900 p-4 rounded-xl border border-slate-800 text-sm">
            <div className="flex justify-between">
              <span className="text-slate-400">Case ID:</span>
              <span className="text-white font-medium">{caseData.caseId}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Deadline:</span>
              <span className="text-white font-medium">{caseData.deadline}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QRScannerPage;
