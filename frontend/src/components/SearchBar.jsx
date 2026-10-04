import React from 'react';
import { Search, Sparkles } from 'lucide-react';

const DEMO_QUERIES = [
  { label: 'కంప్యూటర్ (Single)', query: 'కంప్యూటర్' },
  { label: 'కృత్రిమ మేధస్సు (Phrase)', query: 'కృత్రిమ మేధస్సు' },
  { label: 'కంప్యూటర్ AND భాష (AND)', query: 'కంప్యూటర్ AND భాష' },
  { label: 'కంప్యూటర్ OR భాష (OR)', query: 'కంప్యూటర్ OR భాష' },
  { label: 'తెలంగాణ (Location)', query: 'తెలంగాణ' },
  { label: 'గణితం (Science)', query: 'గణితం' },
];

const LANGUAGES = [
  { code: 'all', label: 'All Languages' },
  { code: 'te', label: 'Telugu (తెలుగు)' },
  { code: 'hi', label: 'Hindi (हिन्दी)' },
  { code: 'ta', label: 'Tamil (தமிழ்)' },
  { code: 'kn', label: 'Kannada (ಕನ್ನಡ)' },
  { code: 'ml', label: 'Malayalam (മലയാളം)' },
  { code: 'bn', label: 'Bengali (বাংলা)' },
  { code: 'mr', label: 'Marathi (मराठी)' },
  { code: 'gu', label: 'Gujarati (ગુજરાતી)' },
  { code: 'pa', label: 'Punjabi (ਪੰਜਾਬੀ)' },
];

export default function SearchBar({
  query,
  setQuery,
  language,
  setLanguage,
  onSearch,
  loading
}) {
  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch();
  };

  const handlePresetClick = (presetQuery) => {
    setQuery(presetQuery);
    onSearch(presetQuery);
  };

  return (
    <div className="search-bar-wrapper" style={{ width: '100%', marginBottom: '1.5rem' }}>
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '0.75rem', width: '100%' }}>
        <div style={{ position: 'relative', flex: 1, display: 'flex', alignItems: 'center' }}>
          <Search
            size={20}
            style={{ position: 'absolute', left: '1rem', color: '#94a3b8' }}
          />
          <input
            type="text"
            className="text-input"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search Indian-language Wikipedia (e.g. కంప్యూటర్, కంప్యూటర్ AND భాష)..."
            style={{
              width: '100%',
              paddingLeft: '2.8rem',
              paddingRight: '1rem',
              height: '50px',
              fontSize: '1rem',
              borderRadius: '10px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
            }}
          />
        </div>

        <select
          className="select-input"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          style={{ height: '50px', minWidth: '160px', borderRadius: '10px', fontWeight: 500 }}
        >
          {LANGUAGES.map((lang) => (
            <option key={lang.code} value={lang.code}>
              {lang.label}
            </option>
          ))}
        </select>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading}
          style={{ height: '50px', padding: '0 1.5rem', borderRadius: '10px', fontSize: '1rem' }}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      <div style={{ marginTop: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
        <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#64748b', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
          <Sparkles size={14} color="#eab308" /> Quick Demo Presets:
        </span>
        {DEMO_QUERIES.map((preset, idx) => (
          <button
            key={idx}
            type="button"
            className="btn btn-outline"
            onClick={() => handlePresetClick(preset.query)}
            style={{ padding: '0.25rem 0.65rem', fontSize: '0.78rem', borderRadius: '6px', backgroundColor: '#f1f5f9' }}
          >
            {preset.label}
          </button>
        ))}
      </div>
    </div>
  );
}
