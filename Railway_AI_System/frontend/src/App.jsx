import React, { useState, useEffect, useRef } from 'react';
import { Routes, Route } from 'react-router-dom';
import './App.css';
import TrainForm from './components/TrainForm';
import TrainStatusCard from './components/TrainStatusCard';
import PredictionPage from './components/PredictionPage';
import { getTrainStatus } from './services/api';
import { Train, AlertCircle, RefreshCw } from 'lucide-react';

const Home = () => {
  const [status, setStatus] = useState(null);
  const [lastSuccessfulStatus, setLastSuccessfulStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [lastSearchedTrain, setLastSearchedTrain] = useState('');
  const [retryAttempt, setRetryAttempt] = useState(0);

  // 1. REAL API FETCHING logic
  const fetchRealData = async (trainNo) => {
    const data = await getTrainStatus(trainNo);
    if (!data || Object.keys(data).length === 0) {
      throw new Error("Empty operational data");
    }
    return { ...data, is_simulation: false };
  };

  // 3. SMART SIMULATION MODE logic
  const generateSimulationData = (trainNo) => {
    // Specific case for Maharashtra Express
    if (trainNo === "11040") {
      return {
        train_name: "Maharashtra Express",
        source: "SCSMT Kolhapur",
        destination: "Gondia Junction",
        current_station: "Pune Junction",
        delay: "5 min Delay",
        train_status_message: "Running 5 mins Late (Simulated)",
        is_simulation: true
      };
    }

    const routes = [
      ["Mumbai", "Pune"],
      ["Delhi", "Lucknow"],
      ["Chennai", "Bangalore"],
      ["Kolkata", "Patna"]
    ];

    const routeIndex = parseInt(trainNo) % routes.length;
    const [source, destination] = routes[routeIndex];

    const type = trainNo.startsWith('12') ? "Rajdhani" : "Express";
    const trainName = `${type} ${trainNo}`;

    const delayMins = Math.floor(Math.random() * 11);
    const delay = delayMins === 0 ? "On Time" : `${delayMins} min Delay`;
    const statusMessage = delayMins === 0 ? "Running on time (Simulated)" : `Delayed by ${delayMins} mins (Simulated)`;

    return {
      train_name: trainName,
      source: source,
      destination: destination,
      current_station: source,
      delay: delay,
      train_status_message: statusMessage,
      is_simulation: true
    };
  };

  // 2. AUTO FALLBACK logic
  const handleFallback = (trainNo) => {
    const simulatedData = generateSimulationData(trainNo);
    setStatus(simulatedData);
    setLoading(false);
    setRetryAttempt(0);
  };

  const initiateSearch = async (trainNo) => {
    if (!trainNo) return;

    setLoading(true);
    setStatus(null);
    setLastSearchedTrain(trainNo);
    setRetryAttempt(0);

    let attempts = 0;
    const maxRetries = 2; // Retry 2 times = 3 attempts total (1 initial + 2 retries)

    const executeWithRetry = async () => {
      try {
        const data = await getTrainStatus(trainNo);
        if (!data || Object.keys(data).length === 0) throw new Error("Empty Result");

        // Use is_simulation flag from backend
        setStatus(data);
        if (!data.is_simulation) {
          setLastSuccessfulStatus(data);
        }
        setLoading(false);
      } catch (err) {
        if (attempts < maxRetries) {
          attempts++;
          setRetryAttempt(attempts);
          // Auto fallback logic if 429/500/empty
          // We retry first, then fallback
          setTimeout(executeWithRetry, 2000);
        } else {
          handleFallback(trainNo);
        }
      }
    };

    executeWithRetry();
  };

  return (
    <div className="content">
      <TrainForm onSearch={initiateSearch} isLoading={loading} />

      {loading && (
        <div className="dashboard-loading py-10">
          <div className="spinner-large mb-4"></div>
          <p className="pulse-text">Interrogating Terminal Nodes... {retryAttempt > 0 && `(Retry ${retryAttempt}/2)`}</p>
        </div>
      )}

      {status && (
        <TrainStatusCard
          status={status}
          trainNo={lastSearchedTrain}
          isLegacy={false}
        />
      )}

      {!status && !loading && lastSuccessfulStatus && (
        <div className="resilience-mode py-4 text-center">
          <p className="text-slate-400 text-sm italic">Connection unstable. Showing cached intelligence.</p>
          <TrainStatusCard
            status={lastSuccessfulStatus}
            trainNo={lastSearchedTrain}
            isLegacy={true}
          />
        </div>
      )}
    </div>
  );
};

function App() {
  return (
    <div className="app-container dashboard-theme">
      <header className="app-header-premium">
        <div className="logo-box animate-fade-in">
          <Train size={56} strokeWidth={2.5} className="logo-icon" />
          <div className="title-stack">
            <h1>Railway AI</h1>
            <span className="badge-premium">v2.0 Beta</span>
          </div>
        </div>
        <p className="header-tagline">Deep-learning powered train logistics and real-time terminal intelligence.</p>
        <div className="header-decoration"></div>
      </header>

      <main className="app-wrapper">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/predict/:trainNo" element={<PredictionPage />} />
        </Routes>
      </main>

      <footer className="footer">
        <p>&copy; 2026 Railway AI System. Next-gen Rail Intelligence.</p>
      </footer>
    </div>
  );
}

export default App;
