import { useState, useEffect } from "react";
import API from "../services/api";
import { motion } from "framer-motion";

export default function AddStockModal({ onClose, onSuccess }) {
  const [symbol, setSymbol] = useState("");
  const [quantity, setQuantity] = useState("");
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);

  // 🔍 Live Preview Fetch
  useEffect(() => {
    if (symbol.length > 2) {
      setLoading(true);

      API.get(`stock-preview/?symbol=${symbol}`)
        .then((res) => {
          setPreview(res.data);
          setLoading(false);
        })
        .catch(() => {
          setPreview(null);
          setLoading(false);
        });
    } else {
      setPreview(null);
    }
  }, [symbol]);

  // ➕ Add Stock
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await API.post("add-stock/", {
        symbol,
        quantity,
        portfolio: 1,
      });

      onSuccess();
      onClose();
    } catch (err) {
      alert("Error adding stock");
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex justify-center items-center">
      <motion.div
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        className="bg-slate-900 p-8 rounded-2xl w-96 text-white"
      >
        <h2 className="text-xl font-bold mb-6">Add Stock</h2>

        <form onSubmit={handleSubmit}>
          {/* SYMBOL INPUT */}
          <input
            type="text"
            placeholder="Stock Symbol (e.g ADANIPORTS)"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            className="w-full p-3 mb-4 rounded-lg bg-slate-800"
          />

          {/* 🔍 LOADING */}
          {loading && (
            <p className="text-sm text-slate-400 mb-2">
              Fetching stock data...
            </p>
          )}

          {/* 📊 PREVIEW BOX */}
          {preview && (
            <div className="bg-slate-800 p-4 rounded-lg mb-4">
              <p>Current Price: ₹{preview.current_price}</p>
              <p>P/E Ratio: {preview.pe_ratio}</p>
              <p>
                Discount: {preview.discount_level.toFixed(2)}%
              </p>
              <p>
                Opportunity: {preview.opportunity.toFixed(2)}%
              </p>
            </div>
          )}

          {/* QUANTITY */}
          <input
            type="number"
            placeholder="Quantity"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            className="w-full p-3 mb-6 rounded-lg bg-slate-800"
          />

          {/* BUTTONS */}
          <button
            type="submit"
            className="w-full bg-green-500 p-3 rounded-lg mb-3"
          >
            Add Stock
          </button>

          <button
            type="button"
            onClick={onClose}
            className="w-full bg-red-500 p-3 rounded-lg"
          >
            Cancel
          </button>
        </form>
      </motion.div>
    </div>
  );
}