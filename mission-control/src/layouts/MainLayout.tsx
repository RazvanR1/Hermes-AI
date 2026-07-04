import type { ReactNode } from "react";
import BackgroundFX from "../components/layout/BackgroundFX";
import SidebarV2 from "../components/layout/SidebarV2";
import TopBarV2 from "../components/layout/TopBarV2";

export default function MainLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen text-white">
      <BackgroundFX />
      <SidebarV2 />

      <main className="ml-72 min-h-screen">
        <TopBarV2 />
        {children}
      </main>
    </div>
  );
}
