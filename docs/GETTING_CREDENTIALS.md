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

## PostgreSQL

1. Install PostgreSQL locally or use a cloud provider (e.g. Supabase, Neon)
2. Create a database and note the connection URL
3. Format: `postgresql://user:password@host:port/database`
4. Put in `.env` as `POSTGRES_URL`

---

## Twilio (WhatsApp)

1. Sign up at https://www.twilio.com
2. Get `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` from Console
3. Enable WhatsApp Sandbox or Business API
4. Add `TWILIO_WHATSAPP_NUMBER` to `.env`
