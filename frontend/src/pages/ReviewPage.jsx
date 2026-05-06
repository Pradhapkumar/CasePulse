import React, { useState } from "react";
import ExtractedData from "../components/extraction/ExtractedData";
import ActionPlan from "../components/action/ActionPlan";
import VerificationPanel from "../components/verification/VerificationPanel";

export default function ReviewPage() {
  const [extractedData, setExtractedData] = useState(null);
  const [actionPlan, setActionPlan] = useState(null);

  return (
    <div className="review-page">
      <h1>Review Case Data</h1>
      <ExtractedData data={extractedData} />
      <ActionPlan plan={actionPlan} />
      <VerificationPanel data={extractedData} />
    </div>
  );
}
