"""
Prompt Interpreter Service
Converts natural language prompts into executable Python code using OpenAI API
with few-shot prompting and chain-of-thought reasoning.
"""

import re
import random
from typing import List, Tuple, Dict, Any
from openai import OpenAI
from utils.tracker import RandomNumberTracker
from utils.logger import get_logger

logger = get_logger()


class PromptInterpreter:
    """Interprets natural language prompts and converts them to executable code."""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.system_prompt = self._get_system_prompt()
        self.few_shot_examples = self._get_few_shot_examples()
        logger.info("PromptInterpreter initialized")
    
    def _get_system_prompt(self) -> str:
        """System prompt with clear instructions and constraints."""
        return """You are an expert Python code generator that converts natural language instructions about random number operations into clean, executable Python code.

CRITICAL REQUIREMENTS:
1. You MUST generate valid Python code that can be executed directly
2. The code MUST assign the final result to a variable named 'result'
3. The code MUST end with just 'result' on its own line (so it can be evaluated)
4. Use random.random() for all random number generation (returns 0-1)
5. Import required modules (random, math) at the top
6. Round the final result to 10 decimal places: result = round(result, 10)
7. Use clear variable names: result, num1, num2, etc.

SUPPORTED OPERATIONS:
- Random generation: random.random()
- Multiplication: *
- Division: /
- Square root: math.sqrt()
- Conditionals: if/else statements
- Multiple sequential steps

OUTPUT FORMAT:
Return ONLY the Python code. No markdown, no explanations, no code blocks, just pure Python code.

EXAMPLE OUTPUT FORMAT:
import random
import math
num1 = random.random()
result = num1 * 2.5
result = round(result, 10)
result"""
    
    def _get_few_shot_examples(self) -> List[Dict[str, str]]:
        """Few-shot examples demonstrating the expected code generation."""
        return [
            {
                "prompt": "Generate a random number. If the number is less than 0.5, multiply it by 0.1234567, otherwise divide it by 1.1234567. Generate another random number, get the square root of it, and then multiply it by the previous result.",
                "code": """import random
import math

# Generate first random number
num1 = random.random()

# Conditional operation
if num1 < 0.5:
    result = num1 * 0.1234567
else:
    result = num1 / 1.1234567

# Generate second random number
num2 = random.random()

# Get square root and multiply
sqrt_num2 = math.sqrt(num2)
result = result * sqrt_num2

# Round to 10 decimal places
result = round(result, 10)
result"""
            },
            {
                "prompt": "Generate a random number and multiply it by 2.5. Then generate another random number and divide the result by it.",
                "code": """import random

# Generate first random number
num1 = random.random()
result = num1 * 2.5

# Generate second random number
num2 = random.random()
result = result / num2

# Round to 10 decimal places
result = round(result, 10)
result"""
            },
            {
                "prompt": "Generate three random numbers. Multiply the first two, then divide by the third, and finally get the square root of the result.",
                "code": """import random
import math

# Generate three random numbers
num1 = random.random()
num2 = random.random()
num3 = random.random()

# Multiply first two
result = num1 * num2

# Divide by third
result = result / num3

# Get square root
result = math.sqrt(result)

# Round to 10 decimal places
result = round(result, 10)
result"""
            }
        ]
    
    def _build_prompt(self, user_prompt: str) -> str:
        """Build the complete prompt with few-shot examples and chain-of-thought."""
        prompt_parts = [
            "Convert the following natural language instruction into Python code.",
            "",
            "Examples:",
            ""
        ]
        
        # Add few-shot examples
        for i, example in enumerate(self.few_shot_examples, 1):
            prompt_parts.append(f"Example {i}:")
            prompt_parts.append(f"Instruction: {example['prompt']}")
            prompt_parts.append("Code:")
            prompt_parts.append(example['code'])
            prompt_parts.append("")
        
        # Add the actual user prompt
        prompt_parts.append("Now convert this instruction:")
        prompt_parts.append(user_prompt)
        prompt_parts.append("")
        prompt_parts.append("Code:")
        
        return "\n".join(prompt_parts)
    
    def interpret(self, prompt: str) -> str:
        """
        Convert natural language prompt to Python code using OpenAI API.
        
        Args:
            prompt: Natural language instruction string
            
        Returns:
            Generated Python code as string
            
        Raises:
            Exception: If OpenAI API call fails
        """
        try:
            logger.debug(f"Interpreting prompt: {prompt[:50]}...")
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self._build_prompt(prompt)}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # or "gpt-3.5-turbo" for faster/cheaper
                messages=messages,
                temperature=0.1,  # Low temperature for deterministic code generation
                max_tokens=1000
            )
            
            code = response.choices[0].message.content.strip()
            
            # Clean up code (remove markdown code blocks if present)
            code = re.sub(r'```python\n?', '', code, flags=re.IGNORECASE)
            code = re.sub(r'```\n?', '', code)
            # Remove any leading/trailing whitespace and ensure it ends with 'result'
            code = code.strip()
            
            # Ensure code ends with 'result' variable for evaluation
            if not code.rstrip().endswith('result'):
                # Try to add it if the last line doesn't have it
                lines = code.split('\n')
                last_line = lines[-1].strip()
                if 'result' in last_line and '=' in last_line:
                    # If last line assigns to result, add a line with just 'result'
                    code += '\nresult'
            
            logger.debug("Code generated successfully")
            return code
            
        except Exception as e:
            logger.error(f"Failed to interpret prompt: {str(e)}")
            raise Exception(f"Failed to interpret prompt: {str(e)}")
    
    def execute_code(self, code: str) -> Tuple[float, List[float]]:
        """
        Execute generated code and track random numbers.
        
        Args:
            code: Python code string to execute
            
        Returns:
            Tuple of (result: float, random_numbers: List[float])
            
        Raises:
            Exception: If code execution fails
        """
        tracker = RandomNumberTracker()
        
        try:
            logger.debug("Executing generated code")
            with tracker:
                # Create a safe execution namespace
                namespace = {
                    'random': random,
                    'math': __import__('math'),
                    '__builtins__': __builtins__
                }
                
                # Execute the code
                exec(code, namespace)
                
                # Get the result (code should end with 'result' variable)
                if 'result' in namespace:
                    result = float(namespace['result'])
                else:
                    # Fallback: try to evaluate the last line if it's an expression
                    lines = [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
                    if lines:
                        try:
                            # Try to evaluate the last non-comment line
                            result = float(eval(lines[-1], namespace))
                        except:
                            raise ValueError("Code must assign final value to 'result' variable")
                    else:
                        raise ValueError("Code must assign final value to 'result' variable")
                
                # Round to 10 decimal places
                result = round(result, 10)
                
                # Round random numbers to 10 decimal places
                random_numbers = [round(num, 10) for num in tracker.random_numbers]
                
                logger.debug(f"Code executed successfully. Result: {result}, Random numbers: {len(random_numbers)}")
                return result, random_numbers
                
        except Exception as e:
            logger.error(f"Code execution failed: {str(e)}")
            raise Exception(f"Code execution failed: {str(e)}")
    
    def process(self, prompt: str) -> Tuple[float, List[float]]:
        """
        Complete pipeline: interpret prompt and execute code.
        
        Args:
            prompt: Natural language instruction string
            
        Returns:
            Tuple of (result: float, random_numbers: List[float])
        """
        code = self.interpret(prompt)
        return self.execute_code(code)

