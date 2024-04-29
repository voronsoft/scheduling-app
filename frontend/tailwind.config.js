/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  mode: "jit",
  theme: {
    extend: {
      fontFamily: {
        raleway: ["Raleway", "sans-serif"],
        inter: ["Inter", "sans-serif"],
        noto: ["Noto Serif TC", "serif"],
        notoSans: ["Noto Sans TC", "sans-serif"],
      },
    },
    screens: {
      sm: "320px",
      md: "768px",
      lg: "1200px",
      xl: "1440px",
    },
  },

  plugins: [],
};
