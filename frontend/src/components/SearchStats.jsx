import React from 'react';
import { Clock, CheckCircle2, Zap, Sliders } from 'lucide-react';

export default function SearchStats({ stats }) {
  if (!stats) return null;

  const { search_time_ms, total_results, query, mode, ranking } = stats;

  return (
    <div
      style={{
        backgroundColor: '#f1f5f9',
        border: '1px solid #e2e8f0',
        borderRadius: '8px',
        padding: '0.75rem 1rem',
        marginBottom: '1.25rem',
        display: 'flex',
        justify: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '0.75rem',
        fontSize: '0.875rem'
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: '#334155' }}>
        <CheckCircle2 size={18} color="#16a34a" />
        <span>
          Found <strong>{total_results}</strong> documents for query "<strong>{query}</strong>"
        </span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', color: '#64748b' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', fontWeight: 600, color: '#0284c7' }}>
          <Zap size={16} /> Search completed in {search_time_ms} ms
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
          <Sliders size={14} /> Mode: <strong style={{ color: '#1e293b' }}>{mode}</strong> | Ranking: <strong style={{ color: '#1e293b' }}>{ranking.toUpperCase()}</strong>
        </div>
      </div>
    </div>
  );
}
