import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import DashboardPage from './pages/DashboardPage';
import DiscoverPage from './pages/DiscoverPage';
import ResultsPage from './pages/ResultsPage';
import SavedPage from './pages/SavedPage';
import SettingsPage from './pages/SettingsPage';
import { api } from './services/api';

export default function App() {
  const [stats, setStats] = useState({
    total_opportunities: 0,
    new_opportunities: 0,
    saved_opportunities: 0,
    applications_tracked: 0,
    applied_count: 0,
    last_research_run: null,
  });

  const [systemStatus, setSystemStatus] = useState({
    n8n: { connected: false, webhook_url: 'http://localhost:5678/webhook/opportunity-research' },
    llm: { provider: 'mock', configured: true, model: 'meta-llama/llama-3.3-70b-instruct' },
    browser_agent: { headless: true, available: true },
  });

  const [isLoading, setIsLoading] = useState(true);

  const refreshData = async () => {
    try {
      const [statsData, statusData] = await Promise.allSettled([
        api.getDashboardStats(),
        api.getWorkflowStatus(),
      ]);

      if (statsData.status === 'fulfilled' && statsData.value) {
        setStats(statsData.value);
      }
      if (statusData.status === 'fulfilled' && statusData.value) {
        setSystemStatus(statusData.value);
      }
    } catch (err) {
      console.error('Error refreshing system data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshData();
    // Poll stats occasionally
    const interval = setInterval(refreshData, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50 flex flex-col">
        <Navbar systemStatus={systemStatus} />
        <div className="flex flex-1">
          <Sidebar stats={stats} />
          <main className="flex-1 p-6 md:p-8 overflow-y-auto max-w-[1400px]">
            <Routes>
              <Route
                path="/"
                element={
                  <DashboardPage
                    stats={stats}
                    systemStatus={systemStatus}
                    onRefreshStats={refreshData}
                  />
                }
              />
              <Route
                path="/discover"
                element={
                  <DiscoverPage
                    systemStatus={systemStatus}
                    onResearchCompleted={refreshData}
                  />
                }
              />
              <Route
                path="/results"
                element={<ResultsPage onRefreshStats={refreshData} />}
              />
              <Route
                path="/saved"
                element={<SavedPage onRefreshStats={refreshData} />}
              />
              <Route
                path="/settings"
                element={
                  <SettingsPage
                    systemStatus={systemStatus}
                    onRefreshStatus={refreshData}
                  />
                }
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}
