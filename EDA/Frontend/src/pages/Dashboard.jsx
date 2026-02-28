import { useEffect, useState } from "react";
import API from "../services/api";
import KPISection from "../components/KPISection";
import AdvancedChart from "../components/AdvancedChart";
import PEAnalysisChart from "../components/PEAnalysisChart";
import StockCard from "../components/StockCard";

export default function Dashboard() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    API.get("portfolio-stocks/")
      .then((res) => setStocks(res.data))
      .catch((err) => console.log(err));
  }, []);

  // Safety: prevent crash if empty
  const totalInvestment = stocks.reduce(
    (acc, s) => acc + (s.investment_value || 0),
    0
  );

  const totalCurrent = stocks.reduce(
    (acc, s) => acc + (s.current_value || 0),
    0
  );

  const totalProfit = totalCurrent - totalInvestment;

  return (
    <div className="space-y-10">

      {/* 🔵 Portfolio Summary */}
      <div className="bg-slate-900 p-6 rounded-2xl">
        <h2 className="text-2xl font-bold mb-4">
          Portfolio Summary
        </h2>

        <p>Total Investment: ₹{totalInvestment.toFixed(2)}</p>
        <p>Total Current: ₹{totalCurrent.toFixed(2)}</p>

        <p
          className={
            totalProfit >= 0
              ? "text-green-400 font-semibold"
              : "text-red-400 font-semibold"
          }
        >
          Profit/Loss: ₹{totalProfit.toFixed(2)}
        </p>
      </div>

      {/* 🟢 KPI Cards */}
      <KPISection stocks={stocks} />

      {/* 📈 Portfolio Growth Area Chart */}
      <AdvancedChart stocks={stocks} />

      {/* 🔥 NEW SCATTER ANALYSIS */}
      <PEAnalysisChart stocks={stocks} />

      {/* 📦 Stock Cards */}
      <div className="grid md:grid-cols-2 gap-6">
        {stocks.map((stock) => (
          <StockCard key={stock.id} stock={stock} />
        ))}
      </div>

    </div>
  );
}