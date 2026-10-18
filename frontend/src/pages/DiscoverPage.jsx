import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Bot,
  Search,
  CheckCircle2,
  AlertCircle,
  Clock,
  Layers,
  MapPin,
  Briefcase,
  GraduationCap,
  Globe,
  Sliders,
  ExternalLink,
  Loader2,
  X,
  Plus,
  ArrowRight,
} from 'lucide-react';
import { api } from '../services/api';
import OpportunityCard from '../components/OpportunityCard';

const STANDARD_SKILLS = [
  'Python',
  'React',
  'JavaScript',
  'Java',
  'SQL',
  'Machine Learning',
  'Data Structures',
  'TypeScript',
  'FastAPI',
  'Node.js',
  'C++',
];

const OPPORTUNITY_TYPES = [
  { id: 'internship', label: 'Internship' },
  { id: 'hackathon', label: 'Hackathon' },
  { id: 'research', label: 'Research Fellowship' },
  { id: 'job', label: 'Entry-level Job' },
];

const LOCATIONS = ['Remote', 'India', 'United States', 'Worldwide', 'Custom City'];

const EXPERIENCE_LEVELS = ['Beginner', 'Intermediate', 'Advanced'];

const TARGET_DOMAINS = [
  'news.ycombinator.com/jobs',
  'devpost.com/hackathons',
  'github.com/explore',
  'internshala.com',
  'wellfound.com',
];

