"""Impact Agent - Extracts impactful statements about budget, scale, and compliance"""
from .base_agent import BaseAgent


class ImpactfulStatementsAgent(BaseAgent):
    """Extract Impactful Statements: Budget, scale, deadlines, and compliance"""
    
    def extract(self, text: str) -> str:
        return self.run(text)
