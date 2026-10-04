import React, { useState, useEffect } from 'react';
import SearchBar from '../components/SearchBar';
import QueryModeSelector from '../components/QueryModeSelector';
import RankingSelector from '../components/RankingSelector';
import SearchStats from '../components/SearchStats';
import SearchResults from '../components/SearchResults';
import { searchCorpus, getIndexStatus } from '../services/api';
import { Sparkles, Database, FileText, Zap } from 'lucide-react';

export default function Home() {
  const [query, setQuery] = useState('కంప్యూటర్');
  const [language, setLanguage] = useState('all');
  const [mode, setMode] = useState('AND');
  const [ranking, setRanking] = useState('tfidf');
  const [useNaive, setUseNaive] = useState(false);
  const [resultsPerPage, setResultsPerPage] = useState(10);
  const [currentPage, setCurrentPage] = useState(1);

  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [indexStatus, setIndexStatus] = useState(null);

  useEffect(() => {
    // Fetch index status on load
    getIndexStatus()
      .then((data) => setIndexStatus(data))
      .catch(() => setIndexStatus({ ready: false }));

    // Execute default search on mount
    executeSearch('కంప్యూటర్', 1, mode, ranking, language, useNaive, resultsPerPage);
  }, []);

  const executeSearch = async (
    searchQuery = query,
    page = currentPage,
    searchMode = mode,
    rankMethod = ranking,
    langFilter = language,
    naiveFlag = useNaive,
    limitVal = resultsPerPage
  ) => {
    if (!searchQuery || !searchQuery.strip && !searchQuery.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const data = await searchCorpus({
        query: searchQuery,
        mode: searchMode,
        ranking: rankMethod,
        language: langFilter,
        limit: limitVal,
        page: page,
        use_naive: naiveFlag,
      });

      setSearchResults(data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to connect to search API engine.');
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (overrideQuery) => {
    const targetQuery = overrideQuery || query;
    setCurrentPage(1);
    executeSearch(targetQuery, 1, mode, ranking, language, useNaive, resultsPerPage);
  };

  const handleOptionChange = (updatedParams) => {
    const newMode = updatedParams.mode !== undefined ? updatedParams.mode : mode;
    const newRanking = updatedParams.ranking !== undefined ? updatedParams.ranking : ranking;
    const newNaive = updatedParams.use_naive !== undefined ? updatedParams.use_naive : useNaive;
    const newLimit = updatedParams.limit !== undefined ? updatedParams.limit : resultsPerPage;

    setCurrentPage(1);
    executeSearch(query, 1, newMode, newRanking, language, newNaive, newLimit);
  };

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    executeSearch(query, newPage, mode, ranking, language, useNaive, resultsPerPage);
  };

  return (
    <div className="container">
      {/* Hero Header */}
      <div style={{ textAlign: 'center', marginBottom: '2.5rem', marginTop: '1rem' }}>
        <h1 style={{ fontSize: '2.4rem', fontWeight: 800, color: '#0f172a', letterSpacing: '-0.03em', marginBottom: '0.4rem' }}>
          IndicSearch
        </h1>
        <p style={{ fontSize: '1.1rem', color: '#64748b', fontWeight: 500 }}>
          Scalable Unicode Text Analytics & Inverted-Index Search Engine for Indian-Language Wikipedia
        </p>

        {/* System Overview Badges */}
        {indexStatus && indexStatus.ready && (
          <div
            style={{
              display: 'inline-flex',
              gap: '1.25rem',
              alignItems: 'center',
              marginTop: '1rem',
              padding: '0.4rem 1rem',
              backgroundColor: '#ffffff',
              borderRadius: '9999px',
              border: '1px solid #e2e8f0',
              fontSize: '0.8rem',
              color: '#475569',
              boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
            }}
          >
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', color: '#16a34a', fontWeight: 600 }}>
              <span className="status-dot"></span> Index Ready
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
              <FileText size={14} color="#2563eb" /> Documents: <strong>{indexStatus.total_documents?.toLocaleString()}</strong>
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
              <Database size={14} color="#0ea5e9" /> Vocabulary Terms: <strong>{indexStatus.unique_terms?.toLocaleString()}</strong>
            </span>
          </div>
        )}
      </div>

      {/* Main Search Controls */}
      <SearchBar
        query={query}
        setQuery={setQuery}
        language={language}
        setLanguage={(l) => {
          setLanguage(l);
          executeSearch(query, 1, mode, ranking, l, useNaive, resultsPerPage);
        }}
        onSearch={handleSearchSubmit}
        loading={loading}
      />

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <QueryModeSelector
          mode={mode}
          setMode={setMode}
          useNaive={useNaive}
          setUseNaive={setUseNaive}
          resultsPerPage={resultsPerPage}
          setResultsPerPage={setResultsPerPage}
          onOptionChange={handleOptionChange}
        />

        <RankingSelector
          ranking={ranking}
          setRanking={setRanking}
          onOptionChange={handleOptionChange}
        />
      </div>

      {/* Error Alert */}
      {error && (
        <div className="card" style={{ backgroundColor: '#fef2f2', borderColor: '#fecaca', color: '#991b1b', marginBottom: '1.5rem' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Search Stats Banner */}
      {searchResults && <SearchStats stats={searchResults} />}

      {/* Search Results Component */}
      <SearchResults
        results={searchResults?.results}
        totalResults={searchResults?.total_results}
        currentPage={currentPage}
        totalPages={searchResults?.total_pages || 1}
        limit={resultsPerPage}
        onPageChange={handlePageChange}
        loading={loading}
      />
    </div>
  );
}
