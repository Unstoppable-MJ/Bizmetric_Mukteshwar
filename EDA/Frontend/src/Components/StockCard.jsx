export default function StockCard({ stock }) {
  if (!stock) return null;

  const profit = stock.current_value - stock.investment_value;

  return (
    <div
      style={{
        background: "#1e293b",
        padding: 20,
        borderRadius: 15,
        marginBottom: 20,
        color: "white",
      }}
    >
      <h2 style={{ fontSize: 22 }}>{stock.symbol}</h2>
      <p>Quantity: {stock.quantity}</p>
      <p>Investment: ₹{stock.investment_value}</p>
      <p>Current Value: ₹{stock.current_value}</p>
      <p style={{ color: profit >= 0 ? "#22c55e" : "#ef4444" }}>
        Profit/Loss: ₹{profit.toFixed(2)}
      </p>
    </div>
  );
}