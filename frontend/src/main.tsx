import React from "react";
import ReactDOM from "react-dom/client";
import App from "./pages/Home.tsx";
import Admin from "./pages/Admin.tsx";
import ErrorPage from "./components/ErrorPage.tsx";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/english-teacher-website",
    element: <App />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/english-teacher-website/admin",
    element: <Admin />,
  },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
