"use client";

import { useEffect, useRef } from "react";
import type { Message } from "@/types";
import MessageBubble from "./MessageBubble";

interface MessageListProps {
  messages: Message[];
}

export default function MessageList({ messages }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-3 px-4">
        <p className="text-5xl">🎙️</p>
        <p className="text-text-primary font-semibold text-xl text-center">
          बोलकर शुरू करें
        </p>
        <p className="text-text-dim text-base text-center max-w-sm">
          नीचे माइक बटन दबाएं और अपनी समस्या बताएं। SETU आपकी भाषा में जवाब देगा।
        </p>
        <div className="flex flex-wrap gap-2 justify-center mt-4 max-w-sm">
          {["मेरी पात्रता जाँचें", "दस्तावेज़ पढ़ें", "कौशल सीखें"].map((prompt) => (
            <button
              className="text-sm px-4 py-2 rounded-full border border-border
                         bg-white text-text-primary hover:border-saffron
                         hover:text-saffron transition-colors"
              key={prompt}
            >
              {prompt}
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col py-4 min-h-full">
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}
      <div className="h-4" ref={bottomRef} />
    </div>
  );
}
