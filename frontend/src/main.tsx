import React from "react";
import ReactDOM from "react-dom/client";
import App from "./pages/Home.tsx";
import Admin from "./pages/Admin.tsx";
import Login from "./pages/Login.tsx";
import ErrorPage from "./components/ErrorPage.tsx";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { AdminStoreProvider, AdminStore } from "./store/store.tsx";

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
  {
    path: "/english-teacher-website/login",
    element: <Login />,
  },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <AdminStoreProvider value={new AdminStore()}>
      <RouterProvider router={router} />
    </AdminStoreProvider>
  </React.StrictMode>
);
