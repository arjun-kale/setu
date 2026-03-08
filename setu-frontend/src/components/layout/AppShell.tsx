"use client";

import { useRouter } from "next/navigation";
import InputBar from "@/components/chat/InputBar";
import { useChatStore } from "@/store/chatStore";
import type { Message } from "@/types";
import Sidebar from "./Sidebar";
import TopBar from "./TopBar";

interface AppShellProps {
  children: React.ReactNode;
  sessionId?: string;
}

export default function AppShell({ children, sessionId }: AppShellProps) {
  const router = useRouter();
  const { activeSessionId, addMessage, createSession } = useChatStore();

  const handleSendText = (text: string) => {
    let targetSessionId = activeSessionId;

    if (!targetSessionId) {
      targetSessionId = createSession();
      router.push(`/chat/${targetSessionId}`);
    }

    const userMessage: Message = {
      id: `msg-${Date.now()}`,
      role: "user",
      type: "text",
      content: text,
      timestamp: new Date(),
    };

    addMessage(targetSessionId, userMessage);

    // Simulate loading assistant reply
    const loadingMessage: Message = {
      id: `msg-${Date.now()}-loading`,
      role: "assistant",
      type: "text",
      content: "",
      isLoading: true,
      timestamp: new Date(),
      agent: "bhasha_general",
    };
    addMessage(targetSessionId, loadingMessage);

    console.log("[SETU] Sending to backend:", text);
  };

  const handleSendVoice = (blob: Blob) => {
    console.log("[SETU] Voice blob ready for backend:", blob.size, "bytes");
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden">
      <Sidebar activeSessionId={activeSessionId ?? undefined} />
      <div className="flex flex-col flex-1 min-w-0">
        <TopBar />
        <main className="flex-1 overflow-y-auto">{children}</main>
        <InputBar onSendText={handleSendText} onSendVoice={handleSendVoice} />
      </div>
    </div>
  );
}
