import React from 'react';

export default function ExtractedData({ data }) {
  return (
    <div className="extracted-data">
      <h2>Extracted Data</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
