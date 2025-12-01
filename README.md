# Rand-o-mania API Server

A Python API server that processes natural language prompts for random number calculations using OpenAI's GPT models.

## Features

- ✅ Natural language prompt processing
- ✅ Random number generation (0-1 range)
- ✅ Mathematical operations (multiply, divide, square root)
- ✅ Conditional logic (if/then)
- ✅ Precision up to 10 decimal places
- ✅ Tracks all generated random numbers
- ✅ Public access via ngrok

## Requirements

- Python 3.8+
- OpenAI API key
- ngrok (for public access)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
PORT=8000
```

### 3. Start the Server

```bash
python app.py
```

The server will start on `http://localhost:8000`

### 4. Expose Server Publicly with ngrok

In a new terminal, install and run ngrok:

```bash
# Install ngrok (if not already installed)
# Download from https://ngrok.com/download

# Expose local server
ngrok http 8000
```

Copy the HTTPS URL provided by ngrok (e.g., `https://abc123.ngrok.io`)

## API Endpoints

### Health Check

```bash
GET /
GET /health
```

### Calculate

```bash
POST /
POST /calculate
```

**Request Body:**
```json
{
  "prompt": "Generate a random number. If the number is less than 0.5, multiply it by 0.1234567, otherwise divide it by 1.1234567. Generate another random number, get the square root of it, and then multiply it by the previous result."
}
```

**Response:**
```json
{
  "result": 0.262724811,
  "random_integers": [0.61234, 0.232343]
}
```

## Example Usage

### Using curl

```bash
curl -X POST https://your-ngrok-url.ngrok.io \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Generate a random number. If the number is less than 0.5, multiply it by 0.1234567, otherwise divide it by 1.1234567. Generate another random number, get the square root of it, and then multiply it by the previous result."}'
```

### Using Python

```python
import requests

url = "https://your-ngrok-url.ngrok.io"
payload = {
    "prompt": "Generate a random number and multiply it by 2.5"
}

response = requests.post(url, json=payload)
print(response.json())
```

## Supported Operations

The API supports prompts that can handle:

- ✅ Generating random numbers between 0-1
- ✅ Multiplying numbers
- ✅ Dividing numbers
- ✅ Getting square roots
- ✅ Number precision up to 10 decimal points
- ✅ Conditionals (if this then that)
- ✅ Multiple steps

## Architecture

- **FastAPI**: Modern, fast web framework
- **OpenAI GPT-4**: Converts natural language to executable Python code
- **Few-shot Prompting**: Uses examples to guide code generation
- **Random Number Tracking**: Intercepts and records all random number generations
- **Error Handling**: Comprehensive error handling and logging

## Project Structure

```
Random-mania/
├── app.py              # FastAPI server and endpoints
├── interpreter.py      # Prompt interpretation and code execution
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .env               # Environment variables (not in git)
└── .gitignore         # Git ignore rules
```

## Development

### Running in Development Mode

The server runs with auto-reload enabled by default:

```bash
python app.py
```

### Testing Locally

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test calculation endpoint
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Generate a random number and multiply it by 2"}'
```

## Notes

- The server uses GPT-4 Turbo for code generation (can be changed to GPT-3.5-turbo in `interpreter.py`)
- All random numbers are tracked during code execution
- Results are rounded to 10 decimal places
- The API includes CORS middleware to allow requests from anywhere

## License

MIT

