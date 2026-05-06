import React, { useState } from "react";

export default function VerificationPanel({ data, onVerify }) {
  const [verified, setVerified] = useState(false);

  const handleVerify = () => {
    setVerified(true);
    if (onVerify) onVerify(true);
  };

  return (
    <div className="verification-panel">
      <h2>Verification Panel</h2>
      <button onClick={handleVerify} disabled={verified}>
        {verified ? "Verified" : "Verify Data"}
      </button>
    </div>
  );
}
