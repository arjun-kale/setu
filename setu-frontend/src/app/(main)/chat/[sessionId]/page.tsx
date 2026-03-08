"use client";

import { useEffect } from "react";
import MessageList from "@/components/chat/MessageList";
import { useChatStore } from "@/store/chatStore";

export default function ChatSessionPage({
  params,
}: {
  params: { sessionId: string };
}) {
  const messages = useChatStore((s) => s.messages[params.sessionId] ?? []);
  const setActiveSession = useChatStore((s) => s.setActiveSession);

  useEffect(() => {
    setActiveSession(params.sessionId);
  }, [params.sessionId, setActiveSession]);

  return <MessageList messages={messages} />;
}
