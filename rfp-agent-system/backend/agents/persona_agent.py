"""Persona Agent - Identifies user types and stakeholders"""
from agents.base_agent import BaseAgent


class PersonaAgent(BaseAgent):
    """Extract Personas: User types, roles, and stakeholders"""
    
    def extract(self, text):
        return self.run(text)
