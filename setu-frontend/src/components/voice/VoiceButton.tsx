"use client";

import type { RecordingState } from "@/hooks/useVoiceRecorder";

interface VoiceButtonProps {
  recordingState: RecordingState;
  onStartRecording: () => void;
  onStopRecording: () => void;
}

export default function VoiceButton({
  recordingState,
  onStartRecording,
  onStopRecording,
}: VoiceButtonProps) {
  const isRecording = recordingState === "recording";
  const isProcessing = recordingState === "processing";
  const isDisabled = isProcessing;

  const handleClick = () => {
    if (isRecording) onStopRecording();
    else if (recordingState === "idle") onStartRecording();
  };

  return (
    <button
      aria-label={isRecording ? "रिकॉर्डिंग रोकें" : "बोलना शुरू करें"}
      className="relative w-[52px] h-[52px] rounded-full flex items-center
                 justify-center flex-shrink-0 transition-transform duration-150
                 disabled:opacity-50 disabled:cursor-not-allowed
                 hover:scale-105 active:scale-95"
      disabled={isDisabled}
      onClick={handleClick}
      style={{
        backgroundColor: isRecording ? "#E8610A" : "#1A1560",
      }}
    >
      {/* Pulsing ring when recording */}
      {isRecording && (
        <span
          className="absolute inset-0 rounded-full animate-ping opacity-30"
          style={{ backgroundColor: "#E8610A" }}
        />
      )}

      {/* Icon */}
      <span className="text-white text-xl relative z-10">
        {isProcessing ? "⏳" : isRecording ? "⏹" : "🎙️"}
      </span>
    </button>
  );
}
