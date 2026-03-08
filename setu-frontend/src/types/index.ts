export type Language =
  | "hi" | "mai" | "bho" | "mr" | "ta" | "te"
  | "bn" | "gu" | "kn" | "ml" | "pa" | "or"
  | "as" | "ur" | "sa" | "kok" | "doi" | "mni"
  | "sat" | "ks" | "ne" | "sd" | "en";

export type AgentType =
  | "scheme_compass"
  | "docbridge"
  | "sanjeevani"
  | "bhasha_general";

export type MessageRole = "user" | "assistant";

export type MessageType = "text" | "voice" | "document" | "scheme_result";

export interface Message {
  id: string;
  role: MessageRole;
  type: MessageType;
  content: string;
  audioUrl?: string;
  timestamp: Date;
  agent?: AgentType;
  isLoading?: boolean;
}

export interface ChatSession {
  id: string;
  title: string;
  lastMessage: string;
  lastMessageAt: Date;
  language: Language;
  messageCount: number;
}

export interface UserProfile {
  id: string;
  phone: string;
  name?: string;
  language: Language;
  state?: string;
  district?: string;
  occupation?: string;
}

export interface Scheme {
  id: string;
  name: string;
  nameLocal?: string;
  description: string;
  keyBenefit: string;
  eligibilityScore: number;
  applyUrl?: string;
  category: string;
  state?: string;
}

// ─── Backend-aligned types ──────────────────────────────

export interface EligibilityRuleOut {
  age_limit: string | null;
  income_limit: string | null;
  state: string | null;
  occupation: string | null;
}

export interface SchemeOut {
  id: number;
  name: string;
  description: string | null;
  benefits: string | null;
  eligibility_rules: EligibilityRuleOut[];
}

export interface BackendMessage {
  response: string;
  session_id: string;
}

export interface SkillOut {
  id: string;
  title: string;
  description: string;
  content: string;
  topics: string[];
}

export interface EligibilityRequest {
  age?: number | null;
  income?: number | null;
  state?: string | null;
  occupation?: string | null;
}
