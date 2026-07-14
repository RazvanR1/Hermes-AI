import {
  Bot,
  CheckCircle2,
  LoaderCircle,
} from "lucide-react";
import TypingCursor from "./TypingCursor";

const steps = [
  {
    label: "Înțeleg cererea",
    completed: true,
  },
  {
    label: "Selectez skill-ul potrivit",
    completed: true,
  },
  {
    label: "Construiesc planul de execuție",
    completed: false,
  },
];

export default function ThinkingBubble() {
  return (
    <div className="flex justify-start">
      <div className="flex w-full max-w-3xl items-start gap-3">
        <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-xl border border-violet-400/15 bg-violet-400/10 text-violet-300">
          <LoaderCircle
            className="animate-spin"
            size={16}
          />
        </div>

        <div className="w-full rounded-[22px] rounded-bl-md border border-violet-400/15 bg-violet-400/[0.045] px-5 py-4">
          <div className="flex items-center gap-2">
            <Bot
              className="text-violet-300"
              size={15}
            />

            <span className="text-[11px] font-semibold uppercase tracking-[0.16em] text-violet-300">
              Hermes analizează
            </span>

            <TypingCursor />
          </div>

          <div className="mt-4 space-y-2.5">
            {steps.map((step) => (
              <div
                key={step.label}
                className="flex items-center gap-3 text-sm"
              >
                {step.completed ? (
                  <CheckCircle2
                    className="shrink-0 text-emerald-400"
                    size={16}
                  />
                ) : (
                  <LoaderCircle
                    className="shrink-0 animate-spin text-cyan-300"
                    size={16}
                  />
                )}

                <span
                  className={
                    step.completed
                      ? "text-slate-400"
                      : "text-slate-200"
                  }
                >
                  {step.label}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
