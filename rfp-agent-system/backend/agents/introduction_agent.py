"""Introduction Agent - Generates problem statement and executive summary"""
from agents.base_agent import BaseAgent


class IntroductionAgent(BaseAgent):
    """
    Agent specialized in creating executive-level introduction
    including problem statement and summary.
    """
    
    def extract(self, text: str) -> str:
        """
        Generate introduction with problem statement and summary.
        
        Args:
            text: RFP document text
            
        Returns:
            str: Formatted introduction section
        """
        prompt = self.prompt_template.replace("{{input}}", text)
        response = self.llm.generate(prompt)
        return response
