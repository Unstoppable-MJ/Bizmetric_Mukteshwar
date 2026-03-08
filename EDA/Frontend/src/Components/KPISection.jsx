import { motion } from "framer-motion";

export default function KPISection({ stocks }) {
  const avgPE =
    stocks.reduce((acc, s) => acc + s.pe_ratio, 0) / (stocks.length || 1);

  const avgDiscount =
    stocks.reduce((acc, s) => acc + s.discount_level, 0) /
    (stocks.length || 1);

  const avgOpportunity =
    stocks.reduce((acc, s) => acc + s.opportunity, 0) /
    (stocks.length || 1);

  const Card = ({ title, value }) => (
    <motion.div
      whileHover={{ scale: 1.05 }}
      className="bg-slate-900 p-6 rounded-2xl shadow-lg"
    >
      <h3 className="text-slate-400 mb-2">{title}</h3>
      <h2 className="text-2xl font-bold">{value}</h2>
    </motion.div>
  );

  return (
    <div className="grid grid-cols-3 gap-6 mb-10">
      <Card title="Average P/E Ratio" value={avgPE.toFixed(2)} />
      <Card title="Avg Discount Level" value={avgDiscount.toFixed(2)} />
      <Card title="Opportunity %" value={avgOpportunity.toFixed(2)} />
    </div>
  );
}