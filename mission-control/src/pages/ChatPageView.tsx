import PageContainer from "../components/ui/PageContainer";
import { ChatPage } from "../features/chat";

export default function ChatPageView() {
  return (
    <PageContainer>
      <header className="mb-6">
        <div className="text-sm uppercase tracking-[0.35em] text-cyan-400">
          Hermes Operator
        </div>

        <h1 className="mt-2 text-4xl font-black text-white">
          AI Chat
        </h1>

        <p className="mt-2 text-slate-400">
          Cere informații, creează misiuni și administrează infrastructura.
        </p>
      </header>

      <ChatPage />
    </PageContainer>
  );
}
