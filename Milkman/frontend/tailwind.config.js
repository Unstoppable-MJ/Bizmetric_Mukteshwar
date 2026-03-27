/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#2563eb",
          secondary: "#059669",
          accent: "#f59e0b",
          surface: "#f7fafc",
          glass: "rgba(255, 255, 255, 0.6)",
        },
        state: {
          success: "#10b981",
          warning: "#f59e0b",
          danger: "#ef4444",
          info: "#0ea5e9",
        }
      },
      borderRadius: {
        'xl': '16px',
        '2xl': '24px',
      },
      boxShadow: {
        'soft': '0 6px 20px rgba(0, 0, 0, 0.06)',
        'premium': '0 10px 30px rgba(0, 0, 0, 0.08)',
        'glass': '0 8px 24px rgba(15, 23, 42, 0.08)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      backdropBlur: {
        'glass': '16px',
      }
    },
  },
  plugins: [],
};
