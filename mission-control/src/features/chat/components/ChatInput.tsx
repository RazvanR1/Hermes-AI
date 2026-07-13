import { ArrowUp, LoaderCircle } from "lucide-react";

interface ChatInputProps {
  value: string;
  busy?: boolean;
  onChange: (value: string) => void;
  onSubmit: () => void;
}

export default function ChatInput({
  value,
  busy = false,
  onChange,
  onSubmit,
}: ChatInputProps) {
  return (
    <div className="sticky bottom-0 z-10 bg-gradient-to-t from-[#07101b] via-[#07101b]/95 to-transparent pb-4 pt-5">
      <div className="rounded-[24px] border border-white/10 bg-[#0d1623]/95 p-2 shadow-[0_22px_80px_rgba(0,0,0,0.45)] backdrop-blur-xl">
        <div className="flex items-end gap-2">
          <textarea
            rows={1}
            value={value}
            onChange={(event) => onChange(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                onSubmit();
              }
            }}
            placeholder="Vorbește cu Hermes..."
            className="max-h-40 min-h-12 flex-1 resize-none bg-transparent px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500"
          />
          <button
            type="button"
            onClick={onSubmit}
            disabled={busy || !value.trim()}
            className="mb-1 mr-1 inline-flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-400 text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:bg-slate-800 disabled:text-slate-500"
            aria-label="Trimite mesajul"
          >
            {busy ? <LoaderCircle className="animate-spin" size={18} /> : <ArrowUp size={18} />}
          </button>
        </div>
        <div className="px-4 pb-1 text-[11px] text-slate-600">
          Enter pentru trimitere · Shift+Enter pentru linie nouă
        </div>
      </div>
    </div>
  );
}
