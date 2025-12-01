# Quick Setup Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Create .env File

Create a `.env` file in the project root with:

```env
OPENAI_API_KEY=
PORT=8000
```

## Step 3: Start the Server

```bash
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 4: Expose with ngrok

In a **new terminal window**:

1. Install ngrok (if not already installed):
   - Download from: https://ngrok.com/download
   - Or use: `choco install ngrok` (Windows) or `brew install ngrok` (Mac)

2. Run ngrok:
   ```bash
   ngrok http 8000
   ```

3. Copy the HTTPS URL (e.g., `https://abc123.ngrok-free.app`)

## Step 5: Test the API

### Test locally:
```bash
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Generate a random number and multiply it by 2"}'
```curl -X POST https://zola-unreasoned-jaleesa.ngrok-free.dev \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Generate a random number. If the number is less than 0.5, multiply it by 0.1234567, otherwise divide it by 1.1234567. Generate another random number, get the square root of it, and then multiply it by the previous result."}'

### Test via ngrok URL:
```bash

```

## Troubleshooting

- **Port already in use**: Change PORT in .env file
- **OpenAI API error**: Check your API key is correct
- **ngrok not working**: Make sure ngrok is pointing to the correct port (8000)
- **Connection refused**: Make sure the server is running before starting ngrok

