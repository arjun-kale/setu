"use client";

import { useCallback, useRef, useState } from "react";

export type RecordingState = "idle" | "recording" | "processing";

interface UseVoiceRecorderReturn {
  recordingState: RecordingState;
  startRecording: () => Promise<void>;
  stopRecording: () => void;
  audioBlob: Blob | null;
  error: string | null;
}

export function useVoiceRecorder(): UseVoiceRecorderReturn {
  const [recordingState, setRecordingState] = useState<RecordingState>("idle");
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [error, setError] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = useCallback(async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        setAudioBlob(blob);
        console.log("[SETU] Audio recorded:", blob.size, "bytes");
        stream.getTracks().forEach((track) => track.stop());
        setRecordingState("idle");
      };

      mediaRecorder.start();
      setRecordingState("recording");
    } catch (err) {
      setError("माइक की अनुमति नहीं मिली। कृपया माइक एक्सेस दें।");
      setRecordingState("idle");
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && recordingState === "recording") {
      setRecordingState("processing");
      mediaRecorderRef.current.stop();
    }
  }, [recordingState]);

  return { recordingState, startRecording, stopRecording, audioBlob, error };
}
