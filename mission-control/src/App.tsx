import { Navigate, Route, Routes } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";
import DashboardV2 from "./pages/DashboardV2";
import HomePage from "./pages/HomePage";
import ChatPageView from "./pages/ChatPageView";
import MissionsPage from "./pages/MissionsPage";
import PageContainer from "./components/ui/PageContainer";
import GlassPanel from "./components/ui/GlassPanel";
import { AgentStoreProvider } from "./context/AgentStore";

function SettingsPage() {
  return (
    <PageContainer>
      <header className="mb-6">
        <div className="text-sm uppercase tracking-[0.35em] text-cyan-400">
          Configuration
        </div>

        <h1 className="mt-2 text-4xl font-black text-white">
          Settings
        </h1>

        <p className="mt-2 text-slate-400">
          Configurarea Hermes va fi disponibilă aici.
        </p>
      </header>

      <GlassPanel className="p-6">
        <div className="text-slate-400">
          Pagina Settings este în curs de dezvoltare.
        </div>
      </GlassPanel>
    </PageContainer>
  );
}

function NotFoundPage() {
  return (
    <PageContainer>
      <GlassPanel className="p-8">
        <div className="text-sm uppercase tracking-[0.25em] text-cyan-400">
          404
        </div>

        <h1 className="mt-2 text-3xl font-black text-white">
          Pagina nu există
        </h1>

        <p className="mt-3 text-slate-400">
          Adresa accesată nu corespunde unei pagini Hermes.
        </p>
      </GlassPanel>
    </PageContainer>
  );
}

function App() {
  return (
    <AgentStoreProvider>
      <MainLayout>
        <Routes>
          <Route
            path="/"
            element={<Navigate to="/home" replace />}
          />

          <Route path="/home" element={<HomePage />} />

          <Route
            path="/infrastructure"
            element={<DashboardV2 />}
          />

          <Route path="/chat" element={<ChatPageView />} />

          <Route path="/missions" element={<MissionsPage />} />

          <Route path="/settings" element={<SettingsPage />} />

          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </MainLayout>
    </AgentStoreProvider>
  );
}

export default App;
