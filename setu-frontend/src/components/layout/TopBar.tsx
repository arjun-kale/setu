"use client";

export default function TopBar() {
  return (
    <header
      className="h-14 flex items-center justify-between px-5
                       bg-white border-b border-border flex-shrink-0"
    >
      <div>
        <p className="font-semibold text-text-primary text-sm">
          Scheme Compass
        </p>
        <p className="text-text-dim text-xs">सरकारी योजनाएं खोजें</p>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-xs text-text-dim bg-surface-2 px-2.5 py-1 rounded-full">
          हिंदी
        </span>
      </div>
    </header>
  );
}
