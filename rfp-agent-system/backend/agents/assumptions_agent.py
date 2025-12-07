"""Assumptions Agent - Identifies assumptions and dependencies"""
from agents.base_agent import BaseAgent


class AssumptionsAgent(BaseAgent):
    """Extract Assumptions: Dependencies, prerequisites, and implicit assumptions"""
    
    def extract(self, text):
        return self.run(text)
