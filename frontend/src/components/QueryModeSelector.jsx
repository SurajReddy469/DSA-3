import React from 'react';
import { Filter, Cpu } from 'lucide-react';

export default function QueryModeSelector({
  mode,
  setMode,
  useNaive,
  setUseNaive,
  resultsPerPage,
  setResultsPerPage,
  onOptionChange
}) {
  const handleModeChange = (e) => {
    const val = e.target.value;
    setMode(val);
    if (onOptionChange) onOptionChange({ mode: val });
  };

  const handleNaiveChange = (e) => {
    const val = e.target.checked;
    setUseNaive(val);
    if (onOptionChange) onOptionChange({ use_naive: val });
  };

  const handleLimitChange = (e) => {
    const val = parseInt(e.target.value, 10);
    setResultsPerPage(val);
    if (onOptionChange) onOptionChange({ limit: val });
  };

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '1.25rem',
        flexWrap: 'wrap',
        backgroundColor: '#ffffff',
        padding: '0.65rem 1rem',
        borderRadius: '8px',
        border: '1px solid #e2e8f0',
        marginBottom: '1rem'
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
        <label style={{ fontSize: '0.85rem', fontWeight: 600, color: '#475569', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
          <Filter size={15} /> Search Mode:
        </label>
        <select
          className="select-input"
          value={mode}
          onChange={handleModeChange}
          style={{ padding: '0.35rem 0.65rem', fontSize: '0.85rem' }}
        >
          <option value="AND">AND (All Terms)</option>
          <option value="OR">OR (Any Term)</option>
        </select>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
        <label style={{ fontSize: '0.85rem', fontWeight: 600, color: '#475569' }}>
          Results / Page:
        </label>
        <select
          className="select-input"
          value={resultsPerPage}
          onChange={handleLimitChange}
          style={{ padding: '0.35rem 0.65rem', fontSize: '0.85rem' }}
        >
          <option value={10}>10</option>
          <option value={20}>20</option>
          <option value={50}>50</option>
        </select>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginLeft: 'auto' }}>
        <label
          style={{
            fontSize: '0.85rem',
            fontWeight: 600,
            color: useNaive ? '#b91c1c' : '#475569',
            display: 'flex',
            alignItems: 'center',
            gap: '0.35rem',
            cursor: 'pointer'
          }}
        >
          <input
            type="checkbox"
            checked={useNaive}
            onChange={handleNaiveChange}
            style={{ width: '15px', height: '15px', cursor: 'pointer' }}
          />
          <Cpu size={15} color={useNaive ? '#dc2626' : '#64748b'} />
          Benchmark Mode (Naive Scan Baseline)
        </label>
      </div>
    </div>
  );
}
