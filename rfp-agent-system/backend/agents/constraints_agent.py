"""Constraints Agent - Identifies limitations and restrictions"""
from agents.base_agent import BaseAgent


class ConstraintsAgent(BaseAgent):
    """Extract Constraints: Technical, budget, timeline, and regulatory limitations"""
    
    def extract(self, text):
        return self.run(text)
