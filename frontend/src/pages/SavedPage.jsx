import React, { useState, useEffect } from 'react';
import {
  BookmarkCheck,
  Briefcase,
  CheckCircle2,
  Clock,
  ExternalLink,
  Filter,
  Layers,
  Sparkles,
  Compass,
} from 'lucide-react';
import { api } from '../services/api';
import OpportunityCard from '../components/OpportunityCard';

const STAGE_FILTERS = [
  { id: 'all_tracked', label: 'All Tracked' },
  { id: 'saved', label: 'Saved' },
  { id: 'interested', label: 'Interested' },
  { id: 'applied', label: 'Applied' },
  { id: 'rejected', label: 'Archived / Rejected' },
];

export default function SavedPage({ onRefreshStats }) {
  const [opportunities, setOpportunities] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeStage, setActiveStage] = useState('all_tracked');

  const fetchTracked = async () => {
    try {
      setIsLoading(true);
      const params = {};
      if (activeStage !== 'all_tracked') {
        params.status = activeStage;
      }
      const data = await api.getOpportunities(params);
      // Filter client side if all_tracked to exclude 'new'
      const trackedOnly = (data || []).filter((opp) => {
        if (activeStage === 'all_tracked') {
          return opp.status !== 'new';
        }
        return opp.status === activeStage;
      });
      setOpportunities(trackedOnly);
    } catch (err) {
      console.error('Failed to load saved opportunities:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTracked();
  }, [activeStage]);

  const handleStatusChange = async (id, newStatus) => {
    await api.updateOpportunity(id, { status: newStatus });
    fetchTracked();
    if (onRefreshStats) onRefreshStats();
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Top Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900">Saved & Applications Tracker</h1>
        <p className="text-xs text-slate-500 mt-1">
          Manage your saved opportunities and advance through active application stages
        </p>
      </div>

      {/* Stage Selector Pills */}
      <div className="flex flex-wrap gap-2">
        {STAGE_FILTERS.map((stage) => (
          <button
            key={stage.id}
            onClick={() => setActiveStage(stage.id)}
            className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
              activeStage === stage.id
                ? 'bg-indigo-600 text-white shadow-xs'
                : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'
            }`}
          >
            {stage.label}
          </button>
        ))}
      </div>

      {/* Opportunities Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {[1, 2, 3].map((n) => (
            <div key={n} className="h-64 bg-slate-100 animate-pulse rounded-2xl" />
          ))}
        </div>
      ) : opportunities.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {opportunities.map((opp) => (
            <OpportunityCard
              key={opp.id}
              opportunity={opp}
              onStatusChange={handleStatusChange}
            />
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-3xl border border-slate-200/90 p-16 text-center">
          <BookmarkCheck className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-900">No tracked opportunities in this stage</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1 mb-6">
            Bookmark interesting listings from your search results to keep track of deadlines and status.
          </p>
        </div>
      )}
    </div>
  );
}
