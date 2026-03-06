# AI Chatbot

A full-featured AI chatbot built with Next.js, the AI SDK, and PostgreSQL.

## Features

- **Next.js App Router** — Server components, server actions, and optimized routing
- **AI SDK** — Unified API for generating text, structured objects, and tool calls with LLMs
- **shadcn/ui + Tailwind CSS** — Clean, accessible UI components
- **PostgreSQL** — Chat history and user data persistence
- **Auth.js** — Secure authentication with credentials
- **Artifacts** — Create and edit documents, code, and spreadsheets inline
- **File uploads** — Image attachments stored locally

## Getting Started

### Prerequisites

- Node.js 18+
- PostgreSQL database
- OpenAI API key
- pnpm

### Setup

1. Clone & install dependencies:

```bash
pnpm install
```

2. Copy `.env.example` to `.env.local` and fill in your values:

```bash
cp .env.example .env.local
```

3. Set up the database:

```bash
pnpm db:migrate
```

4. Start the dev server:

```bash
pnpm dev
```

The app will be running at [localhost:3000](http://localhost:3000).

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AUTH_SECRET` | Random secret for auth sessions (`openssl rand -base64 32`) |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `POSTGRES_URL` | PostgreSQL connection string |
| `REDIS_URL` | (Optional) Redis URL for resumable streams |
