"""Functional Requirements Agent - Extracts functional requirements"""
from agents.base_agent import BaseAgent


class FunctionalRequirementsAgent(BaseAgent):
    """
    Agent specialized in extracting functional requirements
    from RFP documents.
    """
    
    def extract(self, text: str) -> str:
        """
        Extract functional requirements from RFP.
        
        Args:
            text: RFP document text
            
        Returns:
            str: Formatted functional requirements
        """
        prompt = self.prompt_template.replace("{{input}}", text)
        response = self.llm.generate(prompt)
        return response
