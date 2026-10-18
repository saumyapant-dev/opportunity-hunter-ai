import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Compass,
  Sparkles,
  BookmarkCheck,
  Briefcase,
  TrendingUp,
  Clock,
  ArrowRight,
  Bot,
  Activity,
  CheckCircle2,
  RefreshCw,
  Search,
} from 'lucide-react';
import { api } from '../services/api';
import OpportunityCard from '../components/OpportunityCard';

export default function DashboardPage({ stats, systemStatus, onRefreshStats }) {
  const [recentOpportunities, setRecentOpportunities] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchRecent = async () => {
    try {
      setIsLoading(true);
      const data = await api.getOpportunities({ limit: 6 });
      setRecentOpportunities(data || []);
    } catch (err) {
      console.error('Failed to load recent opportunities:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchRecent();
  }, []);

  const handleStatusChange = async (id, newStatus) => {
    await api.updateOpportunity(id, { status: newStatus });
    fetchRecent();
    if (onRefreshStats) onRefreshStats();
  };

  const lastRun = stats?.last_research_run;

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Welcome Banner */}
      <div className="rounded-3xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 p-8 text-white relative overflow-hidden shadow-xl shadow-slate-200">
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-indigo-500/20 via-transparent to-transparent pointer-events-none" />
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-400/30 text-indigo-300 text-xs font-semibold mb-4 backdrop-blur-xs">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Autonomous Career Intelligence</span>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            Welcome to Opportunity Hunter AI
          </h1>
          <p className="mt-3 text-sm text-slate-300 leading-relaxed font-normal">
            Automating web discovery of student internships, high-impact hackathons, undergraduate
            research fellowships, and entry-level positions using Browser Use Web AI and n8n orchestration.
          </p>
          <div className="mt-6 flex flex-wrap items-center gap-3">
            <Link
              to="/discover"
              className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition-all shadow-md shadow-indigo-600/30 hover:-translate-y-0.5"
            >
              <Search className="w-4 h-4" />
              <span>Launch New Research Run</span>
            </Link>
            <Link
              to="/results"
              className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-white/10 hover:bg-white/15 text-white text-xs font-bold transition-all border border-white/10"
            >
              <span>Explore All Opportunities</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>

      {/* Primary Analytics KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-xs flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Discovered</p>
            <h3 className="text-2xl font-bold text-slate-900 mt-1">{stats?.total_opportunities ?? 0}</h3>
            <p className="text-[11px] text-slate-400 mt-1">From verified opportunity sources</p>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600">
            <Compass className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-xs flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">New Opportunities</p>
            <h3 className="text-2xl font-bold text-indigo-600 mt-1">{stats?.new_opportunities ?? 0}</h3>
            <p className="text-[11px] text-slate-400 mt-1">Awaiting your initial review</p>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600">
            <Sparkles className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-xs flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Saved for Later</p>
            <h3 className="text-2xl font-bold text-slate-900 mt-1">{stats?.saved_opportunities ?? 0}</h3>
            <p className="text-[11px] text-slate-400 mt-1">Bookmarked opportunities</p>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-purple-50 border border-purple-100 flex items-center justify-center text-purple-600">
            <BookmarkCheck className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-xs flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Applications Tracked</p>
            <h3 className="text-2xl font-bold text-emerald-600 mt-1">{stats?.applications_tracked ?? 0}</h3>
            <p className="text-[11px] text-slate-400 mt-1">{stats?.applied_count ?? 0} submitted applications</p>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600">
            <Briefcase className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Execution Status & Agent Diagnostic Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Last Research Execution Card */}
        <div className="lg:col-span-2 bg-white rounded-2xl p-6 border border-slate-200/90 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-indigo-600" />
              <h2 className="text-sm font-bold text-slate-900">Last Research Execution</h2>
            </div>
            {lastRun && (
              <span
                className={`text-xs font-semibold px-2.5 py-0.5 rounded-full capitalize ${
                  lastRun.status === 'completed'
                    ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                    : lastRun.status === 'failed'
                    ? 'bg-rose-50 text-rose-700 border border-rose-200'
                    : 'bg-amber-50 text-amber-700 border border-amber-200'
                }`}
              >
                {lastRun.status}
              </span>
            )}
          </div>

          {lastRun ? (
            <div className="bg-slate-50 rounded-xl p-4 border border-slate-200/70 space-y-3 text-xs">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div>
                  <span className="text-slate-500">Run ID:</span>
                  <p className="font-mono text-slate-800 truncate font-medium">{lastRun.id.slice(0, 12)}...</p>
                </div>
                <div>
                  <span className="text-slate-500">Execution Mode:</span>
                  <p className="font-semibold text-slate-800 capitalize">{lastRun.mode} Mode</p>
                </div>
                <div>
                  <span className="text-slate-500">Listings Discovered:</span>
                  <p className="font-bold text-indigo-600">{lastRun.results_count}</p>
                </div>
                <div>
                  <span className="text-slate-500">Started At:</span>
                  <p className="text-slate-700">{new Date(lastRun.started_at).toLocaleTimeString()}</p>
                </div>
              </div>
              {lastRun.request_params && (
                <div className="pt-2 border-t border-slate-200/80 flex flex-wrap items-center gap-2">
                  <span className="text-slate-500 font-medium">Targeted Skills:</span>
                  {lastRun.request_params.skills?.map((s, i) => (
                    <span key={i} className="px-2 py-0.5 bg-white rounded border border-slate-200 font-medium">
                      {s}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-8 text-slate-500 text-xs">
              <p>No research executions logged yet. Launch your first search above!</p>
            </div>
          )}
        </div>

        {/* Pipeline & Agent Health Card */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <Activity className="w-4 h-4 text-indigo-600" />
              <h2 className="text-sm font-bold text-slate-900">System Integration Status</h2>
            </div>
            <div className="space-y-3 text-xs">
              <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-200/60">
                <span className="text-slate-600 font-medium">Browser Automation</span>
                <span className="inline-flex items-center font-semibold text-emerald-700">
                  <CheckCircle2 className="w-3.5 h-3.5 mr-1 text-emerald-600" />
                  Playwright Ready
                </span>
              </div>
              <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-200/60">
                <span className="text-slate-600 font-medium">LLM Provider</span>
                <span className="font-semibold text-slate-800 capitalize">
                  {systemStatus?.llm?.provider || 'Mock'} ({systemStatus?.llm?.configured ? 'Active' : 'Unconfigured'})
                </span>
              </div>
              <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-200/60">
                <span className="text-slate-600 font-medium">n8n Orchestrator</span>
                <span
                  className={`font-semibold ${
                    systemStatus?.n8n?.connected ? 'text-emerald-700' : 'text-slate-500'
                  }`}
                >
                  {systemStatus?.n8n?.connected ? 'Live Webhook Connected' : 'Standalone Runner'}
                </span>
              </div>
            </div>
          </div>
          <Link
            to="/settings"
            className="mt-4 text-xs font-semibold text-indigo-600 hover:text-indigo-700 flex items-center justify-between pt-3 border-t border-slate-100"
          >
            <span>Configure Integrations & Sources</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* Recent Discoveries Stream */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Recent Discoveries</h2>
            <p className="text-xs text-slate-500">Newly harvested listings across configured career portals</p>
          </div>
          <Link
            to="/results"
            className="text-xs font-semibold text-indigo-600 hover:text-indigo-700 flex items-center space-x-1"
          >
            <span>View All ({stats?.total_opportunities ?? 0})</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {[1, 2, 3].map((n) => (
              <div key={n} className="h-64 bg-slate-100 animate-pulse rounded-2xl" />
            ))}
          </div>
        ) : recentOpportunities.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {recentOpportunities.map((opp) => (
              <OpportunityCard
                key={opp.id}
                opportunity={opp}
                onStatusChange={handleStatusChange}
              />
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-2xl border border-slate-200/90 p-12 text-center">
            <Compass className="w-12 h-12 text-slate-300 mx-auto mb-3" />
            <h3 className="text-base font-bold text-slate-900">No opportunities discovered yet</h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1 mb-6">
              Launch your first automated research task to search opportunity boards for student roles.
            </p>
            <Link
              to="/discover"
              className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-indigo-600 text-white text-xs font-bold hover:bg-indigo-700 shadow-sm"
            >
              <Sparkles className="w-4 h-4" />
              <span>Discover Opportunities</span>
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
