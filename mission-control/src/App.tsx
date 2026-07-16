import { useEffect, useState } from "react";

import MainLayout from "./layouts/MainLayout";
import DashboardV2 from "./pages/DashboardV2";
import HomePage from "./pages/HomePage";
import ChatPageView from "./pages/ChatPageView";
import MissionsPage from "./pages/MissionsPage";
import { AgentStoreProvider } from "./context/AgentStore";

type PageId =
  | "home"
  | "infrastructure"
  | "chat"
  | "missions"
  | "settings";

function App() {
  const [page, setPage] = useState<PageId>("home");

  useEffect(() => {
    const handleNavigate = (event: Event) => {
      const customEvent = event as CustomEvent<PageId>;

      if (customEvent.detail) {
        setPage(customEvent.detail);
      }
    };

    window.addEventListener("hermes:navigate", handleNavigate);

    return () => {
      window.removeEventListener("hermes:navigate", handleNavigate);
    };
  }, []);

  function renderPage() {
    switch (page) {
      case "infrastructure":
        return <DashboardV2 />;

      case "chat":
        return <ChatPageView />;

      case "missions":
        return <MissionsPage />;

      case "settings":
        return (
          <div className="p-8 text-slate-400">
            Settings va fi disponibil în curând.
          </div>
        );

      case "home":
      default:
        return <HomePage />;
    }
  }

  return (
    <AgentStoreProvider>
      <MainLayout>{renderPage()}</MainLayout>
    </AgentStoreProvider>
  );
}

export default App;
