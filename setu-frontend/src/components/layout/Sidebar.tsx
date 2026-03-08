"use client";

import type { ChatSession } from "@/types";

interface SidebarProps {
  activeSessionId?: string;
}

const MOCK_SESSIONS: ChatSession[] = [
  {
    id: "1",
    title: "PM Vishwakarma Yojana",
    lastMessage: "आप इस योजना के लिए पात्र हैं",
    lastMessageAt: new Date(),
    language: "hi",
    messageCount: 6,
  },
  {
    id: "2",
    title: "Kisan Credit Card",
    lastMessage: "आवेदन की प्रक्रिया शुरू करें",
    lastMessageAt: new Date(Date.now() - 86_400_000),
    language: "hi",
    messageCount: 4,
  },
];

export default function Sidebar({ activeSessionId }: SidebarProps) {
  return (
    <aside
      className="w-[280px] flex-shrink-0 flex flex-col h-full"
      style={{ backgroundColor: "#1A1560" }}
    >
      {/* Logo area */}
      <div className="h-16 flex items-center px-5 flex-shrink-0">
        <div>
          <p className="text-white font-bold text-xl tracking-wide">SETU</p>
          <p className="text-white/50 text-xs">आपका सहायक</p>
        </div>
      </div>

      {/* New Chat button */}
      <div className="px-4 pb-3 flex-shrink-0">
        <button
          className="w-full h-11 rounded-lg font-semibold text-white text-sm
                     transition-opacity hover:opacity-90 active:opacity-80"
          style={{ backgroundColor: "#E8610A" }}
        >
          + नई बातचीत
        </button>
      </div>

      {/* Divider */}
      <div className="mx-4 border-t border-white/10 flex-shrink-0" />

      {/* Chat history */}
      <div className="flex-1 overflow-y-auto py-2">
        <p className="text-white/40 text-xs font-medium px-4 py-2 uppercase tracking-wider">
          पिछली बातचीत
        </p>
        {MOCK_SESSIONS.map((session) => (
          <button
            className={`w-full text-left px-4 py-3 rounded-lg mx-1 transition-colors
              ${
                activeSessionId === session.id
                  ? "bg-white/15 text-white"
                  : "text-white/70 hover:bg-white/10 hover:text-white"
              }`}
            key={session.id}
          >
            <p className="text-sm font-medium truncate">{session.title}</p>
            <p className="text-xs truncate mt-0.5 opacity-60">
              {session.lastMessage}
            </p>
          </button>
        ))}
      </div>

      {/* Profile strip */}
      <div className="h-12 border-t border-white/10 flex items-center px-4 flex-shrink-0">
        <div
          className="w-7 h-7 rounded-full bg-saffron flex items-center justify-center
                        text-white text-xs font-bold flex-shrink-0"
        >
          R
        </div>
        <p className="text-white/70 text-sm ml-2.5 truncate">+91 98765 43210</p>
      </div>
    </aside>
  );
}
