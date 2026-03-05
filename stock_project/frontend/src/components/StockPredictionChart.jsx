import { useState, useEffect, useMemo } from "react";
import { ResponsiveContainer, ComposedChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, Area } from "recharts";
import API from "../services/api";

export default function StockPredictionChart({ symbol, allStocks = [], onSymbolChange }) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [horizon, setHorizon] = useState("7d");
    const [algorithm, setAlgorithm] = useState("linear");

    // Get unique stocks for the dropdown selector
    const uniqueStocks = useMemo(() => {
        const unique = [];
        const seen = new Set();
        allStocks.forEach(s => {
            const sym = s.stock?.symbol || s.symbol;
            if (!sym) return; // Skip if no symbol is found

            if (!seen.has(sym)) {
                seen.add(sym);
                unique.push({
                    name: s.stock?.name || s.name || sym,
                    symbol: sym.replace(".NS", ""),
                    rawSymbol: sym
                });
            }
        });
        return unique;
    }, [allStocks]);

    const currentStock = uniqueStocks.find(s => s.symbol === symbol) || { name: symbol, symbol: symbol };

    useEffect(() => {
        if (!symbol) return;

        setLoading(true);
        setError(null);
        API.get(`stock-prediction/?symbol=${symbol}&horizon=${horizon}&algorithm=${algorithm}`)
            .then(res => {
                const historyData = res.data.history.map(d => ({ ...d, historical: d.price }));
                const predictionsData = res.data.predictions.map(d => ({ ...d, predicted: d.price }));

                // Connect the lines seamlessly by anchoring the predicted line to the final historical node 
                // without creating a duplicate XAxis date entry.
                if (historyData.length > 0) {
                    const lastIndex = historyData.length - 1;
                    historyData[lastIndex].predicted = historyData[lastIndex].historical;
                }

                const combined = [...historyData, ...predictionsData];
                setData(combined);
                setLoading(false);
            })
            .catch(err => {
                setError("Could not load prediction data");
                setLoading(false);
            });
    }, [symbol, horizon, algorithm]);

    const algoDisplayNames = {
        "linear": "Linear Regression",
        "logistic": "Logistic Regression",
        "ridge": "Ridge Regression",
        "lasso": "Lasso Regression"
    };

    return (
        <div className="bg-slate-950/40 backdrop-blur-md rounded-2xl border border-slate-800 p-6 shadow-2xl relative overflow-hidden h-[450px] flex flex-col">
            <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/5 rounded-full blur-3xl" />

            <div className="flex flex-col md:flex-row justify-between md:items-center gap-4 mb-6 relative z-10">
                <div>
                    <h3 className="text-lg font-bold text-white flex items-center gap-2">
                        <span className="text-indigo-400">🔮</span> Trend Forecast
                        {currentStock.name && ` – ${currentStock.name} (${currentStock.symbol})`}
                    </h3>
                    <p className="text-xs text-slate-500 mt-1">
                        {algoDisplayNames[algorithm]} • {horizon === '7d' ? '7-Day' : horizon === '1mo' ? '1-Month' : horizon === '6mo' ? '6-Month' : '12-Month'} Projection
                    </p>
                </div>

                <div className="flex flex-wrap items-center gap-4">
                    {/* Algorithm Selector */}
                    <select
                        value={algorithm}
                        onChange={(e) => setAlgorithm(e.target.value)}
                        className="bg-slate-950/50 border border-slate-800 text-fuchsia-300 text-sm font-semibold rounded-xl px-3 py-1.5 focus:outline-none focus:border-indigo-500 transition-colors cursor-pointer appearance-none pr-8 relative shadow-sm"
                        style={{ backgroundImage: 'url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23c084fc%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E")', backgroundRepeat: 'no-repeat', backgroundPosition: 'right 0.7rem top 50%', backgroundSize: '0.65rem auto' }}
                    >
                        <option value="linear">Linear Regression</option>
                        <option value="logistic">Logistic Regression</option>
                        <option value="ridge">Ridge Regression</option>
                        <option value="lasso">Lasso Regression</option>
                    </select>

                    {/* Stock Selector */}
                    {uniqueStocks.length > 0 && (
                        <select
                            value={symbol || ""}
                            onChange={(e) => onSymbolChange && onSymbolChange(e.target.value)}
                            className="bg-slate-950/50 border border-slate-800 text-slate-300 text-sm font-semibold rounded-xl px-3 py-1.5 focus:outline-none focus:border-indigo-500 transition-colors cursor-pointer appearance-none pr-8 relative shadow-sm"
                            style={{ backgroundImage: 'url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%2394a3b8%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E")', backgroundRepeat: 'no-repeat', backgroundPosition: 'right 0.7rem top 50%', backgroundSize: '0.65rem auto' }}
                        >
                            {uniqueStocks.map(s => (
                                <option key={s.symbol} value={s.symbol}>
                                    {s.name} ({s.symbol})
                                </option>
                            ))}
                        </select>
                    )}

                    {/* Horizon Selector */}
                    <select
                        value={horizon}
                        onChange={(e) => setHorizon(e.target.value)}
                        className="bg-slate-950/50 border border-slate-800 text-indigo-300 text-sm font-bold rounded-xl px-3 py-1.5 focus:outline-none focus:border-indigo-500 transition-colors cursor-pointer appearance-none pr-8 relative shadow-sm"
                        style={{ backgroundImage: 'url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23818cf8%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E")', backgroundRepeat: 'no-repeat', backgroundPosition: 'right 0.7rem top 50%', backgroundSize: '0.65rem auto' }}
                    >
                        <option value="7d">7 Days</option>
                        <option value="1mo">1 Month</option>
                        <option value="6mo">6 Months</option>
                        <option value="1y">12 Months</option>
                    </select>

                    <div className="hidden lg:flex gap-4 text-[10px] items-center">
                        <div className="flex items-center gap-1.5 text-slate-400">
                            <span className="w-2 h-2 rounded-full bg-indigo-400"></span>
                            HISTORICAL
                        </div>
                        <div className="flex items-center gap-1.5 text-slate-400">
                            <span className="w-2 h-0.5 bg-indigo-400 border-t border-dashed"></span>
                            PREDICTED
                        </div>
                    </div>
                </div>
            </div>

            <div className="flex-grow w-full relative min-h-0">
                {loading && (
                    <div className="absolute inset-0 z-20 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-800/50">
                        <div className="flex flex-col items-center gap-3">
                            <div className="w-6 h-6 border-2 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
                            <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">Calculating Projection...</span>
                        </div>
                    </div>
                )}

                {error && !loading && (
                    <div className="absolute inset-0 z-20 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm rounded-xl border border-rose-500/20">
                        <div className="text-center p-6 text-rose-400 font-medium">
                            {error}
                        </div>
                    </div>
                )}

                {data && !error && (
                    <ResponsiveContainer width="100%" height="100%">
                        <ComposedChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                            <defs>
                                <linearGradient id="predGradient" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#818cf8" stopOpacity={0.1} />
                                    <stop offset="95%" stopColor="#818cf8" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                            <XAxis
                                dataKey="date"
                                tick={{ fill: '#64748b', fontSize: 10 }}
                                axisLine={false}
                                tickLine={false}
                                minTickGap={30}
                                padding={{ left: 10, right: 10 }}
                            />
                            <YAxis
                                hide
                                domain={['auto', 'auto']}
                            />
                            <Tooltip
                                contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', fontSize: '12px' }}
                                itemStyle={{ color: '#fff' }}
                                labelStyle={{ color: '#64748b', marginBottom: '4px' }}
                                formatter={(value, name) => [
                                    `₹${Number(value).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
                                    name === 'historical' ? 'Historical Price' : 'Predicted Price'
                                ]}
                            />
                            <Area
                                type="monotone"
                                dataKey="price"
                                stroke="none"
                                fill="url(#predGradient)"
                                connectNulls
                            />
                            <Line
                                type="monotone"
                                dataKey="historical"
                                stroke="#818cf8"
                                strokeWidth={3}
                                dot={false}
                                animationDuration={1500}
                                connectNulls
                            />
                            <Line
                                type="monotone"
                                dataKey="predicted"
                                stroke="#818cf8"
                                strokeWidth={2}
                                strokeDasharray="5 5"
                                dot={{ r: 4, fill: '#818cf8', strokeWidth: 0 }}
                                animationDuration={2000}
                                connectNulls
                            />
                            {/* Last historical point vertical line */}
                            <ReferenceLine x={data.filter(d => d.historical).slice(-1)[0]?.date} stroke="#334155" strokeDasharray="3 3" />
                        </ComposedChart>
                    </ResponsiveContainer>
                )}
            </div>
        </div>
    );
}
