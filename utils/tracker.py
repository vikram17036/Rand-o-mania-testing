"""
Random Number Tracker Utility
Context manager to track all random numbers generated during code execution.
"""

import random
from typing import List


class RandomNumberTracker:
    """Context manager to track all random numbers generated during execution."""
    
    def __init__(self):
        self.random_numbers: List[float] = []
        self.original_random = random.random
    
    def __enter__(self):
        def tracked_random():
            num = self.original_random()
            self.random_numbers.append(num)
            return num
        
        random.random = tracked_random
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        random.random = self.original_random
        return False

