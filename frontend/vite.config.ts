import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  base: "/english-teacher-website",
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://127.0.0.10:8888",
    },
  },
});
