import React, { useState } from "react";
import { useLanguage } from "../../context/LanguageContext";
import { t } from "../../language/translations";

export default function UploadPDF() {
  const { language } = useLanguage();
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    // Upload logic here
  };

  return (
    <div className="upload-pdf">
      <h2>{t(language, "uploadPDF")}</h2>
      <input
        id="pdf-file-input"
        type="file"
        accept=".pdf"
        onChange={handleFileChange}
        aria-label={t(language, "selectFile")}
      />
      <button id="upload-btn" onClick={handleUpload}>
        {t(language, "uploadBtn")}
      </button>
    </div>
  );
}
