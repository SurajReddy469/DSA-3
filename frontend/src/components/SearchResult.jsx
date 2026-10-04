import React from 'react';
import { BookOpen, Hash, Award, Tag } from 'lucide-react';

const LANG_MAP = {
  te: 'Telugu',
  hi: 'Hindi',
  ta: 'Tamil',
  kn: 'Kannada',
  ml: 'Malayalam',
  bn: 'Bengali',
  mr: 'Marathi',
  gu: 'Gujarati',
  pa: 'Punjabi',
  en: 'English'
};

export default function SearchResult({ result }) {
  const {
    document_id,
    title,
    language,
    score,
    occurrences,
    matched_terms,
    snippet,
    source,
    ranking_method
  } = result;

  const langLabel = LANG_MAP[language] || language;

  return (
    <div className="card" style={{ marginBottom: '1rem', borderLeft: '4px solid #2563eb' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.5rem' }}>
        <div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#1e293b', marginBottom: '0.25rem' }}>
            <a href={`#doc-${document_id}`} onClick={(e) => e.preventDefault()} style={{ color: '#1d4ed8' }}>
              {title}
            </a>
          </h3>
          <div style={{ display: 'flex', gap: '0.75rem', fontSize: '0.8rem', color: '#64748b', alignItems: 'center', marginBottom: '0.6rem' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.2rem', backgroundColor: '#e0f2fe', color: '#0369a1', padding: '0.15rem 0.5rem', borderRadius: '4px', fontWeight: 600 }}>
              <BookOpen size={12} /> {langLabel}
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
              <Hash size={12} /> Doc #{document_id}
            </span>
            <span>• Source: {source}</span>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '0.6rem', alignItems: 'center' }}>
          <div style={{ textAlign: 'right', background: '#f8fafc', padding: '0.35rem 0.75rem', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
            <div style={{ fontSize: '0.7rem', textTransform: 'uppercase', color: '#64748b', fontWeight: 600 }}>
              {ranking_method === 'tfidf' ? 'TF-IDF Score' : 'Freq Score'}
            </div>
            <div style={{ fontSize: '1rem', fontWeight: 700, color: '#2563eb', display: 'flex', alignItems: 'center', gap: '0.25rem', justifyContent: 'flex-end' }}>
              <Award size={14} /> {score}
            </div>
          </div>

          <div style={{ textAlign: 'right', background: '#f8fafc', padding: '0.35rem 0.75rem', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
            <div style={{ fontSize: '0.7rem', textTransform: 'uppercase', color: '#64748b', fontWeight: 600 }}>
              Matches
            </div>
            <div style={{ fontSize: '1rem', fontWeight: 700, color: '#059669' }}>
              {occurrences}
            </div>
          </div>
        </div>
      </div>

      {/* Snippet with HTML highlighted tags */}
      <p
        style={{ fontSize: '0.92rem', color: '#334155', lineHeight: 1.6, marginBottom: '0.75rem' }}
        dangerouslySetInnerHTML={{ __html: snippet }}
      />

      {/* Matched Keywords Chips */}
      {matched_terms && matched_terms.length > 0 && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
            <Tag size={12} /> Matched Keywords:
          </span>
          {matched_terms.map((term, idx) => (
            <span
              key={idx}
              style={{
                fontSize: '0.75rem',
                backgroundColor: '#fef3c7',
                color: '#92400e',
                padding: '0.1rem 0.45rem',
                borderRadius: '4px',
                fontWeight: 600
              }}
            >
              {term}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
