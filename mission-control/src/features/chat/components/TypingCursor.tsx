interface TypingCursorProps {
  className?: string;
}

export default function TypingCursor({
  className = "",
}: TypingCursorProps) {
  return (
    <span
      aria-hidden="true"
      className={`inline-block h-4 w-1 animate-pulse rounded-full bg-cyan-300 ${className}`}
    />
  );
}
