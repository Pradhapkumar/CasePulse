import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Briefcase, Clock, CheckCircle2, AlertTriangle, Filter, Search } from 'lucide-react';
import api from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import TranslatedText from '../components/common/TranslatedText';
import { useNavigate } from 'react-router-dom';

const DashboardPage = () => {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const [filterPriority, setFilterPriority] = useState('All');
  const [summary, setSummary] = useState(null);
  const [actions, setActions] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const sum = await api.getDashboardSummary();
        const acts = await api.getDashboardActions();
        setSummary(sum);
        setActions(acts);
      } catch (err) {
        console.error("Dashboard error:", err);
      }
    };
    fetchData();
  }, []);

  const stats = [
    { title: t('totalCases'), value: summary ? summary.total_cases : '-', icon: Briefcase, color: 'text-blue-500', bg: 'bg-blue-500/10' },
    { title: t('pendingReview'), value: summary ? summary.pending_review : '-', icon: Clock, color: 'text-warning', bg: 'bg-warning/10' },
    { title: t('verified'), value: summary ? summary.verified_cases : '-', icon: CheckCircle2, color: 'text-success', bg: 'bg-success/10' },
    { title: t('highPriority'), value: summary ? summary.high_priority : '-', icon: AlertTriangle, color: 'text-danger', bg: 'bg-danger/10' },
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

  const recentCases = actions.map((act, i) => ({
    id: act.case_uid || act.case_id || `CP-${i}`,
    dept: act.department || 'N/A',
    deadline: act.deadline || 'TBD',
    status: act.status || 'Pending',
    priority: act.priority || 'Medium',
    original: act
  }));

  const filteredCases = filterPriority === 'All' 
    ? recentCases 
    : recentCases.filter(c => c.priority === filterPriority);

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-6">
        <div className="flex items-center gap-4">
          <h1 className="text-3xl font-bold text-white tracking-tight">{t("dashboard")}</h1>
          <button 
            onClick={() => navigate('/upload')}
            className="flex items-center gap-2 px-5 py-2 bg-primary text-white rounded-xl font-bold shadow-lg shadow-primary/20 hover:bg-blue-600 transition-all hover:-translate-y-0.5 active:scale-95"
          >
            <Briefcase size={18} />
            Upload Document
          </button>
        </div>
        
        <div className="flex flex-1 max-w-md w-full gap-2">
          <div className="relative flex-1">
            <input 
              type="text" 
              placeholder="Search CasePulse ID..." 
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-white focus:ring-2 focus:ring-primary outline-none"
              onKeyDown={(e) => {
                if (e.key === 'Enter') navigate('/search-case');
              }}
            />
            <Search className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
          </div>
          <button 
            onClick={() => navigate('/search-case')}
            className="px-4 py-2 bg-slate-800 text-white rounded-xl border border-slate-700 hover:bg-slate-700 transition-colors"
          >
            <Filter className="w-4 h-4" />
          </button>
        </div>
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

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div 
          onClick={() => navigate('/upload')}
          className="bg-gradient-to-br from-primary/20 to-surface border border-primary/30 p-8 rounded-[32px] flex items-center gap-6 cursor-pointer hover:scale-[1.02] transition-all shadow-xl group"
        >
          <div className="w-16 h-16 bg-primary text-white rounded-2xl flex items-center justify-center shadow-lg group-hover:rotate-12 transition-transform">
            <Briefcase size={32} />
          </div>
          <div>
            <h3 className="text-2xl font-bold text-white">Upload Judgment</h3>
            <p className="text-slate-400">Process new court order for action plan</p>
          </div>
        </div>

        <div 
          onClick={() => navigate('/search-case')}
          className="bg-gradient-to-br from-green-500/20 to-surface border border-green-500/30 p-8 rounded-[32px] flex items-center gap-6 cursor-pointer hover:scale-[1.02] transition-all shadow-xl group"
        >
          <div className="w-16 h-16 bg-green-500 text-white rounded-2xl flex items-center justify-center shadow-lg group-hover:-rotate-12 transition-transform">
            <Search size={32} />
          </div>
          <div>
            <h3 className="text-2xl font-bold text-white">Scan or Search Case</h3>
            <p className="text-slate-400">Verify case details via unique ID or QR</p>
          </div>
        </div>
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
                  <span className="text-slate-300">
                    <TranslatedText text={entry.name} />
                  </span>
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
          <h3 className="text-lg font-semibold text-white">{t("verifiedActions")}</h3>
          <select 
            value={filterPriority}
            onChange={(e) => setFilterPriority(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-white text-sm rounded-lg px-3 py-1.5 focus:ring-primary"
          >
            <option value="All">{t("totalCases")}</option>
            <option value="High">{t("highPriority")}</option>
            <option value="Medium">Medium Priority</option>
            <option value="Low">Low Priority</option>
          </select>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-800/50 text-slate-400">
              <tr>
                <th className="px-6 py-4 font-medium">CasePulse ID</th>
                <th className="px-6 py-4 font-medium">{t("department")}</th>
                <th className="px-6 py-4 font-medium">{t("deadline")}</th>
                <th className="px-6 py-4 font-medium">{t("priority")}</th>
                <th className="px-6 py-4 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/50">
              {filteredCases.length === 0 ? (
                <tr>
                  <td colSpan="5" className="px-6 py-8 text-center text-slate-400">
                    No verified cases found. Approve some action plans in the review stage!
                  </td>
                </tr>
              ) : (
                filteredCases.map((caseItem, index) => (
                  <tr key={caseItem.id || index} className="hover:bg-slate-800/50 transition-colors">
                    <td className="px-6 py-4 font-bold text-primary">{caseItem.id}</td>
                    <td className="px-6 py-4 text-slate-300">
                      <TranslatedText text={caseItem.dept} />
                    </td>
                    <td className="px-6 py-4">
                      <span className={`flex items-center gap-1.5 ${caseItem.deadline === 'Today' || caseItem.deadline === 'Tomorrow' ? 'text-danger font-medium' : 'text-slate-300'}`}>
                        <Clock className="w-3.5 h-3.5" /> <TranslatedText text={caseItem.deadline} />
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs font-semibold rounded-md border ${
                        caseItem.priority === 'High' ? 'text-danger border-danger/30 bg-danger/10' :
                        caseItem.priority === 'Medium' ? 'text-warning border-warning/30 bg-warning/10' :
                        'text-success border-success/30 bg-success/10'
                      }`}>
                        {t(caseItem.priority.toLowerCase()) || caseItem.priority}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <button 
                        onClick={() => navigate(`/case-summary/${caseItem.original.case_id}`)}
                        className="text-xs font-bold text-white bg-slate-700 hover:bg-slate-600 px-3 py-1.5 rounded-lg transition-all"
                      >
                        View Summary
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
