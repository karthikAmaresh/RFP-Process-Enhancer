"""Business Process Agent - Extracts current system workflows and processes"""
from agents.base_agent import BaseAgent


class BusinessProcessAgent(BaseAgent):
    """Extract Business Process: Current system workflows and activities"""
    
    def extract(self, text):
        return self.run(text)
