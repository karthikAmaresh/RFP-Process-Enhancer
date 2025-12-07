"""Solution Architect Agent - Defines technical architecture and design"""
from agents.base_agent import BaseAgent


class ArchitectAgent(BaseAgent):
    """Extract Architecture Requirements: System design, integrations, technology stack"""
    
    def extract(self, text):
        return self.run(text)
