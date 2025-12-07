"""NFR Agent - Extracts non-functional requirements"""
from agents.base_agent import BaseAgent


class NFRAgent(BaseAgent):
    """Extract Non-Functional Requirements: Performance, security, scalability"""
    
    def extract(self, text):
        return self.run(text)
