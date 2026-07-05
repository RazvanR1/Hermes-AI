import MainLayout from "./layouts/MainLayout";
import DashboardV2 from "./pages/DashboardV2";
import { AgentStoreProvider } from "./context/AgentStore";

function App() {
  return (
    <AgentStoreProvider>
      <MainLayout>
        <DashboardV2 />
      </MainLayout>
    </AgentStoreProvider>
  );
}

export default App;
