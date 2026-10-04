import React from 'react';
import { BookOpen, Code2, Database, Cpu, Award } from 'lucide-react';

export default function About() {
  return (
    <div className="container" style={{ maxWidth: '960px' }}>
      <div style={{ marginBottom: '2.5rem', textAlign: 'center' }}>
        <h1 style={{ fontSize: '2.2rem', fontWeight: 800, color: '#0f172a', letterSpacing: '-0.02em' }}>
          About IndicSearch
        </h1>
        <p style={{ fontSize: '1.05rem', color: '#64748b', marginTop: '0.4rem' }}>
          Academic Search Engine & Text Analytics Platform for Indian-Language Wikipedia
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div className="card">
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#1e293b', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <BookOpen size={20} color="#2563eb" /> Project Motivation & Objectives
          </h2>
          <p style={{ color: '#334155', lineHeight: 1.6 }}>
            Indian languages like Telugu, Hindi, Tamil, and Bengali are rich in cultural and scientific knowledge, yet traditional full-text search tools often fail to handle Indic grapheme clusters correctly or require bulky external dependencies. <strong>IndicSearch</strong> demonstrates a high-performance, Unicode-aware Information Retrieval (IR) system built from scratch in pure Python using custom Data Structures and Algorithms (DSA).
          </p>
        </div>

        <div className="card">
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#1e293b', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Database size={20} color="#0ea5e9" /> Key Data Structures
          </h2>
          <ul style={{ paddingLeft: '1.25rem', color: '#334155', lineHeight: 1.7 }}>
            <li>
              <strong>Hash-Table Term Dictionary (O(1) Average Lookup):</strong> Maps normalized Unicode term strings directly to posting lists.
            </li>
            <li>
              <strong>Sorted Posting Lists:</strong> Maintains document IDs in strictly ascending order with term frequencies ($tf$) and document metadata.
            </li>
            <li>
              <strong>Two-Pointer Posting List Intersection (O(|A| + |B|)):</strong> Evaluates Boolean AND queries efficiently by advancing pointers over sorted document IDs without full corpus scans.
            </li>
            <li>
              <strong>Two-Pointer Posting List Union (O(|A| + |B|)):</strong> Combines posting sets for Boolean OR queries in linear time relative to posting lengths.
            </li>
          </ul>
        </div>

        <div className="card">
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#1e293b', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Award size={20} color="#10b981" /> Mathematical Ranking Models
          </h2>

          <div style={{ backgroundColor: '#f8fafc', padding: '1rem', borderRadius: '6px', border: '1px solid #e2e8f0', marginBottom: '1rem' }}>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#0f172a' }}>1. Term Frequency (TF) Ranking</h4>
            <code style={{ fontSize: '0.85rem', color: '#1d4ed8' }}>Score(d) = ∑ (tf(t, d) for t ∈ Query)</code>
          </div>

          <div style={{ backgroundColor: '#f8fafc', padding: '1rem', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#0f172a' }}>2. TF-IDF (Term Frequency - Inverse Document Frequency)</h4>
            <div style={{ fontSize: '0.85rem', color: '#334155', marginTop: '0.4rem', lineHeight: 1.6 }}>
              <div><strong>TF(t, d):</strong> normalized term frequency in document = count(t, d) / |d|</div>
              <div><strong>IDF(t):</strong> inverse document frequency = log((N + 1) / (DF(t) + 1)) + 1</div>
              <div style={{ marginTop: '0.4rem', color: '#1d4ed8', fontWeight: 600 }}>Score(d) = ∑ (TF(t, d) × IDF(t) for t ∈ Query)</div>
            </div>
          </div>
        </div>

        <div className="card">
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#1e293b', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Cpu size={20} color="#f59e0b" /> Technology Stack
          </h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', fontSize: '0.9rem', color: '#334155' }}>
            <div>
              <strong>Backend:</strong> Python 3.11+, FastAPI, Pydantic, NumPy, Pandas, Uvicorn
            </div>
            <div>
              <strong>Frontend:</strong> React, Vite, Recharts, Lucide Icons, CSS3
            </div>
            <div>
              <strong>Data Persistence:</strong> Pickle Inverted Index & JSON Corpus
            </div>
            <div>
              <strong>Unicode Standard:</strong> NFC Normalization (Unicode Standard 15.0)
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
