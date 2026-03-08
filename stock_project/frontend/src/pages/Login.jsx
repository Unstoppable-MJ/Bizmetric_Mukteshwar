import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function Login() {
  const navigate = useNavigate();

  return (
    <div className="h-screen flex items-center justify-center relative overflow-hidden">
      {/* Background Gradients */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-emerald-600/20 rounded-full blur-[120px] pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="relative z-10 bg-slate-900/50 backdrop-blur-xl p-10 rounded-3xl w-[400px] border border-slate-700/50 shadow-2xl"
      >
        <div className="flex flex-col items-center mb-8">
          <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-emerald-400 rounded-2xl flex items-center justify-center mb-4 shadow-lg shadow-blue-500/30">
            <span className="text-3xl">📈</span>
          </div>
          <h2 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
            Welcome Back
          </h2>
          <p className="text-slate-400 mt-2 text-sm">Sign in to your portfolio</p>
        </div>

        <div className="space-y-4">
          <div>
            <input
              type="text"
              placeholder="Username"
              className="w-full p-4 rounded-xl bg-slate-950/50 border border-slate-800 text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-300"
            />
          </div>

          <div>
            <input
              type="password"
              placeholder="Password"
              className="w-full p-4 rounded-xl bg-slate-950/50 border border-slate-800 text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-300"
            />
          </div>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => navigate("/dashboard")}
            className="w-full bg-gradient-to-r from-blue-600 to-emerald-500 hover:from-blue-500 hover:to-emerald-400 text-white font-semibold p-4 rounded-xl shadow-lg shadow-blue-500/25 transition-all duration-300 mt-2"
          >
            Access Dashboard
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
}