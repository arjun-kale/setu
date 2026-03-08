"use client";

import type { Message } from "@/types";

interface MessageBubbleProps {
  message: Message;
}

function formatTime(date: Date): string {
  return date.toLocaleTimeString("hi-IN", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function AgentChip({ agent }: { agent: string }) {
  const labels: Record<string, string> = {
    scheme_compass: "Scheme Compass",
    docbridge: "DocBridge",
    sanjeevani: "Sanjeevani",
    bhasha_general: "SETU",
  };
  return (
    <span
      className="text-xs px-2 py-0.5 rounded-full font-medium"
      style={{ backgroundColor: "#EEF2FF", color: "#1A1560" }}
    >
      {labels[agent] ?? "SETU"}
    </span>
  );
}

function LoadingDots() {
  return (
    <div className="flex items-center gap-1.5 py-1">
      {[0, 1, 2].map((i) => (
        <span
          className="w-2 h-2 rounded-full bg-text-dim animate-bounce"
          key={i}
          style={{ animationDelay: `${i * 150}ms` }}
        />
      ))}
    </div>
  );
}

function VoiceWaveform() {
  const bars = [3, 6, 10, 8, 12, 7, 9, 5, 11, 4, 8, 6, 10, 7, 4];
  return (
    <div className="flex items-center gap-1.5">
      <button
        className="w-8 h-8 rounded-full flex items-center justify-center
                   flex-shrink-0 text-white text-xs"
        style={{ backgroundColor: "#E8610A" }}
      >
        ▶
      </button>
      <div className="flex items-end gap-0.5 h-8">
        {bars.map((h, i) => (
          <div
            className="w-1 rounded-full bg-text-dim/40"
            key={i}
            style={{ height: `${h}px` }}
          />
        ))}
      </div>
      <span className="text-xs text-text-dim ml-1">0:08</span>
    </div>
  );
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end px-4 py-1.5">
        <div className="max-w-[70%]">
          <div
            className="px-4 py-3 text-white text-lg leading-relaxed"
            style={{
              backgroundColor: "#E8610A",
              borderRadius: "18px 18px 4px 18px",
            }}
          >
            {message.type === "voice" ? <VoiceWaveform /> : message.content}
          </div>
          <p className="text-xs text-text-dim mt-1 text-right">
            {formatTime(message.timestamp)}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-2.5 px-4 py-1.5">
      {/* Avatar */}
      <div
        className="w-8 h-8 rounded-full flex items-center justify-center
                    flex-shrink-0 text-white text-xs font-bold mt-1"
        style={{ backgroundColor: "#1A1560" }}
      >
        S
      </div>
      <div className="max-w-[75%]">
        <div
          className="bg-white border border-border px-4 py-3
                     text-text-primary text-lg leading-relaxed"
          style={{ borderRadius: "18px 18px 18px 4px" }}
        >
          {message.isLoading ? (
            <LoadingDots />
          ) : message.type === "voice" ? (
            <VoiceWaveform />
          ) : (
            message.content
          )}
        </div>
        <div className="flex items-center gap-2 mt-1">
          <p className="text-xs text-text-dim">
            {formatTime(message.timestamp)}
          </p>
          {message.agent && <AgentChip agent={message.agent} />}
        </div>
      </div>
    </div>
  );
}
