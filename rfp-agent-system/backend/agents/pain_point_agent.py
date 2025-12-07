# Pain Points Agent
from .base_agent import BaseAgent


class PainPointsAgent(BaseAgent):
    """
    Extract Pain Points: What problems need solving?
    """
    
    def extract(self, text: str) -> str:
        """Extract pain points from RFP text"""
        return self.run(text)
