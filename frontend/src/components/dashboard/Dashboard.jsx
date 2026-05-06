import React from 'react';

export default function Dashboard({ stats }) {
  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      {stats && (
        <div className="stats">
          <p>Total Cases: {stats.totalCases}</p>
          <p>Processed: {stats.processed}</p>
          <p>Pending: {stats.pending}</p>
        </div>
      )}
    </div>
  );
}
