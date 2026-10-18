import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Search,
  ListFilter,
  BookmarkCheck,
  Settings,
  Database,
  Workflow,
  Zap,
} from 'lucide-react';

export default function Sidebar({ stats }) {
  const navItems = [
    { to: '/', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/discover', label: 'Discover Opportunities', icon: Search, badge: 'Agent' },
    { to: '/results', label: 'Opportunity Results', icon: ListFilter, count: stats?.total_opportunities },
    { to: '/saved', label: 'Saved & Applications', icon: BookmarkCheck, count: stats?.saved_opportunities },
    { to: '/settings', label: 'Settings & Workflows', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-white border-r border-slate-200 flex flex-col justify-between shrink-0 min-h-[calc(100vh-4rem)]">
      <div className="p-4 space-y-1">
        <div className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
          Navigation
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-indigo-50 text-indigo-700 font-semibold shadow-xs'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`
              }
            >
              <div className="flex items-center space-x-3">
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-indigo-100 text-indigo-700">
                  {item.badge}
                </span>
              )}
              {item.count !== undefined && item.count > 0 && (
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                  {item.count}
                </span>
              )}
            </NavLink>
          );
        })}
      </div>

      {/* System Status Summary at bottom */}
      <div className="p-4 border-t border-slate-100 m-3 rounded-2xl bg-gradient-to-b from-slate-50 to-slate-100/80 border border-slate-200/80 text-xs">
        <div className="flex items-center space-x-2 text-slate-800 font-semibold mb-2">
          <Database className="w-3.5 h-3.5 text-indigo-600" />
          <span>Database Snapshot</span>
        </div>
        <div className="space-y-1.5 text-slate-500">
          <div className="flex justify-between items-center">
            <span>Discovered:</span>
            <span className="font-semibold text-slate-800">{stats?.total_opportunities ?? 0}</span>
          </div>
          <div className="flex justify-between items-center">
            <span>Tracked:</span>
            <span className="font-semibold text-indigo-600">{stats?.applications_tracked ?? 0}</span>
          </div>
          <div className="flex justify-between items-center">
            <span>Applied:</span>
            <span className="font-semibold text-emerald-600">{stats?.applied_count ?? 0}</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
