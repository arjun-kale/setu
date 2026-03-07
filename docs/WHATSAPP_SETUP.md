# WhatsApp Setup — Step by Step

Complete guide to test the WhatsApp assistant with ngrok.

---

## Step 1: Add ngrok auth token

1. Open **Command Prompt** or **PowerShell**
2. Run (replace with your token from ngrok dashboard):

```
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

3. If you see "Authtoken saved" — done

---

## Step 2: Start the backend

1. Open a terminal
2. Go to project folder:

```
cd d:\Projects\Setu-Backend
```

3. Start the server:

```
uvicorn app.main:app --reload --port 8000
```

4. Leave this terminal open (server must keep running)

---

## Step 3: Start ngrok (new terminal)

1. Open a **second** terminal
2. Run:

```
ngrok http 8000
```

3. You'll see a screen with:
   - **Forwarding** — a URL like `https://xxxx-xx-xx-xx.ngrok-free.app`
   - Copy this **https** URL (you need it for Step 5)

---

## Step 4: Set webhook URL in Twilio

1. Open browser → [console.twilio.com](https://console.twilio.com)
2. Left menu → **Messaging** → **Try it out** → **Send a WhatsApp message**
3. Click the **Sandbox settings** tab
4. Find **"When a message comes in"**
5. In the URL box, enter:

```
https://YOUR-NGROK-URL/webhooks/whatsapp
```

   Replace `YOUR-NGROK-URL` with your ngrok URL (e.g. `https://abc123.ngrok-free.app/webhooks/whatsapp`)
6. Set method to **HTTP POST**
7. Click **Save**

---

## Step 5: Test on WhatsApp

1. Open **WhatsApp** on your phone
2. Send a message to your Twilio sandbox number (`+1 415 523 8886`)
3. Try messages like:
   - "Hello"
   - "What schemes for farmers?"
   - "Am I eligible?"
   - "I want to learn digital skills"
4. You should get a reply from the assistant

---

## Troubleshooting

| Problem | Fix |
|--------|-----|
| ngrok says "command not found" | Add ngrok to PATH or run from its folder |
| Twilio doesn't reply | Check webhook URL has `/webhooks/whatsapp` at the end |
| Server not running | Make sure Step 2 terminal is still open |
| ngrok URL changed | Free ngrok URLs change each time — update Twilio webhook |

---

## Summary

```
Terminal 1: uvicorn app.main:app --reload --port 8000
Terminal 2: ngrok http 8000
Twilio: Set webhook = https://YOUR-NGROK-URL/webhooks/whatsapp
WhatsApp: Send message to sandbox number
```
