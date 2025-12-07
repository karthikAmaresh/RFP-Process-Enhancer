# Impactful Statements Agent
from .base_agent import BaseAgent


class ImpactfulStatementsAgent(BaseAgent):
    """
    Extract Impactful Statements: Budget, user count, compliance pressure
    """
    
    def extract(self, text: str) -> str:
        """Extract impactful statements from RFP text"""
        return self.run(text)
