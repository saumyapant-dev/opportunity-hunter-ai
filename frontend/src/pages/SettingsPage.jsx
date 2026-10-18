import React, { useState, useEffect } from 'react';
import {
  Settings,
  Bell,
  Activity,
  Bot,
  Cpu,
  Key,
  Globe,
  Save,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  ExternalLink,
  ShieldCheck,
} from 'lucide-react';
import { api } from '../services/api';

export default function SettingsPage({ systemStatus, onRefreshStatus }) {
  const [preferences, setPreferences] = useState({
    skills: ['Python', 'React', 'JavaScript', 'SQL'],
    opportunity_types: ['internship', 'hackathon'],
    location: 'Remote',
    experience: 'Beginner',
    keywords: ['AI', 'Full Stack'],
    preferred_domains: ['news.ycombinator.com', 'devpost.com', 'github.com'],
    max_results: 10,
    email_notifications_enabled: false,
    notification_email: 'student@example.com',
    cron_schedule: '0 8 * * *',
    llm_provider: 'mock',
    llm_model: 'meta-llama/llama-3.3-70b-instruct',
  });

  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [isTestingN8n, setIsTestingN8n] = useState(false);
  const [n8nTestResult, setN8nTestResult] = useState(null);

  useEffect(() => {
    async function loadPrefs() {
      try {
        const data = await api.getPreferences();
        if (data) setPreferences(data);
      } catch (err) {
        console.error('Failed to load preferences:', err);
      }
    }
    loadPrefs();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    setSaveSuccess(false);
    try {
      await api.updatePreferences(preferences);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
      if (onRefreshStatus) onRefreshStatus();
    } catch (err) {
      alert(`Error saving preferences: ${err.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  const testN8nConnection = async () => {
    setIsTestingN8n(true);
    setN8nTestResult(null);
    try {
      const statusData = await api.getWorkflowStatus();
      setN8nTestResult(statusData?.n8n);
    } catch (err) {
      setN8nTestResult({ connected: false, message: err.message });
    } finally {
      setIsTestingN8n(false);
    }
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto pb-12">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2 text-indigo-600 font-semibold text-xs tracking-wider uppercase">
          <Settings className="w-4 h-4" />
          <span>System & Preferences</span>
        </div>
        <h1 className="text-2xl font-extrabold text-slate-900 mt-1">Platform Settings</h1>
        <p className="text-xs text-slate-500 mt-1">
          Manage automated research profiles, n8n orchestration endpoints, and LLM integrations.
        </p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* Card 1: Default Search Preferences */}
        <div className="bg-white rounded-3xl border border-slate-200/90 p-6 shadow-xs space-y-4">
          <div className="flex items-center space-x-2 pb-3 border-b border-slate-100">
            <Bot className="w-4 h-4 text-indigo-600" />
            <h2 className="text-sm font-bold text-slate-900">Default Discovery Profile</h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                Default Location
              </label>
              <input
                type="text"
                value={preferences.location}
                onChange={(e) => setPreferences({ ...preferences, location: e.target.value })}
                className="w-full text-xs px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                Default Experience Level
              </label>
              <select
                value={preferences.experience}
                onChange={(e) => setPreferences({ ...preferences, experience: e.target.value })}
                className="w-full text-xs font-semibold px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
              </select>
            </div>
          </div>
        </div>

        {/* Card 2: Email & Notification Settings */}
        <div className="bg-white rounded-3xl border border-slate-200/90 p-6 shadow-xs space-y-4">
          <div className="flex items-center space-x-2 pb-3 border-b border-slate-100">
            <Bell className="w-4 h-4 text-indigo-600" />
            <h2 className="text-sm font-bold text-slate-900">Notification & Schedule Preferences</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-3.5 rounded-2xl bg-slate-50 border border-slate-200/70">
              <div>
                <span className="text-xs font-bold text-slate-900 block">Daily Email Digest</span>
                <span className="text-[11px] text-slate-500">
                  Receive an automated email whenever new opportunities are discovered via scheduled n8n runs.
                </span>
              </div>
              <input
                type="checkbox"
                checked={preferences.email_notifications_enabled}
                onChange={(e) =>
                  setPreferences({ ...preferences, email_notifications_enabled: e.target.checked })
                }
                className="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500 cursor-pointer"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                  Recipient Email
                </label>
                <input
                  type="email"
                  value={preferences.notification_email}
                  onChange={(e) =>
                    setPreferences({ ...preferences, notification_email: e.target.value })
                  }
                  className="w-full text-xs px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
                  Schedule Cron Expression (Daily Trigger)
                </label>
                <input
                  type="text"
                  value={preferences.cron_schedule}
                  onChange={(e) =>
                    setPreferences({ ...preferences, cron_schedule: e.target.value })
                  }
                  placeholder="0 8 * * *"
                  className="w-full font-mono text-xs px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Card 3: System Diagnostics (n8n, Browser Use, LLM) */}
        <div className="bg-white rounded-3xl border border-slate-200/90 p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center space-x-2">
              <Activity className="w-4 h-4 text-indigo-600" />
              <h2 className="text-sm font-bold text-slate-900">Integration Health & Diagnostics</h2>
            </div>
            <button
              type="button"
              onClick={testN8nConnection}
              disabled={isTestingN8n}
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700 text-xs font-semibold"
            >
              <RefreshCw className={`w-3 h-3 ${isTestingN8n ? 'animate-spin' : ''}`} />
              <span>Ping Services</span>
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {/* LLM Status */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-800 flex items-center space-x-1.5">
                  <Cpu className="w-3.5 h-3.5 text-indigo-600" />
                  <span>LLM Engine</span>
                </span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                  Ready
                </span>
              </div>
              <p className="text-[11px] text-slate-500">
                Provider: <strong className="text-slate-800 capitalize">{systemStatus?.llm?.provider || 'mock'}</strong>
              </p>
              <p className="text-[11px] text-slate-500 truncate">
                Model: <span className="font-mono text-[10px] text-slate-700">{systemStatus?.llm?.model}</span>
              </p>
              <div className="pt-1 text-[10px] flex items-center space-x-1">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                <span className="text-slate-600">
                  {systemStatus?.llm?.has_openrouter_key || systemStatus?.llm?.has_openai_key
                    ? 'API Key Securely Loaded'
                    : 'Mock Mode Active (No Key Needed)'}
                </span>
              </div>
            </div>

            {/* Browser Use Status */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-800 flex items-center space-x-1.5">
                  <Bot className="w-3.5 h-3.5 text-indigo-600" />
                  <span>Browser Use</span>
                </span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                  Online
                </span>
              </div>
              <p className="text-[11px] text-slate-500">
                Engine: <strong className="text-slate-800">Playwright Chromium</strong>
              </p>
              <p className="text-[11px] text-slate-500">
                Headless Mode: <strong className="text-slate-800">{systemStatus?.browser_agent?.headless ? 'True' : 'False'}</strong>
              </p>
              <p className="text-[10px] text-slate-400 truncate">
                Config Dir: .browseruse
              </p>
            </div>

            {/* n8n Status */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-800 flex items-center space-x-1.5">
                  <Activity className="w-3.5 h-3.5 text-indigo-600" />
                  <span>n8n Webhook</span>
                </span>
                <span
                  className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                    systemStatus?.n8n?.connected
                      ? 'bg-emerald-100 text-emerald-800'
                      : 'bg-slate-200 text-slate-700'
                  }`}
                >
                  {systemStatus?.n8n?.connected ? 'Online' : 'Standalone'}
                </span>
              </div>
              <p className="text-[11px] text-slate-500 truncate">
                URL: <span className="font-mono text-[10px] text-slate-700">{systemStatus?.n8n?.webhook_url}</span>
              </p>
              <p className="text-[10px] text-slate-400">
                {systemStatus?.n8n?.connected
                  ? 'Ready to receive triggers'
                  : 'Start n8n via "npx n8n"'}
              </p>
            </div>
          </div>

          {n8nTestResult && (
            <div className={`p-3 rounded-xl border text-xs ${
              n8nTestResult.connected
                ? 'bg-emerald-50 border-emerald-200 text-emerald-800'
                : 'bg-slate-50 border-slate-200 text-slate-700'
            }`}>
              <strong>Ping Result:</strong> {n8nTestResult.message}
            </div>
          )}
        </div>

        {/* Save Bar */}
        <div className="flex items-center justify-end space-x-3">
          {saveSuccess && (
            <span className="text-xs font-semibold text-emerald-600 flex items-center space-x-1">
              <CheckCircle2 className="w-4 h-4" />
              <span>Preferences saved successfully!</span>
            </span>
          )}
          <button
            type="submit"
            disabled={isSaving}
            className="inline-flex items-center space-x-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs shadow-sm hover:shadow transition-all disabled:opacity-60"
          >
            <Save className="w-4 h-4" />
            <span>{isSaving ? 'Saving...' : 'Save All Preferences'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
