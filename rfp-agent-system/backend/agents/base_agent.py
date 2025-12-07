"""Base Agent class for all RFP analysis agents"""
from abc import ABC, abstractmethod
from typing import Any, Callable


class BaseAgent(ABC):
    """
    Abstract base class for all RFP analysis agents.
    Works with local LLM (Ollama) via llm_client.
    """
    
    def __init__(self, llm: Callable = None, prompt_template: str = None):
        """
        Initialize base agent.
        
        Args:
            llm: Language model callable (e.g., local_llm from llm_client)
            prompt_template: Prompt template with {{input}} placeholder
        """
        self.llm = llm
        self.prompt_template = prompt_template
    
    @abstractmethod
    def extract(self, text: str) -> Any:
        """
        Extract information from the RFP text
        
        Args:
            text: The RFP text content to analyze
            
        Returns:
            Extracted information (format depends on specific agent)
        """
        pass
    
    def run(self, text: str) -> str:
        """
        Execute the agent analysis on the given text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Analysis result from LLM
        """
        if not self.llm:
            return "Error: LLM not configured"
        
        if not self.prompt_template:
            return "Error: Prompt template not configured"
        
        try:
            prompt = self.prompt_template.replace("{{input}}", text)
            response = self.llm(prompt)
            return str(response)
        except Exception as e:
            return f"Error during analysis: {str(e)}"
