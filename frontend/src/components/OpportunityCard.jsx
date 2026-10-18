import React, { useState } from 'react';
import {
  Building2,
  MapPin,
  Calendar,
  ExternalLink,
  Bookmark,
  BookmarkCheck,
  CheckCircle2,
  Clock,
  Sparkles,
  ShieldCheck,
  ShieldAlert,
  Globe,
  Share2,
} from 'lucide-react';

const TYPE_STYLES = {
  internship: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' },
  hackathon: { bg: 'bg-purple-50', text: 'text-purple-700', border: 'border-purple-200' },
  research: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200' },
  job: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200' },
};

const STATUS_OPTIONS = [
  { value: 'new', label: 'New', color: 'text-slate-600' },
  { value: 'saved', label: 'Saved', color: 'text-indigo-600' },
  { value: 'interested', label: 'Interested', color: 'text-cyan-600' },
  { value: 'applied', label: 'Applied', color: 'text-emerald-600' },
  { value: 'rejected', label: 'Rejected', color: 'text-rose-600' },
];

export default function OpportunityCard({ opportunity, onStatusChange, onDelete }) {
  const [currentStatus, setCurrentStatus] = useState(opportunity.status);
  const [isUpdating, setIsUpdating] = useState(false);

  const typeStyle = TYPE_STYLES[opportunity.type] || TYPE_STYLES.internship;
  const isSaved = currentStatus === 'saved';

  const handleStatusSelect = async (newStatus) => {
    setIsUpdating(true);
    setCurrentStatus(newStatus);
    try {
      if (onStatusChange) {
        await onStatusChange(opportunity.id, newStatus);
      }
    } catch (err) {
      setCurrentStatus(opportunity.status);
    } finally {
      setIsUpdating(false);
    }
  };

  const toggleSave = () => {
    handleStatusSelect(isSaved ? 'new' : 'saved');
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return null;
    try {
      const d = new Date(dateStr);
      return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    } catch (e) {
      return dateStr;
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-xs hover:shadow-md transition-all duration-200 flex flex-col justify-between group">
      <div>
        {/* Top Header: Category, Remote, Verification & Bookmark */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <div className="flex items-center flex-wrap gap-1.5">
            <span
              className={`text-xs font-semibold px-2.5 py-0.5 rounded-full border capitalize ${typeStyle.bg} ${typeStyle.text} ${typeStyle.border}`}
            >
              {opportunity.type}
            </span>
            {opportunity.remote && (
              <span className="text-[11px] font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
                Remote Friendly
              </span>
            )}
            {opportunity.verification_status === 'verified' ? (
              <span className="inline-flex items-center text-[11px] font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200/60">
                <ShieldCheck className="w-3 h-3 mr-1" />
                Verified
              </span>
            ) : (
              <span className="inline-flex items-center text-[11px] font-medium px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200/60">
                <Sparkles className="w-3 h-3 mr-1" />
                Discovered
              </span>
            )}
          </div>

          <button
            onClick={toggleSave}
            title={isSaved ? 'Remove from Saved' : 'Save Opportunity'}
            className={`p-1.5 rounded-lg border transition-colors ${
              isSaved
                ? 'bg-indigo-50 border-indigo-200 text-indigo-600'
                : 'bg-slate-50 border-slate-200 text-slate-400 hover:text-slate-700'
            }`}
          >
            {isSaved ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
          </button>
        </div>

        {/* Title and Organization */}
        <h3 className="font-bold text-slate-900 text-base leading-snug group-hover:text-indigo-600 transition-colors">
          {opportunity.title}
        </h3>
        <div className="flex items-center space-x-2 text-xs font-semibold text-slate-600 mt-1 mb-3">
          <Building2 className="w-3.5 h-3.5 text-slate-400" />
          <span>{opportunity.organization}</span>
          <span className="text-slate-300">&bull;</span>
          <MapPin className="w-3.5 h-3.5 text-slate-400" />
          <span>{opportunity.location}</span>
        </div>

        {/* Description */}
        <p className="text-xs text-slate-600 line-clamp-3 leading-relaxed mb-4">
          {opportunity.description}
        </p>

        {/* Required Skills Badges */}
        {opportunity.required_skills && opportunity.required_skills.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-4">
            {opportunity.required_skills.map((skill, idx) => (
              <span
                key={idx}
                className="text-[11px] font-medium px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 border border-slate-200/50"
              >
                {skill}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Footer Info & Actions */}
      <div className="pt-3 border-t border-slate-100 space-y-3">
        {/* Deadline and Discovered Date */}
        <div className="flex items-center justify-between text-[11px] text-slate-500">
          <div className="flex items-center space-x-1">
            <Clock className="w-3.5 h-3.5 text-slate-400" />
            <span>
              {opportunity.deadline ? (
                <strong className="text-rose-700">Deadline: {formatDate(opportunity.deadline)}</strong>
              ) : (
                'Rolling / Not Specified'
              )}
            </span>
          </div>
          <div>Discovered {formatDate(opportunity.discovered_at)}</div>
        </div>

        {/* Status Dropdown and Apply Button */}
        <div className="flex items-center justify-between gap-2">
          {/* Status selector */}
          <div className="relative">
            <select
              value={currentStatus}
              disabled={isUpdating}
              onChange={(e) => handleStatusSelect(e.target.value)}
              className="text-xs font-semibold rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-1.5 text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer"
            >
              {STATUS_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  Status: {opt.label}
                </option>
              ))}
            </select>
          </div>

          {/* Action Links */}
          <div className="flex items-center space-x-1.5">
            <a
              href={opportunity.application_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold shadow-xs hover:shadow transition-all"
            >
              <span>Apply</span>
              <ExternalLink className="w-3 h-3 ml-0.5" />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
