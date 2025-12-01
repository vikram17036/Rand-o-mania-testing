"""
API Routes
FastAPI route handlers for the Rand-o-mania API.
"""

from fastapi import APIRouter, HTTPException, Request
from models.schemas import PromptRequest, PromptResponse
from services.interpreter import PromptInterpreter
from utils.logger import get_logger

logger = get_logger()
router = APIRouter()

# Interpreter will be set by main app
interpreter: PromptInterpreter = None


@router.get("/")
async def root():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "service": "Rand-o-mania API",
        "version": "1.0.0"
    }


@router.get("/health")
async def health():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {"status": "healthy"}


@router.post("/", response_model=PromptResponse)
@router.post("/calculate", response_model=PromptResponse)
async def calculate(
    request: PromptRequest,
    http_request: Request
) -> PromptResponse:
    """
    Process a prompt and return calculation result with random numbers.
    
    Args:
        request: PromptRequest containing the natural language instruction
        http_request: FastAPI Request object for getting client IP
        
    Returns:
        PromptResponse with result and random numbers array
        
    Raises:
        HTTPException: If processing fails
    """
    # Get client IP if available
    client_ip = http_request.client.host if http_request.client else None
    
    # Log the request
    logger.log_request(request.prompt, client_ip)
    
    try:
        # Process the prompt
        result, random_numbers = interpreter.process(request.prompt)
        
        # Log successful response
        logger.log_response(result, len(random_numbers), success=True)
        
        return PromptResponse(
            result=result,
            random_integers=random_numbers
        )
        
    except ValueError as e:
        logger.log_error(str(e), "ValidationError")
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
    
    except Exception as e:
        logger.log_error(str(e), "ProcessingError")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process prompt: {str(e)}"
        )

