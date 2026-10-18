import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Compass, Bot, Activity, Sparkles, ExternalLink, ShieldCheck } from 'lucide-react';

export default function Navbar({ systemStatus }) {
  const isMock = systemStatus?.llm?.provider === 'mock';
  const n8nConnected = systemStatus?.n8n?.connected;

  return (
    <header className="h-16 bg-white border-b border-slate-200 sticky top-0 z-30 px-6 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <Link to="/" className="flex items-center space-x-2.5 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-700 to-violet-600 flex items-center justify-center text-white shadow-md shadow-indigo-100 group-hover:scale-105 transition-transform duration-200">
            <Compass className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-1.5">
              <span className="font-bold text-lg text-slate-900 tracking-tight">Opportunity Hunter</span>
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200/60">
                AI Agent
              </span>
            </div>
            <p className="text-[11px] text-slate-500 font-medium leading-none">Automated Student Intelligence</p>
          </div>
        </Link>
      </div>

      <div className="flex items-center space-x-4">
        {/* System Diagnostics Badges */}
        <div className="hidden md:flex items-center space-x-2.5">
          {/* Agent Engine Badge */}
          <div className="flex items-center space-x-1.5 px-3 py-1 rounded-lg bg-slate-50 border border-slate-200 text-xs">
            <Bot className="w-3.5 h-3.5 text-indigo-600" />
            <span className="text-slate-600 font-medium">Agent:</span>
            <span className={`font-semibold ${isMock ? 'text-amber-700' : 'text-emerald-700'}`}>
              {isMock ? 'Mock Engine' : 'Browser Use Live'}
            </span>
          </div>

          {/* n8n Status Badge */}
          <div className="flex items-center space-x-1.5 px-3 py-1 rounded-lg bg-slate-50 border border-slate-200 text-xs">
            <Activity className={`w-3.5 h-3.5 ${n8nConnected ? 'text-emerald-500' : 'text-slate-400'}`} />
            <span className="text-slate-600 font-medium">n8n:</span>
            <span className={`font-semibold ${n8nConnected ? 'text-emerald-700' : 'text-slate-500'}`}>
              {n8nConnected ? 'Connected' : 'Standalone'}
            </span>
          </div>
        </div>

        {/* Quick Discover CTA */}
        <Link
          to="/discover"
          className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold shadow-sm shadow-indigo-200 transition-all hover:shadow hover:-translate-y-0.5"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Discover Now</span>
        </Link>
      </div>
    </header>
  );
}
