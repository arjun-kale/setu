import type {
  BackendMessage,
  EligibilityRequest,
  SchemeOut,
  SkillOut,
} from "@/types";

// ─── Base config ────────────────────────────────────────

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// ─── Error type ─────────────────────────────────────────

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public detail?: string,
  ) {
    super(message);
  }
}

// ─── Generic request helper ─────────────────────────────

async function request<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(
      res.status,
      body.message ?? "Request failed",
      body.detail,
    );
  }

  return res.json();
}

// ─── Health ─────────────────────────────────────────────

export async function checkHealth(): Promise<{
  status: string;
  timestamp: string;
  service: string;
}> {
  return request("/health");
}

// ─── Auth ───────────────────────────────────────────────

export async function register(payload: {
  email: string;
  password: string;
  name?: string;
}): Promise<{
  user_id: string;
  email: string;
  token: string;
  message: string;
}> {
  return request("/api/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function login(payload: {
  email: string;
  password: string;
}): Promise<{
  user_id: string;
  email: string;
  token: string;
  message: string;
}> {
  return request("/api/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

// ─── Chat ───────────────────────────────────────────────

export async function sendMessage(payload: {
  user_id: string;
  message: string;
  language?: string;
}): Promise<BackendMessage> {
  return request("/api/chat", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

// ─── Voice ──────────────────────────────────────────────

export interface VoiceResponse {
  audio: Blob;
  transcript: string;
  responseText: string;
}

export async function sendVoiceMessage(
  audioBlob: Blob,
  userId: string = "anonymous",
  language: string = "en-IN",
): Promise<VoiceResponse> {
  const form = new FormData();
  form.append("audio", audioBlob, "recording.webm");
  form.append("user_id", userId);
  form.append("language", language);

  const res = await fetch(`${BASE_URL}/api/voice`, {
    method: "POST",
    body: form,
    // Content-Type omitted — browser sets multipart boundary automatically
  });

  if (!res.ok) {
    throw new ApiError(res.status, "Voice processing failed");
  }

  const audio = await res.blob();
  const transcript = res.headers.get("X-Transcript") ?? "";
  const responseText = res.headers.get("X-Response-Text") ?? "";

  return { audio, transcript, responseText };
}

// ─── Schemes ────────────────────────────────────────────

export async function getSchemes(
  query?: string,
): Promise<{ schemes: SchemeOut[] }> {
  const params = query ? `?q=${encodeURIComponent(query)}` : "";
  return request(`/api/schemes${params}`);
}

export async function getScheme(
  schemeId: number,
): Promise<SchemeOut> {
  return request(`/api/schemes/${schemeId}`);
}

// ─── Eligibility ────────────────────────────────────────

export async function checkEligibility(
  payload: EligibilityRequest,
): Promise<{ schemes: SchemeOut[] }> {
  return request("/api/check-eligibility", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

// ─── Skills ─────────────────────────────────────────────

export async function getSkills(): Promise<SkillOut[]> {
  return request("/api/skills");
}

export async function getSkill(
  skillId: string,
): Promise<SkillOut> {
  return request(`/api/skills/${skillId}`);
}

// ─── User profile ───────────────────────────────────────

export async function updateUserProfile(
  userId: string,
  payload: {
    age?: number | null;
    income?: number | null;
    state?: string | null;
    occupation?: string | null;
  },
): Promise<{ message: string; profile: Record<string, unknown> }> {
  return request(`/api/users/${userId}/profile`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}
