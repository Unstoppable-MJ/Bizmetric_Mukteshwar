import { useState } from "react";
import AddStockModal from "./AddStockModal";

export default function Navbar({ refreshData }) {
  const [showModal, setShowModal] = useState(false);

  return (
    <div className="bg-slate-900 p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold">📊 Fintech Dashboard</h1>

      <div className="flex items-center gap-6">
        <select className="bg-slate-800 p-2 rounded-lg">
          <option>My Portfolio</option>
        </select>

        <button
          onClick={() => setShowModal(true)}
          className="bg-green-500 px-4 py-2 rounded-lg"
        >
          + Add Stock
        </button>

        <span className="text-slate-400">👤 Mukteshwar</span>
      </div>

      {showModal && (
        <AddStockModal
          onClose={() => setShowModal(false)}
          onSuccess={refreshData}
        />
      )}
    </div>
  );
}