import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import { LanguageProvider } from "./context/LanguageContext";
import { WorkflowProvider } from "./context/WorkflowContext";
import "./index.css";
import "./App.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <LanguageProvider>
      <WorkflowProvider>
        <App />
      </WorkflowProvider>
    </LanguageProvider>
  </React.StrictMode>,
);
