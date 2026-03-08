import { useState } from "react";
import { createPortal } from "react-dom";
import { useNavigate, useLocation } from "react-router-dom";
import AddStockModal from "./AddStockModal";
import AddPortfolioModal from "./AddPortfolioModal";
import { motion } from "framer-motion";

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
        <select
          value={location.pathname === '/nifty50-pca' ? 'nifty50-ai' : location.pathname === '/precious-metals' ? 'precious-metals-ai' : location.pathname === '/crypto-ai' ? 'crypto-ai' : (activePortfolio || "")}
          onChange={(e) => {
            const val = e.target.value;
            if (val === 'nifty50-ai') {
              navigate('/nifty50-pca');
            } else if (val === 'precious-metals-ai') {
              navigate('/precious-metals');
            } else if (val === 'crypto-ai') {
              navigate('/crypto-ai');
            } else {
              setActivePortfolio(val);
              if (location.pathname === '/nifty50-pca' || location.pathname === '/precious-metals' || location.pathname === '/crypto-ai') {
                navigate('/dashboard');
              }
            }
          }}
          className="bg-slate-950/50 border border-slate-700/50 text-sm p-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all cursor-pointer text-slate-200"
        >
          {portfolios.map(p => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
          {portfolios.length === 0 && location.pathname !== '/nifty50-pca' && location.pathname !== '/precious-metals' && location.pathname !== '/crypto-ai' && <option disabled value="">No Portfolios</option>}
          <option value="nifty50-ai" className="font-bold text-indigo-400">⚡ NIFTY50 AI Portfolio</option>
          <option value="precious-metals-ai" className="font-bold text-amber-500">🥇 Precious Metals AI</option>
          <option value="crypto-ai" className="font-bold text-violet-400">🪙 Crypto AI Portfolio</option>
        </select>

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