import {
    LineChart,
    Line,
    AreaChart,
    Area,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
  } from "recharts";
  
  export default function AdvancedChart({ stocks }) {
    const chartData = stocks.map((s) => ({
      name: s.symbol,
      Investment: s.investment_value,
      Current: s.current_value,
    }));
  
    return (
      <div className="bg-slate-900 p-6 rounded-2xl mb-10">
        <h2 className="text-xl font-bold mb-4">Portfolio Growth</h2>
  
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={chartData}>
            <XAxis dataKey="name" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip />
            <Area
              type="monotone"
              dataKey="Investment"
              stroke="#38bdf8"
              fill="#38bdf8"
              fillOpacity={0.2}
            />
            <Area
              type="monotone"
              dataKey="Current"
              stroke="#22c55e"
              fill="#22c55e"
              fillOpacity={0.2}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    );
  }