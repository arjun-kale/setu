# Getting Credentials

How to obtain credentials for the Rural AI Assistant backend.

## AWS (DynamoDB, S3, Polly)

1. Create an AWS account at https://aws.amazon.com
2. Go to IAM → Users → Create user
3. Attach policies: `AmazonDynamoDBFullAccess`, `AmazonS3FullAccess`, `AmazonPollyFullAccess`
4. Create access key → use `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in `.env`

## PostgreSQL

1. Install PostgreSQL locally or use a cloud provider (e.g. Supabase, Neon)
2. Create a database and note the connection URL
3. Format: `postgresql://user:password@host:port/database`
4. Put in `.env` as `POSTGRES_URL`

## Twilio (WhatsApp)

1. Sign up at https://www.twilio.com
2. Get `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` from Console
3. Enable WhatsApp Sandbox or Business API
4. Add `TWILIO_WHATSAPP_NUMBER` to `.env`

## Google Speech-to-Text

1. Go to Google Cloud Console
2. Enable Speech-to-Text API
3. Create API key or service account
4. Add `GOOGLE_STT_API_KEY` to `.env`
