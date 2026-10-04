import React, { useState, useEffect } from 'react';
import { getIndexStats, runBenchmark, triggerRebuildIndex } from '../services/api';
import PerformanceChart from '../components/PerformanceChart';
import { BarChart3, RefreshCw, Cpu, Layers, HardDrive, FileText, Globe } from 'lucide-react';

export default function Analytics() {
  const [stats, setStats] = useState(null);
  const [benchmarkData, setBenchmarkData] = useState(null);
  const [benchmarking, setBenchmarking] = useState(false);
  const [rebuilding, setRebuilding] = useState(false);
  const [benchmarkQuery, setBenchmarkQuery] = useState('కంప్యూటర్');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const data = await getIndexStats();
      setStats(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunBenchmark = async () => {
    setBenchmarking(true);
    try {
      const data = await runBenchmark({
        query: benchmarkQuery,
        sample_sizes: [500, 1000, 2500, 5000],
        runs_per_size: 3
      });
      setBenchmarkData(data);
    } catch (err) {
      console.error('Benchmark failed:', err);
    } finally {
      setBenchmarking(false);
    }
  };

  const handleRebuildIndex = async () => {
    setRebuilding(true);
    try {
      await triggerRebuildIndex();
      await fetchStats();
    } catch (err) {
      console.error('Index rebuild failed:', err);
    } finally {
      setRebuilding(false);
    }
  };

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: '#0f172a' }}>
            Index & Search Analytics
          </h1>
          <p style={{ color: '#64748b', fontSize: '0.95rem' }}>
            Empirical data structures performance benchmarks and corpus metrics.
          </p>
        </div>

        <button
          className="btn btn-outline"
          onClick={handleRebuildIndex}
          disabled={rebuilding}
        >
          <RefreshCw size={16} className={rebuilding ? 'spin' : ''} />
          {rebuilding ? 'Rebuilding Index...' : 'Rebuild Index'}
        </button>
      </div>

      {/* Index Metrics Summary Grid */}
      {stats && (
        <div className="grid-4" style={{ marginBottom: '2rem' }}>
          <div className="card" style={{ borderTop: '4px solid #2563eb' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748b', fontSize: '0.8rem', fontWeight: 600, textTransform: 'uppercase' }}>
              <FileText size={16} color="#2563eb" /> Total Documents
            </div>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#0f172a', marginTop: '0.5rem' }}>
              {stats.total_documents?.toLocaleString()}
            </div>
          </div>

          <div className="card" style={{ borderTop: '4px solid #0ea5e9' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748b', fontSize: '0.8rem', fontWeight: 600, textTransform: 'uppercase' }}>
              <Layers size={16} color="#0ea5e9" /> Vocabulary Terms
            </div>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#0f172a', marginTop: '0.5rem' }}>
              {stats.unique_terms?.toLocaleString()}
            </div>
          </div>

          <div className="card" style={{ borderTop: '4px solid #10b981' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748b', fontSize: '0.8rem', fontWeight: 600, textTransform: 'uppercase' }}>
              <HardDrive size={16} color="#10b981" /> Index File Size
            </div>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#0f172a', marginTop: '0.5rem' }}>
              {stats.index_file_size_mb} MB
            </div>
          </div>

          <div className="card" style={{ borderTop: '4px solid #f59e0b' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748b', fontSize: '0.8rem', fontWeight: 600, textTransform: 'uppercase' }}>
              <Cpu size={16} color="#f59e0b" /> Index Build Time
            </div>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#0f172a', marginTop: '0.5rem' }}>
              {stats.index_build_time_sec} s
            </div>
          </div>
        </div>
      )}

      {/* Language Breakdown & Top Terms */}
      {stats && (
        <div className="grid-2" style={{ marginBottom: '2.5rem' }}>
          <div className="card">
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '1rem', color: '#1e293b', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Globe size={18} color="#2563eb" /> Documents by Indian Language
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
              {Object.entries(stats.languages_supported || {}).map(([langCode, count]) => (
                <div key={langCode} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.9rem' }}>
                  <span style={{ fontWeight: 500, color: '#334155' }}>
                    {langCode === 'te' ? 'Telugu (తెలుగు)' :
                     langCode === 'hi' ? 'Hindi (हिन्दी)' :
                     langCode === 'ta' ? 'Tamil (தமிழ்)' :
                     langCode === 'kn' ? 'Kannada (ಕನ್ನಡ)' :
                     langCode === 'ml' ? 'Malayalam (മലയാളം)' :
                     langCode === 'bn' ? 'Bengali (বাংলা)' :
                     langCode === 'mr' ? 'Marathi (मराठी)' :
                     langCode === 'pa' ? 'Punjabi (ਪੰਜਾਬੀ)' : langCode}
                  </span>
                  <span style={{ fontWeight: 700, color: '#2563eb', background: '#eff6ff', padding: '0.15rem 0.6rem', borderRadius: '4px' }}>
                    {count} docs
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '1rem', color: '#1e293b', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <BarChart3 size={18} color="#0ea5e9" /> Top 10 High-DF Vocabulary Terms
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {(stats.top_20_terms || []).slice(0, 10).map((item, idx) => (
                <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.88rem' }}>
                  <span style={{ fontWeight: 600, color: '#1e293b' }}>
                    {idx + 1}. {item.term}
                  </span>
                  <div style={{ display: 'flex', gap: '0.5rem', fontSize: '0.78rem' }}>
                    <span style={{ color: '#64748b' }}>DF: <strong>{item.df}</strong></span>
                    <span style={{ color: '#0284c7' }}>Total TF: <strong>{item.total_tf}</strong></span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Performance Benchmarking Section */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#0f172a' }}>
              ⚡ Real Empirical Search Benchmark
            </h2>
            <p style={{ fontSize: '0.875rem', color: '#64748b' }}>
              Compares high-precision runtime execution (using time.perf_counter) between Naive Linear Scan and Inverted Index.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
            <input
              type="text"
              className="text-input"
              value={benchmarkQuery}
              onChange={(e) => setBenchmarkQuery(e.target.value)}
              placeholder="Query for benchmark..."
              style={{ width: '200px' }}
            />
            <button
              className="btn btn-primary"
              onClick={handleRunBenchmark}
              disabled={benchmarking}
            >
              {benchmarking ? 'Benchmarking...' : 'Run Benchmark'}
            </button>
          </div>
        </div>

        {/* Charts */}
        <PerformanceChart benchmarkData={benchmarkData} />
      </div>
    </div>
  );
}
