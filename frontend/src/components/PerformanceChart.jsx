import React from 'react';
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

export default function PerformanceChart({ benchmarkData }) {
  if (!benchmarkData || !benchmarkData.benchmarks || benchmarkData.benchmarks.length === 0) {
    return <div style={{ color: '#64748b', fontStyle: 'italic' }}>No benchmark data available. Click "Run Empirical Benchmark" to measure timing.</div>;
  }

  const chartData = benchmarkData.benchmarks.map((item) => ({
    name: `${item.dataset_size} docs`,
    datasetSize: item.dataset_size,
    NaiveSearchMs: item.naive_time_ms,
    IndexedSearchMs: item.indexed_time_ms,
    SpeedupFactor: item.speedup_factor,
  }));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div className="card">
        <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '1rem', color: '#1e293b' }}>
          ⏱️ Search Latency: Naive Linear Scan vs. Inverted Index (ms)
        </h3>
        <div style={{ width: '100%', height: 320 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="name" stroke="#64748b" />
              <YAxis label={{ value: 'Search Time (ms)', angle: -90, position: 'insideLeft', style: { textAnchor: 'middle', fill: '#64748b' } }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="NaiveSearchMs" name="Naive Search (Linear Scan)" stroke="#ef4444" strokeWidth={3} dot={{ r: 6 }} />
              <Line type="monotone" dataKey="IndexedSearchMs" name="Inverted Index Search" stroke="#2563eb" strokeWidth={3} dot={{ r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card">
        <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '1rem', color: '#1e293b' }}>
          🚀 Empirical Speedup Factor (X-fold Faster)
        </h3>
        <div style={{ width: '100%', height: 280 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="name" stroke="#64748b" />
              <YAxis label={{ value: 'Speedup Factor (x)', angle: -90, position: 'insideLeft', style: { textAnchor: 'middle', fill: '#64748b' } }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="SpeedupFactor" name="Speedup Factor (Naive Time / Indexed Time)" fill="#10b981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
