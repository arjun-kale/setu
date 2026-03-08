import { create } from "zustand";
import type { ChatSession, Message } from "@/types";

interface ChatStore {
  sessions: ChatSession[];
  activeSessionId: string | null;
  messages: Record<string, Message[]>;

  setActiveSession: (id: string) => void;
  addMessage: (sessionId: string, message: Message) => void;
  setMessageLoading: (
    sessionId: string,
    messageId: string,
    loading: boolean
  ) => void;
  createSession: () => string;
}

let sessionCounter = 1;

export const useChatStore = create<ChatStore>((set) => ({
  sessions: [],
  activeSessionId: null,
  messages: {},

  setActiveSession: (id) => set({ activeSessionId: id }),

  addMessage: (sessionId, message) =>
    set((state) => ({
      messages: {
        ...state.messages,
        [sessionId]: [...(state.messages[sessionId] ?? []), message],
      },
      sessions: state.sessions.map((s) =>
        s.id === sessionId
          ? {
              ...s,
              lastMessage: message.content || "🎙️ Voice",
              lastMessageAt: message.timestamp,
            }
          : s
      ),
    })),

  setMessageLoading: (sessionId, messageId, loading) =>
    set((state) => ({
      messages: {
        ...state.messages,
        [sessionId]: (state.messages[sessionId] ?? []).map((m) =>
          m.id === messageId ? { ...m, isLoading: loading } : m
        ),
      },
    })),

  createSession: () => {
    const id = `session-${Date.now()}`;
    const session: ChatSession = {
      id,
      title: `बातचीत ${sessionCounter++}`,
      lastMessage: "",
      lastMessageAt: new Date(),
      language: "hi",
      messageCount: 0,
    };
    set((state) => ({
      sessions: [session, ...state.sessions],
      activeSessionId: id,
      messages: { ...state.messages, [id]: [] },
    }));
    return id;
  },
}));
