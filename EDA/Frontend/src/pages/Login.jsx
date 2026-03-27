import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function Login() {
  const navigate = useNavigate();

  return (
    <div className="h-screen flex items-center justify-center bg-slate-950">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-slate-900 p-10 rounded-2xl w-96 shadow-xl"
      >
        <h2 className="text-2xl font-bold mb-6 text-center">
          🔐 Portfolio Login
        </h2>

        <input
          type="text"
          placeholder="Username"
          className="w-full p-3 mb-4 rounded-lg bg-slate-800"
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full p-3 mb-6 rounded-lg bg-slate-800"
        />

        <button
          onClick={() => navigate("/dashboard")}
          className="w-full bg-blue-500 hover:bg-blue-600 p-3 rounded-lg"
        >
          Login
        </button>
      </motion.div>
    </div>
  );
}