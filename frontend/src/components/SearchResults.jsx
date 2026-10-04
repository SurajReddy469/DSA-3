import React from 'react';
import SearchResult from './SearchResult';
import { ChevronLeft, ChevronRight, Inbox } from 'lucide-react';

export default function SearchResults({
  results,
  totalResults,
  currentPage,
  totalPages,
  limit,
  onPageChange,
  loading
}) {
  if (loading) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem 1rem', color: '#64748b' }}>
        <div className="spinner" style={{ marginBottom: '1rem' }}>⚡ Searching inverted index posting lists...</div>
      </div>
    );
  }

  if (!results || results.length === 0) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem 1rem', color: '#64748b' }}>
        <Inbox size={48} style={{ margin: '0 auto 1rem', color: '#cbd5e1' }} />
        <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: '#475569' }}>No Matching Documents Found</h3>
        <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
          Try searching for keywords in Telugu like <strong>కంప్యూటర్</strong>, <strong>కృత్రిమ మేధస్సు</strong>, or <strong>తెలంగాణ</strong>.
        </p>
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: '1rem' }}>
        {results.map((result) => (
          <SearchResult key={result.document_id} result={result} />
        ))}
      </div>

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1.5rem', padding: '1rem 0' }}>
          <div style={{ fontSize: '0.875rem', color: '#64748b' }}>
            Showing page <strong>{currentPage}</strong> of <strong>{totalPages}</strong> ({totalResults} total documents)
          </div>

          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              className="btn btn-outline"
              disabled={currentPage <= 1}
              onClick={() => onPageChange(currentPage - 1)}
              style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}
            >
              <ChevronLeft size={16} /> Previous
            </button>
            <button
              className="btn btn-outline"
              disabled={currentPage >= totalPages}
              onClick={() => onPageChange(currentPage + 1)}
              style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}
            >
              Next <ChevronRight size={16} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
