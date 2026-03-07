# Rural AI Assistant — Backend Project Context

This document describes the **backend** of the Rural AI Assistant: its purpose, users, features, and technical architecture. Use it to understand scope and design when building or extending the backend.

---

## 1. Project Overview

**Project name:** Rural AI Assistant  

**Purpose:** Help citizens (especially in rural areas) understand government schemes, learn digital skills, and complete digital tasks using **voice or chat** in **local languages**.

**Backend role:** The backend powers all client interactions (web app and WhatsApp), handles AI orchestration, scheme data, eligibility logic, voice processing, and messaging.

---

## 2. Users & Access Channels

| Channel        | Description |
|----------------|-------------|
| **Web application** | Users with internet access interact via a web UI (chat and/or voice). |
| **WhatsApp**       | Users without smartphones or preferring WhatsApp can use the same assistant via WhatsApp. |

The backend must support both channels through a consistent set of APIs and shared business logic.

---

## 3. Main Features (Backend Scope)

### 3.1 Government scheme discovery

- **User intent:** Find schemes by topic, sector, or keyword (e.g. “What schemes are available for farmers?”).
- **Backend responsibility:** Query scheme data, optionally use RAG (vector search) for natural-language questions, and return relevant schemes with clear, local-language-friendly content.

### 3.2 Scheme eligibility checker

- **User input:** Age, income, state, occupation, and other relevant attributes.
- **Backend responsibility:** Apply eligibility rules (stored in PostgreSQL), match user profile to schemes, and return **eligible schemes** (and optionally why others are not eligible).

### 3.3 Voice assistant

- **User interaction:** Speak in local languages; receive **voice responses**.
- **Backend responsibility:**  
  - Accept audio (or receive transcript from client).  
  - Use **Google Speech-to-Text** for transcription.  
  - Process via the same AI/chat pipeline as text.  
  - Use **Amazon Polly** for text-to-speech responses.  
  - Store audio in **AWS S3** as required.

### 3.4 WhatsApp access

- **User interaction:** Chat (and possibly voice) over WhatsApp.
- **Backend responsibility:**  
  - **Twilio WhatsApp API** for sending/receiving messages.  
  - Webhook endpoint to receive incoming WhatsApp events.  
  - Map WhatsApp conversations to the same chat/session and AI pipeline as the web app.

---

## 4. Architecture Overview

### 4.1 Backend framework

- **FastAPI** — All HTTP APIs, webhooks, and server logic.

### 4.2 Data stores

| Store       | Use case |
|------------|----------|
| **DynamoDB**   | User sessions, chat history, conversation state. |
| **PostgreSQL** | Government scheme metadata, eligibility rules, reference data. |

### 4.3 Voice pipeline

| Component              | Role |
|------------------------|------|
| **Google Speech-to-Text** | Transcribe user audio (local languages). |
| **Amazon Polly**          | Synthesize voice responses from text. |
| **AWS S3**                | Store audio files (input/output as needed). |

### 4.4 Messaging

| Component           | Role |
|--------------------|------|
| **Twilio WhatsApp API** | Send/receive WhatsApp messages; backend exposes a **webhook** for incoming events. |

### 4.5 AI & RAG

| Component        | Role |
|-----------------|------|
| **LangGraph**   | Agent orchestration (routing, tools, multi-step flows). |
| **Pinecone**    | Vector database for RAG over scheme documents and FAQs. |

---

## 5. APIs the Backend Exposes

The backend exposes at least the following API surfaces:

| API / area           | Purpose |
|----------------------|--------|
| **Chat**             | Text-based conversation (web and/or WhatsApp server-side logic). Session-aware; may use LangGraph + RAG. |
| **Voice**            | Submit audio and receive audio (or transcript + TTS URL). Integrates Speech-to-Text, chat pipeline, Polly, S3. |
| **Scheme discovery** | Search/browse schemes by query or filters; can be used by chat/agent as a tool or as a direct API. |
| **Eligibility checking** | Submit user attributes; return list of eligible schemes (and optionally reasons). |
| **WhatsApp webhook** | HTTP endpoint for Twilio to deliver incoming WhatsApp messages; backend processes and responds via Twilio. |

Additional endpoints may be needed for health, auth, admin, or internal use.

---

## 6. Summary for Developers

- **Stack:** FastAPI, DynamoDB (sessions/chat), PostgreSQL (schemes/eligibility), S3 (audio), Twilio (WhatsApp), Google Speech-to-Text, Amazon Polly, LangGraph, Pinecone.
- **Channels:** Web app and WhatsApp share the same backend APIs and logic where possible.
- **Core flows:** Chat, voice, scheme discovery, eligibility check, WhatsApp webhook — all designed for local-language and low-literacy-friendly use cases.

Use this document as the single source of truth for **backend** purpose and architecture when implementing or reviewing code.
