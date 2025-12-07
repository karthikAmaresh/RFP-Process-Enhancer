"""Pain Points Agent - Identifies problems that need solving"""
from .base_agent import BaseAgent


class PainPointsAgent(BaseAgent):
    """Extract Pain Points: Problems, complaints, and inefficiencies"""
    
    def extract(self, text: str) -> str:
        return self.run(text)
