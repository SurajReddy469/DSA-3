import React from 'react';
import { Routes, Route, NavLink } from 'react-router-dom';
import Home from './pages/Home';
import Analytics from './pages/Analytics';
import About from './pages/About';
import { Search, BarChart2, Info, BookOpen } from 'lucide-react';

export default function App() {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Navigation Bar */}
      <header className="navbar">
        <div className="nav-container">
          <NavLink to="/" className="logo-group">
            <div className="logo-icon">
              <BookOpen size={20} />
            </div>
            <div>
              <div className="logo-title">IndicSearch</div>
              <div className="logo-subtitle">Unicode Text Analytics & Search</div>
            </div>
          </NavLink>

          <nav>
            <ul className="nav-links">
              <li>
                <NavLink to="/" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                  <Search size={16} /> Search Engine
                </NavLink>
              </li>
              <li>
                <NavLink to="/analytics" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                  <BarChart2 size={16} /> Analytics & Benchmarks
                </NavLink>
              </li>
              <li>
                <NavLink to="/about" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                  <Info size={16} /> About Project
                </NavLink>
              </li>
            </ul>
          </nav>
        </div>
      </header>

      {/* Main Content View */}
      <main style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>

      {/* Footer */}
      <footer style={{ backgroundColor: '#ffffff', borderTop: '1px solid #e2e8f0', padding: '1.5rem 0', textAlign: 'center', marginTop: '3rem', fontSize: '0.85rem', color: '#64748b' }}>
        <div className="container" style={{ padding: '0 1.5rem' }}>
          <strong>IndicSearch Project</strong> • Scalable Unicode Text Analytics and Inverted-Index Search Engine for Indian-Language Wikipedia.
        </div>
      </footer>
    </div>
  );
}
