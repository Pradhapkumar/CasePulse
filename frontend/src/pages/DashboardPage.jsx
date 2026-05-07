import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Briefcase, Clock, CheckCircle2, AlertTriangle, Filter } from 'lucide-react';

const DashboardPage = () => {
  const [filterPriority, setFilterPriority] = useState('All');

  const stats = [
    { title: 'Total Cases', value: '1,248', icon: Briefcase, color: 'text-blue-500', bg: 'bg-blue-500/10' },
    { title: 'Pending Review', value: '45', icon: Clock, color: 'text-warning', bg: 'bg-warning/10' },
    { title: 'Verified Today', value: '12', icon: CheckCircle2, color: 'text-success', bg: 'bg-success/10' },
    { title: 'High Priority', value: '8', icon: AlertTriangle, color: 'text-danger', bg: 'bg-danger/10' },
  ];

  const barData = [
    { name: 'Mon', cases: 12 },
    { name: 'Tue', cases: 19 },
    { name: 'Wed', cases: 15 },
    { name: 'Thu', cases: 22 },
    { name: 'Fri', cases: 30 },
    { name: 'Sat', cases: 5 },
    { name: 'Sun', cases: 2 },
  ];

  const pieData = [
    { name: 'Supreme Court', value: 400 },
    { name: 'High Court', value: 300 },
    { name: 'District Court', value: 300 },
  ];
  const COLORS = ['#3b82f6', '#8b5cf6', '#10b981'];

  const recentCases = [
    { id: 'SC-2023-892', dept: 'Legal Cell', deadline: 'Tomorrow', status: 'Pending', priority: 'High' },
    { id: 'HC-2023-104', dept: 'IT Ops', deadline: '15 Nov 2023', status: 'Verified', priority: 'Medium' },
    { id: 'DC-2023-551', dept: 'HR', deadline: '20 Nov 2023', status: 'In Progress', priority: 'Low' },
    { id: 'SC-2023-901', dept: 'Finance', deadline: 'Today', status: 'Action Required', priority: 'High' },
  ];

  const filteredCases = filterPriority === 'All' 
    ? recentCases 
    : recentCases.filter(c => c.priority === filterPriority);

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-white tracking-tight">Dashboard Overview</h1>
        <button className="flex items-center gap-2 px-4 py-2 bg-slate-800 text-white rounded-lg border border-slate-700 hover:bg-slate-700">
          <Filter className="w-4 h-4" /> Filter
        </button>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, i) => (
          <div key={i} className="bg-surface border border-slate-700 p-6 rounded-2xl shadow-sm flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm font-medium mb-1">{stat.title}</p>
              <h3 className="text-3xl font-bold text-white">{stat.value}</h3>
            </div>
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${stat.bg}`}>
              <stat.icon className={`w-6 h-6 ${stat.color}`} />
            </div>
          </div>
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-surface border border-slate-700 p-6 rounded-2xl shadow-sm">
          <h3 className="text-lg font-semibold text-white mb-6">Cases Processed (This Week)</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                <XAxis dataKey="name" stroke="#94a3b8" axisLine={false} tickLine={false} />
                <YAxis stroke="#94a3b8" axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#f8fafc' }} />
                <Bar dataKey="cases" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-surface border border-slate-700 p-6 rounded-2xl shadow-sm">
          <h3 className="text-lg font-semibold text-white mb-6">Distribution by Court</h3>
          <div className="h-64 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#f8fafc' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex flex-col gap-2 mt-4">
            {pieData.map((entry, index) => (
              <div key={entry.name} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[index] }}></div>
                  <span className="text-slate-300">{entry.name}</span>
                </div>
                <span className="text-white font-medium">{entry.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="bg-surface border border-slate-700 rounded-2xl shadow-sm overflow-hidden">
        <div className="p-6 border-b border-slate-700 flex justify-between items-center">
          <h3 className="text-lg font-semibold text-white">Actionable Cases</h3>
          <select 
            value={filterPriority}
            onChange={(e) => setFilterPriority(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-white text-sm rounded-lg px-3 py-1.5 focus:ring-primary"
          >
            <option value="All">All Priorities</option>
            <option value="High">High Priority</option>
            <option value="Medium">Medium Priority</option>
            <option value="Low">Low Priority</option>
          </select>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-800/50 text-slate-400">
              <tr>
                <th className="px-6 py-4 font-medium">Case ID</th>
                <th className="px-6 py-4 font-medium">Department</th>
                <th className="px-6 py-4 font-medium">Deadline</th>
                <th className="px-6 py-4 font-medium">Priority</th>
                <th className="px-6 py-4 font-medium">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/50">
              {filteredCases.map((caseItem) => (
                <tr key={caseItem.id} className="hover:bg-slate-800/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-white">{caseItem.id}</td>
                  <td className="px-6 py-4 text-slate-300">{caseItem.dept}</td>
                  <td className="px-6 py-4">
                    <span className={`flex items-center gap-1.5 ${caseItem.deadline === 'Today' || caseItem.deadline === 'Tomorrow' ? 'text-danger font-medium' : 'text-slate-300'}`}>
                      <Clock className="w-3.5 h-3.5" /> {caseItem.deadline}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-md border ${
                      caseItem.priority === 'High' ? 'text-danger border-danger/30 bg-danger/10' :
                      caseItem.priority === 'Medium' ? 'text-warning border-warning/30 bg-warning/10' :
                      'text-success border-success/30 bg-success/10'
                    }`}>
                      {caseItem.priority}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-slate-300">{caseItem.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
