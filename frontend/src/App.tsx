import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ProjectCreate } from "./pages/ProjectCreate";
import { AuditDashboard } from "./pages/AuditDashboard";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProjectCreate />} />
        <Route path="/project/:id/audit" element={<AuditDashboard />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
