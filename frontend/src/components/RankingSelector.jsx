import React from 'react';
import { Award } from 'lucide-react';

export default function RankingSelector({ ranking, setRanking, onOptionChange }) {
  const handleChange = (e) => {
    const val = e.target.value;
    setRanking(val);
    if (onOptionChange) onOptionChange({ ranking: val });
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
      <label style={{ fontSize: '0.85rem', fontWeight: 600, color: '#475569', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
        <Award size={15} /> Ranking:
      </label>
      <select
        className="select-input"
        value={ranking}
        onChange={handleChange}
        style={{ padding: '0.35rem 0.65rem', fontSize: '0.85rem', fontWeight: 500 }}
      >
        <option value="tfidf">TF-IDF Scoring</option>
        <option value="frequency">Term Frequency</option>
      </select>
    </div>
  );
}
