import {
    ScatterChart,
    Scatter,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    ZAxis
  } from "recharts";
  
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
  
      return (
        <div className="bg-slate-800 p-4 rounded-xl border border-slate-600 shadow-lg">
          <p className="text-sm text-slate-300">
            <strong>{data.symbol}</strong>
          </p>
          <p className="text-sm">P/E Ratio: {data.pe.toFixed(2)}</p>
          <p className="text-sm">Discount: {data.discount.toFixed(2)}%</p>
          <p className="text-sm text-green-400">
            Opportunity: {data.opportunity.toFixed(2)}%
          </p>
        </div>
      );
    }
    return null;
  };
  
  export default function PEAnalysisChart({ stocks }) {
    if (!stocks.length) return null;
  
    const chartData = stocks.map((s) => ({
      symbol: s.symbol,
      pe: Number(s.pe_ratio) || 0,
      discount: Number(s.discount_level) || 0,
      opportunity: Number(s.opportunity) || 5
    }));
  
    return (
      <div className="bg-slate-900 p-6 rounded-2xl">
        <h2 className="text-2xl font-bold mb-6">
          P/E vs Discount Analysis
        </h2>
  
        <ResponsiveContainer width="100%" height={400}>
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
  
            <XAxis
              type="number"
              dataKey="pe"
              name="P/E Ratio"
              stroke="#94a3b8"
            />
  
            <YAxis
              type="number"
              dataKey="discount"
              name="Discount %"
              stroke="#94a3b8"
            />
  
            <ZAxis
              type="number"
              dataKey="opportunity"
              range={[100, 600]}
            />
  
            <Tooltip content={<CustomTooltip />} />
  
            <Scatter
              data={chartData}
              fill="#22c55e"
            />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    );
  }