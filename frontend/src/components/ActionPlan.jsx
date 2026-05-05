import React from "react";

export default function ActionPlan({ plan }) {
  return (
    <div className="action-plan">
      <h2>Action Plan</h2>
      {plan ? <div>{plan}</div> : <p>No action plan available</p>}
    </div>
  );
}
