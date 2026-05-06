import React, { useState, useEffect } from "react";
import Dashboard from "../components/dashboard/Dashboard";

export default function DashboardPage() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    // Fetch dashboard stats
  }, []);

  return (
    <div className="dashboard-page">
      <h1>Dashboard</h1>
      <Dashboard stats={stats} />
    </div>
  );
}
