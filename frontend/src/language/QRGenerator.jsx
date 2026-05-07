import React from "react";
import { QRCodeSVG } from "qrcode.react";
import { useLanguage } from "../context/LanguageContext";
import { t } from "../language/translations";

/**
 * QRGenerator — renders a QR code from any JSON-serialisable data.
 *
 * Props:
 *   data  {any}    - Data to encode (objects are JSON-stringified)
 *   size  {number} - Side length in px (default 200)
 */
const QRGenerator = ({ data, size = 200 }) => {
  const { language } = useLanguage();
  const value = typeof data === "string" ? data : JSON.stringify(data);

  return (
    <div className="qr-generator">
      <p className="qr-label">{t(language, "generateQR")}</p>
      <div className="qr-code-wrapper">
        <QRCodeSVG
          value={value}
          size={size}
          bgColor="#ffffff"
          fgColor="#1e293b"
          level="H"
          includeMargin={true}
        />
      </div>
    </div>
  );
};

export default QRGenerator;
