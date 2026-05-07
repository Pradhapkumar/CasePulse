import React from 'react';
import { QRCodeCanvas } from "qrcode.react";
import { QrCode, Download } from 'lucide-react';

const QRCodeCard = ({ value, caseUid }) => {
  const downloadQR = () => {
    const canvas = document.getElementById("qr-canvas");
    const pngUrl = canvas
      .toDataURL("image/png")
      .replace("image/png", "image/octet-stream");
    let downloadLink = document.createElement("a");
    downloadLink.href = pngUrl;
    downloadLink.download = `CasePulse_QR_${caseUid}.png`;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  };

  return (
    <div className="bg-white border border-slate-200 rounded-3xl p-8 flex flex-col items-center text-center shadow-sm">
      <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center text-primary mb-6">
        <QrCode size={32} />
      </div>
      <h3 className="text-xl font-bold text-slate-900 mb-2">QR Authentication</h3>
      <p className="text-slate-500 text-sm mb-8 px-4">
        Scan this code to verify official judgment details on the public portal.
      </p>
      
      <div className="p-4 bg-white border-2 border-slate-50 rounded-2xl shadow-inner mb-6">
        <QRCodeCanvas 
          id="qr-canvas"
          value={value} 
          size={200} 
          level="H"
          includeMargin={true}
        />
      </div>

      <button 
        onClick={downloadQR}
        className="flex items-center gap-2 text-primary font-bold text-sm hover:underline"
      >
        <Download size={18} />
        Download Official QR
      </button>
    </div>
  );
};

export default QRCodeCard;
