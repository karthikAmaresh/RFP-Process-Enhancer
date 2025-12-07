"""Challenges Agent - Identifies technical and operational challenges"""
from .base_agent import BaseAgent


class ChallengesAgent(BaseAgent):
    """Extract Challenges: Performance, data, maintenance, and operational issues"""
    
    def extract(self, text: str) -> str:
        return self.run(text)
