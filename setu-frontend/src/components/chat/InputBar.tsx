"use client";

import { useState } from "react";
import VoiceButton from "@/components/voice/VoiceButton";
import { useVoiceRecorder } from "@/hooks/useVoiceRecorder";

interface InputBarProps {
  onSendText: (text: string) => void;
  onSendVoice: (blob: Blob) => void;
  disabled?: boolean;
}

export default function InputBar({
  onSendText,
  onSendVoice,
  disabled = false,
}: InputBarProps) {
  const [text, setText] = useState("");
  const { recordingState, startRecording, stopRecording, error } =
    useVoiceRecorder();

  const handleSendText = () => {
    const trimmed = text.trim();
    if (!trimmed) return;
    onSendText(trimmed);
    setText("");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendText();
    }
  };

  const hasText = text.trim().length > 0;

  return (
    <div
      className="h-[72px] border-t border-border bg-white flex items-center
                  px-4 gap-3 flex-shrink-0"
    >
      <VoiceButton
        onStartRecording={startRecording}
        onStopRecording={stopRecording}
        recordingState={recordingState}
      />

      <input
        className="flex-1 h-11 bg-surface-2 border border-border rounded-[22px]
                   px-4 text-base text-text-primary placeholder:text-text-dim
                   outline-none focus:border-indigo transition-colors
                   disabled:opacity-50"
        disabled={disabled || recordingState !== "idle"}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="यहाँ टाइप करें या माइक दबाएं..."
        type="text"
        value={text}
      />

      <button
        className="w-11 h-11 rounded-full flex items-center justify-center
                   flex-shrink-0 text-white text-base transition-opacity"
        disabled={!hasText || disabled}
        onClick={handleSendText}
        style={{
          backgroundColor: "#E8610A",
          opacity: hasText && !disabled ? 1 : 0.4,
        }}
      >
        →
      </button>

      {/* Mic error toast */}
      {error && (
        <div
          className="absolute bottom-20 left-1/2 -translate-x-1/2
                      bg-red-50 border border-red-200 text-red-700
                      text-sm px-4 py-2 rounded-lg shadow-sm"
        >
          {error}
        </div>
      )}
    </div>
  );
}
