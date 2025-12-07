"""Gap Analysis Agent - Identifies gaps between current and desired state"""
from agents.base_agent import BaseAgent


class GapAgent(BaseAgent):
    """Extract Gap Analysis: Differences between current and desired state"""
    
    def extract(self, text):
        return self.run(text)
