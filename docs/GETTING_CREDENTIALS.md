# Getting Credentials

How to obtain credentials for the Rural AI Assistant backend.

---

## AWS (DynamoDB, S3, Polly)

1. Create an AWS account at https://aws.amazon.com
2. Go to **IAM** → **Users** → **Create user**
3. Attach policies: `AmazonDynamoDBFullAccess`, `AmazonS3FullAccess`, `AmazonPollyFullAccess`
4. Create **Access key** → use `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in `.env`
5. Set `AWS_REGION` in `.env` (e.g. `ap-south-1`)

---

## Speech-to-Text (Voice API)

**Default: Whisper (free, no setup)** — runs locally, no API key or billing.

- Set `STT_PROVIDER=whisper` in `.env` (default)
- Model size: `WHISPER_MODEL_SIZE=base` (or `tiny` for faster, `small` for better quality)
- Supports: en, hi, ta, te, mr, and more

**Optional: Google Speech-to-Text** — only if you need it (requires billing):

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable **Cloud Speech-to-Text API** → Create service account → Download JSON key
3. Set `STT_PROVIDER=google` and `GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json`

---

## Auth (JWT)

Set in `.env`:
- `JWT_SECRET` — random string for signing tokens (use a strong secret in production)
- `JWT_EXPIRE_HOURS` — token expiry (default: 24)

---

## PostgreSQL

1. Install PostgreSQL locally or use a cloud provider (e.g. Supabase, Neon)
2. Create a database and note the connection URL
3. Format: `postgresql://user:password@host:port/database`
4. Put in `.env` as `POSTGRES_URL`

---

## Twilio (WhatsApp Webhook) — Step by Step

You need **3 values** in `.env` for the WhatsApp webhook to work:

| Variable | Example | Where to get it |
|----------|---------|-----------------|
| `TWILIO_ACCOUNT_SID` | `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` | Twilio Console → Account Info |
| `TWILIO_AUTH_TOKEN` | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` | Twilio Console → Account Info |
| `TWILIO_WHATSAPP_NUMBER` | `whatsapp:+14155238886` | Twilio Console → WhatsApp Sandbox |

---

### Step 1: Create a Twilio account

1. Go to [https://www.twilio.com](https://www.twilio.com)
2. Click **Sign up** (or **Log in** if you have an account)
3. Enter email, password, and verify your phone
4. Complete the signup flow

---

### Step 2: Get Account SID and Auth Token

1. After login, you land on the **Twilio Console** (dashboard)
2. On the right side, find **Account Info**
3. Copy:
   - **Account SID** → put in `.env` as `TWILIO_ACCOUNT_SID`
   - **Auth Token** → click **Show** and copy → put in `.env` as `TWILIO_AUTH_TOKEN`

---

### Step 3: Enable WhatsApp Sandbox (free for testing)

1. In the left menu, go to **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Or go to **Messaging** → **Senders** → **WhatsApp senders**
3. Click **Sandbox** (or **Get started with WhatsApp**)
4. You’ll see a **Sandbox** section with:
   - A **phone number** (e.g. `+1 415 523 8886`)
   - A **join code** (e.g. `join happy-tiger`)
5. On your phone:
   - Open WhatsApp
   - Send a message to the sandbox number with the join code (e.g. `join happy-tiger`)
   - You’ll get a confirmation when joined
6. Copy the sandbox number in format: `whatsapp:+14155238886` (no spaces)
7. Put it in `.env` as `TWILIO_WHATSAPP_NUMBER`

---

### Step 4: Set the webhook URL (after backend is deployed)

1. In Twilio Console → **Messaging** → **WhatsApp Sandbox**
2. Under **Sandbox configuration**, find **When a message comes in**
3. Set the URL to your backend webhook, e.g.:
   - Local (with ngrok): `https://xxxx.ngrok.io/webhooks/whatsapp`
   - Production: `https://your-api.com/webhooks/whatsapp`
4. Set method to **HTTP POST**
5. Save

**Note:** Twilio must reach your server over HTTPS. For local testing, use [ngrok](https://ngrok.com) to expose `http://localhost:8000` as an HTTPS URL.

---

### Step 5: Add to `.env`

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

---

### Summary

| Step | Action |
|------|--------|
| 1 | Sign up at twilio.com |
| 2 | Copy Account SID and Auth Token from Console |
| 3 | Enable WhatsApp Sandbox, join with your phone, copy sandbox number |
| 4 | Deploy backend, set webhook URL in Twilio (use ngrok for local) |
| 5 | Add the 3 variables to `.env` |