export default function DiscoverPage({ systemStatus, onResearchCompleted }) {
  // Search parameters state
  const [selectedSkills, setSelectedSkills] = useState(['Python', 'React']);
  const [customSkillInput, setCustomSkillInput] = useState('');
  const [selectedTypes, setSelectedTypes] = useState(['internship', 'hackathon']);
  const [location, setLocation] = useState('Remote');
  const [customCity, setCustomCity] = useState('');
  const [experience, setExperience] = useState('Beginner');
  const [keywords, setKeywords] = useState('AI, Full Stack');
  const [maxResults, setMaxResults] = useState(6);
  const [selectedDomains, setSelectedDomains] = useState(TARGET_DOMAINS);
  const [mode, setMode] = useState('mock'); // 'mock' or 'live'
  const [useN8n, setUseN8n] = useState(false);

  // Execution state
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [currentRun, setCurrentRun] = useState(null);
  const [executionStep, setExecutionStep] = useState(0); // 0: idle, 1: initiated, 2: searching/extracting, 3: deduplicating, 4: complete
  const [errorMessage, setErrorMessage] = useState(null);
  const [newlyDiscovered, setNewlyDiscovered] = useState([]);

  // Check initial mode based on system status
  useEffect(() => {
    if (systemStatus?.llm?.configured && systemStatus?.llm?.provider !== 'mock') {
      setMode('live');
    }
    if (systemStatus?.n8n?.connected) {
      setUseN8n(true);
    }
  }, [systemStatus]);

  const toggleSkill = (skill) => {
    setSelectedSkills((prev) =>
      prev.includes(skill) ? prev.filter((s) => s !== skill) : [...prev, skill]
    );
  };

  const addCustomSkill = (e) => {
    e?.preventDefault();
    const trimmed = customSkillInput.trim();
    if (trimmed && !selectedSkills.includes(trimmed)) {
      setSelectedSkills((prev) => [...prev, trimmed]);
      setCustomSkillInput('');
    }
  };

  const toggleType = (typeId) => {
    setSelectedTypes((prev) =>
      prev.includes(typeId)
        ? prev.length > 1
          ? prev.filter((t) => t !== typeId)
          : prev
        : [...prev, typeId]
    );
  };

  const toggleDomain = (domain) => {
    setSelectedDomains((prev) =>
      prev.includes(domain) ? prev.filter((d) => d !== domain) : [...prev, domain]
    );
  };

  // Launch research task
  const handleFindOpportunities = async (e) => {
    e.preventDefault();
    setErrorMessage(null);
    setNewlyDiscovered([]);

    // 1. Validation
    if (selectedSkills.length === 0) {
      setErrorMessage('Please select or specify at least one skill.');
      return;
    }
    if (selectedTypes.length === 0) {
      setErrorMessage('Please select at least one opportunity type.');
      return;
    }

    const effectiveLocation = location === 'Custom City' ? (customCity.trim() || 'Remote') : location;
    const keywordsList = keywords
      .split(',')
      .map((k) => k.trim())
      .filter(Boolean);

    const payload = {
      skills: selectedSkills,
      opportunity_types: selectedTypes,
      location: effectiveLocation,
      experience: experience,
      keywords: keywordsList,
      preferred_domains: selectedDomains,
      max_results: maxResults,
      mode: mode,
    };

    setIsSubmitting(true);
    setExecutionStep(1);

    try {
      // 2. Submit research request
      const triggerRes = await api.triggerResearch(payload, useN8n ? true : false);
      const runId = triggerRes.run_id;
      setCurrentRun({ id: runId, status: 'running', mode });

      setExecutionStep(2); // Browser Use navigating & extracting

      // 3. Poll for run status
      const pollInterval = setInterval(async () => {
        try {
          const runStatus = await api.getResearchRun(runId);
          setCurrentRun(runStatus);

          if (runStatus.status === 'running') {
            setExecutionStep(2);
          } else if (runStatus.status === 'completed') {
            clearInterval(pollInterval);
            setExecutionStep(4);
            setIsSubmitting(false);

            // Fetch newly discovered results
            const results = await api.getOpportunities({ limit: maxResults });
            setNewlyDiscovered(results || []);

            if (onResearchCompleted) {
              onResearchCompleted();
            }
          } else if (runStatus.status === 'failed') {
            clearInterval(pollInterval);
            setExecutionStep(0);
            setIsSubmitting(false);
            setErrorMessage(runStatus.error_message || 'Research run encountered an error.');
          }
        } catch (pollErr) {
          console.error('Error polling run:', pollErr);
        }
      }, 1200);
    } catch (err) {
      setIsSubmitting(false);
      setExecutionStep(0);
      setErrorMessage(err.message || 'Failed to submit research request.');
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Page Header */}
      <div>
        <div className="flex items-center space-x-2 text-indigo-600 font-semibold text-xs tracking-wider uppercase">
          <Bot className="w-4 h-4" />
          <span>Research Console</span>
        </div>
        <h1 className="text-2xl font-extrabold text-slate-900 mt-1">Discover Opportunities</h1>
        <p className="text-xs text-slate-500 mt-1">
          Configure your skills and preferences. The AI agent will navigate configured boards,
          extract structured listings, remove duplicates, and sync with your pipeline.
        </p>
      </div>

      {/* Main Search Configuration Card */}
      <form
        onSubmit={handleFindOpportunities}
        className="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-8 shadow-xs space-y-6"
      >
        {/* Skills Selection */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
            Target Skills & Stacks
          </label>
          <div className="flex flex-wrap gap-2 mb-3">
            {STANDARD_SKILLS.map((skill) => {
              const selected = selectedSkills.includes(skill);
              return (
                <button
                  type="button"
                  key={skill}
                  onClick={() => toggleSkill(skill)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                    selected
                      ? 'bg-indigo-600 text-white shadow-xs'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200/80'
                  }`}
                >
                  {skill}
                </button>
              );
            })}
          </div>

          {/* Custom Skills Tag Input */}
          <div className="flex items-center space-x-2">
            <input
              type="text"
              value={customSkillInput}
              onChange={(e) => setCustomSkillInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && addCustomSkill(e)}
              placeholder="Add other custom skill (e.g. Next.js, Rust)..."
              className="text-xs px-3.5 py-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full sm:w-80"
            />
            <button
              type="button"
              onClick={addCustomSkill}
              className="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold flex items-center space-x-1"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Add</span>
            </button>
          </div>
          {selectedSkills.length > 0 && (
            <div className="mt-2.5 flex flex-wrap gap-1.5 items-center">
              <span className="text-[11px] text-slate-500">Selected:</span>
              {selectedSkills.map((s) => (
                <span
                  key={s}
                  className="inline-flex items-center space-x-1 text-[11px] font-semibold bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-md border border-indigo-200/50"
                >
                  <span>{s}</span>
                  <X
                    className="w-3 h-3 cursor-pointer hover:text-indigo-900"
                    onClick={() => toggleSkill(s)}
                  />
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Opportunity Types */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
            Opportunity Types
          </label>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {OPPORTUNITY_TYPES.map((type) => {
              const selected = selectedTypes.includes(type.id);
              return (
                <button
                  type="button"
                  key={type.id}
                  onClick={() => toggleType(type.id)}
                  className={`p-3 rounded-2xl border text-left transition-all ${
                    selected
                      ? 'border-indigo-600 bg-indigo-50/60 text-indigo-950 font-bold shadow-xs'
                      : 'border-slate-200 hover:border-slate-300 text-slate-700 bg-white'
                  }`}
                >
                  <div className="text-xs font-bold">{type.label}</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">
                    {selected ? 'Included in search' : 'Click to include'}
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Location & Experience Level */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
              Location
            </label>
            <select
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="w-full text-xs font-semibold px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer"
            >
              {LOCATIONS.map((loc) => (
                <option key={loc} value={loc}>
                  {loc}
                </option>
              ))}
            </select>
            {location === 'Custom City' && (
              <input
                type="text"
                value={customCity}
                onChange={(e) => setCustomCity(e.target.value)}
                placeholder="Enter specific city name (e.g. Bangalore, London)..."
                className="mt-2 text-xs px-3.5 py-2 rounded-xl border border-slate-200 bg-white text-slate-800 w-full focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            )}
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
              Experience Level
            </label>
            <div className="grid grid-cols-3 gap-2">
              {EXPERIENCE_LEVELS.map((lvl) => (
                <button
                  type="button"
                  key={lvl}
                  onClick={() => setExperience(lvl)}
                  className={`py-2 text-xs font-semibold rounded-xl border text-center transition-all ${
                    experience === lvl
                      ? 'border-indigo-600 bg-indigo-600 text-white shadow-xs'
                      : 'border-slate-200 bg-slate-50 text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  {lvl}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Keywords & Max Results */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
              Domain Keywords (Comma Separated)
            </label>
            <input
              type="text"
              value={keywords}
              onChange={(e) => setKeywords(e.target.value)}
              placeholder="e.g. LLM, Autonomous Agents, Frontend, FinTech"
              className="w-full text-xs px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div>
            <div className="flex justify-between items-center mb-1.5">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-700">
                Max Opportunities to Harvest
              </label>
              <span className="text-xs font-bold text-indigo-600">{maxResults} listings</span>
            </div>
            <input
              type="range"
              min="2"
              max="20"
              value={maxResults}
              onChange={(e) => setMaxResults(Number(e.target.value))}
              className="w-full accent-indigo-600 cursor-pointer"
            />
          </div>
        </div>

        {/* Configurable Source Websites */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
            Target Research Sources
          </label>
          <div className="flex flex-wrap gap-2">
            {TARGET_DOMAINS.map((domain) => {
              const active = selectedDomains.includes(domain);
              return (
                <button
                  type="button"
                  key={domain}
                  onClick={() => toggleDomain(domain)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-medium border flex items-center space-x-1.5 transition-all ${
                    active
                      ? 'border-indigo-200 bg-indigo-50 text-indigo-800'
                      : 'border-slate-200 bg-white text-slate-400'
                  }`}
                >
                  <Globe className="w-3 h-3 text-indigo-500" />
                  <span>{domain}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Execution Mode & Orchestrator Toggles */}
        <div className="pt-4 border-t border-slate-100 grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* Mock vs Live */}
          <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
            <div>
              <span className="text-xs font-bold text-slate-900 block">Agent Execution Mode</span>
              <span className="text-[11px] text-slate-500">
                {mode === 'mock'
                  ? 'Fast Simulated Engine (Zero API cost)'
                  : 'Live Browser Use Agent (Playwright + LLM)'}
              </span>
            </div>
            <div className="flex rounded-xl p-1 bg-slate-200/70">
              <button
                type="button"
                onClick={() => setMode('mock')}
                className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition-all ${
                  mode === 'mock' ? 'bg-white text-indigo-700 shadow-xs' : 'text-slate-600'
                }`}
              >
                Mock
              </button>
              <button
                type="button"
                onClick={() => setMode('live')}
                className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition-all ${
                  mode === 'live' ? 'bg-white text-indigo-700 shadow-xs' : 'text-slate-600'
                }`}
              >
                Live AI
              </button>
            </div>
          </div>

          {/* Orchestrator choice */}
          <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
            <div>
              <span className="text-xs font-bold text-slate-900 block">Workflow Orchestration</span>
              <span className="text-[11px] text-slate-500">
                {useN8n ? 'Route through n8n Webhook' : 'Direct FastAPI Background Runner'}
              </span>
            </div>
            <button
              type="button"
              onClick={() => setUseN8n(!useN8n)}
              className={`text-xs font-semibold px-3 py-1.5 rounded-xl border transition-all ${
                useN8n
                  ? 'bg-emerald-50 border-emerald-300 text-emerald-800'
                  : 'bg-white border-slate-200 text-slate-600'
              }`}
            >
              {useN8n ? 'n8n Active' : 'Direct Runner'}
            </button>
          </div>
        </div>

        {/* Error notification banner */}
        {errorMessage && (
          <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />
            <span>{errorMessage}</span>
          </div>
        )}

        {/* Prominent Find Opportunities Submit Button */}
        <div>
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-4 rounded-2xl bg-gradient-to-r from-indigo-600 via-indigo-700 to-violet-700 hover:from-indigo-500 hover:to-violet-600 text-white font-bold text-sm shadow-md shadow-indigo-200 flex items-center justify-center space-x-2 transition-all hover:shadow-lg disabled:opacity-60 disabled:cursor-not-allowed hover:-translate-y-0.5"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-white" />
                <span>Running Opportunity Research Agent...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4 text-indigo-200" />
                <span>Find Opportunities Now</span>
              </>
            )}
          </button>
        </div>
      </form>

      {/* Live Execution Stepper (Shows during and after submission) */}
      {executionStep > 0 && (
        <div className="bg-white rounded-3xl border border-slate-200/90 p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Bot className="w-4 h-4 text-indigo-600" />
              <h3 className="text-sm font-bold text-slate-900">Agent Execution Stepper</h3>
            </div>
            {currentRun && (
              <span className="font-mono text-[11px] text-slate-500">
                Run ID: {currentRun.id.slice(0, 14)}...
              </span>
            )}
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs">
            {/* Step 1 */}
            <div
              className={`p-3 rounded-xl border flex items-center space-x-2.5 ${
                executionStep >= 1
                  ? 'border-indigo-200 bg-indigo-50/60 text-indigo-900'
                  : 'border-slate-100 bg-slate-50 text-slate-400'
              }`}
            >
              <CheckCircle2
                className={`w-4 h-4 ${executionStep >= 1 ? 'text-indigo-600' : 'text-slate-300'}`}
              />
              <span className="font-semibold">1. Request Validated</span>
            </div>

            {/* Step 2 */}
            <div
              className={`p-3 rounded-xl border flex items-center space-x-2.5 ${
                executionStep === 2
                  ? 'border-indigo-400 bg-indigo-50 text-indigo-900 animate-pulse'
                  : executionStep > 2
                  ? 'border-indigo-200 bg-indigo-50/60 text-indigo-900'
                  : 'border-slate-100 bg-slate-50 text-slate-400'
              }`}
            >
              {executionStep === 2 ? (
                <Loader2 className="w-4 h-4 animate-spin text-indigo-600" />
              ) : (
                <CheckCircle2
                  className={`w-4 h-4 ${executionStep > 2 ? 'text-indigo-600' : 'text-slate-300'}`}
                />
              )}
              <span className="font-semibold">2. Web Extraction</span>
            </div>

            {/* Step 3 */}
            <div
              className={`p-3 rounded-xl border flex items-center space-x-2.5 ${
                executionStep === 3
                  ? 'border-indigo-400 bg-indigo-50 text-indigo-900 animate-pulse'
                  : executionStep > 3
                  ? 'border-indigo-200 bg-indigo-50/60 text-indigo-900'
                  : 'border-slate-100 bg-slate-50 text-slate-400'
              }`}
            >
              <CheckCircle2
                className={`w-4 h-4 ${executionStep >= 4 ? 'text-indigo-600' : 'text-slate-300'}`}
              />
              <span className="font-semibold">3. Deduplication</span>
            </div>

            {/* Step 4 */}
            <div
              className={`p-3 rounded-xl border flex items-center space-x-2.5 ${
                executionStep >= 4
                  ? 'border-emerald-300 bg-emerald-50 text-emerald-900'
                  : 'border-slate-100 bg-slate-50 text-slate-400'
              }`}
            >
              <CheckCircle2
                className={`w-4 h-4 ${executionStep >= 4 ? 'text-emerald-600' : 'text-slate-300'}`}
              />
              <span className="font-semibold">4. Sync Complete</span>
            </div>
          </div>
        </div>
      )}

      {/* Discovered Opportunities Instant Results */}
      {newlyDiscovered.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                Discovered Opportunities ({newlyDiscovered.length})
              </h2>
              <p className="text-xs text-slate-500">
                Fresh listings discovered for your research run
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {newlyDiscovered.map((opp) => (
              <OpportunityCard
                key={opp.id}
                opportunity={opp}
                onStatusChange={async (id, newStatus) => {
                  await api.updateOpportunity(id, { status: newStatus });
                  if (onResearchCompleted) onResearchCompleted();
                }}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
