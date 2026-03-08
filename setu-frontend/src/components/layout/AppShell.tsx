"use client";

import { useRouter } from "next/navigation";
import InputBar from "@/components/chat/InputBar";
import { useChatStore } from "@/store/chatStore";
import type { Message } from "@/types";
import { sendMessage } from "@/lib/api";
import Sidebar from "./Sidebar";
import TopBar from "./TopBar";

interface AppShellProps {
  children: React.ReactNode;
  sessionId?: string;
}

export default function AppShell({ children, sessionId }: AppShellProps) {
  const router = useRouter();
  const { activeSessionId, addMessage, replaceMessage, createSession } = useChatStore();

  const handleSendText = async (text: string) => {
    let targetSessionId = activeSessionId;

    if (!targetSessionId) {
      targetSessionId = createSession();
      router.push(`/chat/${targetSessionId}`);
    }

    // Optimistic user message
    const userMessage: Message = {
      id: `msg-${Date.now()}`,
      role: "user",
      type: "text",
      content: text,
      timestamp: new Date(),
    };
    addMessage(targetSessionId, userMessage);

    // Loading placeholder
    const loadingId = `msg-${Date.now() + 1}-loading`;
    addMessage(targetSessionId, {
      id: loadingId,
      role: "assistant",
      type: "text",
      content: "",
      isLoading: true,
      timestamp: new Date(),
      agent: "bhasha_general",
    });

    try {
      const data = await sendMessage({
        user_id: "demo-user-001",
        message: text,
        language: "hi",
      });

      replaceMessage(targetSessionId, loadingId, {
        id: loadingId,
        role: "assistant",
        type: "text",
        content: data.response,
        isLoading: false,
        timestamp: new Date(),
        agent: "bhasha_general",
      });
    } catch (err) {
      replaceMessage(targetSessionId, loadingId, {
        id: loadingId,
        role: "assistant",
        type: "text",
        content: "माफ करें, कुछ गलत हुआ। कृपया दोबारा कोशिश करें।",
        isLoading: false,
        timestamp: new Date(),
      });
      console.error("[SETU] sendMessage error:", err);
    }
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
