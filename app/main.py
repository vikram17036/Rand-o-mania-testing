"""
Main FastAPI Application
Initializes the FastAPI app with routes and middleware.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app import routes
from services.interpreter import PromptInterpreter
from utils.logger import get_logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = get_logger()
logger.info("Starting Rand-o-mania API Server")

# Initialize FastAPI app
app = FastAPI(
    title="Rand-o-mania API",
    description="API for processing random number calculation prompts",
    version="1.0.0"
)

# Add CORS middleware to allow requests from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize interpreter
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY environment variable is required")
    raise ValueError("OPENAI_API_KEY environment variable is required")

interpreter = PromptInterpreter(api_key=OPENAI_API_KEY)

# Set interpreter on routes module
routes.interpreter = interpreter

# Include routes
app.include_router(routes.router)

logger.info("Rand-o-mania API Server started successfully")


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )

