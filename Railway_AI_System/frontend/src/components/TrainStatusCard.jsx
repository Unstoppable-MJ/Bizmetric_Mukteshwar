import React from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin, Clock, Info, Navigation, Train, ArrowRight, BrainCircuit, Activity } from 'lucide-react';

const TrainStatusCard = ({ status, trainNo, isLegacy }) => {
    const navigate = useNavigate();
    if (!status) return null;

    const isSimulation = status.is_simulation;

    const getDelayColor = (delay) => {
        if (!delay) return 'green';
        const delayStr = String(delay).toLowerCase();
        const match = delayStr.match(/(\d+)/);
        if (!match) return delayStr.includes('on time') ? 'green' : 'red';
        const mins = parseInt(match[0]);
        if (mins <= 2) return 'green';
        if (mins <= 5) return 'yellow';
        return 'red';
    };

    const delayColor = getDelayColor(status.delay);

    return (
        <div className={`status-card glass-card animate-slide-up ${isLegacy ? 'legacy-mode' : ''}`}>
            {isLegacy && (
                <div className="legacy-banner">
                    <RefreshCw size={14} className="animate-spin" />
                    <span>Resilience Offline: Showing Last Known State</span>
                </div>
            )}
            <div className="card-hero-premium">
                <div className="train-meta">
                    <div className="train-id">
                        <Activity size={16} className="text-blue-400" />
                        <span>Live Analytics: #{trainNo}</span>
                    </div>
                    {/* Status Indicator */}
                    <div className={`status-indicator-badge ${isSimulation ? 'sim-mode' : 'live-mode'}`}>
                        {isSimulation ? (
                            <>
                                <span className="dot yellow"></span>
                                <span>Simulation Mode (API unavailable)</span>
                            </>
                        ) : (
                            <>
                                <span className="dot green"></span>
                                <span>Live Data</span>
                            </>
                        )}
                    </div>
                </div>
                <div className="train-title-box">
                    <div className="icon-badge">
                        <Train size={32} strokeWidth={2.5} />
                    </div>
                    <h2>{status.train_name}</h2>
                </div>

                <div className="route-viz">
                    <div className="route-node">
                        <span className="node-label">Origin</span>
                        <span className="node-name">{status.source}</span>
                    </div>
                    <div className="route-line">
                        <ArrowRight size={24} />
                    </div>
                    <div className="route-node text-right">
                        <span className="node-label">Dest</span>
                        <span className="node-name">{status.destination}</span>
                    </div>
                </div>
            </div>

            <div className="card-metrics-grid">
                <div className="metric-tile">
                    <div className="tile-icon">
                        <MapPin size={24} />
                    </div>
                    <div className="tile-data">
                        <span className="tile-label">Node Position</span>
                        <span className="tile-value">{status.current_station}</span>
                    </div>
                </div>

                <div className="metric-tile">
                    <div className="tile-icon">
                        <Clock size={24} />
                    </div>
                    <div className="tile-data">
                        <span className="tile-label">Track Latency</span>
                        <span className={`tile-value latency-${delayColor}`}>
                            {status.delay}
                        </span>
                    </div>
                </div>
            </div>

            <div className="intel-segment">
                <div className="intel-header">
                    <Info size={18} />
                    <span>Neural Intelligence Feed</span>
                </div>
                <p className="intel-content">{status.train_status_message}</p>
            </div>

            <div className="card-actions-premium">
                <div className="eta-badge">
                    <span>Next Node:</span>
                    <strong>{status.next_station || 'N/A'}</strong>
                </div>

                <button
                    className="analyze-btn-premium"
                    onClick={() => navigate(`/predict/${trainNo}`)}
                >
                    <BrainCircuit size={20} />
                    <span>Initiate Prediction</span>
                </button>
            </div>
        </div>
    );
};

export default TrainStatusCard;
