# Git Plan — Fix Accidental Push & Work Together

## Current Situation

| Repo | Branch | Content | Issue |
|------|--------|---------|-------|
| **arjun-kale/setu** (friend) | `main` | Frontend only | ✓ OK |
| **arjun-kale/setu** (friend) | `backend` | Frontend + backend mixed | ❌ Accidental push |
| **cybercomet-07/setu-backend** (you) | `main` | Backend only | ✓ OK |

The `backend` branch on friend's repo has frontend folders (`components/`, `hooks/`, `lib/`, `artifacts/`) that shouldn't be there.

---

## Plan — 3 Steps

### Step 1: Commit & Push to Your Repo (setu-backend)

Your local backend has new features (voice API, etc.) not yet pushed.

```bash
cd d:\Projects\Setu-Backend
git add -A
git status   # Confirm .env is NOT staged
git commit -m "Add voice API (Whisper STT, Polly TTS), update docs"
git push setu-backend backend:main
```

**Result:** cybercomet-07/setu-backend has the latest backend.

---

### Step 2: Fix Friend's Repo — Replace Messy Backend Branch

Force-push your clean backend-only to friend's `backend` branch. This **replaces** the messy content.

```bash
git push origin backend --force
```

**Result:** arjun-kale/setu `backend` branch = clean backend-only (no frontend).

---

### Step 3: How You & Friend Work Together

| Who | Repo/Branch | What they do |
|-----|-------------|--------------|
| **You** | cybercomet-07/setu-backend (main) | Backend development, push here |
| **Friend** | arjun-kale/setu (main) | Frontend development, push here |

**Friend runs both locally:**

```bash
# Terminal 1 — Backend (from your repo or friend's backend branch)
git clone https://github.com/cybercomet-07/setu-backend.git setu-backend
cd setu-backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Terminal 2 — Frontend (friend's repo)
git clone https://github.com/arjun-kale/setu.git setu-frontend
cd setu-frontend
git checkout main
npm install
npm run dev   # Runs on port 3000
```

Frontend calls `http://localhost:8000/api/...` for chat, voice, schemes, eligibility.

**No mashup:** Backend and frontend stay in separate folders/repos. Clean separation.

---

## Optional: Sync Backend to Friend's Repo

If friend wants backend in arjun-kale/setu (e.g. to have one repo):

- You push to **setu-backend** (your repo) = source of truth
- Periodically: you can also push to **origin backend** so friend's repo has an up-to-date `backend` branch
- Friend pulls `backend` when needed: `git fetch origin && git checkout backend`

---

## Summary

| Action | Command |
|--------|---------|
| Push latest to your repo | `git push setu-backend backend:main` |
| Fix friend's backend branch | `git push origin backend --force` |
| Friend gets backend | Clone setu-backend OR checkout backend on setu |
| Friend gets frontend | Clone setu, checkout main |

**Do NOT push to `main` on arjun-kale/setu** — that's friend's frontend. Only push to `backend` branch.
