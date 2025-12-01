"""
Pydantic models for request and response schemas.
"""

from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):
    """Request model for prompt input."""
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Natural language instruction for random number operations"
    )
    
    @field_validator('prompt')
    @classmethod
    def validate_prompt(cls, v: str) -> str:
        """Validate prompt is not empty."""
        if not v or not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v.strip()


class PromptResponse(BaseModel):
    """Response model for calculation results."""
    result: float = Field(..., description="Final calculation result")
    random_integers: list[float] = Field(
        ...,
        description="Array of randomly generated numbers between 0 and 1"
    )

