import { useState, useRef, useEffect } from "react";
import { createPortal } from "react-dom";
import { useNavigate, useLocation } from "react-router-dom";
import AddStockModal from "./AddStockModal";
import AddPortfolioModal from "./AddPortfolioModal";
import { motion, AnimatePresence } from "framer-motion";

const PortfolioDropdown = ({ portfolios, activePortfolio, setActivePortfolio, navigate, location }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const currentValue = location.pathname === '/nifty50-pca' ? 'nifty50-ai' : location.pathname === '/precious-metals' ? 'precious-metals-ai' : location.pathname === '/crypto-ai' ? 'crypto-ai' : (activePortfolio || "");

  const handleSelect = (val) => {
    setIsOpen(false);
    if (val === 'nifty50-ai') {
      navigate('/nifty50-pca');
    } else if (val === 'precious-metals-ai') {
      navigate('/precious-metals');
    } else if (val === 'crypto-ai') {
      navigate('/crypto-ai');
    } else {
      setActivePortfolio(val);
      if (['/nifty50-pca', '/precious-metals', '/crypto-ai'].includes(location.pathname)) {
        navigate('/dashboard');
      }
    }
  };

  const aiPortfolios = [
    { id: 'nifty50-ai', name: 'NIFTY 50 AI Portfolio', icon: '⚡' },
    { id: 'precious-metals-ai', name: 'Precious Metals AI', icon: '🥇' },
    { id: 'crypto-ai', name: 'Crypto AI Portfolio', icon: '🪙' }
  ];

  let currentLabel = "Select Portfolio";
  let currentIcon = "📁";
  if (currentValue === 'nifty50-ai') { currentLabel = "NIFTY 50 AI Portfolio"; currentIcon = "⚡"; }
  else if (currentValue === 'precious-metals-ai') { currentLabel = "Precious Metals AI"; currentIcon = "🥇"; }
  else if (currentValue === 'crypto-ai') { currentLabel = "Crypto AI Portfolio"; currentIcon = "🪙"; }
  else if (currentValue) {
    const found = portfolios.find(p => p.id === currentValue || p.id === parseInt(currentValue));
    if (found) currentLabel = found.name;
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-between min-w-[240px] h-10 px-4 bg-[#0b1220] border border-white/10 shadow-[0_10px_30px_rgba(0,0,0,0.5)] rounded-xl text-sm transition-all focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-[#e2e8f0]"
      >
        <div className="flex items-center truncate font-medium">
          <span className="mr-2 inline-flex items-center justify-center">{currentIcon}</span>
          <span className="truncate max-w-[160px]">{currentLabel}</span>
        </div>
        <svg className={`shrink-0 ml-2 w-4 h-4 text-slate-400 transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: -10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: -10 }}
            transition={{ duration: 0.2 }}
            className="absolute z-50 mt-2 w-full min-w-[240px] rounded-[12px] overflow-hidden bg-[#0b1220] border border-white/10 shadow-[0_10px_30px_rgba(0,0,0,0.5)]"
          >
            <div className="py-2">
              <div className="px-4 py-1.5 text-[10px] font-bold tracking-widest text-slate-500 uppercase">Standard Portfolios</div>
              {portfolios.map(p => {
                const isSelected = currentValue === p.id || currentValue === String(p.id);
                return (
                  <button
                    key={p.id}
                    onClick={() => handleSelect(p.id)}
                    className={`w-[calc(100%-16px)] mx-2 flex items-center text-left px-3 py-2 text-sm font-medium transition duration-200 group ${isSelected ? 'bg-[#2563eb] text-[#ffffff] rounded-lg' : 'text-[#e2e8f0] hover:bg-[#1e293b] hover:text-[#ffffff] rounded-lg'}`}
                  >
                    <span className="mr-2 inline-flex items-center justify-center">📁</span>
                    <span className="truncate">{p.name}</span>
                  </button>
                );
              })}
              {portfolios.length === 0 && <div className="px-4 py-2 text-sm text-slate-500 italic">No Portfolios</div>}

              <div className="h-px w-full my-1.5" style={{ background: 'rgba(255,255,255,0.08)' }}></div>

              <div className="px-4 py-1.5 text-[10px] font-bold tracking-widest text-slate-500 uppercase mt-1">AI Portfolios</div>
              {aiPortfolios.map(ai => {
                const isSelected = currentValue === ai.id;
                return (
                  <button
                    key={ai.id}
                    onClick={() => handleSelect(ai.id)}
                    className={`w-[calc(100%-16px)] mx-2 flex items-center text-left px-3 py-2 text-sm font-medium transition duration-200 group ${isSelected ? 'bg-[#2563eb] text-[#ffffff] rounded-lg' : 'text-[#e2e8f0] hover:bg-[#1e293b] hover:text-[#ffffff] rounded-lg'}`}
                  >
                    <span className="mr-2 inline-flex items-center justify-center">{ai.icon}</span>
                    <span className="truncate">{ai.name}</span>
                  </button>
                );
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default function Navbar({ refreshData, portfolios, activePortfolio, setActivePortfolio, fetchPortfolios }) {
  const [showAddStock, setShowAddStock] = useState(false);
  const [showAddPortfolio, setShowAddPortfolio] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <motion.div
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="sticky top-4 z-40 mx-6 md:mx-auto max-w-7xl rounded-2xl bg-slate-900/40 backdrop-blur-xl border border-slate-700/50 p-4 px-6 flex justify-between items-center shadow-lg shadow-black/20"
    >
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-emerald-400 rounded-xl flex items-center justify-center shadow-inner">
          <span className="text-xl">📊</span>
        </div>
        <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-300 hidden sm:block">
          Finova
        </h1>
      </div>

      <div className="flex items-center gap-4 sm:gap-6">
        <PortfolioDropdown
          portfolios={portfolios}
          activePortfolio={activePortfolio}
          setActivePortfolio={setActivePortfolio}
          navigate={navigate}
          location={location}
        />

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setShowAddPortfolio(true)}
          className="bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 font-semibold px-4 py-2 rounded-xl text-sm flex items-center gap-2 transition-colors"
        >
          <span>+</span> <span className="hidden sm:inline">Portfolio</span>
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setShowAddStock(true)}
          disabled={!activePortfolio || location.pathname === '/nifty50-pca' || location.pathname === '/precious-metals' || location.pathname === '/crypto-ai'}
          className="bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-semibold px-4 py-2 rounded-xl shadow-lg shadow-emerald-500/20 text-sm flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span>+</span> <span className="hidden sm:inline">Asset</span>
        </motion.button>

        <div className="flex items-center gap-3 pl-4 border-l border-slate-700/50">
          <div className="w-9 h-9 rounded-full bg-slate-800 border border-slate-600 flex items-center justify-center overflow-hidden">
            <img src="https://api.dicebear.com/7.x/notionists/svg?seed=Mukteshwar&backgroundColor=transparent" alt="Avatar" className="w-full h-full object-cover" />
          </div>
        </div>
      </div>

      {showAddStock && createPortal(
        <AddStockModal
          onClose={() => setShowAddStock(false)}
          onSuccess={refreshData}
          activePortfolio={activePortfolio}
        />,
        document.body
      )}

      {showAddPortfolio && createPortal(
        <AddPortfolioModal
          isOpen={showAddPortfolio}
          onClose={() => setShowAddPortfolio(false)}
          onPortfolioAdded={(newPortfolio) => {
            fetchPortfolios();
            setActivePortfolio(newPortfolio.id);
            // Open Add Asset immediately after creating portfolio
            setTimeout(() => setShowAddStock(true), 300);
          }}
        />,
        document.body
      )}
    </motion.div>
  );
}