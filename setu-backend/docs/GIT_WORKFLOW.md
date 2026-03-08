# Git workflow — backend vs frontend (no mashup)

Repo: **https://github.com/arjun-kale/setu**

Your friend pushes **frontend on `main`**. You push **backend on branch `backend`** so `main` stays untouched (no mashup).

---

## Push backend to setu repo (no mashup with main)

- **`main`** = frontend only (don’t push backend here).
- **`backend`** = your backend code; push here so they can pull without touching main.

### First-time setup and push

1. **Go to your project and init + link to setu:**
   ```bash
   cd d:\Projects\Setu-Backend
   git init
   git remote add origin https://github.com/arjun-kale/setu.git
   git fetch origin
   git checkout -b backend origin/main
   ```
   This gives you a `backend` branch that starts from current frontend (main).

2. **Add only backend-related files** (never add `.env`):
   ```bash
   git add backend/ PROJECT_CONTEXT.md docs/
   git status
   ```
   Confirm **.env** does not appear. If it does, ensure `backend/.gitignore` has `.env`.

3. **Commit and push to branch `backend`:**
   ```bash
   git commit -m "Backend: FastAPI, config, DB schema, health, plan"
   git push -u origin backend
   ```

4. **Done.** Main is unchanged. Your friend can pull your work with:
   ```bash
   git fetch origin
   git checkout backend
   ```

### Later: push more backend changes

```bash
git checkout backend
git add backend/ PROJECT_CONTEXT.md docs/
git commit -m "Backend: your message"
git push origin backend
```

### Your friend (frontend)

- Keeps working on **`main`**, push/pull as usual.
- To **see your backend** without merging:
  ```bash
  git fetch origin
  git checkout backend    # or just look at GitHub branch backend
  ```
- They can pull `backend` branch to run the backend locally; `main` stays frontend-only.

---

## When to merge (later)

When you’re both ready to have one combined codebase:

- Merge **`backend` into `main`** (or the other way, by agreement).
- Do it in a pull request so you can fix conflicts (e.g. both added a README) in one place.

---

## Summary

| Branch  | Who uses it   | Content        |
|---------|---------------|----------------|
| `main`  | Friend        | Frontend       |
| `backend` | You         | Backend (this stage + next tasks) |

Push your current backend to **`backend`**, not `main`. Friend stays on `main`; no merge until you decide.
