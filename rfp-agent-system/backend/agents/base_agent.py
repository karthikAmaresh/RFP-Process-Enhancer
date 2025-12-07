# Base Agent class for all RFP analysis agents
from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """
    Abstract base class for all RFP analysis agents
    Works with local LLM (Ollama) or any callable LLM function
    """
    
    def __init__(self, llm=None, prompt_template: str = None):
        """
        Initialize base agent
        
        Args:
            llm: Language model callable function (e.g., local_llm from llm_client)
            prompt_template: Prompt template string with {{input}} placeholder
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
        Run the agent on the given text
        
        Args:
            text: The input text to process
            
        Returns:
            str: Response from the LLM
        """
        if not self.llm:
            return "LLM not configured. Cannot perform analysis."
        
        if not self.prompt_template:
            return "Prompt template not configured for this agent."
        
        try:
            # Replace placeholder with actual text
            prompt = self.prompt_template.replace("{{input}}", text)
            
            # Call LLM (works with simple callable or langchain-style invoke)
            if callable(self.llm):
                response = self.llm(prompt)
            elif hasattr(self.llm, 'invoke'):
                response = self.llm.invoke(prompt)
                if hasattr(response, 'content'):
                    response = response.content
            else:
                response = str(self.llm)
            
            return str(response)
        except Exception as e:
            return f"Error during analysis: {str(e)}"
