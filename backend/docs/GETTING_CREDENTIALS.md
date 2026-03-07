# Step-by-Step: Getting Your .env Credentials

Use this guide to obtain each value for your `backend/.env` file. **Never commit `.env` or share production secrets in chat.**

---

## 1. AWS (DynamoDB, S3, Polly)

You need an AWS account.

### Step 1.1 — Sign in to AWS
- Go to [https://aws.amazon.com](https://aws.amazon.com) and sign in (or create an account).

### Step 1.2 — Open IAM and create a user (if you don’t have one)
- In the AWS Console search bar, type **IAM** and open **IAM**.
- Go to **Users** → **Create user**.
- Choose a name (e.g. `rural-ai-backend`) → **Next**.
- **Attach policies:** e.g. `AmazonDynamoDBFullAccess`, `AmazonS3FullAccess`, `AmazonPollyFullAccess` (or create a custom policy with minimal permissions).
- Create user.

### Step 1.3 — Create access keys
- Click the new user → **Security credentials** tab.
- Under **Access keys** → **Create access key**.
- Choose **Application running outside AWS** (or CLI) → **Next** → **Create access key**.
- **Copy and save:**
  - **Access key ID** → use as `AWS_ACCESS_KEY_ID`
  - **Secret access key** → use as `AWS_SECRET_ACCESS_KEY` (shown only once).

### Step 1.4 — Region
- Use the region where you will create DynamoDB tables and S3 bucket (e.g. `ap-south-1` for Mumbai).
- Set `AWS_REGION=ap-south-1` (or your chosen region).

**You give me:** `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` (or say “use defaults” and I’ll use the values you already have).

---

## 2. PostgreSQL (POSTGRES_URL)

You need a running PostgreSQL database and a connection URL.

### Option A — Local PostgreSQL
- Install PostgreSQL (e.g. from [postgresql.org](https://www.postgresql.org/download/)).
- Create a database, e.g. `ruralai`.
- URL format: `postgresql://USERNAME:PASSWORD@localhost:5432/ruralai`
- Replace `USERNAME`, `PASSWORD`, and DB name if different.

### Option B — Cloud (e.g. AWS RDS, Supabase, Neon)
- Create a PostgreSQL instance and get the connection string from the provider’s dashboard.
- It usually looks like: `postgresql://user:password@host:5432/dbname`
- Use that as `POSTGRES_URL`.

**You give me:** The full `POSTGRES_URL` (you can redact the password as `***` and type it locally into `.env` yourself if you prefer).

---

## 3. S3 bucket (S3_BUCKET_NAME)

- In AWS Console go to **S3** → **Create bucket**.
- Choose a unique name (e.g. `rural-ai-audio-yourname`) and the same region as above.
- Create bucket.
- Use that bucket name as `S3_BUCKET_NAME`.

**You give me:** The bucket name (e.g. `rural-ai-audio` or `rural-ai-audio-yourname`).

---

## 4. Twilio (WhatsApp)

### Step 4.1 — Twilio account
- Go to [https://www.twilio.com](https://www.twilio.com) and sign up.

### Step 4.2 — Account SID and Auth Token
- In Twilio Console **Dashboard**, copy:
  - **Account SID** → `TWILIO_ACCOUNT_SID`
  - **Auth Token** → `TWILIO_AUTH_TOKEN` (click “Show” to reveal).

### Step 4.3 — WhatsApp number
- In Twilio Console go to **Messaging** → **Try it out** → **Send a WhatsApp message**.
- Or go to **Phone Numbers** → **Manage** → **WhatsApp senders**.
- Use the WhatsApp-enabled number Twilio gives you (e.g. `whatsapp:+14155238886` for sandbox).
- Set `TWILIO_WHATSAPP_NUMBER=whatsapp:+1XXXXXXXXXX` (with country code, no spaces).

**You give me:** `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_NUMBER` (or say “leave Twilio empty” and I’ll leave them blank for later).

---

## 5. Google Speech-to-Text (GOOGLE_STT_API_KEY)

### Step 5.1 — Google Cloud account
- Go to [https://console.cloud.google.com](https://console.cloud.google.com).

### Step 5.2 — Enable Speech-to-Text API
- Select or create a project.
- Go to **APIs & Services** → **Library**.
- Search for **Speech-to-Text API** → **Enable**.

### Step 5.3 — Create an API key
- **APIs & Services** → **Credentials** → **Create credentials** → **API key**.
- Copy the key → use as `GOOGLE_STT_API_KEY`.
- (Optional) Restrict the key to Speech-to-Text only for security.

**You give me:** `GOOGLE_STT_API_KEY` (or say “leave Google STT empty” and I’ll leave it blank for later).

---

## What to send back

Reply with one of the following:

1. **Paste your values** (only if you’re okay with them being in chat; prefer dev/test keys):
   - `AWS_ACCESS_KEY_ID=...`
   - `AWS_SECRET_ACCESS_KEY=...`
   - … etc.

2. **Or say:** “I’ll fill .env myself” — then create `backend/.env` and paste the contents of `.env.example`, then replace the right-hand sides with your real values.

3. **Or give only non-secret values** and keep secrets local:
   - e.g. “Use region ap-south-1, bucket rural-ai-audio, Postgres URL postgresql://me:***@localhost:5432/ruralai”
   - Then add `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `TWILIO_*`, `GOOGLE_STT_API_KEY` yourself in `.env`.

After you provide what you want to share, your `backend/.env` can be updated (or you update it locally with the guide above).
