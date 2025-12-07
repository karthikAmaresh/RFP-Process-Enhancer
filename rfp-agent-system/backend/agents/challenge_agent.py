# Challenges Agent
from .base_agent import BaseAgent


class ChallengesAgent(BaseAgent):
    """
    Extract Challenges: Performance, data issues, maintenance pain
    """
    
    def extract(self, text: str) -> str:
        """Extract challenges from RFP text"""
        return self.run(text)
